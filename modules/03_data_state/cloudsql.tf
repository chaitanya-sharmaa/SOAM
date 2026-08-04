# ==============================================================================
# Cloud SQL: Agent Registry DB & Agent Gateway DB (PostgreSQL 15 Private IP)
# ==============================================================================

# 1. Cloud SQL Instance for Agent Registry
resource "google_sql_database_instance" "agent_registry_db" {
  name                = "${var.environment}-dap-agent-registry-sql"
  database_version    = "POSTGRES_15"
  region              = var.region
  project             = var.project_id
  deletion_protection = false # Set true for production

  settings {
    tier              = var.db_tier
    availability_type = var.environment == "prod" ? "REGIONAL" : "ZONAL"
    disk_size         = 20
    disk_type         = "PD_SSD"
    disk_autoresize   = true

    ip_configuration {
      ipv4_enabled    = false # Zero Public IP
      private_network = var.vpc_id
    }

    backup_configuration {
      enabled                        = true
      point_in_time_recovery_enabled = true
      start_time                     = "03:00"
    }

    database_flags {
      name  = "log_checkpoints"
      value = "on"
    }
  }

  encryption_key_name = var.kms_cloudsql_key_id
}

resource "google_sql_database" "registry_database" {
  name     = "agent_registry"
  instance = google_sql_database_instance.agent_registry_db.name
  project  = var.project_id
}

resource "google_sql_user" "registry_user" {
  name     = "registry_admin"
  instance = google_sql_database_instance.agent_registry_db.name
  password = random_password.registry_db_pass.result
  project  = var.project_id
}

# 2. Cloud SQL Instance for Agent Gateway (SOAM Orchestration)
resource "google_sql_database_instance" "agent_gateway_db" {
  name                = "${var.environment}-dap-agent-gateway-sql"
  database_version    = "POSTGRES_15"
  region              = var.region
  project             = var.project_id
  deletion_protection = false

  settings {
    tier              = var.db_tier
    availability_type = var.environment == "prod" ? "REGIONAL" : "ZONAL"
    disk_size         = 20
    disk_type         = "PD_SSD"
    disk_autoresize   = true

    ip_configuration {
      ipv4_enabled    = false # Zero Public IP
      private_network = var.vpc_id
    }

    backup_configuration {
      enabled                        = true
      point_in_time_recovery_enabled = true
      start_time                     = "03:30"
    }
  }

  encryption_key_name = var.kms_cloudsql_key_id
}

resource "google_sql_database" "gateway_database" {
  name     = "agent_gateway"
  instance = google_sql_database_instance.agent_gateway_db.name
  project  = var.project_id
}

resource "google_sql_user" "gateway_user" {
  name     = "gateway_admin"
  instance = google_sql_database_instance.agent_gateway_db.name
  password = random_password.gateway_db_pass.result
  project  = var.project_id
}
