# ==============================================================================
# Security: Azure Key Vault (CMEK Encryption Keys & Secret Management)
# Equivalent to GCP Cloud KMS & Secret Manager
# ==============================================================================

resource "random_string" "kv_suffix" {
  length  = 5
  special = false
  upper   = false
}

# 1. Azure Key Vault
resource "azurerm_key_vault" "kv" {
  name                       = "kv-${var.environment}-dap-${random_string.kv_suffix.result}"
  location                   = var.location
  resource_group_name        = var.resource_group_name
  tenant_id                  = var.tenant_id
  sku_name                   = "premium" # Supports HSM-backed CMEK keys
  purge_protection_enabled   = false     # Set to true in prod
  soft_delete_retention_days = 7
  enable_rbac_authorization  = true

  tags = var.tags
}

# 2. Grant Current Deployer Key Vault Administrator Role
resource "azurerm_role_assignment" "deployer_kv_admin" {
  scope                = azurerm_key_vault.kv.id
  role_definition_name = "Key Vault Administrator"
  principal_id         = data.azurerm_client_config.current.object_id
}

# 3. Customer-Managed Encryption Keys (CMEK)
resource "azurerm_key_vault_key" "cmek_keys" {
  for_each = toset([
    "key-postgres",
    "key-cosmos",
    "key-servicebus",
    "key-storage"
  ])

  name         = each.key
  key_vault_id = azurerm_key_vault.kv.id
  key_type     = "RSA"
  key_size     = 3072

  key_opts = [
    "decrypt",
    "encrypt",
    "sign",
    "unwrapKey",
    "verify",
    "wrapKey"
  ]

  depends_on = [azurerm_role_assignment.deployer_kv_admin]
}

# 4. Key Vault Secrets for Database Passwords and Integrations
resource "random_password" "registry_db_pass" {
  length  = 24
  special = false
}

resource "random_password" "gateway_db_pass" {
  length  = 24
  special = false
}

resource "azurerm_key_vault_secret" "registry_db_password" {
  name         = "agent-registry-db-password"
  value        = random_password.registry_db_pass.result
  key_vault_id = azurerm_key_vault.kv.id
  depends_on   = [azurerm_role_assignment.deployer_kv_admin]
}

resource "azurerm_key_vault_secret" "gateway_db_password" {
  name         = "agent-gateway-db-password"
  value        = random_password.gateway_db_pass.result
  key_vault_id = azurerm_key_vault.kv.id
  depends_on   = [azurerm_role_assignment.deployer_kv_admin]
}

resource "azurerm_key_vault_secret" "pingidentity_secret" {
  name         = "pingidentity-client-secret"
  value        = "dap-azure-pingidentity-placeholder-secret-v1"
  key_vault_id = azurerm_key_vault.kv.id
  depends_on   = [azurerm_role_assignment.deployer_kv_admin]
}

resource "azurerm_key_vault_secret" "mcp_api_key" {
  name         = "external-mcp-api-key"
  value        = "dap-azure-mcp-gateway-default-token"
  key_vault_id = azurerm_key_vault.kv.id
  depends_on   = [azurerm_role_assignment.deployer_kv_admin]
}

# 5. Grant Microservice Managed Identities Access to Read Key Vault Secrets
resource "azurerm_role_assignment" "secrets_user" {
  for_each             = azurerm_user_assigned_identity.microservice_identities
  scope                = azurerm_key_vault.kv.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = each.value.principal_id
}

# 6. Grant Microservice Managed Identities Access to Crypto Operations
resource "azurerm_role_assignment" "crypto_user" {
  for_each             = azurerm_user_assigned_identity.microservice_identities
  scope                = azurerm_key_vault.kv.id
  role_definition_name = "Key Vault Crypto User"
  principal_id         = each.value.principal_id
}
