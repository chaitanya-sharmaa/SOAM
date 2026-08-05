# ==============================================================================
# Fast Session State: Azure Cosmos DB (Serverless NoSQL)
# Equivalent to Google Cloud Firestore Native Database
# ==============================================================================

resource "random_string" "cosmos_suffix" {
  length  = 4
  special = false
  upper   = false
}

# 1. Cosmos DB Account (Serverless Mode)
resource "azurerm_cosmosdb_account" "dap_cosmos" {
  name                = "cosmos-${var.environment}-dap-${random_string.cosmos_suffix.result}"
  location            = var.location
  resource_group_name = var.resource_group_name
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"

  capabilities {
    name = "EnableServerless"
  }

  consistency_policy {
    consistency_level       = "Session"
    max_interval_in_seconds = 5
    max_staleness_prefix    = 100
  }

  geo_location {
    location          = var.location
    failover_priority = 0
  }

  tags = merge(var.tags, {
    Service = "session-state"
  })
}

# 2. Cosmos DB SQL Database
resource "azurerm_cosmosdb_sql_database" "sessions_db" {
  name                = "dap_sessions"
  resource_group_name = var.resource_group_name
  account_name        = azurerm_cosmosdb_account.dap_cosmos.name
}

# 3. Cosmos DB SQL Container for Multi-Agent History & State
resource "azurerm_cosmosdb_sql_container" "agent_sessions" {
  name                = "agent_sessions"
  resource_group_name = var.resource_group_name
  account_name        = azurerm_cosmosdb_account.dap_cosmos.name
  database_name       = azurerm_cosmosdb_sql_database.sessions_db.name
  partition_key_paths = ["/session_id"]

  indexing_policy {
    indexing_mode = "consistent"

    included_path {
      path = "/*"
    }

    excluded_path {
      path = "/\"_etag\"/?"
    }
  }
}
