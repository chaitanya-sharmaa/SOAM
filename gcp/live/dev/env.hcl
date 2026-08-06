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

  # PingIdentity OIDC Settings
  pingidentity_issuer_url = "https://auth.enterprise.com"
  pingidentity_jwks_url   = "https://auth.enterprise.com/.well-known/jwks.json"
  pingidentity_audience   = "dap-platform-api"

  # SOAM Agent Container Images
  container_images = {
    "agent-1" = "us-docker.pkg.dev/cloudrun/container/hello"
    "agent-2" = "us-docker.pkg.dev/cloudrun/container/hello"
  }
}
