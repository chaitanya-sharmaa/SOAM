# ==============================================================================
# Staging Environment Configuration for Terragrunt
# ==============================================================================

locals {
  environment = "staging"
  project_id  = "my-dap-gcp-staging"
  region      = "europe-west1"

  # Networking (Allocated distinct /24 and /28 CIDRs)
  subnet_cidr        = "10.20.1.0/24"
  vpc_connector_cidr = "10.20.2.0/28"

  # Database (4 vCPU, 15 GB RAM for staging load testing)
  db_tier = "db-custom-4-15360"

  # PingIdentity OIDC Settings
  pingidentity_issuer_url = "https://auth-staging.enterprise.com"
  pingidentity_jwks_url   = "https://auth-staging.enterprise.com/.well-known/jwks.json"
  pingidentity_audience   = "dap-platform-staging"

  # Microservice Container Images (Staging tag)
  container_images = {
    "agent-registry"  = "gcr.io/my-dap-gcp-staging/agent-registry:staging"
    "agent-gateway"   = "gcr.io/my-dap-gcp-staging/agent-gateway:staging"
    "gatekeeper"      = "gcr.io/my-dap-gcp-staging/gatekeeper:staging"
    "mcp-gateway"     = "gcr.io/my-dap-gcp-staging/mcp-gateway:staging"
    "guardrails"      = "gcr.io/my-dap-gcp-staging/guardrails:staging"
    "grid-monitoring" = "gcr.io/my-dap-gcp-staging/grid-monitoring:staging"
    "grid-lens"       = "gcr.io/my-dap-gcp-staging/grid-lens:staging"
    "agent-1"         = "gcr.io/my-dap-gcp-staging/agent-1:staging"
    "agent-2"         = "gcr.io/my-dap-gcp-staging/agent-2:staging"
  }
}
