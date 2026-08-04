output "service_accounts" {
  description = "Map of all created service accounts by service name"
  value       = { for k, v in google_service_account.service_accounts : k => v.email }
}

output "kms_keyring_id" {
  description = "ID of the KMS KeyRing"
  value       = google_kms_key_ring.dap_keyring.id
}

output "kms_keys" {
  description = "Map of created CMEK crypto key IDs"
  value = {
    cloudsql = google_kms_crypto_key.cloudsql_key.id
    pubsub   = google_kms_crypto_key.pubsub_key.id
    bigquery = google_kms_crypto_key.bigquery_key.id
    secrets  = google_kms_crypto_key.secrets_key.id
  }
}

output "secrets" {
  description = "Map of created Secret Manager secret IDs"
  value       = { for k, v in google_secret_manager_secret.secrets : k => v.id }
}
