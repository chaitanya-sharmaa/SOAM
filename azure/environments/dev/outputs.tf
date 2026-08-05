output "azure_frontdoor_hostname" {
  description = "Global Edge Ingress Endpoint (Azure Front Door with WAF)."
  value       = module.networking.frontdoor_endpoint_hostname
}

output "azure_apim_gateway_url" {
  description = "Public URL for Azure API Management."
  value       = module.ingress_gateway.apim_gateway_url
}

output "grid_lens_dashboard_url" {
  description = "Direct URL for the Grid Lens Dashboard container app."
  value       = "https://${module.compute_services.grid_lens_fqdn}"
}

output "agent_registry_db_fqdn" {
  description = "Private FQDN for Agent Registry PostgreSQL Flexible Server."
  value       = module.data_state.registry_db_fqdn
}

output "agent_gateway_db_fqdn" {
  description = "Private FQDN for Agent Gateway PostgreSQL Flexible Server."
  value       = module.data_state.gateway_db_fqdn
}

output "cosmosdb_session_endpoint" {
  description = "Cosmos DB Endpoint URL for fast session state."
  value       = module.data_state.cosmosdb_endpoint
}

output "key_vault_uri" {
  description = "Azure Key Vault URI."
  value       = module.security_iam.key_vault_uri
}

output "servicebus_endpoint" {
  description = "Azure Service Bus Endpoint."
  value       = module.messaging.servicebus_endpoint
}

output "nat_gateway_public_ip" {
  description = "Outbound Static Public IP for NAT Gateway."
  value       = module.networking.nat_gateway_public_ip
}
