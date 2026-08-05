# ==============================================================================
# Module: 06_ingress_gateway (Azure)
# Ingress API Gateway: Azure API Management (APIM) & PingIdentity JWT Auth
# Equivalent to Google Cloud API Gateway & PingIdentity Security Specs
# ==============================================================================

resource "random_string" "apim_suffix" {
  length  = 4
  special = false
  upper   = false
}

# 1. Azure API Management (APIM) Instance
resource "azurerm_api_management" "apim" {
  name                = "apim-${var.environment}-dap-${random_string.apim_suffix.result}"
  location            = var.location
  resource_group_name = var.resource_group_name
  publisher_name      = "Digital Agent Platform"
  publisher_email     = "platform-admin@enterprise-dap.com"
  sku_name            = "Consumption_0" # Serverless consumption tier for cost efficiency

  tags = var.tags
}

# 2. OpenAPI 3.0 API Definition for DAP
resource "azurerm_api_management_api" "dap_api" {
  name                = "dap-api"
  resource_group_name = var.resource_group_name
  api_management_name = azurerm_api_management.apim.name
  revision            = "1"
  display_name        = "Digital Agent Platform API"
  path                = "v1"
  protocols           = ["https"]
  service_url         = var.agent_gateway_url

  import {
    content_format = "openapi+json"
    content_value = jsonencode({
      openapi = "3.0.1"
      info = {
        title       = "Digital Agent Platform (DAP) API"
        description = "Enterprise Ingress Gateway for Autonomous AI Agents"
        version     = "1.0.0"
      }
      paths = {
        "/agents/invoke" = {
          post = {
            summary     = "Invoke Autonomous AI Agent"
            operationId = "invokeAgent"
            responses = {
              "200" = { description = "Agent execution response" }
              "401" = { description = "Unauthorized - Invalid PingIdentity JWT" }
              "403" = { description = "Forbidden by WAF or Guardrails" }
            }
          }
        }
        "/agents/registry" = {
          get = {
            summary     = "Discover Registered AI Agents"
            operationId = "getAgentRegistry"
            responses = {
              "200" = { description = "List of active agents and schemas" }
            }
          }
        }
        "/health" = {
          get = {
            summary     = "Gateway Health Check"
            operationId = "getHealth"
            responses = {
              "200" = { description = "System healthy" }
            }
          }
        }
      }
    })
  }
}

# 3. Inbound Policy: PingIdentity JWT Token Validation
resource "azurerm_api_management_api_policy" "jwt_validation" {
  api_name            = azurerm_api_management_api.dap_api.name
  api_management_name = azurerm_api_management.apim.name
  resource_group_name = var.resource_group_name

  xml_content = <<XML
<policies>
    <inbound>
        <base />
        <!-- PingIdentity JWT Token Validation Policy -->
        <validate-jwt header-name="Authorization" failed-validation-httpcode="401" failed-validation-error-message="Unauthorized: Invalid or expired PingIdentity JWT token" require-expiration-time="true" require-scheme="Bearer">
            <openid-config url="${var.pingidentity_jwks_uri}" />
            <issuers>
                <issuer>${var.pingidentity_issuer}</issuer>
            </issuers>
        </validate-jwt>
        <!-- Forward to Agent Gateway Backend -->
        <set-backend-service base-url="${var.agent_gateway_url}" />
    </inbound>
    <backend>
        <base />
    </backend>
    <outbound>
        <base />
    </outbound>
    <on-error>
        <base />
    </on-error>
</policies>
XML
}
