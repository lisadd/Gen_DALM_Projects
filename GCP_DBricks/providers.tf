terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.63"
    }
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

provider "databricks" {
  # Account-level provider for metastore creation
  host = "https://accounts.gcp.databricks.com" # Or your specific Databricks account URL
  client_id = var.databricks_client_id
  client_secret = var.databricks_client_secret
}

provider "databricks" {
  alias = "workspace"
  host = databricks_mws_workspaces.this.workspace_url
  client_id = var.databricks_client_id
  client_secret = var.databricks_client_secret
}

