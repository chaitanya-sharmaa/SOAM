output "gateway_url" {
  description = "Public HTTPS URL of the deployed API Gateway"
  value       = "https://${google_api_gateway_gateway.dap_gateway.default_hostname}"
}

output "agent_1_gateway_endpoint" {
  description = "API Gateway Endpoint for Agent 1 (Coordinator)"
  value       = "https://${google_api_gateway_gateway.dap_gateway.default_hostname}/v1/agent1/tasks"
}

output "agent_2_gateway_endpoint" {
  description = "API Gateway Endpoint for Agent 2 (Worker)"
  value       = "https://${google_api_gateway_gateway.dap_gateway.default_hostname}/v1/agent2/tasks"
}

output "agent_1_direct_url" {
  description = "Direct Cloud Run backend URI for Agent 1"
  value       = var.agent_1_backend_url
}

output "agent_2_direct_url" {
  description = "Direct Cloud Run backend URI for Agent 2"
  value       = var.agent_2_backend_url
}

output "gateway_hostname" {
  description = "Default hostname of the deployed API Gateway"
  value       = google_api_gateway_gateway.dap_gateway.default_hostname
}

output "gateway_id" {
  description = "The ID of the API Gateway"
  value       = google_api_gateway_gateway.dap_gateway.id
}
