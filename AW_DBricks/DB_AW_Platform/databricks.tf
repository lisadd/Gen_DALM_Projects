provider "databricks" {
  host = "https://accounts.cloud.databricks.com" # Or your specific Databricks account URL
  account_id = var.databricks_account_id
  # Authentication details (e.g., client ID/secret for service principal)
  # should be set via environment variables (DATABRICKS_CLIENT_ID, DATABRICKS_CLIENT_SECRET)
}

resource "databricks_mws_workspaces" "this" {
  account_id = var.databricks_account_id
  workspace_name = var.workspace_name
  aws_region = var.aws_region
  # ... other workspace configuration like network, private access settings, etc.
}

