output "service_accounts" {
  description = "Map of all created service accounts by service name"
  value       = { for k, v in google_service_account.service_accounts : k => v.email }
}

output "secrets" {
  description = "Map of created Secret Manager secret IDs"
  value       = { for k, v in google_secret_manager_secret.secrets : k => v.id }
}
