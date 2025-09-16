resource "databricks_metastore" "this" {
  name          = var.metastore_name
  owner         = "account admins" # Or a specific group/user
  storage_root  = "s3://${aws_s3_bucket.metastore_storage.id}/"
  force_destroy = true # Use with caution in production

  provider = databricks.this # If using multiple Databricks providers
}

resource "databricks_metastore_assignment" "this" {
  workspace_id = databricks_mws_workspaces.this.workspace_id
  metastore_id = databricks_metastore.this.id
}

