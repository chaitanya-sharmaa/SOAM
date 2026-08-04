variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region"
  type        = string
  default     = "europe-west1"
}

variable "environment" {
  description = "Deployment environment name"
  type        = string
  default     = "dev"
}

variable "subnet_cidr" {
  description = "CIDR range for the private subnetwork"
  type        = string
  default     = "10.10.0.0/20"
}

variable "vpc_connector_cidr" {
  description = "CIDR range for Serverless VPC Access connector"
  type        = string
  default     = "10.10.16.0/28"
}

variable "container_images" {
  description = "Container images for all microservices"
  type        = map(string)
  default = {
    "agent-1"         = "gcr.io/cloudrun/hello"
    "agent-2"         = "gcr.io/cloudrun/hello"
    "agent-registry"  = "gcr.io/cloudrun/hello"
    "agent-gateway"   = "gcr.io/cloudrun/hello"
    "gatekeeper"      = "gcr.io/cloudrun/hello"
    "mcp-gateway"     = "gcr.io/cloudrun/hello"
    "guardrails"      = "gcr.io/cloudrun/hello"
    "grid-monitoring" = "gcr.io/cloudrun/hello"
    "grid-lens"       = "gcr.io/cloudrun/hello"
  }
}

variable "pingidentity_issuer_url" {
  description = "PingIdentity OIDC token issuer URL"
  type        = string
  default     = "https://auth.enterprise.com"
}

variable "pingidentity_jwks_url" {
  description = "PingIdentity JWKS public key endpoint"
  type        = string
  default     = "https://auth.enterprise.com/.well-known/jwks.json"
}

variable "pingidentity_audience" {
  description = "Expected audience claim in the PingIdentity JWT"
  type        = string
  default     = "dap-platform-api"
}
