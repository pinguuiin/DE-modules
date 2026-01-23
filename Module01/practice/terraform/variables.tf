variable "my_dataset_id" {
  description = "The ID of the BigQuery dataset"
  default     = "my_first_dataset"
}

variable "gcp_region" {
  description = "The GCP region to deploy resources in"
  default     = "europe-north1"
}

variable "gcp_location" {
  description = "The GCP location for resources"
  default     = "EU"
}

variable "gcp_project" {
  description = "The GCP project ID"
  default     = "long-sonar-485113-u0"
}

variable "bucket_name" {
  description = "The name of the GCS bucket"
  default     = "my-first-bucket-485113-u0"
}