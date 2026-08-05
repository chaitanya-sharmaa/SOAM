# ==============================================================================
# Module: 02_security_iam
# Least-Privilege IAM Service Accounts & Role Bindings for All Microservices
# ==============================================================================

locals {
  services = [
    "agent-1",
    "agent-2",
    "agent-registry",
    "agent-gateway",
    "gatekeeper",
    "mcp-gateway",
    "guardrails",
    "grid-monitoring",
    "grid-lens"
  ]
}

# 1. Create Dedicated Service Account for each Microservice
resource "google_service_account" "service_accounts" {
  for_each     = toset(local.services)
  account_id   = "sa-${var.environment}-${each.key}"
  display_name = "DAP Service Account for ${each.key}"
  description  = "Dedicated least-privilege service account for ${each.key} service"
  project      = var.project_id
}

# 2. Grant Vertex AI User & Gemini access to Agents & GateKeeper
resource "google_project_iam_member" "vertex_ai_access" {
  for_each = toset(["agent-1", "agent-2", "gatekeeper", "guardrails"])
  project  = var.project_id
  role     = "roles/aiplatform.user"
  member   = "serviceAccount:${google_service_account.service_accounts[each.key].email}"
}

# 3. Grant Firestore Access to Agents and Gateways for State Management
resource "google_project_iam_member" "firestore_access" {
  for_each = toset(["agent-1", "agent-2", "agent-gateway", "gatekeeper"])
  project  = var.project_id
  role     = "roles/datastore.user"
  member   = "serviceAccount:${google_service_account.service_accounts[each.key].email}"
}

# 4. Grant Cloud SQL Client access to Registry and Gateway services
resource "google_project_iam_member" "cloudsql_client" {
  for_each = toset(["agent-registry", "agent-gateway"])
  project  = var.project_id
  role     = "roles/cloudsql.client"
  member   = "serviceAccount:${google_service_account.service_accounts[each.key].email}"
}

# 5. Grant Pub/Sub Publisher/Subscriber roles
resource "google_project_iam_member" "pubsub_publisher" {
  for_each = toset(["agent-1", "agent-2", "agent-gateway", "gatekeeper"])
  project  = var.project_id
  role     = "roles/pubsub.publisher"
  member   = "serviceAccount:${google_service_account.service_accounts[each.key].email}"
}

# 6. Grant BigQuery Data Editor for CTT telemetry logging
resource "google_project_iam_member" "bigquery_writer" {
  for_each = toset(["gatekeeper", "grid-monitoring", "agent-gateway"])
  project  = var.project_id
  role     = "roles/bigquery.dataEditor"
  member   = "serviceAccount:${google_service_account.service_accounts[each.key].email}"
}

# 7. Grant Cloud Trace / Monitoring Writer for OpenTelemetry
resource "google_project_iam_member" "monitoring_writer" {
  for_each = toset(local.services)
  project  = var.project_id
  role     = "roles/cloudtrace.agent"
  member   = "serviceAccount:${google_service_account.service_accounts[each.key].email}"
}
