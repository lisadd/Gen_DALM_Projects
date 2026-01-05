In Microsoft Fabric, appropriate data stores for batch ingestion and transformation are the Lakehouse and the Data Warehouse. The Lakehouse is ideal for handling raw, semi-structured, and structured data with Spark-based transformations (Python/Scala/SQL), while the Data Warehouse excels at structured data, high-throughput ingestion, and T-SQL-based transformations. 


// Ingest and Transform Batch Data with Code
Below are steps and example code for a common batch processing pattern using a Lakehouse for ingestion and transformation with Python (Spark) or a Data Warehouse using SQL. 


1. Choose an Appropriate Data Store

For typical batch ETL/ELT, the Lakehouse (using Spark in notebooks) or the Data Warehouse (using T-SQL) are excellent choices. 

2. Steps for Batch Ingestion and Transformation
The following examples use a standard Medallion architecture approach (ingest into Bronze, transform into Silver/Gold layers). 

// A. Ingestion (Python in a Fabric Notebook)
Use Python with the Apache Spark environment available in a Fabric notebook to ingest raw data from a source (e.g., Azure Data Lake Storage Gen2 or an external source) into the Lakehouse's raw (Bronze) layer. 

// Steps:

1. Create a new Lakehouse item in your Microsoft Fabric workspace.
2. Create a new Notebook item and attach it to your Lakehouse.
3. Use the following Python code in a notebook cell to read data and write it as a Delta table in the "Files" section or directly to a managed table in the "Tables" section of the Lakehouse. 


# Ingest data from a CSV file in the 'Files' section of the Lakehouse to a 'raw_data' table
from pyspark.sql import SparkSession

# Assumes you have uploaded a file named 'source_data.csv' to the 'Files/bronze' directory
file_location = "Files/bronze/source_data.csv"
file_type = "csv"

# Spark read options
infer_schema = "true"
first_row_is_header = "true"
delimiter = ","

# Read the data into a Spark DataFrame
df = spark.read.format(file_type) \
  .option("inferSchema", infer_schema) \
  .option("header", first_row_is_header) \
  .option("sep", delimiter) \
  .load(file_location)

# Display the first 5 rows (optional)
display(df.limit(5))

# Write the DataFrame to a Delta Lake table in the 'Tables' section (managed table)
# This creates/overwrites a table named 'raw_data'
df.write.mode("overwrite").format("delta").saveAsTable("raw_data")
print("Data ingested to 'raw_data' table in the Lakehouse.")



// B. Transformation (Python/Spark SQL in a Fabric Notebook)
After ingestion, transform the data (e.g., clean, enrich, filter) and save it to a "silver" or "gold" layer table in the Lakehouse. You can use PySpark or Spark SQL. 


# Load the raw data from the 'raw_data' table
df_raw = spark.read.format("delta").load("Tables/raw_data")

# Perform a simple transformation (e.g., filter rows, add new column)
df_transformed = df_raw.filter("value > 10").withColumn("status", when(df_raw.value > 50, "High").otherwise("Low"))

# Write the transformed data to a new 'transformed_data' table (Silver layer)
df_transformed.write.mode("overwrite").format("delta").saveAsTable("transformed_data")
print("Data transformed and saved to 'transformed_data' table.")



// SQL Code (Spark SQL in Notebook):
You can also run SQL directly within a Python notebook cell using the %%sql magic command. 



%%sql
-- Create a new table 'gold_summary' from the 'transformed_data' table with an aggregation
CREATE OR REPLACE TABLE gold_summary AS
SELECT
    status,
    count(*) as count,
    avg(value) as avg_value
FROM
    transformed_data
GROUP BY
    status



// C. Ingestion and Transformation (SQL in a Fabric Data Warehouse)
For a Data Warehouse, you can use T-SQL commands like COPY INTO for ingestion and CREATE TABLE AS SELECT (CTAS) for transformation. 

Steps:
1. Create a Data Warehouse item in your Microsoft Fabric workspace.
2. Open the SQL Query editor.
3. Ensure your source data is accessible via an external Azure storage account or already in the Lakehouse via OneLake. 


// SQL Code (Ingestion using COPY INTO):


-- Ingest data from an external Azure Blob Storage container into a raw table in the Warehouse
COPY INTO dbo.RawBatchDataTable
FROM 'https://<YourStorageAccountName>.blob.core.windows.net/<YourContainer>/<YourFile.csv>'
WITH (
    FILE_TYPE = 'CSV',
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0A',
    FIRSTROW = 2 -- Skip header row
);



// SQL Code (Transformation using CTAS):


-- Transform data from the raw table and create a new aggregated table in the Warehouse
CREATE TABLE dbo.AggregatedSales AS
SELECT
    ProductID,
    SUM(Quantity) AS TotalQuantity,
    AVG(UnitPrice) AS AvgPrice
FROM
    dbo.RawBatchDataTable
GROUP BY
    ProductID;


// D. Transformation (KQL in a KQL Database)

If using a KQL database for real-time analytics, transformations are often defined using KQL functions and update policies. 

/// KQL Code (Create a transformation function):


.create-or-alter function TransformRawData() {
    RawData
    | where value > 10
    | extend status = iff(value > 50, "High", "Low")
    | project status, value
};





