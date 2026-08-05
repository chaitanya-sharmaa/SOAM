output "log_analytics_workspace_id" {
  description = "ID of the Log Analytics Workspace."
  value       = azurerm_log_analytics_workspace.dap_workspace.id
}

output "log_analytics_workspace_name" {
  description = "Name of the Log Analytics Workspace."
  value       = azurerm_log_analytics_workspace.dap_workspace.name
}

output "application_insights_instrumentation_key" {
  description = "Instrumentation key for Application Insights."
  value       = azurerm_application_insights.dap_appinsights.instrumentation_key
  sensitive   = true
}

output "application_insights_connection_string" {
  description = "Connection string for Application Insights."
  value       = azurerm_application_insights.dap_appinsights.connection_string
  sensitive   = true
}

output "audit_storage_account_name" {
  description = "Storage account name for immutable audit logs."
  value       = azurerm_storage_account.audit_storage.name
}

output "audit_container_name" {
  description = "Container name for audit logs."
  value       = azurerm_storage_container.audit_container.name
}
