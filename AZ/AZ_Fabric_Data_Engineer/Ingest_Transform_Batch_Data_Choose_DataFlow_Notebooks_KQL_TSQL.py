In Microsoft Fabric, you can ingest and transform batch data using Dataflows Gen2 (low-code visual editor), Notebooks (code-first using Python/Spark, KQL, or T-SQL), or a combination orchestrated via Data Pipelines. The best choice depends on your technical comfort and desired control level.



// 1. Dataflows Gen2 (Low-Code/No-Code) 
Dataflows Gen2 use the Power Query editor for a visual, drag-and-drop transformation experience, ideal for business analysts and data engineers who prefer a no-code interface. 


Steps for Ingestion and Transformation:


1. Create a Dataflow Gen2 in your Fabric workspace.
2. Connect to data sources using one of hundreds of available connectors (e.g., SQL Server, OData, Excel, CSV).
3. Transform data visually using the Power Query editor (filter, clean, merge, etc.).
4. Add a data destination (e.g., Lakehouse, Warehouse, KQL DB) to load the transformed data.
5. Publish and Schedule the dataflow for recurring batch runs. 


// 2. Notebooks (Code-First: Python/Spark, KQL, T-SQL)
Notebooks offer full control using various languages and are integrated with Fabric's data stores (Lakehouse, Warehouse). They run on Apache Spark infrastructure. 

// A. Python/Spark
This approach is suitable for complex transformations, data science tasks, and leveraging the full power of Spark and Python libraries (pandas, scikit-learn, etc.). 


// Steps & Example Code:
1. Create a Notebook in the Fabric Data Engineering experience.
2. Ingest data from a Lakehouse table or external source into a Spark DataFrame.
3. Transform data using PySpark or Python.
4. Write data back to a Fabric destination. 


// Example Python Code (PySpark in a Notebook):


# Read data from a Lakehouse table into a Spark DataFrame
df = spark.read.format("delta").load("Tables/YourSourceTable")

# Example Transformation: Filter rows and add a new column
from pyspark.sql.functions import col
transformed_df = df.filter(col("CountryOrRegion") == "Belgium").withColumn("NewColumn", col("SomeValue") * 2)

# Write the transformed data to a new table in the Lakehouse
transformed_df.write.format("delta").mode("overwrite").save("Tables/BelgiumFilteredTable")



// B. KQL (Kusto Query Language)
KQL is used for real-time intelligence scenarios and interacting with KQL databases. 
Steps & Example Code:

1. Create a KQL database artifact.
2. Ingest data using a KQL script or data pipeline.
3. Transform data using KQL operators. 

Example KQL Code (using %%kql magic command in a Notebook):


%%kql
// Create a new table with transformed data
.set NewTableName <|
YourSourceTable
| where CountryOrRegion == "Belgium"
| project Column1, Column2, TransformedColumn = Column3 * 2



// C. T-SQL (Transact-SQL)
T-SQL is ideal for data warehouse scenarios and teams familiar with SQL environments, offering high-throughput ingestion via the COPY statement. 

Steps & Example Code:

1. Create a Data Warehouse artifact.
2. Ingest data using the high-performance COPY statement from Azure storage, or use INSERT INTO with OPENROWSET for ad-hoc ingestion from OneLake.
3. Transform data using standard T-SQL queries (joins, updates, inserts). 

Example T-SQL Code (using %%tsql magic command in a Notebook):


%%tsql
-- Use the COPY statement for high-throughput ingestion from an external source
COPY INTO dbo.YourDestinationTable
FROM 'yourstorageaccount.blob.core.windows.net'
WITH (
    FILE_TYPE = 'CSV',
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    HEADER = ON
);

-- Example Transformation: Insert transformed data from one table to another
INSERT INTO dbo.AggregatedSales
SELECT 
    ProductID,
    SUM(Quantity) as TotalQuantity,
    AVG(Price) as AveragePrice
FROM 
    dbo.YourDestinationTable
GROUP BY 
    ProductID;








 
