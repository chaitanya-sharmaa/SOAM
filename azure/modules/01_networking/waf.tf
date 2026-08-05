# ==============================================================================
# Edge Defense: Azure Front Door & Web Application Firewall (WAF)
# Equivalent to Google Cloud Armor Security Policy
# ==============================================================================

# 1. Front Door Web Application Firewall (WAF) Policy
resource "azurerm_cdn_frontdoor_firewall_policy" "waf_policy" {
  name                              = "fdfp${var.environment}dapwaf"
  resource_group_name               = var.resource_group_name
  sku_name                          = "Premium_AzureFrontDoor"
  enabled                           = true
  mode                              = "Prevention"
  custom_block_response_status_code = 403
  custom_block_response_body        = "eyJzdGF0dXMiOiAiZm9yYmlkZGVuIiwgIm1lc3NhZ2UiOiAiUmVxdWVzdCBibG9ja2VkIGJ5IERBUCBFbnRlcnByaXNlIFdBRiBQb2xpY3kifQ=="

  # 1. Rate Limiting Rule: 500 requests per minute per client IP
  custom_rule {
    name                           = "RateLimit500PerMinute"
    enabled                        = true
    priority                       = 100
    type                           = "RateLimitRule"
    action                         = "Block"
    rate_limit_duration_in_minutes = 1
    rate_limit_threshold           = 500

    match_condition {
      match_variable     = "RemoteAddr"
      operator           = "IPMatch"
      negation_condition = false
      match_values       = ["0.0.0.0/0", "::/0"]
    }
  }

  # 2. Managed OWASP Core Rule Set (SQLi, XSS, RCE, LFI)
  managed_rule {
    type    = "Microsoft_DefaultRuleSet"
    version = "2.1"
    action  = "Block"
  }

  # 3. Managed Bot Protection Rule Set
  managed_rule {
    type    = "Microsoft_BotManagerRuleSet"
    version = "1.0"
    action  = "Block"
  }

  tags = var.tags
}

# 2. Azure Front Door Profile (Global Edge)
resource "azurerm_cdn_frontdoor_profile" "frontdoor" {
  name                = "afd-${var.environment}-dap"
  resource_group_name = var.resource_group_name
  sku_name            = "Premium_AzureFrontDoor"

  tags = var.tags
}

# 3. Front Door Endpoint
resource "azurerm_cdn_frontdoor_endpoint" "endpoint" {
  name                     = "fde-${var.environment}-dap"
  cdn_frontdoor_profile_id = azurerm_cdn_frontdoor_profile.frontdoor.id

  tags = var.tags
}

# 4. Security Policy Associating WAF with Endpoint
resource "azurerm_cdn_frontdoor_security_policy" "security_policy" {
  name                     = "secpol-${var.environment}-dap"
  cdn_frontdoor_profile_id = azurerm_cdn_frontdoor_profile.frontdoor.id

  security_policies {
    firewall {
      cdn_frontdoor_firewall_policy_id = azurerm_cdn_frontdoor_firewall_policy.waf_policy.id
      association {
        domain {
          cdn_frontdoor_domain_id = azurerm_cdn_frontdoor_endpoint.endpoint.id
        }
        patterns_to_match = ["/*"]
      }
    }
  }
}
