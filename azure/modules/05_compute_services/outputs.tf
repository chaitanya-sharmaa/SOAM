output "container_app_environment_id" {
  description = "ID of the Azure Container Apps Environment."
  value       = azurerm_container_app_environment.dap_environment.id
}

output "service_urls" {
  description = "Map of Container App FQDNs / URLs."
  value       = { for k, v in azurerm_container_app.microservices : k => "https://${v.latest_revision_fqdn}" }
}

output "agent_gateway_fqdn" {
  description = "Public FQDN of the Agent Gateway container app."
  value       = azurerm_container_app.microservices["agent-gateway"].latest_revision_fqdn
}

output "grid_lens_fqdn" {
  description = "Public FQDN of the Grid Lens dashboard container app."
  value       = azurerm_container_app.microservices["grid-lens"].latest_revision_fqdn
}
