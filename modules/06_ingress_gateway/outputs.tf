output "gateway_hostname" {
  description = "Default public/internal hostname of the deployed API Gateway"
  value       = google_api_gateway_gateway.dap_gateway.default_hostname
}

output "gateway_id" {
  description = "The ID of the API Gateway"
  value       = google_api_gateway_gateway.dap_gateway.id
}
