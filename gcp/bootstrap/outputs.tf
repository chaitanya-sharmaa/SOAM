output "gcs_state_bucket_name" {
  description = "Name of the Google Cloud Storage bucket for Terraform remote state."
  value       = google_storage_bucket.tf_state_bucket.name
}

output "terraform_service_account_email" {
  description = "Email of the Terraform Provisioner Service Account."
  value       = google_service_account.terraform_sa.email
}

output "workload_identity_provider_name" {
  description = "Full resource name of the Workload Identity Provider for GitHub Actions config."
  value       = google_iam_workload_identity_pool_provider.github_provider.name
}
