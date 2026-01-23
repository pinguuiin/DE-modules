terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.16.0"
    }
  }
}

provider "google" {
  # Configuration options
  credentials = "./keys.json"
  project     = var.gcp_project
  region      = var.gcp_region
}

resource "google_storage_bucket" "my-bucket" {
  name          = var.bucket_name
  location      = var.gcp_location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "my-dataset" {
  dataset_id = var.my_dataset_id
  location   = var.gcp_location
  delete_contents_on_destroy = true
}