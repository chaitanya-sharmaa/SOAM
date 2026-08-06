# ==============================================================================
# Terragrunt Module: 02_security_iam
# ==============================================================================

include "root" {
  path = find_in_parent_folders("root.hcl")
}

terraform {
  source = "../../../modules/02_security_iam"
}

inputs = {}
