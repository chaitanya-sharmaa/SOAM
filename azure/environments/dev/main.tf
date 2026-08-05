# ==============================================================================
# Azure Digital Agent Platform (DAP) - Dev Environment Composition
# ==============================================================================

# Core Resource Group for Dev DAP Environment
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location

  tags = {
    Environment = var.environment
    Platform    = "Digital-Agent-Platform"
    ManagedBy   = "Terraform"
  }
}

# 1. Module 01: Networking & Edge Defense (VNet, Subnets, NAT Gateway, Front Door WAF)
module "networking" {
  source              = "../../modules/01_networking"
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.location
  environment         = var.environment
  tags                = azurerm_resource_group.rg.tags
}

# 2. Module 02: Identity & Security (Managed Identities, Key Vault, CMEK, Secrets)
module "security_iam" {
  source              = "../../modules/02_security_iam"
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.location
  environment         = var.environment
  tenant_id           = var.tenant_id
  tags                = azurerm_resource_group.rg.tags
}

# 3. Module 07: Observability & Logging (Log Analytics, App Insights, Audit Storage)
module "observability" {
  source              = "../../modules/07_observability"
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.location
  environment         = var.environment
  tags                = azurerm_resource_group.rg.tags
}

# 4. Module 03: Data & State Tier (PostgreSQL Flexible Server, Cosmos DB, ADLS Gen2)
module "data_state" {
  source               = "../../modules/03_data_state"
  resource_group_name  = azurerm_resource_group.rg.name
  location             = var.location
  environment          = var.environment
  postgres_subnet_id   = module.networking.postgres_subnet_id
  postgres_dns_zone_id = module.networking.postgres_private_dns_zone_id
  registry_db_password = module.security_iam.registry_db_password_secret_id # Password managed via module
  gateway_db_password  = module.security_iam.gateway_db_password_secret_id
  tags                 = azurerm_resource_group.rg.tags

  depends_on = [module.networking]
}

# 5. Module 04: Messaging & SOAM (Service Bus Topics & Subscriptions with DLQ)
module "messaging" {
  source              = "../../modules/04_messaging"
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.location
  environment         = var.environment
  tags                = azurerm_resource_group.rg.tags
}

# 6. Module 05: Compute Tier (Azure Container Apps Environment & 9 Microservices)
module "compute_services" {
  source                     = "../../modules/05_compute_services"
  resource_group_name        = azurerm_resource_group.rg.name
  location                   = var.location
  environment                = var.environment
  container_apps_subnet_id   = module.networking.container_apps_subnet_id
  log_analytics_workspace_id = module.observability.log_analytics_workspace_id
  managed_identities         = module.security_iam.managed_identities
  container_images           = var.container_images
  registry_db_fqdn           = module.data_state.registry_db_fqdn
  gateway_db_fqdn            = module.data_state.gateway_db_fqdn
  cosmosdb_endpoint          = module.data_state.cosmosdb_endpoint
  key_vault_uri              = module.security_iam.key_vault_uri
  servicebus_namespace_name  = module.messaging.servicebus_namespace_name
  tags                       = azurerm_resource_group.rg.tags

  depends_on = [module.networking, module.data_state]
}

# 7. Module 06: Ingress Gateway (Azure API Management & PingIdentity JWT Auth)
module "ingress_gateway" {
  source              = "../../modules/06_ingress_gateway"
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.location
  environment         = var.environment
  agent_gateway_url   = "https://${module.compute_services.agent_gateway_fqdn}"
  tags                = azurerm_resource_group.rg.tags
}
