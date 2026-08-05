variable "subscription_id" {
  description = "The Azure Subscription ID where resources will be provisioned."
  type        = string
}

variable "tenant_id" {
  description = "The Microsoft Entra ID Tenant ID."
  type        = string
}

variable "location" {
  description = "Primary Azure region."
  type        = string
  default     = "westeurope"
}

variable "environment" {
  description = "Environment tier."
  type        = string
  default     = "dev"
}

variable "resource_group_name" {
  description = "Resource Group name for DAP development environment."
  type        = string
  default     = "rg-dev-dap-core"
}

variable "container_images" {
  description = "Map of container images for the microservices."
  type        = map(string)
  default = {
    "agent-1"         = "mcr.microsoft.com/azuredocs/aci-helloworld:latest"
    "agent-2"         = "mcr.microsoft.com/azuredocs/aci-helloworld:latest"
    "agent-gateway"   = "mcr.microsoft.com/azuredocs/aci-helloworld:latest"
    "agent-registry"  = "mcr.microsoft.com/azuredocs/aci-helloworld:latest"
    "gatekeeper"      = "mcr.microsoft.com/azuredocs/aci-helloworld:latest"
    "guardrails"      = "mcr.microsoft.com/azuredocs/aci-helloworld:latest"
    "mcp-gateway"     = "mcr.microsoft.com/azuredocs/aci-helloworld:latest"
    "grid-monitoring" = "mcr.microsoft.com/azuredocs/aci-helloworld:latest"
    "grid-lens"       = "mcr.microsoft.com/azuredocs/aci-helloworld:latest"
  }
}
