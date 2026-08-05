# ==============================================================================
# Agent Project Workspace: Agent 1 & Agent 2 Execution Compute
# ==============================================================================

# ------------------------------------------------------------------------------
# Agent 1
# ------------------------------------------------------------------------------
resource "google_cloud_run_v2_service" "agent_1" {
  name     = "${var.environment}-dap-agent-1"
  location = var.region
  project  = var.project_id
  ingress  = "INGRESS_TRAFFIC_INTERNAL_ONLY"

  template {
    service_account = var.service_account_emails["agent-1"]

    scaling {
      min_instance_count = 0
      max_instance_count = 10
    }

    vpc_access {
      connector = var.vpc_connector_id
      egress    = "PRIVATE_RANGES_ONLY"
    }

    containers {
      image = var.container_images["agent-1"]

      resources {
        limits = {
          cpu    = "2"
          memory = "4Gi"
        }
      }

      env {
        name  = "ENVIRONMENT"
        value = var.environment
      }
      env {
        name  = "PROJECT_ID"
        value = var.project_id
      }
      env {
        name  = "FIRESTORE_DATABASE"
        value = var.firestore_database_name
      }
      env {
        name  = "MCP_GATEWAY_URL"
        value = "http://${var.environment}-dap-mcp-gateway.${var.region}.run.app"
      }
      env {
        name  = "GUARDRAILS_URL"
        value = "http://${var.environment}-dap-guardrails.${var.region}.run.app"
      }
    }
  }
}

# Pub/Sub Push Invoker Permission for Agent 1
resource "google_cloud_run_v2_service_iam_member" "agent_1_invoker" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.agent_1.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.pubsub_invoker_sa.email}"
}

# Push Subscription: Agent 1 Inbound Topic -> Agent 1 Cloud Run
resource "google_pubsub_subscription" "agent_1_push_sub" {
  name    = "${var.environment}-dap-agent-1-push-sub"
  topic   = var.agent_1_inbound_topic_id
  project = var.project_id

  ack_deadline_seconds = 300

  push_config {
    push_endpoint = "${google_cloud_run_v2_service.agent_1.uri}/v1/tasks/process"
    oidc_token {
      service_account_email = google_service_account.pubsub_invoker_sa.email
    }
  }
}

# ------------------------------------------------------------------------------
# Agent 2
# ------------------------------------------------------------------------------
resource "google_cloud_run_v2_service" "agent_2" {
  name     = "${var.environment}-dap-agent-2"
  location = var.region
  project  = var.project_id
  ingress  = "INGRESS_TRAFFIC_INTERNAL_ONLY"

  template {
    service_account = var.service_account_emails["agent-2"]

    scaling {
      min_instance_count = 0
      max_instance_count = 10
    }

    vpc_access {
      connector = var.vpc_connector_id
      egress    = "PRIVATE_RANGES_ONLY"
    }

    containers {
      image = var.container_images["agent-2"]

      resources {
        limits = {
          cpu    = "2"
          memory = "4Gi"
        }
      }

      env {
        name  = "ENVIRONMENT"
        value = var.environment
      }
      env {
        name  = "PROJECT_ID"
        value = var.project_id
      }
      env {
        name  = "FIRESTORE_DATABASE"
        value = var.firestore_database_name
      }
      env {
        name  = "MCP_GATEWAY_URL"
        value = "http://${var.environment}-dap-mcp-gateway.${var.region}.run.app"
      }
    }
  }
}

# Pub/Sub Push Invoker Permission for Agent 2
resource "google_cloud_run_v2_service_iam_member" "agent_2_invoker" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.agent_2.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.pubsub_invoker_sa.email}"
}

# Push Subscription: Agent 2 Inbound Topic -> Agent 2 Cloud Run
resource "google_pubsub_subscription" "agent_2_push_sub" {
  name    = "${var.environment}-dap-agent-2-push-sub"
  topic   = var.agent_2_inbound_topic_id
  project = var.project_id

  ack_deadline_seconds = 300

  push_config {
    push_endpoint = "${google_cloud_run_v2_service.agent_2.uri}/v1/tasks/process"
    oidc_token {
      service_account_email = google_service_account.pubsub_invoker_sa.email
    }
  }
}
