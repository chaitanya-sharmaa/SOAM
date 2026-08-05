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

variable "retention_in_days" {
  description = "Log retention period in days."
  type        = number
  default     = 30
}

variable "tags" {
  description = "Resource tags."
  type        = map(string)
  default     = {}
}
