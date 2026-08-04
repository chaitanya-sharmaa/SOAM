# ==============================================================================
# Google Secret Manager: Sensitive Credential Vault
# ==============================================================================

locals {
  secret_names = [
    "agent-registry-db-password",
    "agent-gateway-db-password",
    "pingidentity-client-secret",
    "external-api-auth",
    "llm-api-token"
  ]
}

# 1. Create Secrets in Secret Manager with CMEK Encryption
resource "google_secret_manager_secret" "secrets" {
  for_each  = toset(local.secret_names)
  secret_id = "${var.environment}-dap-${each.key}"
  project   = var.project_id

  replication {
    user_managed {
      replicas {
        location = var.region
        customer_managed_encryption {
          kms_key_name = google_kms_crypto_key.secrets_key.id
        }
      }
    }
  }

  depends_on = [google_kms_crypto_key.secrets_key]
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

# 3. Granular IAM Access: MCP Gateway can access External API and LLM tokens
resource "google_secret_manager_secret_iam_member" "mcp_gateway_secret_access" {
  for_each  = toset(["external-api-auth", "llm-api-token"])
  project   = var.project_id
  secret_id = google_secret_manager_secret.secrets[each.key].secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.service_accounts["mcp-gateway"].email}"
}

# 4. Granular IAM Access: GateKeeper can access PingIdentity Client Secret
resource "google_secret_manager_secret_iam_member" "gatekeeper_pingidentity_secret_access" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.secrets["pingidentity-client-secret"].secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.service_accounts["gatekeeper"].email}"
}

# 5. Granular IAM Access: Registry & Gateway can access their respective DB passwords
resource "google_secret_manager_secret_iam_member" "registry_db_secret_access" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.secrets["agent-registry-db-password"].secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.service_accounts["agent-registry"].email}"
}

resource "google_secret_manager_secret_iam_member" "gateway_db_secret_access" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.secrets["agent-gateway-db-password"].secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.service_accounts["agent-gateway"].email}"
}
