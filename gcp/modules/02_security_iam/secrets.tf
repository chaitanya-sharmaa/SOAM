# ==============================================================================
# Google Secret Manager: Sensitive Credential Vault for SOAM
# ==============================================================================

locals {
  secret_names = [
    "agent-db-password",
    "pingidentity-client-secret",
    "llm-api-token"
  ]
}

# 1. Create Secrets in Secret Manager with standard Google-managed encryption
resource "google_secret_manager_secret" "secrets" {
  for_each  = toset(local.secret_names)
  secret_id = "${var.environment}-dap-${each.key}"
  project   = var.project_id

  replication {
    auto {}
  }
}

# 2. Add initial placeholder versions (to be updated securely via CI/CD)
resource "google_secret_manager_secret_version" "secret_versions" {
  for_each    = toset(local.secret_names)
  secret      = google_secret_manager_secret.secrets[each.key].id
  secret_data = "initial_placeholder_secret_value"

  lifecycle {
    ignore_changes = [secret_data]
  }
}

# 3. Granular IAM Access: Agent 1 and Agent 2 can access DB and LLM tokens
resource "google_secret_manager_secret_iam_member" "agent_secret_access" {
  for_each = {
    "agent-1-db"  = { agent = "agent-1", secret = "agent-db-password" }
    "agent-1-llm" = { agent = "agent-1", secret = "llm-api-token" }
    "agent-2-db"  = { agent = "agent-2", secret = "agent-db-password" }
    "agent-2-llm" = { agent = "agent-2", secret = "llm-api-token" }
  }
  project   = var.project_id
  secret_id = google_secret_manager_secret.secrets[each.value.secret].secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.service_accounts[each.value.agent].email}"
}
