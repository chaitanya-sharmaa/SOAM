# ==============================================================================
# BigQuery: "CTT BigQuery" (Continuous Telemetry, Tracing & Audit Analytics)
# ==============================================================================
# Enterprise data warehouse storing:
# - Step-by-step agent execution traces & LLM token consumption metrics
# - GateKeeper security audit logs & compliance trails
# ==============================================================================

resource "google_bigquery_dataset" "ctt_analytics_dataset" {
  dataset_id                  = "${var.environment}_dap_ctt_analytics"
  friendly_name               = "DAP Continuous Telemetry & Tracing"
  description                 = "Analytics dataset for multi-agent traces, token costs, and GateKeeper audit logs."
  location                    = var.region
  project                     = var.project_id
  default_table_expiration_ms = 7776000000 # 90 days retention

  default_encryption_configuration {
    kms_key_name = var.kms_bigquery_key_id
  }
}

# 1. Table for Agent Telemetry & Traces
resource "google_bigquery_table" "agent_telemetry_traces" {
  dataset_id          = google_bigquery_dataset.ctt_analytics_dataset.dataset_id
  table_id            = "agent_telemetry_traces"
  project             = var.project_id
  deletion_protection = false

  time_partitioning {
    type  = "DAY"
    field = "timestamp"
  }

  clustering = ["agent_id", "session_id", "status"]

  schema = <<EOF
[
  {"name": "trace_id", "type": "STRING", "mode": "REQUIRED", "description": "Unique trace identifier"},
  {"name": "session_id", "type": "STRING", "mode": "REQUIRED", "description": "Client session ID"},
  {"name": "agent_id", "type": "STRING", "mode": "REQUIRED", "description": "Agent identifier (e.g. agent-1)"},
  {"name": "step_name", "type": "STRING", "mode": "NULLABLE", "description": "Executed step or tool name"},
  {"name": "llm_model", "type": "STRING", "mode": "NULLABLE", "description": "Foundation model used"},
  {"name": "prompt_tokens", "type": "INTEGER", "mode": "NULLABLE", "description": "Input token count"},
  {"name": "completion_tokens", "type": "INTEGER", "mode": "NULLABLE", "description": "Output token count"},
  {"name": "latency_ms", "type": "FLOAT", "mode": "NULLABLE", "description": "Execution latency in milliseconds"},
  {"name": "status", "type": "STRING", "mode": "REQUIRED", "description": "SUCCESS, FAILED, or RETRIED"},
  {"name": "timestamp", "type": "TIMESTAMP", "mode": "REQUIRED", "description": "Event timestamp"}
]
EOF
}

# 2. Table for GateKeeper & Guardrails Audit Logs
resource "google_bigquery_table" "audit_security_logs" {
  dataset_id          = google_bigquery_dataset.ctt_analytics_dataset.dataset_id
  table_id            = "audit_security_logs"
  project             = var.project_id
  deletion_protection = false

  time_partitioning {
    type  = "DAY"
    field = "timestamp"
  }

  clustering = ["user_id", "decision", "rule_triggered"]

  schema = <<EOF
[
  {"name": "audit_id", "type": "STRING", "mode": "REQUIRED", "description": "Unique audit event ID"},
  {"name": "user_id", "type": "STRING", "mode": "NULLABLE", "description": "PingIdentity asserted user ID"},
  {"name": "client_ip", "type": "STRING", "mode": "NULLABLE", "description": "Source IP address"},
  {"name": "decision", "type": "STRING", "mode": "REQUIRED", "description": "ALLOWED, BLOCKED, or SANITIZED"},
  {"name": "rule_triggered", "type": "STRING", "mode": "NULLABLE", "description": "Triggered guardrail policy name"},
  {"name": "payload_hash", "type": "STRING", "mode": "NULLABLE", "description": "SHA-256 hash of the payload"},
  {"name": "timestamp", "type": "TIMESTAMP", "mode": "REQUIRED", "description": "Audit timestamp"}
]
EOF
}
