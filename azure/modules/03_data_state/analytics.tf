# ==============================================================================
# Analytics: Azure Data Lake Storage Gen2 (CTT Analytics & Telemetry)
# Equivalent to Google BigQuery CTT Analytics Dataset
# ==============================================================================

resource "random_string" "adls_suffix" {
  length  = 4
  special = false
  upper   = false
}

# 1. ADLS Gen2 Storage Account for High-Volume Conversation & Transaction Telemetry
resource "azurerm_storage_account" "ctt_analytics" {
  name                     = "stadls${var.environment}ctt${random_string.adls_suffix.result}"
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"
  is_hns_enabled           = true # Hierarchical Namespace for Big Data analytics
  min_tls_version          = "TLS1_2"

  tags = merge(var.tags, {
    Service = "ctt-analytics"
  })
}

# 2. Data Lake Gen2 Filesystem Container
resource "azurerm_storage_data_lake_gen2_filesystem" "ctt_filesystem" {
  name               = "ctt-telemetry"
  storage_account_id = azurerm_storage_account.ctt_analytics.id
}
