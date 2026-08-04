output "audit_bucket_name" {
  description = "Name of the central audit log bucket"
  value       = google_logging_project_bucket_config.audit_bucket.bucket_id
}

output "dashboard_id" {
  description = "ID of the Grid Monitoring Dashboard"
  value       = google_monitoring_dashboard.grid_monitoring_dashboard.id
}
