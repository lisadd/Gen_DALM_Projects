In Azure Data Fabric, data loading patterns primarily involve using Data Factory pipelines, Spark notebooks (Python/PySpark), or T-SQL/KQL commands to ingest data into Lakehouses, Warehouses, or KQL Databases. Streaming data uses the Eventstreams feature. 

// General Loading Patterns (Batch)
For batch loading, the primary tools are Data Factory pipelines for a low-code experience, or notebooks for more complex transformations using Python or KQL. 

1. Using Data Factory Pipelines (UI-based)
This approach is best for repeatable, scheduled data movement from various sources. 

Steps:
  1. In your workspace, create a new Pipeline.
  2. Use the Copy data assistant to configure source (e.g., Azure SQL DB) and destination (e.g., Fabric Warehouse or Lakehouse).
  3. Define mappings and settings (e.g., incremental loading strategy).
  4. Run or schedule the pipeline. 


2. Using T-SQL COPY INTO (Warehouse)
This is the recommended high-throughput method for loading data from external storage accounts into a Fabric Warehouse. 

Steps:
  1. Ensure your source data (Parquet or CSV files) is in an external Azure storage account (ADLS Gen2 or Blob Storage).
  2. Open the Warehouse SQL analytics endpoint query editor.
  3. Execute the COPY INTO command:


COPY INTO MyWarehouseTable
FROM 'https://<your_storage_account>.blob.core.windows.net/<container>/<path>'
WITH (
    FILE_TYPE = 'PARQUET',
    CREDENTIAL = (IDENTITY = 'Managed Identity') -- or other credential
);



3. Using Python in a Notebook (Lakehouse/Warehouse/KQL DB)
Use Spark notebooks for complex ETL processes, accessing data via libraries like Pandas or the Azure Kusto SDK. 

Steps:
  1. Create a new Fabric Notebook and select the PySpark kernel.
  2. Install necessary libraries (e.g., azure-kusto-data) if needed.
  3. Connect to your source and destination. You can use the built-in Spark connector for data sources or use the Kusto SDK for KQL DBs.
  4. Load data into a Spark or Pandas DataFrame, transform it, and write it to the target.


# Example using the Kusto Python SDK for KQL DBs
# Ensure libraries are installed: !pip install azure-kusto-data
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.kusto.data.helpers import dataframe_from_result_table

cluster = "https://<yourKQLdatabaseURI>.z0.kusto.data.microsoft.com"
database = "<your_database_name>"
kusto_url = f"{cluster}/{database}"
tenant_id = spark.conf.get("trident.tenant.id") # Get tenant ID from Fabric context

# Authenticate (Managed Identity works well in Fabric)
kcsb = KustoConnectionStringBuilder.with_interactive_login(cluster) # Or use other auth methods
client = KustoClient(kcsb)

# Execute a KQL query
query = "YourTable | take 10"
response = client.execute(database, query)
df = dataframe_from_result_table(response.primary_results[0])

# Further processing or writing to another Fabric destination (e.g., Lakehouse using Spark)
# df.write.mode("overwrite").format("delta").save("abfss://<container>@<storageaccount>.dfs.core.windows.net/<path>")




/// Loading Pattern for Streaming Data 
The primary service for streaming data in Fabric is Eventstreams, which offers a low-code interface to route real-time events to destinations like KQL databases or Lakehouses. 

// Using Eventstreams (UI-based) 
Steps:
  1. Create an Eventstream item in your Fabric workspace.
  2. Add a source: Configure a source such as Azure Event Hubs, Azure IoT Hub, or a custom application.
  3. Add a destination: Select KQL Database as the destination.
  4. The no-code wizard guides you to select the target KQL table and configures the connection (input format should typically be JSON).
  5. Once configured, data flows automatically into the KQL database table in near real-time.
  6. You can then use KQL queries to analyze the streaming data.


Example KQL Query (in a KQL Queryset or Fabric Notebook):

# Use the 'Query with code' feature on your table to generate a starting query.
# This example projects relevant columns and visualizes data.
YourStreamTable
| project timestamp, deviceId, temperature=ResponseMessage.temperature, humidity=ResponseMessage.humidity
| where temperature > 20
| summarize count() by bin(timestamp, 1h), deviceId
| render timechart



