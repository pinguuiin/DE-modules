variable "credentials" {
  description = "My Credentials"
  default     = "./keys.json"
}

variable "project" {
  description = "Project"
  default     = "long-sonar-485113-u0"
}

variable "region" {
  description = "Region"
  default     = "europe-north1"
}

variable "location" {
  description = "Project Location"
  default     = "EU"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "my_first_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "my-first-bucket-485113-u0"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}