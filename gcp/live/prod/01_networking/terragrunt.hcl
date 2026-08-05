# ==============================================================================
# Terragrunt Module: 01_networking
# ==============================================================================

include "root" {
  path = find_in_parent_folders("root.hcl")
}

locals {
  env_vars = read_terragrunt_config(find_in_parent_folders("env.hcl"))
}

terraform {
  source = "../../../modules/01_networking"
}

inputs = {
  subnet_cidr        = local.env_vars.locals.subnet_cidr
  vpc_connector_cidr = local.env_vars.locals.vpc_connector_cidr
}
