output "registry_db_private_ip" {
  description = "Private IP of the Agent Registry Cloud SQL instance"
  value       = google_sql_database_instance.agent_registry_db.private_ip_address
}

output "gateway_db_private_ip" {
  description = "Private IP of the Agent Gateway Cloud SQL instance"
  value       = google_sql_database_instance.agent_gateway_db.private_ip_address
}

output "firestore_database_name" {
  description = "Name of the Firestore Native database for Agent State"
  value       = google_firestore_database.agent_state_db.name
}

output "bigquery_dataset_id" {
  description = "Dataset ID of CTT Analytics in BigQuery"
  value       = google_bigquery_dataset.ctt_analytics_dataset.dataset_id
}

output "registry_db_admin_password" {
  description = "Generated admin password for Agent Registry DB"
  value       = random_password.registry_db_pass.result
  sensitive   = true
}

output "gateway_db_admin_password" {
  description = "Generated admin password for Agent Gateway DB"
  value       = random_password.gateway_db_pass.result
  sensitive   = true
}
