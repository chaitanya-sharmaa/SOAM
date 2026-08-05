# ==============================================================================
# Terragrunt Module: 07_observability
# ==============================================================================

include "root" {
  path = find_in_parent_folders("root.hcl")
}

terraform {
  source = "../../../modules/07_observability"
}

inputs = {}
