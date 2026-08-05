variable "resource_group_name" {
  description = "Name of the Azure Resource Group."
  type        = string
}

variable "location" {
  description = "Azure region for deployment."
  type        = string
}

variable "environment" {
  description = "Environment tier (dev, staging, prod)."
  type        = string
}

variable "agent_gateway_url" {
  description = "Backend URL of the Agent Gateway microservice."
  type        = string
}

variable "pingidentity_jwks_uri" {
  description = "JWKS URI for PingIdentity JWT token validation."
  type        = string
  default     = "https://auth.pingidentity.com/.well-known/jwks.json"
}

variable "pingidentity_issuer" {
  description = "Expected issuer for PingIdentity JWT tokens."
  type        = string
  default     = "https://auth.pingidentity.com"
}

variable "tags" {
  description = "Resource tags."
  type        = map(string)
  default     = {}
}
