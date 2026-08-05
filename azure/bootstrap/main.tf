# ==============================================================================
# Bootstrap Module: Azure Workload Identity Federation (OIDC) & Terraform State
# ==============================================================================
# This module bootstraps keyless authentication for GitHub Actions to deploy
# to Azure without storing long-lived service principal client secrets.
# ==============================================================================

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.90"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "~> 2.45"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

provider "azuread" {}

# 1. Random suffix for globally unique storage account name
resource "random_string" "storage_suffix" {
  length  = 6
  special = false
  upper   = false
}

# 2. Resource Group for Terraform State
resource "azurerm_resource_group" "tfstate_rg" {
  name     = "rg-${var.resource_prefix}-tfstate"
  location = var.location

  tags = {
    Environment = "Management"
    Project     = "Digital-Agent-Platform"
    ManagedBy   = "Terraform"
  }
}

# 3. Azure Storage Account for Remote State
resource "azurerm_storage_account" "tfstate_sa" {
  name                            = "st${var.resource_prefix}tfstate${random_string.storage_suffix.result}"
  resource_group_name             = azurerm_resource_group.tfstate_rg.name
  location                        = azurerm_resource_group.tfstate_rg.location
  account_tier                    = "Standard"
  account_replication_type        = "GRS"
  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = false
  public_network_access_enabled   = true

  blob_properties {
    versioning_enabled = true
    delete_retention_policy {
      days = 30
    }
    container_delete_retention_policy {
      days = 30
    }
  }

  tags = azurerm_resource_group.tfstate_rg.tags
}

# 4. Storage Container for State Files
resource "azurerm_storage_container" "tfstate_container" {
  name                  = "tfstate"
  storage_account_name  = azurerm_storage_account.tfstate_sa.name
  container_access_type = "private"
}

# 5. Microsoft Entra ID Application for GitHub Actions CI/CD
resource "azuread_application" "github_actions_app" {
  display_name = "app-${var.resource_prefix}-github-actions"
  description  = "Entra ID App for GitHub Actions Workload Identity Federation (DAP CI/CD)"
}

# 6. Service Principal associated with the Entra ID Application
resource "azuread_service_principal" "github_actions_sp" {
  client_id                    = azuread_application.github_actions_app.client_id
  app_role_assignment_required = false
  description                  = "Service Principal for GitHub Actions Workload Identity Federation"
}

# 7. Federated Identity Credential for GitHub Actions (Main Branch Push)
resource "azuread_application_federated_identity_credential" "github_main_branch" {
  application_id = azuread_application.github_actions_app.id
  display_name   = "fic-${var.resource_prefix}-github-main"
  description    = "Allows GitHub Actions on main branch to authenticate to Azure via OIDC"
  audiences      = ["api://AzureADTokenExchange"]
  issuer         = "https://token.actions.githubusercontent.com"
  subject        = "repo:${var.github_repository}:ref:refs/heads/main"
}

# 8. Federated Identity Credential for GitHub Actions (Pull Requests)
resource "azuread_application_federated_identity_credential" "github_pull_requests" {
  application_id = azuread_application.github_actions_app.id
  display_name   = "fic-${var.resource_prefix}-github-pr"
  description    = "Allows GitHub Actions on PRs to authenticate to Azure via OIDC"
  audiences      = ["api://AzureADTokenExchange"]
  issuer         = "https://token.actions.githubusercontent.com"
  subject        = "repo:${var.github_repository}:pull_request"
}

# 9. Role Assignment: Contributor on Subscription
resource "azurerm_role_assignment" "contributor" {
  scope                = "/subscriptions/${var.subscription_id}"
  role_definition_name = "Contributor"
  principal_id         = azuread_service_principal.github_actions_sp.object_id
}

# 10. Role Assignment: User Access Administrator on Subscription (for creating IAM role assignments)
resource "azurerm_role_assignment" "user_access_admin" {
  scope                = "/subscriptions/${var.subscription_id}"
  role_definition_name = "User Access Administrator"
  principal_id         = azuread_service_principal.github_actions_sp.object_id
}

# 11. Role Assignment: Storage Blob Data Contributor on State Storage Account
resource "azurerm_role_assignment" "tfstate_blob_contributor" {
  scope                = azurerm_storage_account.tfstate_sa.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azuread_service_principal.github_actions_sp.object_id
}
