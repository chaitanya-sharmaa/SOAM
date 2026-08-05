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

variable "tenant_id" {
  description = "Microsoft Entra ID Tenant ID."
  type        = string
}

variable "tags" {
  description = "Resource tags."
  type        = map(string)
  default     = {}
}
