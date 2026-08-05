# ==============================================================================
# Module: 03_data_state (Azure)
# Private VNet-Integrated PostgreSQL Flexible Servers (Agent Registry & Gateway)
# ==============================================================================

resource "random_string" "db_suffix" {
  length  = 4
  special = false
  upper   = false
}

# 1. Agent Registry PostgreSQL Flexible Server (Private VNet)
resource "azurerm_postgresql_flexible_server" "registry_db" {
  name                   = "psql-${var.environment}-agent-registry-${random_string.db_suffix.result}"
  resource_group_name    = var.resource_group_name
  location               = var.location
  version                = "16"
  delegated_subnet_id    = var.postgres_subnet_id
  private_dns_zone_id    = var.postgres_dns_zone_id
  administrator_login    = "registry_admin"
  administrator_password = var.registry_db_password
  zone                   = "1"

  storage_mb   = 32768
  storage_tier = "P4"
  sku_name     = "B_Standard_B1ms" # Cost-efficient for dev, upgrade to GP_Standard_D2s_v3 for prod

  backup_retention_days = 7

  tags = merge(var.tags, {
    Service = "agent-registry"
  })
}

resource "azurerm_postgresql_flexible_server_database" "registry_db_instance" {
  name      = "agent_registry_db"
  server_id = azurerm_postgresql_flexible_server.registry_db.id
  collation = "en_US.utf8"
  charset   = "UTF8"
}

# 2. Agent Gateway PostgreSQL Flexible Server (Private VNet)
resource "azurerm_postgresql_flexible_server" "gateway_db" {
  name                   = "psql-${var.environment}-agent-gateway-${random_string.db_suffix.result}"
  resource_group_name    = var.resource_group_name
  location               = var.location
  version                = "16"
  delegated_subnet_id    = var.postgres_subnet_id
  private_dns_zone_id    = var.postgres_dns_zone_id
  administrator_login    = "gateway_admin"
  administrator_password = var.gateway_db_password
  zone                   = "1"

  storage_mb   = 32768
  storage_tier = "P4"
  sku_name     = "B_Standard_B1ms"

  backup_retention_days = 7

  tags = merge(var.tags, {
    Service = "agent-gateway"
  })
}

resource "azurerm_postgresql_flexible_server_database" "gateway_db_instance" {
  name      = "agent_gateway_db"
  server_id = azurerm_postgresql_flexible_server.gateway_db.id
  collation = "en_US.utf8"
  charset   = "UTF8"
}
