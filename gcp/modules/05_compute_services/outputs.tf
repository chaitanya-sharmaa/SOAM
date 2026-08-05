output "agent_1_uri" {
  description = "URI of Agent 1 Cloud Run service"
  value       = google_cloud_run_v2_service.agent_1.uri
}

output "agent_2_uri" {
  description = "URI of Agent 2 Cloud Run service"
  value       = google_cloud_run_v2_service.agent_2.uri
}

output "agent_registry_uri" {
  description = "URI of Agent Registry Cloud Run service"
  value       = google_cloud_run_v2_service.agent_registry.uri
}

output "agent_gateway_uri" {
  description = "URI of Agent Gateway Cloud Run service"
  value       = google_cloud_run_v2_service.agent_gateway.uri
}

output "gatekeeper_uri" {
  description = "URI of GateKeeper Cloud Run service"
  value       = google_cloud_run_v2_service.gatekeeper.uri
}

output "mcp_gateway_uri" {
  description = "URI of MCP Gateway Cloud Run service"
  value       = google_cloud_run_v2_service.mcp_gateway.uri
}

output "grid_lens_uri" {
  description = "URI of Grid Lens Web UI"
  value       = google_cloud_run_v2_service.grid_lens.uri
}
