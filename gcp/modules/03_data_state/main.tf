# ==============================================================================
# Module: 03_data_state
# Cloud SQL (Private IP), Firestore (Agent State), and BigQuery (CTT Analytics)
# ==============================================================================

# Random passwords for Database Admin users
resource "random_password" "registry_db_pass" {
  length  = 24
  special = false
}

resource "random_password" "gateway_db_pass" {
  length  = 24
  special = false
}
