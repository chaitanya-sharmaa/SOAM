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
  description = "CIDR range for the private subnetwork. Use /24 for dev/staging, /22 for prod (supports up to 1022 Direct VPC Egress Cloud Run IPs)"
  type        = string
  default     = "10.10.1.0/24"
}
