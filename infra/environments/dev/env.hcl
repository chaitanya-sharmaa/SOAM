# ==============================================================================
# Development Environment Configuration for Terragrunt (SOAM Minimal Setup)
# ==============================================================================

locals {
  environment = "dev"
  project_id  = "project-ddfa7a80-7677-4268-95a"
  region      = "europe-west1"

  # Networking — Direct VPC Egress uses private subnet directly
  subnet_cidr = "10.10.1.0/24"

  # Database (Free Tier minimal shared-core instance)
  db_tier = "db-f1-micro"

  # SOAM Agent Container Images in Google Artifact Registry
  container_images = {
    "agent-1" = "europe-west1-docker.pkg.dev/project-ddfa7a80-7677-4268-95a/cloud-run-source-deploy/dev-dap-agent-1:latest"
    "agent-2" = "europe-west1-docker.pkg.dev/project-ddfa7a80-7677-4268-95a/cloud-run-source-deploy/dev-dap-agent-2:latest"
  }
}
