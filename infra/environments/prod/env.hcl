# ==============================================================================
# Production Environment Configuration for Terragrunt (SOAM Setup)
# ==============================================================================

locals {
  environment = "prod"
  project_id  = "my-dap-gcp-prod"
  region      = "europe-west1"

  # Networking — Direct VPC Egress uses snet-private-workload directly (no VPC Access Connector)
  # Use /22 in prod to support up to 1022 Cloud Run instance IPs under high scale
  subnet_cidr = "10.30.1.0/22"

  # Database (4 vCPU, 15 GB RAM High-Availability DB)
  db_tier = "db-custom-4-15360"

  # SOAM Agent Container Images in Google Artifact Registry (Immutable release tags)
  container_images = {
    "agent-1" = "europe-west1-docker.pkg.dev/my-dap-gcp-prod/cloud-run-source-deploy/prod-dap-agent-1:v1.0.0"
    "agent-2" = "europe-west1-docker.pkg.dev/my-dap-gcp-prod/cloud-run-source-deploy/prod-dap-agent-2:v1.0.0"
  }
}
