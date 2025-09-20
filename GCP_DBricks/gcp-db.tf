resource "google_project_service" "databricks_required_apis" {
  for_each = toset([
    "compute.googleapis.com",
    "storage.googleapis.com",
    "iam.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "servicenetworking.googleapis.com",
  ])
  project = var.gcp_project_id
  service = each.key
  disable_on_destroy = false
}

resource "databricks_mws_workspaces" "gcp_workspace" {
  provider = databricks.account
  account_id   = "your_databricks_account_id" # Replace with your Databricks account ID
  workspace_name = var.workspace_name
  gcp_workspace_config {
    project_id = var.gcp_project_id
    region     = var.gcp_region
  }
}

