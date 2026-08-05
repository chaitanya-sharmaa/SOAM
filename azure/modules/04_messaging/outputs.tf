output "servicebus_namespace_id" {
  description = "ID of the Azure Service Bus Namespace."
  value       = azurerm_servicebus_namespace.dap_servicebus.id
}

output "servicebus_namespace_name" {
  description = "Name of the Azure Service Bus Namespace."
  value       = azurerm_servicebus_namespace.dap_servicebus.name
}

output "servicebus_endpoint" {
  description = "Endpoint of the Azure Service Bus."
  value       = azurerm_servicebus_namespace.dap_servicebus.endpoint
}

output "topic_ids" {
  description = "Map of Service Bus Topic IDs."
  value       = { for k, v in azurerm_servicebus_topic.topics : k => v.id }
}

output "topic_names" {
  description = "Map of Service Bus Topic names."
  value       = { for k, v in azurerm_servicebus_topic.topics : k => v.name }
}
