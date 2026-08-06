# ==============================================================================
# Module: 02_security_iam
# Least-Privilege IAM Service Accounts & Role Bindings for SOAM Agents
# ==============================================================================

locals {
  services = [
    "agent-1",
    "agent-2"
  ]
}

# 1. Create Dedicated Service Account for each Agent
resource "google_service_account" "service_accounts" {
  for_each     = toset(local.services)
  account_id   = "sa-${var.environment}-${each.key}"
  display_name = "SOAM Service Account for ${each.key}"
  description  = "Dedicated least-privilege service account for ${each.key}"
  project      = var.project_id
}

# 2. Grant Vertex AI User & Gemini access to Agents
resource "google_project_iam_member" "vertex_ai_access" {
  for_each = toset(local.services)
  project  = var.project_id
  role     = "roles/aiplatform.user"
  member   = "serviceAccount:${google_service_account.service_accounts[each.key].email}"
}

# 3. Grant Firestore Access to Agents for State & Conversational Memory
resource "google_project_iam_member" "firestore_access" {
  for_each = toset(local.services)
  project  = var.project_id
  role     = "roles/datastore.user"
  member   = "serviceAccount:${google_service_account.service_accounts[each.key].email}"
}

# 4. Grant Cloud SQL Client access to Agents for Relational Persistence
resource "google_project_iam_member" "cloudsql_client" {
  for_each = toset(local.services)
  project  = var.project_id
  role     = "roles/cloudsql.client"
  member   = "serviceAccount:${google_service_account.service_accounts[each.key].email}"
}

# 5. Grant Pub/Sub Publisher roles (Agent 1 dispatches to Agent 2)
resource "google_project_iam_member" "pubsub_publisher" {
  for_each = toset(local.services)
  project  = var.project_id
  role     = "roles/pubsub.publisher"
  member   = "serviceAccount:${google_service_account.service_accounts[each.key].email}"
}

# 6. Grant Cloud Trace / Monitoring Writer for OpenTelemetry
resource "google_project_iam_member" "monitoring_writer" {
  for_each = toset(local.services)
  project  = var.project_id
  role     = "roles/cloudtrace.agent"
  member   = "serviceAccount:${google_service_account.service_accounts[each.key].email}"
}
