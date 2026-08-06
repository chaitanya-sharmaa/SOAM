# ==============================================================================
# Terragrunt Module: 06_ingress_gateway (SOAM 2-Agent Setup with Google IAM)
# ==============================================================================

include "root" {
  path = find_in_parent_folders("root.hcl")
}

locals {
  env_vars = read_terragrunt_config(find_in_parent_folders("env.hcl"))
}

terraform {
  source = "../../../modules/06_ingress_gateway"
}

dependency "compute" {
  config_path                             = "../05_compute_services"
  mock_outputs_allowed_terraform_commands = ["validate", "plan", "destroy", "init"]
  mock_outputs_merge_strategy_with_state  = "shallow"
  mock_outputs = {
    agent_1_uri = "https://dev-dap-agent-1-xyz.europe-west1.run.app"
    agent_2_uri = "https://dev-dap-agent-2-xyz.europe-west1.run.app"
  }
}

inputs = {
  agent_1_backend_url = dependency.compute.outputs.agent_1_uri
  agent_2_backend_url = dependency.compute.outputs.agent_2_uri
}
