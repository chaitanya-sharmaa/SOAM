variable "subscription_id" {
  description = "The Azure Subscription ID where resources will be provisioned."
  type        = string
}

variable "location" {
  description = "The primary Azure region for DAP resources."
  type        = string
  default     = "westeurope"
}

variable "resource_prefix" {
  description = "Prefix for all Azure DAP resources."
  type        = string
  default     = "dap"
}

variable "github_repository" {
  description = "GitHub repository path in format 'owner/repo' (e.g. 'chaitanya-sharmaa/cloud-run')."
  type        = string
  default     = "chaitanya-sharmaa/cloud-run"
}
