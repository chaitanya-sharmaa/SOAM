output "agent_1_uri" {
  description = "URI of Agent 1 Cloud Run service"
  value       = google_cloud_run_v2_service.agent_1.uri
}

output "agent_2_uri" {
  description = "URI of Agent 2 Cloud Run service"
  value       = google_cloud_run_v2_service.agent_2.uri
}
