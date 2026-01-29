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
  default     = "taxi_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "bucket-pingu"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}