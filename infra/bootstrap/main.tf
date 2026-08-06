# ==============================================================================
# Bootstrap Module: Workload Identity Federation & Terraform State GCS Bucket
# ==============================================================================
# This module bootstraps keyless authentication for GitHub Actions to deploy
# to GCP without storing long-lived service account JSON keys.
# ==============================================================================

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.30"
    }
  }
}

# 1. Enable Core APIs needed for Bootstrap
resource "google_project_service" "required_services" {
  for_each = toset([
    "iam.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "iamcredentials.googleapis.com",
    "sts.googleapis.com",
    "storage.googleapis.com"
  ])
  project            = var.project_id
  service            = each.key
  disable_on_destroy = false
}

# 2. Remote State Storage Buckets (with Object Versioning for dev, staging, prod)
resource "google_storage_bucket" "tf_state_buckets" {
  for_each                    = toset(["dev", "staging", "prod"])
  name                        = "${var.project_id}-tfstate-${each.key}"
  project                     = var.project_id
  location                    = var.region
  force_destroy               = false
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      num_newer_versions = 5
    }
  }

  depends_on = [google_project_service.required_services]
}

# 3. Dedicated Terraform Provisioner Service Account
resource "google_service_account" "terraform_sa" {
  account_id   = var.terraform_sa_name
  display_name = "DAP Terraform Provisioner Service Account"
  project      = var.project_id
  description  = "Service account used by GitHub Actions CI/CD to provision DAP infrastructure."

  depends_on = [google_project_service.required_services]
}

# 4. Assign Required IAM Roles to the Terraform Provisioner SA
locals {
  provisioner_roles = [
    "roles/compute.networkAdmin",
    "roles/compute.securityAdmin",
    "roles/run.admin",
    "roles/cloudsql.admin",
    "roles/datastore.owner",
    "roles/pubsub.admin",
    "roles/bigquery.admin",
    "roles/secretmanager.admin",
    "roles/cloudkms.admin",
    "roles/apigateway.admin",
    "roles/iam.serviceAccountAdmin",
    "roles/resourcemanager.projectIamAdmin",
    "roles/iam.serviceAccountUser",
    "roles/storage.objectAdmin",
    "roles/logging.admin",
    "roles/monitoring.admin",
    "roles/vpcaccess.admin",
    "roles/servicenetworking.networksAdmin"
  ]
}

resource "google_project_iam_member" "provisioner_role_bindings" {
  for_each = toset(local.provisioner_roles)
  project  = var.project_id
  role     = each.key
  member   = "serviceAccount:${google_service_account.terraform_sa.email}"
}

# 5. Workload Identity Pool for GitHub Actions
resource "google_iam_workload_identity_pool" "github_pool" {
  workload_identity_pool_id = var.workload_identity_pool_id
  project                   = var.project_id
  display_name              = "GitHub Actions Pool"
  description               = "Workload Identity Pool for GitHub Actions CI/CD pipelines"
  disabled                  = false

  depends_on = [google_project_service.required_services]
}

# 6. Workload Identity Provider (OIDC with token.actions.githubusercontent.com)
resource "google_iam_workload_identity_pool_provider" "github_provider" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.github_pool.workload_identity_pool_id
  workload_identity_pool_provider_id = var.workload_identity_provider_id
  project                            = var.project_id
  display_name                       = "GitHub Actions Provider"
  description                        = "OIDC identity provider for GitHub repository integration"

  attribute_mapping = {
    "google.subject"             = "assertion.sub"
    "attribute.actor"            = "assertion.actor"
    "attribute.repository"       = "assertion.repository"
    "attribute.repository_owner" = "assertion.repository_owner"
  }

  attribute_condition = "assertion.repository_owner == '${var.github_org_or_user}'"

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

# 7. Bind GitHub Actions Repository to the Terraform Service Account (Impersonation)
resource "google_service_account_iam_member" "wif_sa_binding" {
  service_account_id = google_service_account.terraform_sa.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github_pool.name}/attribute.repository/${var.github_repository}"
}
