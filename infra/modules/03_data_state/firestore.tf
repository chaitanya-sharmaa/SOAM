# ==============================================================================
# Google Cloud Firestore: Agent State & Conversational Memory
# ==============================================================================
# Fast NoSQL document database used by Agent 1 and Agent 2 for:
# - Session context & multi-turn dialog history
# - Intermediate reasoning scratchpads & tool execution checkpoints
# ==============================================================================

resource "google_firestore_database" "agent_state_db" {
  project                     = var.project_id
  name                        = "(default)"
  location_id                 = var.region
  type                        = "FIRESTORE_NATIVE"
  concurrency_mode            = "OPTIMISTIC"
  app_engine_integration_mode = "DISABLED"
  delete_protection_state     = "DELETE_PROTECTION_DISABLED"
}

# Declarative import block ensures Terraform automatically adopts the project singleton (default) database
# on fresh applies or post-destroy runs without throwing HTTP 409 Conflict.
import {
  id = "(default)"
  to = google_firestore_database.agent_state_db
}
