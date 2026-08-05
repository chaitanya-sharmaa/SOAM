variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "environment" {
  description = "Deployment environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "kms_pubsub_key_id" {
  description = "KMS CMEK key ID for Pub/Sub encryption"
  type        = string
}
