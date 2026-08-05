output "vpc_id" {
  description = "The ID of the created VPC"
  value       = google_compute_network.vpc.id
}

output "vpc_name" {
  description = "The Name of the created VPC"
  value       = google_compute_network.vpc.name
}

output "subnet_id" {
  description = "The ID of the private subnetwork"
  value       = google_compute_subnetwork.private_subnet.id
}

output "subnet_name" {
  description = "The Name of the private subnetwork"
  value       = google_compute_subnetwork.private_subnet.name
}

output "vpc_connector_id" {
  description = "The ID of the Serverless VPC Access connector for Cloud Run"
  value       = google_vpc_access_connector.connector.id
}

output "security_policy_id" {
  description = "The ID of the Cloud Armor INT WAF security policy"
  value       = google_compute_security_policy.int_waf_policy.id
}

output "private_vpc_connection" {
  description = "The private service networking connection resource (for dependency chaining with Cloud SQL)"
  value       = google_service_networking_connection.private_vpc_connection.id
}
