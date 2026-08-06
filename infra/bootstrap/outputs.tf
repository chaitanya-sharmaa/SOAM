output "gcs_state_bucket_names" {
  description = "Names of the Google Cloud Storage buckets for Terraform/Terragrunt remote state per environment."
  value       = { for k, b in google_storage_bucket.tf_state_buckets : k => b.name }
}

output "terraform_service_account_email" {
  description = "Email of the Terraform Provisioner Service Account."
  value       = google_service_account.terraform_sa.email
}

output "workload_identity_provider_name" {
  description = "Full resource name of the Workload Identity Provider for GitHub Actions config."
  value       = google_iam_workload_identity_pool_provider.github_provider.name
}
