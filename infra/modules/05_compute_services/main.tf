# ==============================================================================
# Module: 05_compute_services
# Serverless Cloud Run v2 Microservices for the Digital Agent Platform
# ==============================================================================

# Shared Service Account for Pub/Sub push triggers
resource "google_service_account" "pubsub_invoker_sa" {
  account_id   = "sa-${var.environment}-ps-invoker"
  display_name = "Pub/Sub Push Invoker Service Account"
  project      = var.project_id
}
