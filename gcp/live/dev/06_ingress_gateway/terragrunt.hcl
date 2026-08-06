# ==============================================================================
# Terragrunt Module: 06_ingress_gateway
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
  mock_outputs_allowed_terraform_commands = ["validate", "plan"]
  mock_outputs_merge_strategy_with_state  = "shallow"
  mock_outputs = {
    agent_gateway_uri  = "https://dev-dap-agent-gateway-xyz.europe-west1.run.app"
    agent_registry_uri = "https://dev-dap-agent-registry-xyz.europe-west1.run.app"
  }
}

inputs = {
  agent_gateway_backend_url  = dependency.compute.outputs.agent_gateway_uri
  agent_registry_backend_url = dependency.compute.outputs.agent_registry_uri
  pingidentity_issuer_url    = local.env_vars.locals.pingidentity_issuer_url
  pingidentity_jwks_url      = local.env_vars.locals.pingidentity_jwks_url
  pingidentity_audience      = local.env_vars.locals.pingidentity_audience
}
