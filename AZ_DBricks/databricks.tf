# Example: Creating a cluster in the workspace
resource "databricks_cluster" "example_cluster" {
  provider = databricks.workspace # Use the workspace-level provider
  cluster_name = "example-cluster"
  spark_version = "11.3.x-scala2.12"
  node_type_id = "Standard_DS3_v2"
  num_workers = 1
  autotermination_minutes = 60
}

