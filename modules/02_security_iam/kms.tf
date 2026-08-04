# ==============================================================================
# Cloud KMS: Customer-Managed Encryption Keys (CMEK)
# ==============================================================================
# Provides encryption keys to encrypt data at rest for Cloud SQL, Pub/Sub,
# Firestore, BigQuery, and Secret Manager.
# ==============================================================================

resource "google_kms_key_ring" "dap_keyring" {
  name     = "${var.environment}-dap-keyring"
  location = var.region
  project  = var.project_id
}

# 1. Crypto Key for Cloud SQL
resource "google_kms_crypto_key" "cloudsql_key" {
  name            = "key-cloudsql"
  key_ring        = google_kms_key_ring.dap_keyring.id
  rotation_period = "7776000s" # 90 days rotation

  lifecycle {
    prevent_destroy = false
  }
}

# 2. Crypto Key for Pub/Sub Topics
resource "google_kms_crypto_key" "pubsub_key" {
  name            = "key-pubsub"
  key_ring        = google_kms_key_ring.dap_keyring.id
  rotation_period = "7776000s"

  lifecycle {
    prevent_destroy = false
  }
}

# 3. Crypto Key for BigQuery & Cloud Storage
resource "google_kms_crypto_key" "bigquery_key" {
  name            = "key-bigquery"
  key_ring        = google_kms_key_ring.dap_keyring.id
  rotation_period = "7776000s"

  lifecycle {
    prevent_destroy = false
  }
}

# 4. Crypto Key for Secret Manager
resource "google_kms_crypto_key" "secrets_key" {
  name            = "key-secrets"
  key_ring        = google_kms_key_ring.dap_keyring.id
  rotation_period = "7776000s"

  lifecycle {
    prevent_destroy = false
  }
}

# 5. Service Agent IAM Grants to allow GCP services to use CMEK
# Get GCP Project Number for default service agents
data "google_project" "project" {
  project_id = var.project_id
}

# Cloud SQL Service Agent KMS Grant
resource "google_kms_crypto_key_iam_member" "cloudsql_cmek_user" {
  crypto_key_id = google_kms_crypto_key.cloudsql_key.id
  role          = "roles/cloudkms.cryptoKeyEncrypterDecrypter"
  member        = "serviceAccount:service-${data.google_project.project.number}@gcp-sa-cloud-sql.iam.gserviceaccount.com"
}

# Pub/Sub Service Agent KMS Grant
resource "google_kms_crypto_key_iam_member" "pubsub_cmek_user" {
  crypto_key_id = google_kms_crypto_key.pubsub_key.id
  role          = "roles/cloudkms.cryptoKeyEncrypterDecrypter"
  member        = "serviceAccount:service-${data.google_project.project.number}@gcp-sa-pubsub.iam.gserviceaccount.com"
}

# BigQuery Service Agent KMS Grant
resource "google_kms_crypto_key_iam_member" "bigquery_cmek_user" {
  crypto_key_id = google_kms_crypto_key.bigquery_key.id
  role          = "roles/cloudkms.cryptoKeyEncrypterDecrypter"
  member        = "serviceAccount:bq-${data.google_project.project.number}@bigquery-encryption.iam.gserviceaccount.com"
}
