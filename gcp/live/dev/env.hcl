# ==============================================================================
# Development Environment Configuration for Terragrunt
# ==============================================================================

locals {
  environment = "dev"
  project_id  = "project-ddfa7a80-7677-4268-95a"
  region      = "europe-west1"

  # Networking — Direct VPC Egress uses snet-private-workload directly (no VPC Access Connector)
  subnet_cidr        = "10.10.1.0/24"

  # Database
  db_tier = "db-custom-2-7680"

  # PingIdentity OIDC Settings
  pingidentity_issuer_url = "https://auth.enterprise.com"
  pingidentity_jwks_url   = "https://auth.enterprise.com/.well-known/jwks.json"
  pingidentity_audience   = "dap-platform-api"

  # Microservice Container Images
  container_images = {
    "agent-registry"  = "gcr.io/project-ddfa7a80-7677-4268-95a/agent-registry:latest"
    "agent-gateway"   = "gcr.io/project-ddfa7a80-7677-4268-95a/agent-gateway:latest"
    "gatekeeper"      = "gcr.io/project-ddfa7a80-7677-4268-95a/gatekeeper:latest"
    "mcp-gateway"     = "gcr.io/project-ddfa7a80-7677-4268-95a/mcp-gateway:latest"
    "guardrails"      = "gcr.io/project-ddfa7a80-7677-4268-95a/guardrails:latest"
    "grid-monitoring" = "gcr.io/project-ddfa7a80-7677-4268-95a/grid-monitoring:latest"
    "grid-lens"       = "gcr.io/project-ddfa7a80-7677-4268-95a/grid-lens:latest"
    "agent-1"         = "gcr.io/project-ddfa7a80-7677-4268-95a/agent-1:latest"
    "agent-2"         = "gcr.io/project-ddfa7a80-7677-4268-95a/agent-2:latest"
  }
}
