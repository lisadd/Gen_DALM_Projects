variable "resource_group_name" {
  description = "Name of the Azure Resource Group."
  type        = string
}

variable "location" {
  description = "Azure region for resources."
  type        = string
}

variable "databricks_workspace_name" {
  description = "Name of the Azure Databricks Workspace."
  type        = string
}

variable "sku" {
  description = "SKU of the Databricks Workspace (e.g., 'premium')."
  type        = string
  default     = "premium"
}

variable "azure_client_id" {
  description = "Azure AD Client ID for service principal."
  type        = string
  sensitive   = true
}

variable "azure_client_secret" {
  description = "Azure AD Client Secret for service principal."
  type        = string
  sensitive   = true
}

variable "azure_tenant_id" {
  description = "Azure AD Tenant ID."
  type        = string
}

variable "databricks_workspace_url" {
  description = "URL of the Databricks Workspace."
  type        = string
}

variable "metastore_name" {
  description = "Name for the Unity Catalog Metastore."
  type        = string
}

variable "metastore_storage_account_name" {
  description = "Name of the Azure Storage Account for Metastore."
  type        = string
}

variable "metastore_container_name" {
  description = "Name of the Azure Storage Container for Metastore."
  type        = string
}

