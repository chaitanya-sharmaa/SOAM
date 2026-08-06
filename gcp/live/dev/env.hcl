# ==============================================================================
# Development Environment Configuration for Terragrunt
# ==============================================================================

locals {
  environment = "dev"
  project_id  = "project-ddfa7a80-7677-4268-95a"
  region      = "europe-west1"

  # Networking — Direct VPC Egress uses snet-private-workload directly (no VPC Access Connector)
  subnet_cidr        = "10.10.1.0/24"

  # Database (Free Tier minimal shared-core instance)
  db_tier = "db-f1-micro"

  # PingIdentity OIDC Settings
  pingidentity_issuer_url = "https://auth.enterprise.com"
  pingidentity_jwks_url   = "https://auth.enterprise.com/.well-known/jwks.json"
  pingidentity_audience   = "dap-platform-api"

  # Microservice Container Images (Public starter image for initial provisioning)
  container_images = {
    "agent-registry"  = "us-docker.pkg.dev/cloudrun/container/hello"
    "agent-gateway"   = "us-docker.pkg.dev/cloudrun/container/hello"
    "gatekeeper"      = "us-docker.pkg.dev/cloudrun/container/hello"
    "mcp-gateway"     = "us-docker.pkg.dev/cloudrun/container/hello"
    "guardrails"      = "us-docker.pkg.dev/cloudrun/container/hello"
    "grid-monitoring" = "us-docker.pkg.dev/cloudrun/container/hello"
    "grid-lens"       = "us-docker.pkg.dev/cloudrun/container/hello"
    "agent-1"         = "us-docker.pkg.dev/cloudrun/container/hello"
    "agent-2"         = "us-docker.pkg.dev/cloudrun/container/hello"
  }
}
