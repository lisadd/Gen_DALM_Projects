resource "google_storage_bucket" "metastore_storage" {
  project = var.gcp_project_id
  name    = var.metastore_storage_bucket_name
  location = var.gcp_region
  uniform_bucket_level_access = true
  # Add lifecycle rules, versioning, etc. as needed
}

resource "databricks_metastore" "unity_catalog_metastore" {
  provider = databricks.account
  name          = var.metastore_name
  storage_root  = "gs://${google_storage_bucket.metastore_storage.name}"
  owner         = "your_account_admin_email" # Replace with a Databricks account admin email
  force_destroy = true # Use with caution in production
}

resource "databricks_metastore_assignment" "workspace_metastore_assignment" {
  provider = databricks.account
  metastore_id = databricks_metastore.unity_catalog_metastore.id
  workspace_id = databricks_mws_workspaces.gcp_workspace.workspace_id
}

