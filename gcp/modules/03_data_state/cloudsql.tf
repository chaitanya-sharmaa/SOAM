# ==============================================================================
# Cloud SQL: SOAM Agent DB (PostgreSQL 15 Private IP Only)
# ==============================================================================

resource "random_password" "agent_db_pass" {
  length  = 24
  special = false
}

# 1. Single Cloud SQL Instance for SOAM Agents
resource "google_sql_database_instance" "agent_db" {
  name                = "${var.environment}-dap-agent-sql"
  database_version    = "POSTGRES_15"
  region              = var.region
  project             = var.project_id
  deletion_protection = false

  settings {
    tier              = var.db_tier
    availability_type = var.environment == "prod" ? "REGIONAL" : "ZONAL"
    disk_size         = 10
    disk_type         = "PD_SSD"
    disk_autoresize   = false

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
}

resource "google_sql_database" "agent_database" {
  name     = "agent_data"
  instance = google_sql_database_instance.agent_db.name
  project  = var.project_id
}

resource "google_sql_user" "agent_user" {
  name     = "agent_admin"
  instance = google_sql_database_instance.agent_db.name
  password = random_password.agent_db_pass.result
  project  = var.project_id
}
