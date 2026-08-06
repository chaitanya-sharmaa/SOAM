# ==============================================================================
# Terragrunt Module: 04_messaging
# ==============================================================================

include "root" {
  path = find_in_parent_folders("root.hcl")
}

terraform {
  source = "../../../modules/04_messaging"
}

dependency "security" {
  config_path                             = "../02_security_iam"
  mock_outputs_allowed_terraform_commands = ["validate", "plan"]
  mock_outputs_merge_strategy_with_state  = "shallow"
  mock_outputs = {
    kms_keys = {
      pubsub = "projects/my-dap-gcp-project/locations/europe-west1/keyRings/dev-dap-keyring/cryptoKeys/key-pubsub"
    }
  }
}

inputs = {
  kms_pubsub_key_id = dependency.security.outputs.kms_keys["pubsub"]
}
