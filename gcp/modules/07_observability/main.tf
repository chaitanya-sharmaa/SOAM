# ==============================================================================
# Module: 07_observability
# Enterprise Audit Logs, Sinks, Cloud Monitoring Dashboards & Alert Policies
# ==============================================================================

# 1. Dedicated Long-Term Audit Log Bucket (365 Days Retention)
resource "google_logging_project_bucket_config" "audit_bucket" {
  project        = var.project_id
  location       = var.region
  bucket_id      = "${var.environment}-dap-audit-logs-bucket"
  retention_days = 365
  description    = "Centralized immutable audit log bucket for DAP platform compliance."
}

# 2. Log Sink for Security & GateKeeper Audit Logs
resource "google_logging_project_sink" "audit_sink" {
  name                   = "${var.environment}-dap-audit-sink"
  project                = var.project_id
  destination            = "logging.googleapis.com/${google_logging_project_bucket_config.audit_bucket.id}"
  filter                 = "resource.type=\"cloud_run_revision\" AND jsonPayload.audit_id:* OR protoPayload.serviceName=\"cloudarmor.googleapis.com\""
  unique_writer_identity = true
}

# 3. Alert Policy: Dead Letter Queue (DLQ) Not Empty Alert
resource "google_monitoring_alert_policy" "dlq_alert" {
  display_name = "${var.environment}-DAP-DeadLetterQueue-Alert"
  project      = var.project_id
  combiner     = "OR"

  conditions {
    display_name = "DLQ Message Count > 0"
    condition_threshold {
      filter          = "metric.type=\"pubsub.googleapis.com/subscription/num_undelivered_messages\" resource.type=\"pubsub_subscription\" resource.label.\"subscription_id\"=\"${var.environment}-dap-dlq-sub\""
      duration        = "60s"
      comparison      = "COMPARISON_GT"
      threshold_value = 0

      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_MEAN"
      }
    }
  }
}
