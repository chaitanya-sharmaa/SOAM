# ==============================================================================
# Module: 02_security_iam (Azure)
# User-Assigned Managed Identities for 9 DAP Microservices & RBAC
# ==============================================================================

locals {
  microservices = [
    "agent-1",
    "agent-2",
    "agent-gateway",
    "agent-registry",
    "gatekeeper",
    "guardrails",
    "mcp-gateway",
    "grid-monitoring",
    "grid-lens"
  ]
}

# 1. User-Assigned Managed Identity for each microservice
resource "azurerm_user_assigned_identity" "microservice_identities" {
  for_each            = toset(local.microservices)
  name                = "id-${var.environment}-${each.key}"
  location            = var.location
  resource_group_name = var.resource_group_name

  tags = merge(var.tags, {
    Service = each.key
  })
}

# 2. Azure Monitor / Application Insights Metrics Publisher Role
resource "azurerm_role_assignment" "monitoring_publisher" {
  for_each             = azurerm_user_assigned_identity.microservice_identities
  scope                = "/subscriptions/${data.azurerm_client_config.current.subscription_id}/resourceGroups/${var.resource_group_name}"
  role_definition_name = "Monitoring Metrics Publisher"
  principal_id         = each.value.principal_id
}

data "azurerm_client_config" "current" {}
