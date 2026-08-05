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

variable "postgres_subnet_id" {
  description = "Subnet ID delegated to PostgreSQL Flexible Server."
  type        = string
}

variable "postgres_dns_zone_id" {
  description = "Private DNS Zone ID for PostgreSQL."
  type        = string
}

variable "registry_db_password" {
  description = "Master password for agent registry database."
  type        = string
  sensitive   = true
}

variable "gateway_db_password" {
  description = "Master password for agent gateway database."
  type        = string
  sensitive   = true
}

variable "tags" {
  description = "Resource tags."
  type        = map(string)
  default     = {}
}
