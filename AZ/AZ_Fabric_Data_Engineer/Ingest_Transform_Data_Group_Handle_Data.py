In Microsoft Fabric (formerly Azure Data Fabric), batch data ingestion and transformation are typically handled using Data Pipelines (for orchestration and simple copying) and Notebooks (for complex transformations using PySpark, Python, SQL, or KQL). Data quality issues like duplicates, missing, and late-arriving data are addressed using specific techniques within these tools. 


1. Ingest Batch Data
You can use a Data Pipeline's Copy activity for basic ingestion or a Notebook for programmatic control. 

Steps using a Data Pipeline (UI-driven):

1. In your Microsoft Fabric workspace, select New > Pipeline.
2. Use the Copy Data assistant or manually add a Copy data activity to the canvas.
3. Configure the Source (e.g., Azure Data Lake Storage Gen2, Azure Blob Storage, SQL Database).
4. Configure the Destination (e.g., Lakehouse Delta Table, Warehouse).
5. Run the pipeline to ingest the data. 

// Example Python code (within a Fabric Notebook using PySpark):
This loads data from an ADLS Gen2 path into a Lakehouse table. 


# Import necessary libraries
from pyspark.sql import SparkSession

# Assumes a Lakehouse is attached and 'Files' container has the data
# The file path in OneLake is typically /Files/<folder>/<filename>
file_location = "abfss://<container>@<storage_account>.dfs.core.windows.net/<path/to/data.csv>"
file_type = "csv"

# Spark read options
spark_read_options = {
    "header": "true",
    "inferSchema": "true",
    "delimiter": ","
}

# Read the data into a Spark DataFrame
df = spark.read.format(file_type) \
    .options(**spark_read_options) \
    .load(file_location)

# Optional: display the first few rows
display(df)

# Write the DataFrame to a Delta Lake table in the Lakehouse
# 'sales_data_raw' is the name of the target table in your Lakehouse
df.write.mode("append").format("delta").saveAsTable("sales_data_raw")



//  Example SQL Code (within a Fabric Warehouse using T-SQL COPY statement):
This is a high-throughput option for data already in Azure storage. 

COPY INTO dbo.YourTableName
FROM 'https://<storage_account>.blob.core.windows.net/<container>/<path>'
WITH (
    FILE_TYPE = 'CSV',
    CREDENTIAL = (IDENTITY = 'Managed Identity'),
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0A',
    HEADER = 'TRUE'
);



// 2. Transform Batch Data

Transformations are usually best handled in a Fabric Notebook using PySpark for large datasets or KQL/SQL for data already in a KQL database or Warehouse, respectively. 

Example Python code (within a Fabric Notebook using PySpark):
This code reads the raw data, performs a simple transformation (e.g., filtering missing values), and saves it to a "curated" table. 


# Read from the raw Lakehouse table
df_raw = spark.read.format("delta").table("sales_data_raw")

# Transformation: Handle missing data (e.g., drop rows with null in 'product_id')
df_transformed = df_raw.dropna(subset=["product_id"])

# Transformation: Add a new column
from pyspark.sql.functions import col
df_transformed = df_transformed.withColumn("total_price", col("quantity") * col("unit_price"))

# Write the transformed data to a new curated Delta table
df_transformed.write.mode("overwrite").format("delta").saveAsTable("sales_data_curated")



// Example KQL code (within a KQL Database):
You can use an update policy to automatically run transformations. 


// Define a function with transformation logic
.create-or-alter function TransformRawData() {
    sales_data_raw
    | where not(isnull(product_id)) // Handle missing data
    | extend total_price = quantity * unit_price
    | project-away quantity, unit_price // Select relevant columns
};

// Apply an update policy to ingest into a curated table
// First, create the target table "sales_data_curated_kql"
// .create table sales_data_curated_kql ... (define schema)

// Then, set the update policy
.alter table sales_data_curated_kql policy update @'[{"Source": "sales_data_raw", "Query": "TransformRawData()", "IsEnabled": "True", "Is a lightweight update": "True"}]'





// 3. Handle Duplicate, Missing, and Late-Arriving Data 
Strategies depend on the target system (Lakehouse/Spark or KQL DB) and the data flow. 

A. Handling Duplicates
Python/PySpark (Notebook/Lakehouse): Use Delta Lake's MERGE operation for upserts, or deduplication functions.


# Deduplication using Spark SQL in a Notebook
df_dedup = df_transformed.dropDuplicates(["order_id", "product_id"])
df_dedup.write.mode("overwrite").format("delta").saveAsTable("sales_data_final")



For advanced handling, use the MERGE statement in a notebook as shown in the Microsoft documentation.
KQL (KQL Database): Use Materialized Views for automatic, continuous deduplication based on an ID, or use ingest-by: extent tags.


.create materialized-view dedup_sales_data on table sales_data_raw
| summarize take_any(*) by order_id, product_id



SQL (Warehouse): Use the MERGE statement for robust upsert logic to handle duplicates and updates simultaneously. 
B. Handling Missing Data
Python/PySpark: Use DataFrame functions like dropna() or fillna().


# Fill missing prices with a default value (e.g., 0.0)
df_filled = df_transformed.fillna({"unit_price": 0.0})


KQL: Use KQL operators like isnull() in your transformation functions to filter or impute missing values. 

// C. Handling Late-Arriving Data
Pipelines: Configure pipelines with watermark values (timestamps of the last successful load) in a metadata table. Subsequent pipeline runs use the watermark to only pick up new or later data.

Pipelines/General: Use event-based triggers instead of scheduled triggers to process files as soon as they arrive, regardless of timing.

PySpark/SQL: The Delta format and MERGE operations naturally handle late-arriving data by allowing updates or insertions based on a key and a timestamp column. 
