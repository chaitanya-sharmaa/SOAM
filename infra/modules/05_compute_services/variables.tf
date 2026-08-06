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
  description = "ID of the Customer Custom VPC network"
  type        = string
}

variable "subnet_id" {
  description = "ID of private workload subnet for Direct VPC Egress"
  type        = string
}

variable "service_account_emails" {
  description = "Map of service account emails by service key"
  type        = map(string)
}

variable "container_images" {
  description = "Map of container images for each agent"
  type        = map(string)
}

variable "agent_1_source_dir" {
  description = "Absolute path to Agent 1 source directory for automated builds"
  type        = string
  default     = ""
}

variable "agent_2_source_dir" {
  description = "Absolute path to Agent 2 source directory for automated builds"
  type        = string
  default     = ""
}

variable "firestore_database_name" {
  description = "Name of the Firestore database for Agent State"
  type        = string
}

variable "agent_1_inbound_topic_id" {
  description = "ID of Agent 1 Inbound Pub/Sub Topic"
  type        = string
}

variable "agent_2_inbound_topic_id" {
  description = "ID of Agent 2 Inbound Pub/Sub Topic"
  type        = string
}

variable "db_private_ip" {
  description = "Private IP of SOAM Agent Cloud SQL"
  type        = string
  default     = ""
}
