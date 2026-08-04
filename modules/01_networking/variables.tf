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

variable "subnet_cidr" {
  description = "CIDR range for the private subnetwork"
  type        = string
  default     = "10.10.0.0/20"
}

variable "vpc_connector_cidr" {
  description = "CIDR range for the Serverless VPC Access connector (/28 required)"
  type        = string
  default     = "10.10.16.0/28"
}
