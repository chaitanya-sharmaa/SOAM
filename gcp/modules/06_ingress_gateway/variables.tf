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
  description = "Deployment environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "agent_gateway_backend_url" {
  description = "Cloud Run backend URI for Agent Gateway"
  type        = string
}

variable "agent_registry_backend_url" {
  description = "Cloud Run backend URI for Agent Registry"
  type        = string
}

variable "pingidentity_issuer_url" {
  description = "PingIdentity OIDC token issuer URL (e.g. https://auth.enterprise.com)"
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
