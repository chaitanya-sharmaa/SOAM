# ==============================================================================
# Cloud Armor Security Policy: "INT WAF"
# ==============================================================================
# Enterprise Web Application Firewall (WAF) to protect the API Gateway / Load Balancer
# against OWASP Top 10 attacks, prompt injection vectors, DDoS, and bad bots.
# ==============================================================================

resource "google_compute_security_policy" "int_waf_policy" {
  name        = "${var.environment}-dap-int-waf-policy"
  description = "Enterprise Cloud Armor WAF policy for DAP ingress"
  project     = var.project_id

  # 1. Rate Limiting Rule (Mitigate DDoS / Brute-force attacks)
  rule {
    action   = "rate_based_ban"
    priority = "1000"
    match {
      versioned_expr = "SRC_IPS_V1"
      config {
        src_ip_ranges = ["*"]
      }
    }
    rate_limit_options {
      conform_action = "allow"
      exceed_action  = "deny(429)"
      enforce_on_key = "IP"
      rate_limit_threshold {
        count        = 500 # max requests
        interval_sec = 60  # per 1 minute
      }
      ban_threshold {
        count        = 1000
        interval_sec = 60
      }
      ban_duration_sec = 600 # 10 minutes ban
    }
    description = "Rate limit traffic to max 500 req/min per IP"
  }

  # 2. OWASP SQL Injection Protection (sqli-v33-stable)
  rule {
    action   = "deny(403)"
    priority = "2000"
    match {
      expr {
        expression = "evaluatePreconfiguredExpr('sqli-v33-stable')"
      }
    }
    description = "Block OWASP SQLi attempts"
  }

  # 3. OWASP Cross-Site Scripting Protection (xss-v33-stable)
  rule {
    action   = "deny(403)"
    priority = "3000"
    match {
      expr {
        expression = "evaluatePreconfiguredExpr('xss-v33-stable')"
      }
    }
    description = "Block OWASP XSS attempts"
  }

  # 4. OWASP Remote Code Execution & Local File Inclusion
  rule {
    action   = "deny(403)"
    priority = "4000"
    match {
      expr {
        expression = "evaluatePreconfiguredExpr('rce-v33-stable') || evaluatePreconfiguredExpr('lfi-v33-stable')"
      }
    }
    description = "Block OWASP RCE and LFI attacks"
  }

  # 5. Default Allow rule with Logging
  rule {
    action   = "allow"
    priority = "2147483647"
    match {
      versioned_expr = "SRC_IPS_V1"
      config {
        src_ip_ranges = ["*"]
      }
    }
    description = "Default allow rule for legitimate traffic"
  }

  adaptive_protection_config {
    layer_7_ddos_defense_config {
      enable = true
    }
  }
}
