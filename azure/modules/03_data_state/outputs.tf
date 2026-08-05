output "registry_db_fqdn" {
  description = "Private FQDN for Agent Registry PostgreSQL Flexible Server."
  value       = azurerm_postgresql_flexible_server.registry_db.fqdn
}

output "gateway_db_fqdn" {
  description = "Private FQDN for Agent Gateway PostgreSQL Flexible Server."
  value       = azurerm_postgresql_flexible_server.gateway_db.fqdn
}

output "cosmosdb_endpoint" {
  description = "Endpoint URL for Cosmos DB Session State database."
  value       = azurerm_cosmosdb_account.dap_cosmos.endpoint
}

output "cosmosdb_database_name" {
  description = "Name of the Cosmos DB database."
  value       = azurerm_cosmosdb_sql_database.sessions_db.name
}

output "ctt_storage_account_name" {
  description = "Storage account name for CTT Telemetry Analytics."
  value       = azurerm_storage_account.ctt_analytics.name
}
