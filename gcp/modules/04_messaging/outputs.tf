output "topic_ids" {
  description = "Map of all Pub/Sub topic IDs"
  value       = { for k, v in google_pubsub_topic.topics : k => v.id }
}

output "topic_names" {
  description = "Map of all Pub/Sub topic names"
  value       = { for k, v in google_pubsub_topic.topics : k => v.name }
}

output "agent_1_inbound_topic_id" {
  description = "ID of Agent 1 Inbound Topic"
  value       = google_pubsub_topic.topics["agent-1-inbound-topic"].id
}

output "agent_2_inbound_topic_id" {
  description = "ID of Agent 2 Inbound Topic"
  value       = google_pubsub_topic.topics["agent-2-inbound-topic"].id
}

output "gatekeeper_topic_id" {
  description = "ID of GateKeeper Topic"
  value       = google_pubsub_topic.topics["gatekeeper-topic"].id
}

output "agent_gateway_topic_id" {
  description = "ID of Agent Gateway Topic"
  value       = google_pubsub_topic.topics["agent-gateway-topic"].id
}

output "dlq_topic_id" {
  description = "ID of the Dead Letter Topic"
  value       = google_pubsub_topic.dead_letter_topic.id
}
