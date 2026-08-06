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

variable "google_audiences" {
  description = "Comma-separated list of allowed JWT audiences (e.g. gcloud SDK client ID or Gateway URL)"
  type        = string
  default     = "32555940559.apps.googleusercontent.com"
}
