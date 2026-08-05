# Digital Agent Platform (DAP) - Azure Deployment Runbook

This guide covers the deployment, configuration, and maintenance of the Azure DAP architecture.

---

## 1. Prerequisites

1. **Azure CLI**: `az login`
2. **Terraform CLI**: `terraform version` (>= 1.5.0)
3. **Permissions**: Azure `Owner` or `Contributor` + `User Access Administrator` on the target subscription.

---

## 2. Phase 1: Bootstrap OIDC & Remote State

Navigate to the `azure/bootstrap/` directory:

```bash
cd azure/bootstrap

# 1. Initialize Terraform
terraform init

# 2. Review and Apply Bootstrap Configuration
terraform apply -var="subscription_id=<YOUR_AZURE_SUBSCRIPTION_ID>"
```

### Outputs from Bootstrap:
- `azure_client_id`: Entra ID Application Client ID for GitHub Actions
- `azure_tenant_id`: Microsoft Entra ID Tenant ID
- `terraform_state_storage_account`: Name of the storage account for remote state

---

## 3. Phase 2: Configure GitHub Repository Secrets

Add the following GitHub Secrets under **Repository Settings ➔ Secrets and variables ➔ Actions**:

| Secret Name | Description | Value Example |
| :--- | :--- | :--- |
| `AZURE_CLIENT_ID` | Entra ID App Client ID | `11111111-2222-3333-4444-555555555555` |
| `AZURE_TENANT_ID` | Microsoft Entra Tenant ID | `66666666-7777-8888-9999-aaaaaaaaaaaa` |
| `AZURE_SUBSCRIPTION_ID` | Target Azure Subscription ID | `bbbbbbbb-cccc-dddd-eeee-ffffffffffff` |

---

## 4. Phase 3: Deploy Dev Environment

Navigate to `azure/environments/dev/`:

```bash
cd azure/environments/dev

# 1. Update terraform.tfvars with your Subscription ID and Tenant ID
cp terraform.tfvars.example terraform.tfvars # or edit terraform.tfvars

# 2. Initialize Terraform
terraform init

# 3. Plan & Validate
terraform plan -out=tfplan

# 4. Apply Deployment
terraform apply tfplan
```

---

## 5. Automated CI/CD Execution

Every pull request modifying files under `azure/**` triggers `.github/workflows/terraform-azure.yml`:
1. Authenticates securely via **OIDC (Workload Identity Federation)**.
2. Runs `terraform fmt -check`, `terraform init`, and `terraform validate`.
3. Runs `terraform plan` and posts a detailed summary comment on the GitHub PR.
