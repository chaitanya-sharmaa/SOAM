# ==============================================================================
# Module: 01_networking (Azure)
# Virtual Network, Subnets, Subnet Delegations, NAT Gateway, Private DNS
# ==============================================================================

# 1. Main Virtual Network
resource "azurerm_virtual_network" "vnet" {
  name                = "vnet-${var.environment}-dap"
  location            = var.location
  resource_group_name = var.resource_group_name
  address_space       = var.vnet_address_space

  tags = var.tags
}

# 2. Subnet for Azure Container Apps Infrastructure
resource "azurerm_subnet" "snet_container_apps" {
  name                 = "snet-${var.environment}-container-apps"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = var.container_apps_subnet_cidr

  # Delegation for Container Apps Environment
  delegation {
    name = "container-apps-delegation"
    service_delegation {
      name    = "Microsoft.App/environments"
      actions = ["Microsoft.Network/virtualNetworks/subnets/join/action"]
    }
  }
}

# 3. Subnet for PostgreSQL Flexible Server (Delegated)
resource "azurerm_subnet" "snet_postgres" {
  name                 = "snet-${var.environment}-postgres"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = var.postgres_subnet_cidr

  delegation {
    name = "postgres-delegation"
    service_delegation {
      name    = "Microsoft.DBforPostgreSQL/flexibleServers"
      actions = ["Microsoft.Network/virtualNetworks/subnets/join/action"]
    }
  }
}

# 4. Subnet for Private Endpoints (Key Vault, Cosmos DB, Service Bus, Storage)
resource "azurerm_subnet" "snet_private_endpoints" {
  name                 = "snet-${var.environment}-private-endpoints"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = var.private_endpoints_subnet_cidr
}

# 5. Subnet for Ingress API Gateway (APIM)
resource "azurerm_subnet" "snet_gateway" {
  name                 = "snet-${var.environment}-apim-gateway"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = var.gateway_subnet_cidr
}

# 6. Static Outbound Egress: Azure NAT Gateway & Public IP
resource "azurerm_public_ip" "nat_pip" {
  name                = "pip-${var.environment}-dap-nat"
  location            = var.location
  resource_group_name = var.resource_group_name
  allocation_method   = "Static"
  sku                 = "Standard"

  tags = var.tags
}

resource "azurerm_nat_gateway" "nat_gw" {
  name                    = "nat-${var.environment}-dap"
  location                = var.location
  resource_group_name     = var.resource_group_name
  sku_name                = "Standard"
  idle_timeout_in_minutes = 10

  tags = var.tags
}

resource "azurerm_nat_gateway_public_ip_association" "nat_pip_assoc" {
  nat_gateway_id       = azurerm_nat_gateway.nat_gw.id
  public_ip_address_id = azurerm_public_ip.nat_pip.id
}

resource "azurerm_subnet_nat_gateway_association" "container_apps_nat" {
  subnet_id      = azurerm_subnet.snet_container_apps.id
  nat_gateway_id = azurerm_nat_gateway.nat_gw.id
}

# 7. Private DNS Zone for PostgreSQL Flexible Server
resource "azurerm_private_dns_zone" "postgres_dns" {
  name                = "${var.environment}.dap.postgres.database.azure.com"
  resource_group_name = var.resource_group_name

  tags = var.tags
}

resource "azurerm_private_dns_zone_virtual_network_link" "postgres_dns_link" {
  name                  = "link-${var.environment}-postgres-dns"
  private_dns_zone_name = azurerm_private_dns_zone.postgres_dns.name
  resource_group_name   = var.resource_group_name
  virtual_network_id    = azurerm_virtual_network.vnet.id
}

# 8. Network Security Group for Microservices Subnet
resource "azurerm_network_security_group" "nsg_container_apps" {
  name                = "nsg-${var.environment}-container-apps"
  location            = var.location
  resource_group_name = var.resource_group_name

  security_rule {
    name                       = "Allow-Internal-VNet-Inbound"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "VirtualNetwork"
    destination_address_prefix = "VirtualNetwork"
  }

  security_rule {
    name                       = "Deny-Direct-Internet-Inbound"
    priority                   = 1000
    direction                  = "Inbound"
    access                     = "Deny"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "Internet"
    destination_address_prefix = "*"
  }

  tags = var.tags
}

resource "azurerm_subnet_network_security_group_association" "nsg_assoc" {
  subnet_id                 = azurerm_subnet.snet_container_apps.id
  network_security_group_id = azurerm_network_security_group.nsg_container_apps.id
}
