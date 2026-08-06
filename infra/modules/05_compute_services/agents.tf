# ==============================================================================
# Module: 05_compute_services
# SOAM Mesh: Agent 1 (Primary Coordinator) & Agent 2 (Worker) Compute
# Cloud Run Direct VPC Egress: instances attach directly to private subnet.
# ==============================================================================

locals {
  should_build_agent_1 = var.agent_1_source_dir != ""
  should_build_agent_2 = var.agent_2_source_dir != ""

  # Detect code changes to trigger automated image builds during apply
  agent_1_src_hash = local.should_build_agent_1 ? sha1(join("", [for f in fileset(var.agent_1_source_dir, "*") : filesha1("${var.agent_1_source_dir}/${f}")])) : ""
  agent_2_src_hash = local.should_build_agent_2 ? sha1(join("", [for f in fileset(var.agent_2_source_dir, "*") : filesha1("${var.agent_2_source_dir}/${f}")])) : ""
}

# ------------------------------------------------------------------------------
# Automated Container Build Triggers
# ------------------------------------------------------------------------------
resource "null_resource" "build_agent_1" {
  count = local.should_build_agent_1 ? 1 : 0

  triggers = {
    source_hash = local.agent_1_src_hash
    project_id  = var.project_id
    image_tag   = var.container_images["agent-1"]
  }

  provisioner "local-exec" {
    command = "gcloud builds submit '${var.agent_1_source_dir}' --tag='${var.container_images["agent-1"]}' --project='${var.project_id}' --quiet"
  }
}

resource "null_resource" "build_agent_2" {
  count = local.should_build_agent_2 ? 1 : 0

  triggers = {
    source_hash = local.agent_2_src_hash
    project_id  = var.project_id
    image_tag   = var.container_images["agent-2"]
  }

  provisioner "local-exec" {
    command = "gcloud builds submit '${var.agent_2_source_dir}' --tag='${var.container_images["agent-2"]}' --project='${var.project_id}' --quiet"
  }
}

# ------------------------------------------------------------------------------
# Agent 1 (Coordinator)
# ------------------------------------------------------------------------------
resource "google_cloud_run_v2_service" "agent_1" {
  name     = "${var.environment}-dap-agent-1"
  location = var.region
  project  = var.project_id
  ingress  = "INGRESS_TRAFFIC_ALL"

  depends_on = [null_resource.build_agent_1]

  template {
    service_account = var.service_account_emails["agent-1"]

    scaling {
      min_instance_count = 0
      max_instance_count = 2
    }

    vpc_access {
      network_interfaces {
        network    = var.vpc_id
        subnetwork = var.subnet_id
      }
      egress = "PRIVATE_RANGES_ONLY"
    }

    containers {
      image = var.container_images["agent-1"]

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
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
        name  = "DB_HOST"
        value = var.db_private_ip
      }
      env {
        name  = "AGENT_2_TOPIC"
        value = var.agent_2_inbound_topic_id
      }
      env {
        name  = "CODE_HASH"
        value = local.agent_1_src_hash
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

# API Gateway Invoker Permission for Agent 1
resource "google_cloud_run_v2_service_iam_member" "agent_1_gateway_invoker" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.agent_1.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:sa-${var.environment}-api-gateway@${var.project_id}.iam.gserviceaccount.com"
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

  dead_letter_policy {
    dead_letter_topic     = "projects/${var.project_id}/topics/${var.environment}-dap-dlq-topic"
    max_delivery_attempts = 5
  }

  retry_policy {
    minimum_backoff = "10s"
    maximum_backoff = "600s"
  }
}

# ------------------------------------------------------------------------------
# Agent 2 (Worker / Specialist)
# ------------------------------------------------------------------------------
resource "google_cloud_run_v2_service" "agent_2" {
  name     = "${var.environment}-dap-agent-2"
  location = var.region
  project  = var.project_id
  ingress  = "INGRESS_TRAFFIC_ALL"

  depends_on = [null_resource.build_agent_2]

  template {
    service_account = var.service_account_emails["agent-2"]

    scaling {
      min_instance_count = 0
      max_instance_count = 2
    }

    vpc_access {
      network_interfaces {
        network    = var.vpc_id
        subnetwork = var.subnet_id
      }
      egress = "PRIVATE_RANGES_ONLY"
    }

    containers {
      image = var.container_images["agent-2"]

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
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
        name  = "DB_HOST"
        value = var.db_private_ip
      }
      env {
        name  = "CODE_HASH"
        value = local.agent_2_src_hash
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

# API Gateway Invoker Permission for Agent 2
resource "google_cloud_run_v2_service_iam_member" "agent_2_gateway_invoker" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.agent_2.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:sa-${var.environment}-api-gateway@${var.project_id}.iam.gserviceaccount.com"
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

  dead_letter_policy {
    dead_letter_topic     = "projects/${var.project_id}/topics/${var.environment}-dap-dlq-topic"
    max_delivery_attempts = 5
  }

  retry_policy {
    minimum_backoff = "10s"
    maximum_backoff = "600s"
  }
}
