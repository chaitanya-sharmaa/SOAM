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

variable "agent_1_backend_url" {
  description = "Cloud Run backend URI for Agent 1"
  type        = string
}

variable "agent_2_backend_url" {
  description = "Cloud Run backend URI for Agent 2"
  type        = string
}
