provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "metastore_storage" {
  bucket = var.metastore_storage_bucket_name
  acl    = "private"

  tags = {
    Environment = "Databricks"
    Purpose     = "UnityCatalogMetastoreStorage"
  }
}

