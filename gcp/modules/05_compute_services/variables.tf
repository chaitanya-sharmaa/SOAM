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

variable "vpc_connector_id" {
  description = "ID of the Serverless VPC Access connector"
  type        = string
}

variable "service_account_emails" {
  description = "Map of service account emails by service key"
  type        = map(string)
}

variable "container_images" {
  description = "Map of container images for each microservice"
  type        = map(string)
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

variable "gatekeeper_topic_id" {
  description = "ID of GateKeeper Pub/Sub Topic"
  type        = string
}

variable "registry_db_private_ip" {
  description = "Private IP of Agent Registry Cloud SQL"
  type        = string
}

variable "gateway_db_private_ip" {
  description = "Private IP of Agent Gateway Cloud SQL"
  type        = string
}

variable "bigquery_dataset_id" {
  description = "Dataset ID of CTT Analytics in BigQuery"
  type        = string
}
