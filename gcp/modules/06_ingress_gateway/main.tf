# ==============================================================================
# Module: 06_ingress_gateway
# Google Cloud API Gateway with PingIdentity JWT Security & Backend Routing
# ==============================================================================

# 1. Service Account for API Gateway
resource "google_service_account" "api_gateway_sa" {
  account_id   = "sa-${var.environment}-api-gateway"
  display_name = "DAP API Gateway Service Account"
  project      = var.project_id
}

# Grant API Gateway permission to invoke Cloud Run backends
resource "google_project_iam_member" "api_gateway_run_invoker" {
  project = var.project_id
  role    = "roles/run.invoker"
  member  = "serviceAccount:${google_service_account.api_gateway_sa.email}"
}

# 2. Cloud API Gateway Definition
resource "google_api_gateway_api" "dap_api" {
  provider     = google-beta
  api_id       = "${var.environment}-dap-api"
  display_name = "Digital Agent Platform API"
  project      = var.project_id
}

# 3. API Gateway Configuration with OpenAPI Spec
resource "google_api_gateway_api_config" "dap_api_cfg" {
  provider      = google-beta
  api           = google_api_gateway_api.dap_api.api_id
  api_config_id = "${var.environment}-dap-cfg-${formatdate("YYYYMMDDhhmmss", timestamp())}"
  display_name  = "DAP API Config"
  project       = var.project_id

  openapi_documents {
    document {
      path = "openapi_spec.yaml"
      contents = base64encode(templatefile("${path.module}/openapi_spec.yaml.tpl", {
        agent_gateway_backend_url  = var.agent_gateway_backend_url
        agent_registry_backend_url = var.agent_registry_backend_url
        pingidentity_issuer_url    = var.pingidentity_issuer_url
        pingidentity_jwks_url      = var.pingidentity_jwks_url
        pingidentity_audience      = var.pingidentity_audience
      }))
    }
  }

  gateway_config {
    backend_config {
      google_service_account = google_service_account.api_gateway_sa.email
    }
  }

  lifecycle {
    create_before_destroy = true
    ignore_changes        = [api_config_id]
  }
}

# 4. API Gateway Deployment Instance
resource "google_api_gateway_gateway" "dap_gateway" {
  provider   = google-beta
  gateway_id = "${var.environment}-dap-gateway"
  api_config = google_api_gateway_api_config.dap_api_cfg.id
  region     = var.region
  project    = var.project_id
}
