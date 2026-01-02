""" In Microsoft Fabric, data loading patterns leverage a combination of Data Factory pipelines, Notebooks (PySpark/Python, T-SQL, KQL), and specific commands like COPY INTO to implement both full and incremental data loads.

/// Design and Implementation Steps
The general steps for designing and implementing data loads in Fabric are:

  1. Identify Data Source & Destination: Determine the source (e.g., Azure SQL DB, API) and destination (e.g., Lakehouse, Data Warehouse, KQL DB).
  
  2. Choose a Loading Pattern:
    - Full Load: Suitable for initial data ingestion or when the entire dataset is small or frequently changing. In Fabric, this is often an overwrite operation to a staging area.
    - Incremental Load: Used to process only new or changed records, reducing execution time and compute costs. Common methods include using a watermark column (timestamp or incrementing key) or Change Data Capture (CDC).
  3. Orchestrate with Data Factory Pipeline: Use pipelines to manage the workflow, which can include activities like Lookup, If Condition, Copy Data, and Notebook or KQL activities.
  4. Implement Logic (Python/SQL/KQL): Use the relevant code language within a Notebook or as a SQL stored procedure to perform the data extraction, transformation, and loading (ETL/ELT). 

/// Example Code and Patterns
Full Data Load
A full load typically overwrites the destination or a staging table with the entire dataset from the source. 
Using T-SQL COPY INTO in a Data Warehouse: The most performant way to ingest bulk data from Azure Data Lake Storage Gen2 (ADLS Gen2) into a Fabric Data Warehouse.

-- Example for a full load using T-SQL in a Fabric Data Warehouse
-- Assumes data is already staged in ADLS Gen2 (e.g., in a Delta-Parquet format)
COPY INTO dbo.YourTargetTable
FROM 'https://<your_storage_account>.dfs.core.windows.net/<your_container>/<path_to_files>/*.parquet'
WITH (
    FILE_TYPE = 'PARQUET',
    CREDENTIAL = (IDENTITY = 'Managed Identity') -- Or other credential setup
);

-- For a full reload/overwrite pattern, you would truncate the table first or use CTAS
TRUNCATE TABLE dbo.YourTargetTable;
INSERT INTO dbo.YourTargetTable SELECT * FROM dbo.YourStagingTable;



/// Incremental Data Load
This pattern involves tracking changes using a watermark and only loading the delta. 
Using Python (PySpark) in a Notebook: This approach reads the delta data based on a filter and merges or appends it to the destination Lakehouse table.


# Example Python code in a Fabric Notebook using PySpark
from delta.tables import DeltaTable

# Define paths and watermark value
source_path = "abfss://<container>@<storage_account>"
delta_table_path = f"abfss://<workspace>@onelake.dfs.fabric.microsoft.com/<Lakehouse_name>.Lakehouse/Tables/YourTargetTable"
last_watermark_value = "2024-01-01 00:00:00" # Retrieved from a watermark table using a Lookup activity

# Read new data using a watermark column filter
# Assume 'last_updated' is the watermark column in the source data
df_delta = spark.read.format("parquet").load(source_path).filter(f"last_updated > '{last_watermark_value}'")

# Perform merge operation (SCD Type 2 or simple updates/inserts)
# This requires the destination to be a Delta table in the Lakehouse
if DeltaTable.isDeltaTable(spark, delta_table_path):
    deltaTable = DeltaTable.forPath(spark, delta_table_path)
    deltaTable.alias("target").merge(
        df_delta.alias("source"),
        "target.id = source.id"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
else:
    # Initial load or simple append if merge is not needed
    df_delta.write.format("delta").mode("append").save(delta_table_path)

# Update the watermark table with the new maximum date/ID in a subsequent pipeline step


// Using T-SQL Stored Procedures in a Data Warehouse: This uses a dedicated watermark table to manage the loading process.

-- Step 1: Create a watermark table (if not exists)
CREATE TABLE watermarktable (
    TableName VARCHAR(255),
    WatermarkValue DATETIME
);

-- Step 2: Stored procedure to update the watermark value
CREATE PROCEDURE update_watermarkvalue 
    @TableName VARCHAR(50), 
    @LastModifiedtime DATETIME
AS
BEGIN
    UPDATE watermarktable
    SET WatermarkValue = @LastModifiedtime
    WHERE TableName = @TableName;
END;

-- Step 3: Use a Data Factory pipeline with Lookup and Stored Procedure activities
-- The Lookup activity fetches the current watermark.
-- A subsequent Copy activity uses the watermark in its source query:
-- SELECT * FROM source_table WHERE LastModifiedDate > '@{activity(\'LookupOldWatermark\').output.firstRow.WatermarkValue}'
-- After the copy, another Stored Procedure activity calls 'update_watermarkvalue' with the new watermark (e.g., the current pipeline run time).



/// Using KQL in a Notebook or Pipeline Activity: Ingesting data into a KQL database often uses simple append operations or data connections. KQL is mainly for querying and real-time analytics once data is landed.


# Example using the Kusto Python SDK in a Fabric Notebook
# This is for writing data to a KQL DB, typically appending new records
# ... (connection setup as per snippet 1.5.2) ...

# Prepare data in a DataFrame
# df_new_data = ...

# Write data to KQL database
kusto_write_uri = "https://<yourKQLdatabaseURI>.ingest.<region>.kusto.data.microsoft.com"
database = "DocsDatabase"
table = "YourTargetTable"

# Use the Kusto Ingest client to append new data
# (Requires azure-kusto-ingest library)
# The orchestration in a pipeline manages which "new" data is passed to the notebook





