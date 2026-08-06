# ==============================================================================
# Terragrunt Module: 05_compute_services (SOAM 2-Agent Setup)
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
  config_path                             = "../01_networking"
  mock_outputs_allowed_terraform_commands = ["validate", "plan", "destroy", "init"]
  mock_outputs_merge_strategy_with_state  = "shallow"
  mock_outputs = {
    vpc_id    = "projects/my-dap-gcp-project/global/networks/dev-dap-vpc"
    subnet_id = "projects/my-dap-gcp-project/regions/europe-west1/subnetworks/dev-dap-private-subnet"
  }
}

dependency "security" {
  config_path                             = "../02_security_iam"
  mock_outputs_allowed_terraform_commands = ["validate", "plan", "destroy", "init"]
  mock_outputs_merge_strategy_with_state  = "shallow"
  mock_outputs = {
    service_accounts = {
      "agent-1" = "sa-dev-agent-1@my-dap-gcp-project.iam.gserviceaccount.com"
      "agent-2" = "sa-dev-agent-2@my-dap-gcp-project.iam.gserviceaccount.com"
    }
  }
}

dependency "data_state" {
  config_path                             = "../03_data_state"
  mock_outputs_allowed_terraform_commands = ["validate", "plan", "destroy", "init"]
  mock_outputs_merge_strategy_with_state  = "shallow"
  mock_outputs = {
    firestore_database_name = "(default)"
    db_private_ip           = "10.10.16.2"
    bigquery_dataset_id     = "dev_dap_ctt_analytics"
  }
}

dependency "messaging" {
  config_path                             = "../04_messaging"
  mock_outputs_allowed_terraform_commands = ["validate", "plan", "destroy", "init"]
  mock_outputs_merge_strategy_with_state  = "shallow"
  mock_outputs = {
    agent_1_inbound_topic_id = "projects/my-dap-gcp-project/topics/dev-dap-agent-1-inbound-topic"
    agent_2_inbound_topic_id = "projects/my-dap-gcp-project/topics/dev-dap-agent-2-inbound-topic"
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
  db_private_ip            = dependency.data_state.outputs.db_private_ip
}
