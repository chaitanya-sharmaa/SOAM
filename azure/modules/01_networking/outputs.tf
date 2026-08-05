output "vnet_id" {
  description = "ID of the Virtual Network."
  value       = azurerm_virtual_network.vnet.id
}

output "vnet_name" {
  description = "Name of the Virtual Network."
  value       = azurerm_virtual_network.vnet.name
}

output "container_apps_subnet_id" {
  description = "Subnet ID for Container Apps Environment."
  value       = azurerm_subnet.snet_container_apps.id
}

output "postgres_subnet_id" {
  description = "Subnet ID for PostgreSQL Flexible Server."
  value       = azurerm_subnet.snet_postgres.id
}

output "private_endpoints_subnet_id" {
  description = "Subnet ID for Private Endpoints."
  value       = azurerm_subnet.snet_private_endpoints.id
}

output "gateway_subnet_id" {
  description = "Subnet ID for Ingress Gateway (APIM)."
  value       = azurerm_subnet.snet_gateway.id
}

output "nat_gateway_public_ip" {
  description = "Static outbound public IP for Azure NAT Gateway."
  value       = azurerm_public_ip.nat_pip.ip_address
}

output "postgres_private_dns_zone_id" {
  description = "ID of the Private DNS Zone for PostgreSQL."
  value       = azurerm_private_dns_zone.postgres_dns.id
}

output "frontdoor_endpoint_hostname" {
  description = "Global Front Door Ingress Endpoint Hostname."
  value       = azurerm_cdn_frontdoor_endpoint.endpoint.host_name
}
