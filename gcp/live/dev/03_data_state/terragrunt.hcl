# ==============================================================================
# Terragrunt Module: 03_data_state
# ==============================================================================

include "root" {
  path = find_in_parent_folders("root.hcl")
}

locals {
  env_vars = read_terragrunt_config(find_in_parent_folders("env.hcl"))
}

terraform {
  source = "../../../modules/03_data_state"
}

dependency "networking" {
  config_path                             = "../01_networking"
  mock_outputs_allowed_terraform_commands = ["validate", "plan"]
  mock_outputs_merge_strategy_with_state  = "shallow"
  mock_outputs = {
    vpc_id = "projects/my-dap-gcp-project/global/networks/dev-dap-vpc"
  }
}

inputs = {
  vpc_id  = dependency.networking.outputs.vpc_id
  db_tier = local.env_vars.locals.db_tier
}
