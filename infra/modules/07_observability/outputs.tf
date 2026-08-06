output "audit_bucket_name" {
  description = "Name of the central audit log bucket"
  value       = google_storage_bucket.audit_bucket.name
}

output "dashboard_id" {
  description = "ID of the Grid Monitoring Dashboard"
  value       = google_monitoring_dashboard.grid_monitoring_dashboard.id
}
