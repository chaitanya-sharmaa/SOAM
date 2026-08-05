output "api_gateway_hostname" {
  description = "Edge API Gateway Entrypoint Hostname for Business Apps & Clients"
  value       = module.ingress_gateway.gateway_hostname
}

output "grid_lens_dashboard_url" {
  description = "Observability UI (Grid Lens) URL"
  value       = module.compute_services.grid_lens_uri
}

output "agent_registry_db_private_ip" {
  description = "Private IP of Agent Registry Cloud SQL"
  value       = module.data_state.registry_db_private_ip
}

output "agent_gateway_db_private_ip" {
  description = "Private IP of Agent Gateway Cloud SQL"
  value       = module.data_state.gateway_db_private_ip
}

output "firestore_database" {
  description = "Firestore Native Database ID for Agent State"
  value       = module.data_state.firestore_database_name
}

output "ctt_bigquery_dataset" {
  description = "BigQuery Dataset for Continuous Telemetry & Tracing"
  value       = module.data_state.bigquery_dataset_id
}

output "audit_logs_bucket" {
  description = "Immutable Centralized Audit Log Bucket"
  value       = module.observability.audit_bucket_name
}
