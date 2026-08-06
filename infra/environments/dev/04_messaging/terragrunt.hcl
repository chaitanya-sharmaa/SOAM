# ==============================================================================
# Terragrunt Module: 04_messaging
# ==============================================================================

include "root" {
  path = find_in_parent_folders("root.hcl")
}

terraform {
  source = "../../../modules/04_messaging"
}

inputs = {}
