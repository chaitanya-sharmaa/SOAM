output "apim_gateway_url" {
  description = "Public Gateway URL for Azure API Management."
  value       = azurerm_api_management.apim.gateway_url
}

output "apim_id" {
  description = "ID of the Azure API Management instance."
  value       = azurerm_api_management.apim.id
}
