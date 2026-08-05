variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region"
  type        = string
  default     = "europe-west1"
}

variable "environment" {
  description = "Deployment environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "vpc_id" {
  description = "VPC ID where private databases will attach"
  type        = string
}

variable "db_tier" {
  description = "Machine tier for Cloud SQL instances"
  type        = string
  default     = "db-custom-2-7680"
}

variable "kms_cloudsql_key_id" {
  description = "KMS CMEK key ID for Cloud SQL"
  type        = string
}

variable "kms_bigquery_key_id" {
  description = "KMS CMEK key ID for BigQuery"
  type        = string
}
