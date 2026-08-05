# Deployment Runbook: DAP Infrastructure on GCP via GitHub Actions

This guide walks you through deploying the complete Digital Agent Platform (DAP) infrastructure using **Terraform** and **GitHub Actions** with **Keyless Workload Identity Federation (WIF)**.

---

## Prerequisites

1. Google Cloud CLI (`gcloud`) installed and authenticated.
2. A GCP Project with Billing enabled.
3. A GitHub repository containing this codebase.

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
* `gcs_state_bucket_name` (e.g. `YOUR_GCP_PROJECT_ID-dap-tfstate`)

---

## Step 2: Configure GitHub Repository Secrets

In your GitHub repository:
1. Go to **Settings** > **Secrets and variables** > **Actions**.
2. Click **New repository secret** and add:
   * `GCP_WIF_PROVIDER`: Value of `workload_identity_provider_name` output.
   * `GCP_TF_SA_EMAIL`: Value of `terraform_service_account_email` output.

---

## Step 3: Configure Dev Environment Backend

Update `environments/dev/provider.tf` with your GCS state bucket name:

```hcl
backend "gcs" {
  bucket = "YOUR_GCP_PROJECT_ID-dap-tfstate"
  prefix = "terraform/state/dev"
}
```

Update `environments/dev/terraform.tfvars` with your project ID and configuration:

```hcl
project_id  = "YOUR_GCP_PROJECT_ID"
region      = "europe-west1"
environment = "dev"
```

---

## Step 4: Deploy via GitHub Actions

1. Create a feature branch and push your changes:
   ```bash
   git checkout -b feature/dap-infra
   git add .
   git commit -m "feat: configure DAP enterprise infrastructure"
   git push origin feature/dap-infra
   ```
2. Open a **Pull Request** to `main`.
   * The `terraform-plan` workflow triggers automatically.
   * Terraform format, validation, and plan results are posted as a comment on the PR.
3. Review and **Merge** the Pull Request.
   * The `terraform-apply` workflow executes and provisions all 7 modules automatically in GCP.

---

## Step 5: Verification & Inspection

Once the workflow completes:

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
