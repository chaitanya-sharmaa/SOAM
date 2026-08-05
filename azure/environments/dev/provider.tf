# ==============================================================================
# Terraform Providers & Remote State Backend (Azure Dev Environment)
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

  # Remote State in Azure Blob Storage
  # Configure during 'terraform init -backend-config=...' or uncomment when bootstrap is applied
  # backend "azurerm" {
  #   resource_group_name  = "rg-dap-tfstate"
  #   storage_account_name = "stdaptfstateXXXX"
  #   container_name       = "tfstate"
  #   key                  = "dev.dap.terraform.tfstate"
  #   use_oidc             = true
  # }
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

provider "azuread" {}

provider "random" {}
