output "azure_client_id" {
  description = "The Client (Application) ID of the Entra ID App for GitHub Actions WIF."
  value       = azuread_application.github_actions_app.client_id
}

output "azure_tenant_id" {
  description = "The Microsoft Entra ID Tenant ID."
  value       = azuread_service_principal.github_actions_sp.application_tenant_id
}

output "azure_subscription_id" {
  description = "The Azure Subscription ID."
  value       = var.subscription_id
}

output "terraform_state_resource_group" {
  description = "The resource group containing the remote state storage account."
  value       = azurerm_resource_group.tfstate_rg.name
}

output "terraform_state_storage_account" {
  description = "The Azure Storage Account name storing Terraform state."
  value       = azurerm_storage_account.tfstate_sa.name
}

output "terraform_state_container" {
  description = "The container name for Terraform remote state."
  value       = azurerm_storage_container.tfstate_container.name
}
