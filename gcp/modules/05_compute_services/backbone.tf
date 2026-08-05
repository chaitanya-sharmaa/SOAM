# ==============================================================================
# Agent Backbone & Infrastructure Microservices
# Cloud Run Direct VPC Egress: instances attach directly to snet-private-workload.
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. Agent Registry Service
# ------------------------------------------------------------------------------
resource "google_cloud_run_v2_service" "agent_registry" {
  name     = "${var.environment}-dap-agent-registry"
  location = var.region
  project  = var.project_id
  ingress  = "INGRESS_TRAFFIC_INTERNAL_ONLY"

  template {
    service_account = var.service_account_emails["agent-registry"]

    scaling {
      min_instance_count = 1
      max_instance_count = 10
    }

    vpc_access {
      network_interfaces {
        network    = var.vpc_id
        subnetwork = var.subnet_id
      }
      egress = "PRIVATE_RANGES_ONLY"
    }

    containers {
      image = var.container_images["agent-registry"]

      env {
        name  = "DB_HOST"
        value = var.registry_db_private_ip
      }
      env {
        name  = "DB_NAME"
        value = "agent_registry"
      }
      env {
        name  = "DB_USER"
        value = "registry_admin"
      }
    }
  }
}

# ------------------------------------------------------------------------------
# 2. Agent Gateway (SOAM Engine)
# ------------------------------------------------------------------------------
resource "google_cloud_run_v2_service" "agent_gateway" {
  name     = "${var.environment}-dap-agent-gateway"
  location = var.region
  project  = var.project_id
  ingress  = "INGRESS_TRAFFIC_INTERNAL_ONLY"

  template {
    service_account = var.service_account_emails["agent-gateway"]

    scaling {
      min_instance_count = 1
      max_instance_count = 20
    }

    vpc_access {
      network_interfaces {
        network    = var.vpc_id
        subnetwork = var.subnet_id
      }
      egress = "PRIVATE_RANGES_ONLY"
    }

    containers {
      image = var.container_images["agent-gateway"]

      env {
        name  = "DB_HOST"
        value = var.gateway_db_private_ip
      }
      env {
        name  = "DB_NAME"
        value = "agent_gateway"
      }
      env {
        name  = "DB_USER"
        value = "gateway_admin"
      }
      env {
        name  = "GATEKEEPER_TOPIC"
        value = var.gatekeeper_topic_id
      }
    }
  }
}

# ------------------------------------------------------------------------------
# 3. GateKeeper (Security & Validation)
# ------------------------------------------------------------------------------
resource "google_cloud_run_v2_service" "gatekeeper" {
  name     = "${var.environment}-dap-gatekeeper"
  location = var.region
  project  = var.project_id
  ingress  = "INGRESS_TRAFFIC_INTERNAL_ONLY"

  template {
    service_account = var.service_account_emails["gatekeeper"]

    scaling {
      min_instance_count = 1
      max_instance_count = 20
    }

    vpc_access {
      network_interfaces {
        network    = var.vpc_id
        subnetwork = var.subnet_id
      }
      egress = "PRIVATE_RANGES_ONLY"
    }

    containers {
      image = var.container_images["gatekeeper"]

      env {
        name  = "GUARDRAILS_URL"
        value = "https://${var.environment}-dap-guardrails-${var.project_id}.${var.region}.run.app"
      }
      env {
        name  = "CTT_BIGQUERY_DATASET"
        value = var.bigquery_dataset_id
      }
    }
  }
}

# Pub/Sub Push Invoker Permission for GateKeeper
resource "google_cloud_run_v2_service_iam_member" "gatekeeper_invoker" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.gatekeeper.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.pubsub_invoker_sa.email}"
}

# Push Subscription: GateKeeper Topic -> GateKeeper Cloud Run
resource "google_pubsub_subscription" "gatekeeper_push_sub" {
  name    = "${var.environment}-dap-gatekeeper-push-sub"
  topic   = var.gatekeeper_topic_id
  project = var.project_id

  ack_deadline_seconds = 60

  push_config {
    push_endpoint = "${google_cloud_run_v2_service.gatekeeper.uri}/v1/inspect"
    oidc_token {
      service_account_email = google_service_account.pubsub_invoker_sa.email
    }
  }

  dead_letter_policy {
    dead_letter_topic     = "projects/${var.project_id}/topics/${var.environment}-dap-gatekeeper-dlq"
    max_delivery_attempts = 5
  }

  retry_policy {
    minimum_backoff = "10s"
    maximum_backoff = "300s"
  }
}

# ------------------------------------------------------------------------------
# 4. MCP Gateway (Model Context Protocol Gateway to External APIs)
#    Needs VPC egress for Cloud NAT → static public IP → external APIs/SaaS
# ------------------------------------------------------------------------------
resource "google_cloud_run_v2_service" "mcp_gateway" {
  name     = "${var.environment}-dap-mcp-gateway"
  location = var.region
  project  = var.project_id
  ingress  = "INGRESS_TRAFFIC_INTERNAL_ONLY"

  template {
    service_account = var.service_account_emails["mcp-gateway"]

    scaling {
      min_instance_count = 1
      max_instance_count = 15
    }

    vpc_access {
      network_interfaces {
        network    = var.vpc_id
        subnetwork = var.subnet_id
      }
      egress = "PRIVATE_RANGES_ONLY"
    }

    containers {
      image = var.container_images["mcp-gateway"]
    }
  }
}

# ------------------------------------------------------------------------------
# 5. Guardrails (Safety & Policy Engine)
#    No VPC needed — only calls Vertex AI via PGA
# ------------------------------------------------------------------------------
resource "google_cloud_run_v2_service" "guardrails" {
  name     = "${var.environment}-dap-guardrails"
  location = var.region
  project  = var.project_id
  ingress  = "INGRESS_TRAFFIC_INTERNAL_ONLY"

  template {
    service_account = var.service_account_emails["guardrails"]

    scaling {
      min_instance_count = 1
      max_instance_count = 10
    }

    containers {
      image = var.container_images["guardrails"]
    }
  }
}

# ------------------------------------------------------------------------------
# 6. Grid Monitoring (Telemetry Collector)
#    Writes to BigQuery via PGA — no VPC connector needed
# ------------------------------------------------------------------------------
resource "google_cloud_run_v2_service" "grid_monitoring" {
  name     = "${var.environment}-dap-grid-monitoring"
  location = var.region
  project  = var.project_id
  ingress  = "INGRESS_TRAFFIC_INTERNAL_ONLY"

  template {
    service_account = var.service_account_emails["grid-monitoring"]

    scaling {
      min_instance_count = 1
      max_instance_count = 5
    }

    containers {
      image = var.container_images["grid-monitoring"]

      env {
        name  = "CTT_BIGQUERY_DATASET"
        value = var.bigquery_dataset_id
      }
    }
  }
}

# ------------------------------------------------------------------------------
# 7. Grid Lens (Observability & Admin UI)
# ------------------------------------------------------------------------------
resource "google_cloud_run_v2_service" "grid_lens" {
  name     = "${var.environment}-dap-grid-lens"
  location = var.region
  project  = var.project_id
  ingress  = "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER"

  template {
    service_account = var.service_account_emails["grid-lens"]

    scaling {
      min_instance_count = 1
      max_instance_count = 5
    }

    containers {
      image = var.container_images["grid-lens"]
    }
  }
}
