# ==============================================================================
# Terragrunt Module: 05_compute_services
# ==============================================================================

include "root" {
  path = find_in_parent_folders("root.hcl")
}

locals {
  env_vars = read_terragrunt_config(find_in_parent_folders("env.hcl"))
}

terraform {
  source = "../../../modules/05_compute_services"
}

dependency "networking" {
  config_path = "../01_networking"
  mock_outputs = {
    vpc_id    = "projects/my-dap-gcp-prod/global/networks/prod-dap-vpc"
    subnet_id = "projects/my-dap-gcp-prod/regions/europe-west1/subnetworks/prod-dap-private-subnet"
  }
}

dependency "security" {
  config_path = "../02_security_iam"
  mock_outputs = {
    service_accounts = {
      "agent-registry"  = "sa-prod-agent-registry@my-dap-gcp-prod.iam.gserviceaccount.com"
      "agent-gateway"   = "sa-prod-agent-gateway@my-dap-gcp-prod.iam.gserviceaccount.com"
      "gatekeeper"      = "sa-prod-gatekeeper@my-dap-gcp-prod.iam.gserviceaccount.com"
      "mcp-gateway"     = "sa-prod-mcp-gateway@my-dap-gcp-prod.iam.gserviceaccount.com"
      "guardrails"      = "sa-prod-guardrails@my-dap-gcp-prod.iam.gserviceaccount.com"
      "grid-monitoring" = "sa-prod-grid-monitoring@my-dap-gcp-prod.iam.gserviceaccount.com"
      "grid-lens"       = "sa-prod-grid-lens@my-dap-gcp-prod.iam.gserviceaccount.com"
      "agent-1"         = "sa-prod-agent-1@my-dap-gcp-prod.iam.gserviceaccount.com"
      "agent-2"         = "sa-prod-agent-2@my-dap-gcp-prod.iam.gserviceaccount.com"
    }
  }
}

dependency "data_state" {
  config_path = "../03_data_state"
  mock_outputs = {
    firestore_database_name = "prod-dap-firestore"
    registry_db_private_ip  = "10.30.16.2"
    gateway_db_private_ip   = "10.30.16.3"
    bigquery_dataset_id     = "prod_dap_ctt_analytics"
  }
}

dependency "messaging" {
  config_path = "../04_messaging"
  mock_outputs = {
    agent_1_inbound_topic_id = "projects/my-dap-gcp-prod/topics/prod-dap-agent-1-inbound-topic"
    agent_2_inbound_topic_id = "projects/my-dap-gcp-prod/topics/prod-dap-agent-2-inbound-topic"
    gatekeeper_topic_id      = "projects/my-dap-gcp-prod/topics/prod-dap-gatekeeper-topic"
  }
}

inputs = {
  vpc_id                   = dependency.networking.outputs.vpc_id
  subnet_id                = dependency.networking.outputs.subnet_id
  service_account_emails   = dependency.security.outputs.service_accounts
  container_images         = local.env_vars.locals.container_images
  firestore_database_name  = dependency.data_state.outputs.firestore_database_name
  agent_1_inbound_topic_id = dependency.messaging.outputs.agent_1_inbound_topic_id
  agent_2_inbound_topic_id = dependency.messaging.outputs.agent_2_inbound_topic_id
  gatekeeper_topic_id      = dependency.messaging.outputs.gatekeeper_topic_id
  registry_db_private_ip   = dependency.data_state.outputs.registry_db_private_ip
  gateway_db_private_ip    = dependency.data_state.outputs.gateway_db_private_ip
  bigquery_dataset_id      = dependency.data_state.outputs.bigquery_dataset_id
}
