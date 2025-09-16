variable "aws_region" {
  description = "AWS region for the workspace and metastore"
  type        = string
  default     = "us-east-1"
}

variable "databricks_account_id" {
  description = "Databricks account ID"
  type        = string
}

variable "workspace_name" {
  description = "Name of the Databricks workspace"
  type        = string
}

variable "metastore_name" {
  description = "Name of the Unity Catalog metastore"
  type        = string
}

variable "metastore_storage_bucket_name" {
  description = "Name of the S3 bucket for metastore storage"
  type        = string
}

