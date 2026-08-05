# ==============================================================================
# Module: 05_compute_services (Azure)
# Serverless Microservices: Azure Container Apps (ACA) Environment & Apps
# Equivalent to Google Cloud Run v2 Services
# ==============================================================================

# 1. Managed Azure Container Apps Environment (VNet-Integrated)
resource "azurerm_container_app_environment" "dap_environment" {
  name                           = "cae-${var.environment}-dap"
  location                       = var.location
  resource_group_name            = var.resource_group_name
  infrastructure_subnet_id       = var.container_apps_subnet_id
  log_analytics_workspace_id     = var.log_analytics_workspace_id
  internal_load_balancer_enabled = false

  tags = var.tags
}

locals {
  services = {
    "agent-1" = {
      is_external = false
      target_port = 8080
      cpu         = 0.5
      memory      = "1.0Gi"
    }
    "agent-2" = {
      is_external = false
      target_port = 8080
      cpu         = 0.5
      memory      = "1.0Gi"
    }
    "agent-gateway" = {
      is_external = true
      target_port = 8080
      cpu         = 1.0
      memory      = "2.0Gi"
    }
    "agent-registry" = {
      is_external = false
      target_port = 8080
      cpu         = 0.5
      memory      = "1.0Gi"
    }
    "gatekeeper" = {
      is_external = false
      target_port = 8080
      cpu         = 0.5
      memory      = "1.0Gi"
    }
    "guardrails" = {
      is_external = false
      target_port = 8080
      cpu         = 0.5
      memory      = "1.0Gi"
    }
    "mcp-gateway" = {
      is_external = false
      target_port = 8080
      cpu         = 0.5
      memory      = "1.0Gi"
    }
    "grid-monitoring" = {
      is_external = false
      target_port = 8080
      cpu         = 0.5
      memory      = "1.0Gi"
    }
    "grid-lens" = {
      is_external = true
      target_port = 8080
      cpu         = 0.5
      memory      = "1.0Gi"
    }
  }
}

# 2. Azure Container Apps for 9 DAP Microservices
resource "azurerm_container_app" "microservices" {
  for_each                     = local.services
  name                         = "ca-${var.environment}-${each.key}"
  container_app_environment_id = azurerm_container_app_environment.dap_environment.id
  resource_group_name          = var.resource_group_name
  revision_mode                = "Single"

  # User-Assigned Managed Identity Binding
  identity {
    type         = "UserAssigned"
    identity_ids = [var.managed_identities[each.key]]
  }

  ingress {
    external_enabled = each.value.is_external
    target_port      = each.value.target_port
    transport        = "auto"

    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  template {
    min_replicas = 0
    max_replicas = 10

    container {
      name   = each.key
      image  = var.container_images[each.key]
      cpu    = each.value.cpu
      memory = each.value.memory

      env {
        name  = "ENVIRONMENT"
        value = var.environment
      }
      env {
        name  = "SERVICE_NAME"
        value = each.key
      }
      env {
        name  = "KEY_VAULT_URI"
        value = var.key_vault_uri
      }
      env {
        name  = "COSMOS_ENDPOINT"
        value = var.cosmosdb_endpoint
      }
      env {
        name  = "REGISTRY_DB_HOST"
        value = var.registry_db_fqdn
      }
      env {
        name  = "GATEWAY_DB_HOST"
        value = var.gateway_db_fqdn
      }
      env {
        name  = "SERVICEBUS_NAMESPACE"
        value = var.servicebus_namespace_name
      }
    }
  }

  tags = merge(var.tags, {
    Service = each.key
  })
}
