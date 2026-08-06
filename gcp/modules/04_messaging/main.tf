# ==============================================================================
# Module: 04_messaging
# Enterprise Pub/Sub Topics, Subscriptions & Dead Letter Queues (DLQ)
# ==============================================================================

locals {
  topics = [
    "agent-1-inbound-topic",
    "agent-2-inbound-topic",
    "gatekeeper-topic",
    "agent-gateway-topic"
  ]
}

# 1. Dead Letter Topic for Poison Messages / Failed Tasks
resource "google_pubsub_topic" "dead_letter_topic" {
  name         = "${var.environment}-dap-dlq-topic"
  project      = var.project_id

  message_retention_duration = "604800s" # 7 days retention
}

resource "google_pubsub_subscription" "dlq_subscription" {
  name                 = "${var.environment}-dap-dlq-sub"
  topic                = google_pubsub_topic.dead_letter_topic.name
  project              = var.project_id
  ack_deadline_seconds = 60
}

# 2. Main Inbound and Routing Topics with CMEK Encryption
resource "google_pubsub_topic" "topics" {
  for_each = toset(local.topics)
  name     = "${var.environment}-dap-${each.key}"
  project  = var.project_id

  message_retention_duration = "86400s" # 1 day retention
}

# 3. Pull Subscriptions with Dead Letter Policy (for manual pulling or worker pods)
resource "google_pubsub_subscription" "subscriptions" {
  for_each = toset(local.topics)
  name     = "${var.environment}-dap-${each.key}-sub"
  topic    = google_pubsub_topic.topics[each.key].name
  project  = var.project_id

  ack_deadline_seconds = 300 # 5 minutes for AI agent reasoning

  dead_letter_policy {
    dead_letter_topic     = google_pubsub_topic.dead_letter_topic.id
    max_delivery_attempts = 5
  }

  retry_policy {
    minimum_backoff = "10s"
    maximum_backoff = "600s"
  }
}
