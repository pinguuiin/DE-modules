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
  project = "long-sonar-485113-u0"
  region  = "us-central1"
}

resource "google_storage_bucket" "my-bucket" {
  name          = "my-first-bucket-485113-u0"
  location      = "US"
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