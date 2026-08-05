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

variable "vnet_address_space" {
  description = "Address space CIDR for the Virtual Network."
  type        = list(string)
  default     = ["10.20.0.0/16"]
}

variable "container_apps_subnet_cidr" {
  description = "Subnet CIDR for Azure Container Apps Environment."
  type        = list(string)
  default     = ["10.20.1.0/23"]
}

variable "postgres_subnet_cidr" {
  description = "Subnet CIDR for Azure Database for PostgreSQL Flexible Server."
  type        = list(string)
  default     = ["10.20.4.0/24"]
}

variable "private_endpoints_subnet_cidr" {
  description = "Subnet CIDR for Private Endpoints."
  type        = list(string)
  default     = ["10.20.5.0/24"]
}

variable "gateway_subnet_cidr" {
  description = "Subnet CIDR for Ingress Gateway (APIM)."
  type        = list(string)
  default     = ["10.20.6.0/24"]
}

variable "tags" {
  description = "Resource tags."
  type        = map(string)
  default     = {}
}
