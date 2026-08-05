output "managed_identities" {
  description = "Map of User-Assigned Managed Identity IDs."
  value       = { for k, v in azurerm_user_assigned_identity.microservice_identities : k => v.id }
}

output "managed_identity_client_ids" {
  description = "Map of User-Assigned Managed Identity Client IDs."
  value       = { for k, v in azurerm_user_assigned_identity.microservice_identities : k => v.client_id }
}

output "managed_identity_principal_ids" {
  description = "Map of User-Assigned Managed Identity Principal (Object) IDs."
  value       = { for k, v in azurerm_user_assigned_identity.microservice_identities : k => v.principal_id }
}

output "key_vault_id" {
  description = "Azure Key Vault ID."
  value       = azurerm_key_vault.kv.id
}

output "key_vault_uri" {
  description = "Azure Key Vault URI."
  value       = azurerm_key_vault.kv.vault_uri
}

output "cmek_key_ids" {
  description = "Map of Customer-Managed Encryption Key IDs."
  value       = { for k, v in azurerm_key_vault_key.cmek_keys : k => v.id }
}

output "registry_db_password_secret_id" {
  description = "Secret ID for agent registry database password."
  value       = azurerm_key_vault_secret.registry_db_password.id
}

output "gateway_db_password_secret_id" {
  description = "Secret ID for agent gateway database password."
  value       = azurerm_key_vault_secret.gateway_db_password.id
}
