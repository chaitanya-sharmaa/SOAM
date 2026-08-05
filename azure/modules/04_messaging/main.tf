# ==============================================================================
# Module: 04_messaging (Azure)
# Event-Driven Messaging: Azure Service Bus Topics, Subscriptions & Dead-Letter
# Equivalent to Google Cloud Pub/Sub Topics & Push Subscriptions with DLQ
# ==============================================================================

resource "random_string" "sb_suffix" {
  length  = 4
  special = false
  upper   = false
}

# 1. Service Bus Namespace
resource "azurerm_servicebus_namespace" "dap_servicebus" {
  name                = "sb-${var.environment}-dap-${random_string.sb_suffix.result}"
  location            = var.location
  resource_group_name = var.resource_group_name
  sku                 = "Standard" # Supports Topics & Subscriptions

  tags = var.tags
}

locals {
  topics = [
    "agent-1-inbound-topic",
    "agent-2-inbound-topic",
    "gatekeeper-topic",
    "agent-gateway-topic"
  ]
}

# 2. Service Bus Topics (Asynchronous SOAM Event Queues)
resource "azurerm_servicebus_topic" "topics" {
  for_each     = toset(local.topics)
  name         = "sb-${var.environment}-${each.key}"
  namespace_id = azurerm_servicebus_namespace.dap_servicebus.id

  partitioning_enabled                    = true
  max_size_in_megabytes                   = 1024
  default_message_ttl                     = "P1D" # 1 day retention
  requires_duplicate_detection            = true
  duplicate_detection_history_time_window = "PT10M"
}

# 3. Subscriptions with Dead-Lettering (DLQ) & Retry Policies
resource "azurerm_servicebus_subscription" "subscriptions" {
  for_each = azurerm_servicebus_topic.topics
  name     = "sub-${var.environment}-${each.key}-default"
  topic_id = each.value.id

  max_delivery_count                        = 5 # Moves to Dead-Letter subqueue after 5 failed deliveries
  dead_lettering_on_message_expiration      = true
  dead_lettering_on_filter_evaluation_error = true
  lock_duration                             = "PT1M" # 1 minute processing lock
  batched_operations_enabled                = true
}
