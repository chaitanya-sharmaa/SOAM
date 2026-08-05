# ==============================================================================
# Module: 01_networking
# Enterprise VPC, Subnets, Private Service Access & Direct VPC Egress
# NOTE: VPC Access Connector (e2-micro VMs) replaced with Cloud Run Direct VPC Egress.
#       Cloud Run instances attach directly to snet-private-workload — no proxy layer.
# ==============================================================================

# 1. Custom VPC Network
resource "google_compute_network" "vpc" {
  name                            = "${var.environment}-dap-vpc"
  auto_create_subnetworks         = false
  routing_mode                    = "GLOBAL"
  delete_default_routes_on_create = false
  project                         = var.project_id
}

# 2. Private Subnetwork with Private Google Access enabled
#    This subnet is also used by Cloud Run Direct VPC Egress.
#    Each Cloud Run instance gets an IP from this range directly — no connector VMs.
resource "google_compute_subnetwork" "private_subnet" {
  name                     = "${var.environment}-dap-private-subnet"
  ip_cidr_range            = var.subnet_cidr
  region                   = var.region
  network                  = google_compute_network.vpc.id
  private_ip_google_access = true
  project                  = var.project_id

  log_config {
    aggregation_interval = "INTERVAL_5_SEC"
    flow_sampling        = var.environment == "prod" ? 1.0 : 0.5
    metadata             = "INCLUDE_ALL_METADATA"
  }
}

# 3. Reserved IP Range for Private Service Access (Cloud SQL Private IP peering)
resource "google_compute_global_address" "private_ip_address" {
  name          = "${var.environment}-dap-psa-range"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 20
  network       = google_compute_network.vpc.id
  project       = var.project_id
}

# 4. Private Service Networking Connection (VPC Peering with Google Services for Cloud SQL)
resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = google_compute_network.vpc.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_address.name]
}

# 5. Static External IP for Cloud NAT (dedicated, allowlistable egress IP for external APIs)
#    Cloud Run → Direct VPC Egress → Cloud NAT → this static IP → External APIs/SaaS
resource "google_compute_address" "nat_static_ip" {
  name    = "${var.environment}-dap-nat-ip"
  region  = var.region
  project = var.project_id
}

# 6. Cloud NAT Router
resource "google_compute_router" "router" {
  name    = "${var.environment}-dap-router"
  region  = var.region
  network = google_compute_network.vpc.id
  project = var.project_id
}

# 7. Cloud NAT Gateway (MANUAL_ONLY with static IP for deterministic external egress)
resource "google_compute_router_nat" "nat" {
  name                               = "${var.environment}-dap-nat"
  router                             = google_compute_router.router.name
  region                             = var.region
  project                            = var.project_id
  nat_ip_allocate_option             = "MANUAL_ONLY"
  nat_ips                            = [google_compute_address.nat_static_ip.self_link]
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"

  log_config {
    enable = true
    filter = "ERRORS_ONLY"
  }
}

# 8. Internal Ingress Firewall Rule (Zero Trust within VPC)
resource "google_compute_firewall" "allow_internal" {
  name    = "${var.environment}-dap-allow-internal"
  network = google_compute_network.vpc.name
  project = var.project_id

  allow {
    protocol = "tcp"
    ports    = ["443", "5432", "8080"]
  }

  source_ranges = [var.subnet_cidr]
}
