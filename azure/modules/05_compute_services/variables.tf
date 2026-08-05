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

variable "container_apps_subnet_id" {
  description = "Subnet ID for Container Apps Environment infrastructure."
  type        = string
}

variable "log_analytics_workspace_id" {
  description = "ID of the Log Analytics Workspace for Container Apps."
  type        = string
}

variable "managed_identities" {
  description = "Map of User-Assigned Managed Identity IDs."
  type        = map(string)
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

variable "registry_db_fqdn" {
  description = "FQDN of the Agent Registry PostgreSQL server."
  type        = string
}

variable "gateway_db_fqdn" {
  description = "FQDN of the Agent Gateway PostgreSQL server."
  type        = string
}

variable "cosmosdb_endpoint" {
  description = "Endpoint of the Cosmos DB session store."
  type        = string
}

variable "key_vault_uri" {
  description = "URI of the Azure Key Vault."
  type        = string
}

variable "servicebus_namespace_name" {
  description = "Name of the Azure Service Bus namespace."
  type        = string
}

variable "tags" {
  description = "Resource tags."
  type        = map(string)
  default     = {}
}
