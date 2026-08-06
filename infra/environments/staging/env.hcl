# ==============================================================================
# Staging Environment Configuration for Terragrunt (SOAM Setup)
# ==============================================================================

locals {
  environment = "staging"
  project_id  = "my-dap-gcp-staging"
  region      = "europe-west1"

  # Networking — Direct VPC Egress uses private subnet directly
  subnet_cidr = "10.20.1.0/24"

  # Database (2 vCPU, 7.5 GB RAM for staging load testing)
  db_tier = "db-custom-2-7680"

  # SOAM Agent Container Images in Google Artifact Registry
  container_images = {
    "agent-1" = "europe-west1-docker.pkg.dev/my-dap-gcp-staging/cloud-run-source-deploy/staging-dap-agent-1:staging"
    "agent-2" = "europe-west1-docker.pkg.dev/my-dap-gcp-staging/cloud-run-source-deploy/staging-dap-agent-2:staging"
  }
}
