In Microsoft Fabric, the process of designing and implementing data loading patterns for a dimensional model typically involves using Pipelines for orchestration and ingestion, and Notebooks or SQL query editors with Python, KQL, or T-SQL for data preparation and transformation. 

// Design and Implement Loading Patterns
Common loading patterns in Microsoft Fabric for dimensional models include full and incremental loads. 

- Full Load: Ingesting the entire dataset from the source system. This is typically used for initial loads or small dimension tables.
- Incremental Load: Processing only new or changed data using techniques like watermarking (e.g., tracking a Modified Date or sequence number column) to optimize performance. This is ideal for large fact tables and dimensions with frequent changes. 

// Implementation tools in Fabric:
- Pipelines and Dataflows Gen2 offer low-code/no-code options for copy activities and basic transformations.
- Notebooks (PySpark, T-SQL, KQL) provide a code-first approach for complex transformations.
- COPY INTO (T-SQL) is efficient for ingesting files (Parquet/CSV) from external storage like Azure Data Lake Storage Gen2 into a Warehouse.
- INSERT...SELECT, SELECT INTO, and CREATE TABLE AS SELECT (CTAS) are set-based operations for cross-warehouse ingestion and transformation within Fabric, which is highly efficient. 

// Prepare Data for Loading into a Dimensional Model 
Data preparation involves classic ETL steps: extraction, cleaning, transformation (e.g., data type conversion, calculating new values), and loading into staged and then final dimension/fact tables. 

Steps with Example Code
The following examples use Python (PySpark in a Notebook) for data preparation in a Lakehouse and SQL (T-SQL in a Warehouse) for the final loading steps. 

 1. Ingest Raw Data (Staging)
 Data is typically landed in a staging area (e.g., a Lakehouse bronze layer) in its raw format. This can be done using a Data Factory Pipeline's Copy activity. 
 
 2. Prepare and Transform Data (Python/PySpark) 
 Use a Fabric Notebook with PySpark to clean, validate, and transform the data. This example demonstrates creating a new dimension table and adding a surrogate key using a common Spark pattern. 
python

# In a Fabric Notebook, ensure the default language is PySpark (Python)
from pyspark.sql.functions import row_number, monotonically_increasing_id
from pyspark.sql.window import Window

# Assume 'raw_data_df' is a DataFrame loaded from your source/staging area

# Example: Prepare a DimDate table
# (A real date dimension would be more complex and pre-generated, but this is for illustration)

# Select and transform columns
dim_date_df = raw_data_df.select(
    col("source_date").cast("date").alias("Date_PK"),
    year("source_date").alias("Calendar_Year"),
    month("source_date").alias("Calendar_Month"),
    dayofmonth("source_date").alias("Day_of_Month")
).distinct()

# In a Fabric Warehouse, surrogate keys can be added using T-SQL's ROW_NUMBER().
# If preparing entirely in PySpark before loading to a Lakehouse Delta table:
windowSpec = Window.orderBy("Date_PK")
dim_date_df = dim_date_df.withColumn("Date_SK", row_number().over(windowSpec))

# Write the prepared dimension data to the Lakehouse silver/gold layer as a Delta table
dim_date_df.write.format("delta").mode("overwrite").save("abfss://<container>@<storage_account>.dfs.core.windows.net/dimDate")


 3. Load into Dimensional Model (SQL/T-SQL) 
 Once data is staged and prepared, use T-SQL within a Fabric Warehouse SQL query editor or a T-SQL Notebook to load the final dimension and fact tables, ensuring dimensions are loaded before facts to maintain referential integrity. 

 Example 1: Create Dimension Table in Warehouse (T-SQL):

 -- Connect to your Fabric Warehouse via the SQL endpoint
-- Create a staging schema if needed
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'staging')
    EXEC('CREATE SCHEMA staging');

-- Create the final dimension table structure (consider SCD types, audit columns)
CREATE TABLE dbo.DimProduct (
    ProductSK INT IDENTITY(1,1) PRIMARY KEY, -- Surrogate Key
    ProductID VARCHAR(50) NOT NULL,          -- Natural Key
    ProductName VARCHAR(100),
    ProductCategory VARCHAR(50),
    IsCurrent BIT NOT NULL DEFAULT 1,
    ValidFrom DATE NOT NULL,
    ValidTo DATE
);


// Example 2: Load Dimension Table (T-SQL MERGE for SCD Type 2)
MERGE statements are powerful for handling inserts and updates (including slowly changing dimensions - SCD Type 2) in a single operation. This requires data to be in a staging table first. 

-- Assume 'staging.ProductUpdates' table exists with new/updated data

MERGE dbo.DimProduct AS Target
USING staging.ProductUpdates AS Source
    ON Target.ProductID = Source.ProductID AND Target.IsCurrent = 1
WHEN MATCHED AND (Target.ProductName <> Source.ProductName OR Target.ProductCategory <> Source.ProductCategory) THEN
    UPDATE SET 
        Target.IsCurrent = 0, 
        Target.ValidTo = GETDATE() -- End the old record
WHEN NOT MATCHED THEN
    INSERT (ProductID, ProductName, ProductCategory, ValidFrom)
    VALUES (Source.ProductID, Source.ProductName, Source.ProductCategory, GETDATE());

-- After the MERGE, insert new records for updated products if using a full SCD Type 2 approach, 
-- or handle inserts separately.



//  Example 3: Load Fact Table (T-SQL INSERT...SELECT)
Load the fact table by joining the staging data with the new dimension tables to look up and insert the correct surrogate keys. 

-- Assume 'staging.FactSales' contains raw sales data with natural keys
-- Assume 'dbo.DimProduct' and 'dbo.DimDate' are loaded

INSERT INTO dbo.FactSales (ProductSK, DateSK, SaleAmount, Quantity)
SELECT
    dp.ProductSK,
    dd.DateSK,
    s.SourceSaleAmount,
    s.SourceQuantity
FROM
    staging.FactSales s
JOIN
    dbo.DimProduct dp ON s.ProductID = dp.ProductID AND dp.IsCurrent = 1
JOIN
    dbo.DimDate dd ON s.SaleDate = dd.Date_PK;




