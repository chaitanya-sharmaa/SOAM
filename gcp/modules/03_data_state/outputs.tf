output "db_private_ip" {
  description = "Private IP of the SOAM Agent Cloud SQL instance"
  value       = google_sql_database_instance.agent_db.private_ip_address
}

output "firestore_database_name" {
  description = "Name of the Firestore Native database for Agent State"
  value       = google_firestore_database.agent_state_db.name
}

output "bigquery_dataset_id" {
  description = "Dataset ID of CTT Analytics in BigQuery"
  value       = google_bigquery_dataset.ctt_analytics_dataset.dataset_id
}

output "db_admin_password" {
  description = "Generated admin password for SOAM Agent DB"
  value       = random_password.agent_db_pass.result
  sensitive   = true
}
