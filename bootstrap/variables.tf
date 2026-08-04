variable "project_id" {
  description = "The GCP Project ID where resources will be bootstrapped."
  type        = string
}

variable "region" {
  description = "The GCP region for the state bucket."
  type        = string
  default     = "europe-west1"
}

variable "terraform_sa_name" {
  description = "The name of the service account used by Terraform CI/CD."
  type        = string
  default     = "sa-dap-tf-provisioner"
}

variable "workload_identity_pool_id" {
  description = "ID for the Workload Identity Pool."
  type        = string
  default     = "github-actions-pool"
}

variable "workload_identity_provider_id" {
  description = "ID for the Workload Identity Pool Provider."
  type        = string
  default     = "github-actions-provider"
}

variable "github_org_or_user" {
  description = "GitHub organization or username (used in WIF condition check)."
  type        = string
}

variable "github_repository" {
  description = "GitHub repository path in format 'owner/repo' (e.g. 'myorg/dap-infrastructure')."
  type        = string
}
