In Microsoft Fabric, you can ingest and transform batch data using Data Pipelines, Notebooks (Python/Spark), or the T-SQL COPY statement in a Warehouse. Data shortcuts in OneLake virtualize data, eliminating the need for physical data movement. 

// Ingest and Transform Batch Data


1. Using Python (in a Fabric Notebook)
This approach is code-first and provides granular control using PySpark for data processing. The output is typically saved in Delta format within a Lakehouse. 

// Steps:
1. In your Fabric workspace, create a new Lakehouse and a new Notebook.
2. Use the azure-kusto-ingest library for KQL databases or Spark for Lakehouses to read/write data.
3. Write PySpark code in a notebook cell to read data from a source (e.g., ADLS Gen2 via a shortcut), apply transformations, and write the result to a new table or location in the Lakehouse.


// Example Python Code (PySpark for Lakehouse):


# Read data from an existing source (e.g., a CSV file in the 'Files' section or a shortcut)
df = spark.read.format("csv").option("header", "true").load("Files/raw_data/input.csv")

# Perform a simple transformation (e.g., filter rows, add a column)
transformed_df = df.filter(df["value"] > 10).withColumn("status", lit("processed"))

# Write the transformed data to a new Delta table in the 'Tables' section of the Lakehouse
transformed_df.write.mode("overwrite").saveAsTable("transformed_table")



2. Using KQL (in a KQL Database)
Kusto Query Language is used within the Real-Time Intelligence experience to transform data after ingestion. An update policy can be used to automatically transform data as it arrives. 

// Steps:

1. Create a KQL Database in your workspace.
2. Ingest raw data into an initial staging table (e.g., "SourceTable").
3. Create a function with the transformation logic and an update policy to push data into a target table.


// Example KQL Code:


// 1. Create the target table schema
.create table TargetTable (id: int, name: string, value: real, status: string)

// 2. Define a function with transformation logic
.create function SourceTable_Transform() : table
{
    SourceTable
    | where value > 10
    | extend status = "processed"
}

// 3. Create an update policy to run the function when new data is ingested into SourceTable
.alter table TargetTable policy update @'[{ "Source": "SourceTable", "Query": "SourceTable_Transform()", "IsEnabled": true, "Is a snapshot": false }]'



// 3. Using SQL (T-SQL in a Data Warehouse or Lakehouse SQL Endpoint)
You can use standard T-SQL for ingestion (via COPY statement) and transformation within a Fabric Data Warehouse, which supports full read/write operations. 

// Steps:
1. Create a Data Warehouse in your workspace.
2. Use the COPY statement to ingest data from Azure Storage.
3. Use T-SQL INSERT INTO ... SELECT statements to transform and move data between tables.



-- Ingest data into a raw table using the high-throughput COPY statement
COPY INTO RawDataTable
FROM 'yourstorageaccount.blob.core.windows.net'
WITH (
    FILE_TYPE = 'CSV',
    CREDENTIAL = (IDENTITY = 'Managed Identity'),
    HEADER = 'FIRST_ROW'
);

-- Transform data and insert into a target table
INSERT INTO TransformedDataTable (id, name, value, status)
SELECT
    CAST(id AS INT),
    name,
    CAST(value AS REAL),
    'processed' AS status
FROM
    RawDataTable
WHERE
    CAST(value AS REAL) > 10;



// Create and Manage Shortcuts to Data 
Shortcuts in OneLake provide a unified view of your data without moving it, integrating data from different sources (OneLake, ADLS Gen2, Amazon S3) into your Lakehouse, Warehouse, or KQL Database. 


// 1. Via the User Interface (UI) in a Lakehouse 
This is the standard, low-code method for managing shortcuts. 


Steps:

1. Open your Lakehouse in the Microsoft Fabric portal.
2. In the Explorer pane, right-click on the Files or Tables section, or an existing directory.
3. Select New shortcut.
4. Choose the data source type (e.g., Azure Data Lake Storage Gen2, Amazon S3, or OneLake for internal references).
5. Configure the connection details and navigate to the target folder or container.
6. Review and Create the shortcut. It appears instantly in the Explorer pane. 


// 2. Programmatically (using Python/Spark)
You can interact with shortcuts and the data they point to using the Spark APIs in a Fabric Notebook. 

// Steps:

1. Ensure a shortcut already exists (created via UI or other means).
2. In a Fabric notebook, reference the shortcut path within the OneLake file system.

Example Python Code (PySpark):


# List the contents of a directory pointed to by a shortcut named 'MyADLSShortcut'
# Shortcuts appear under the 'Files' section in a Lakehouse
shortcut_path = "Files/MyADLSShortcut/"
files = mssparkutils.fs.ls(shortcut_path)

for file in files:
    print(file.name, file.path)

# Read data from the shortcut path directly using Spark
df_shortcut = spark.read.parquet(shortcut_path + "data.parquet")
df_shortcut.show()


