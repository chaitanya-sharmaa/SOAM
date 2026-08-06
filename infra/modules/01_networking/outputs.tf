output "vpc_id" {
  description = "The ID of the created VPC"
  value       = google_compute_network.vpc.id
}

output "vpc_name" {
  description = "The Name of the created VPC"
  value       = google_compute_network.vpc.name
}

output "subnet_id" {
  description = "The ID of the private subnetwork (snet-private-workload). Used by Cloud Run Direct VPC Egress."
  value       = google_compute_subnetwork.private_subnet.id
}

output "subnet_name" {
  description = "The Name of the private subnetwork (snet-private-workload)"
  value       = google_compute_subnetwork.private_subnet.name
}

output "nat_static_ip" {
  description = "The static public IP address used by Cloud NAT for predictable external egress (allowlistable by partner firewalls)"
  value       = google_compute_address.nat_static_ip.address
}

output "private_vpc_connection" {
  description = "The private service networking connection resource (for dependency chaining with Cloud SQL)"
  value       = google_service_networking_connection.private_vpc_connection.id
}
