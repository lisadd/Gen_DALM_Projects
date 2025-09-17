resource "azurerm_storage_account" "metastore_storage" {
  name                     = var.metastore_storage_account_name
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "GRS"
}

resource "azurerm_storage_container" "metastore_container" {
  name                  = var.metastore_container_name
  storage_account_name  = azurerm_storage_account.metastore_storage.name
  container_access_type = "private"
}

resource "databricks_metastore" "this" {
  provider = databricks # Use the account-level provider
  name = var.metastore_name
  storage_root = "abfss://${azurerm_storage_container.metastore_container.name}@${azurerm_storage_account.metastore_storage.name}.dfs.core.windows.net/"
  owner = "users" # Or a specific group/user
  force_destroy = true # Use with caution in production
}

resource "databricks_metastore_assignment" "this" {
  provider = databricks # Use the account-level provider
  metastore_id = databricks_metastore.this.id
  workspace_id = azurerm_databricks_workspace.workspace.workspace_id
}

