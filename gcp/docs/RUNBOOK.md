# Deployment Runbook: DAP Infrastructure on GCP via Terragrunt & GitHub Actions

This guide walks you through deploying the complete Digital Agent Platform (DAP) infrastructure using **Terragrunt** and **GitHub Actions** with **Keyless Workload Identity Federation (WIF)**.

---

## 🎨 Architecture & CI/CD Flow

![Terragrunt Multi-Environment CI/CD Orchestration](file:///Users/chasharm4/gcp-arch/cloud-run/gcp/docs/terragrunt_multienv_cicd_diagram.png)

---

## Prerequisites

1. Google Cloud CLI (`gcloud`) installed and authenticated.
2. Terragrunt CLI (`>= 1.1.0`) and Terraform CLI (`>= 1.7.0`) installed.
3. A GCP Project with Billing enabled.
4. A GitHub repository containing this codebase.

---

## Step 1: Bootstrap WIF & GCS State Bucket (One-Time Setup)

Navigate to the `bootstrap` directory:

```bash
cd bootstrap

# Initialize Terraform
terraform init

# Plan and Apply
terraform apply \
  -var="project_id=YOUR_GCP_PROJECT_ID" \
  -var="region=europe-west1" \
  -var="github_org_or_user=YOUR_GITHUB_ORG" \
  -var="github_repository=YOUR_GITHUB_ORG/YOUR_REPO_NAME"
```

Save the generated outputs:
* `workload_identity_provider_name` (e.g. `projects/123456789/locations/global/workloadIdentityPools/github-actions-pool/providers/github-actions-provider`)
* `terraform_service_account_email` (e.g. `sa-dap-tf-provisioner@YOUR_GCP_PROJECT_ID.iam.gserviceaccount.com`)

---

## Step 2: Configure GitHub Repository Secrets

In your GitHub repository:
1. Go to **Settings** > **Secrets and variables** > **Actions**.
2. Click **New repository secret** and add:
   * `GCP_WIF_PROVIDER`: Value of `workload_identity_provider_name` output.
   * `GCP_TF_SA_EMAIL`: Value of `terraform_service_account_email` output.

---

## Step 3: Configure Environment Variables

Update `gcp/live/<env>/env.hcl` with your GCP project ID and network configuration:

```hcl
# gcp/live/dev/env.hcl
locals {
  environment = "dev"
  project_id  = "YOUR_GCP_DEV_PROJECT_ID"
  region      = "europe-west1"
  subnet_cidr = "10.10.1.0/24"
  vpc_connector_cidr = "10.10.2.0/28"
  db_tier     = "db-custom-2-7680"
}
```

---

## Step 4: Local Deployment (Terragrunt CLI)

To deploy locally using Terragrunt:

```bash
# 1. Navigate to target environment
cd gcp/live/dev

# 2. Check dependency graph
terragrunt dag graph

# 3. Plan all modules in topological order
terragrunt run --all plan

# 4. Apply all modules across the DAG
terragrunt run --all apply
```

---

## Step 5: Automated CI/CD via GitHub Actions

1. Create a feature branch and push your changes:
   ```bash
   git checkout -b feature/dap-infra
   git add .
   git commit -m "feat: configure DAP enterprise infrastructure"
   git push origin feature/dap-infra
   ```
2. Open a **Pull Request** to `develop` or `main`.
   * The `terragrunt-plan` matrix workflow triggers automatically across `[dev, staging, prod]`.
3. Review and **Merge** the Pull Request.
   * Merging to `develop` deploys **`dev`**.
   * Merging to `main` deploys **`prod`**.

---

## Step 6: Verification & Inspection

Once the deployment completes:

```bash
# Check Cloud Run microservices
gcloud run services list --project=YOUR_GCP_PROJECT_ID

# Check Pub/Sub topics
gcloud pubsub topics list --project=YOUR_GCP_PROJECT_ID

# Check Cloud SQL private instances
gcloud sql instances list --project=YOUR_GCP_PROJECT_ID

# Check API Gateway entrypoint
gcloud api-gateway gateways list --project=YOUR_GCP_PROJECT_ID
```
