# ==============================================================================
# Production Environment Configuration for Terragrunt
# ==============================================================================

locals {
  environment = "prod"
  project_id  = "my-dap-gcp-prod"
  region      = "europe-west1"

  # Networking — Direct VPC Egress uses snet-private-workload directly (no VPC Access Connector)
  # Use /22 in prod to support up to 1022 Cloud Run instance IPs under high scale
  subnet_cidr        = "10.30.1.0/22"

  # Database (8 vCPU, 32 GB RAM Regional High-Availability DB)
  db_tier = "db-custom-8-32768"


  # Microservice Container Images (Production immutable SHA / Release tag)
  container_images = {
    "agent-registry"  = "gcr.io/my-dap-gcp-prod/agent-registry:v1.0.0"
    "agent-gateway"   = "gcr.io/my-dap-gcp-prod/agent-gateway:v1.0.0"
    "gatekeeper"      = "gcr.io/my-dap-gcp-prod/gatekeeper:v1.0.0"
    "mcp-gateway"     = "gcr.io/my-dap-gcp-prod/mcp-gateway:v1.0.0"
    "guardrails"      = "gcr.io/my-dap-gcp-prod/guardrails:v1.0.0"
    "grid-monitoring" = "gcr.io/my-dap-gcp-prod/grid-monitoring:v1.0.0"
    "grid-lens"       = "gcr.io/my-dap-gcp-prod/grid-lens:v1.0.0"
    "agent-1"         = "gcr.io/my-dap-gcp-prod/agent-1:v1.0.0"
    "agent-2"         = "gcr.io/my-dap-gcp-prod/agent-2:v1.0.0"
  }
}
