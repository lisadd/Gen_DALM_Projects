terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    databricks = {
      source = "databricks/databricks"
      version = "~> 1.0"
    }
    azuread = {
      source = "hashicorp/azuread"
      version = "~> 2.0"
    }
  }
}

provider "azurerm" {
  features {}
}

provider "databricks" {
  # Configuration for the Databricks account-level provider
  # This typically uses Azure AD authentication for Unity Catalog
  host = "https://accounts.azuredatabricks.net"
  azure_client_id = var.azure_client_id
  azure_client_secret = var.azure_client_secret
  azure_tenant_id = var.azure_tenant_id
}

provider "databricks" {
  alias = "workspace" # Alias for workspace-level operations
  # This typically uses Azure AD authentication for workspace resources
  host = var.databricks_workspace_url
  azure_client_id = var.azure_client_id
  azure_client_secret = var.azure_client_secret
  azure_tenant_id = var.azure_tenant_id
}

