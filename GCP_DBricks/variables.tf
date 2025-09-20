variable "gcp_project_id" {
  description = "The GCP project ID."
  type        = string
}

variable "gcp_region" {
  description = "The GCP region for the Databricks workspace."
  type        = string
}

variable "databricks_account_id" {
  description = "Your Databricks account ID."
  type        = string
}

variable "databricks_client_id" {
  description = "Client ID of the Databricks service principal with account admin role."
  type        = string
  sensitive   = true
}

variable "databricks_client_secret" {
  description = "Client secret of the Databricks service principal."
  type        = string
  sensitive   = true
}

variable "workspace_name" {
  description = "Name for the Databricks workspace."
  type        = string
}

variable "metastore_name" {
  description = "Name for the Unity Catalog metastore."
  type        = string
}

variable "metastore_storage_bucket_name" {
  description = "Name of the GCS bucket for metastore storage."
  type        = string
}

