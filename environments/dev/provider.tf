# ==============================================================================
# Terraform & Provider Setup (Dev Environment)
# ==============================================================================

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.30"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 5.30"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }

  # Remote State in GCS Bucket
  # Set the bucket name using: terraform init -backend-config="bucket=<YOUR_BUCKET_NAME>"
  backend "gcs" {
    bucket = "project-ddfa7a80-7677-4268-95a-dap-tfstate"
    prefix = "terraform/state/dev"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}
