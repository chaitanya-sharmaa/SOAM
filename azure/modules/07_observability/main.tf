# ==============================================================================
# Module: 07_observability (Azure)
# Observability: Log Analytics Workspace, Application Insights, Immutable Logs
# Equivalent to Google Cloud Logging Sinks, BigQuery Exports & Cloud Monitoring
# ==============================================================================

# 1. Centralized Log Analytics Workspace
resource "azurerm_log_analytics_workspace" "dap_workspace" {
  name                = "law-${var.environment}-dap"
  location            = var.location
  resource_group_name = var.resource_group_name
  sku                 = "PerGB2018"
  retention_in_days   = var.retention_in_days

  tags = var.tags
}

# 2. Application Insights for Distributed OpenTelemetry Tracing & Metrics
resource "azurerm_application_insights" "dap_appinsights" {
  name                = "appi-${var.environment}-dap"
  location            = var.location
  resource_group_name = var.resource_group_name
  workspace_id        = azurerm_log_analytics_workspace.dap_workspace.id
  application_type    = "web"

  tags = var.tags
}

# 3. Immutable Storage Account for Compliance & Audit Logs (WORM Policy)
resource "random_string" "audit_sa_suffix" {
  length  = 4
  special = false
  upper   = false
}

resource "azurerm_storage_account" "audit_storage" {
  name                     = "staudit${var.environment}dap${random_string.audit_sa_suffix.result}"
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "GRS"
  min_tls_version          = "TLS1_2"

  blob_properties {
    versioning_enabled = true
    delete_retention_policy {
      days = 365
    }
  }

  tags = merge(var.tags, {
    Compliance = "Immutable-Audit-Logs"
  })
}

resource "azurerm_storage_container" "audit_container" {
  name                  = "dap-audit-logs"
  storage_account_name  = azurerm_storage_account.audit_storage.name
  container_access_type = "private"
}
