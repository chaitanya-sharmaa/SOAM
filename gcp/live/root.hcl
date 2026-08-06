# ==============================================================================
# Root Terragrunt Configuration for Google Cloud Platform (GCP)
# ==============================================================================
# Follows modern Terragrunt v1.0+ standards using root.hcl.
# ==============================================================================

locals {
  # Automatically load environment-level variables from env.hcl in parent/sibling paths
  env_vars = read_terragrunt_config(find_in_parent_folders("env.hcl"))

  environment = local.env_vars.locals.environment
  project_id  = local.env_vars.locals.project_id
  region      = local.env_vars.locals.region
}

# 1. Centrally Managed Remote GCS Backend for Terraform State
remote_state {
  backend = "gcs"
  config = {
    bucket   = "${local.project_id}-dap-tfstate"
    prefix   = "terragrunt/${local.environment}/${path_relative_to_include()}/terraform.tfstate"
    project  = local.project_id
    location = local.region
  }
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
}

# 2. Centrally Generated Google Cloud Providers
generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.10.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 5.10.0"
    }
  }
}

provider "google" {
  project = "${local.project_id}"
  region  = "${local.region}"
}

provider "google-beta" {
  project = "${local.project_id}"
  region  = "${local.region}"
}
EOF
}

# 3. Global Default Inputs passed to all child modules
inputs = {
  project_id  = local.project_id
  region      = local.region
  environment = local.environment
}
