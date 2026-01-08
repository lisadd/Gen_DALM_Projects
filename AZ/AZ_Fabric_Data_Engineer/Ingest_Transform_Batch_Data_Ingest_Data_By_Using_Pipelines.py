"Azure Data Fabric" is a conceptual term for a unified data platform, primarily realized as Microsoft Fabric, which integrates various services like Data Factory, Synapse Data Engineering, and Power BI into a single Software as a Service (SaaS) environment. 

Below are the steps and example code for data ingestion and transformation in Microsoft Fabric using pipelines with SQL, KQL, and Python. 

//Ingest Data Using Pipelines (Low-Code Approach) 

The primary low-code method for batch data ingestion is using the Copy Data activity within a Fabric pipeline. 

//Steps:
  1. Create a Workspace: Navigate to the Microsoft Fabric home page and create a workspace with a Fabric-enabled license (Trial, Premium, or Fabric capacity).

  2. Create a Data Item: Create a destination data item, such as a Lakehouse (for a data lake with a built-in SQL endpoint) or a Warehouse.
  3. Create a New Data Pipeline: From the workspace, select + New > Data Pipeline and give it a name.
  4. Configure the Copy Data Activity:

    1. In the pipeline editor, select Copy data > Use copy assistant.
    2. Choose a Data Source: Select your source type (e.g., Azure SQL Database, Azure Blob Storage, or a sample dataset like "NYC Taxi - Green") and provide connection details.
    3. Choose a Data Destination (Sink): Select your target Fabric Lakehouse or Warehouse. You can choose to load to a new or existing table.
    4. Review and Run: Follow the prompts to review column mappings and other settings, then run the pipeline. The activity runs pane will show the progress. 

// Ingest and Transform Batch Data with Code 
For transformation logic beyond the visual data flows, you can integrate Python (PySpark), KQL, or T-SQL code within your pipelines, often using Notebook or KQL activities. 

1. Python (PySpark) for Ingestion and Transformation
You can use a Notebook activity within a pipeline to run PySpark code, which is ideal for complex transformations. 

Steps:
1. Create a Lakehouse and a Data Pipeline (as above).
2. In the pipeline, add a Notebook activity.
3. Create a new notebook and use PySpark code in a cell to read, transform, and write data. 

// Example Python (PySpark) Code (in a Fabric Notebook):

# Assuming the raw data is in a 'raw_data' folder in the Lakehouse files section
raw_data_path = "abfss://<container>@<storage_account>.dfs.core.windows.net/new_data/raw_data.csv"
transformed_table_name = "FilteredSalesData"

# Read the data from the lakehouse
df = spark.read.format("csv").option("header", "true").load(raw_data_path)

# Perform transformation (e.g., filter records where 'Sales' > 100)
from pyspark.sql.functions import col
transformed_df = df.filter(col("Sales") > 100)

# Write the transformed data to a new Delta table in the Lakehouse
# 'overwrite' mode is used for batch processing updates
transformed_df.write.format("delta").mode("overwrite").saveAsTable(transformed_table_name)
print(f"Data successfully written to table: {transformed_table_name}")



2. . T-SQL for Ingestion and Transformation
T-SQL (Transact-SQL) can be used directly in a Warehouse environment or via a pipeline's SQL activity or Lookup activity. 

Example T-SQL Code (using the COPY statement or CREATE TABLE AS SELECT):
This example creates a new table based on a query from existing tables and external files in the Lakehouse/Warehouse. 

You can use T-SQL within a Warehouse or through a pipeline's SQL or Lookup activity. The COPY statement is another option for high-throughput data loading from Azure storage accounts. 

3. KQL for Ingestion and Transformation
Kusto Query Language (KQL) is used within the Real-Time Analytics experience. Steps include creating a KQL Database, using the ingest data wizard or pipelines to load raw data, and employing KQL update policies or functions for transformation. Ad-hoc KQL queries can also be run in a Fabric Notebook. 
This script reads raw data, performs a simple filter transformation, and writes it to a "transformed" table in the Lakehouse. 
