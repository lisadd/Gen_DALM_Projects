In Microsoft Fabric, data ingestion and transformation using PySpark, SQL, and KQL is typically done within a Lakehouse or KQL database using Notebooks or Data Pipelines. Denormalization is often achieved by joining related tables into a single, wider structure using the appropriate language. 

// Steps for Data Ingestion, Transformation, and Denormalization
The general workflow involves:

1. Ingestion: Loading raw data into the Bronze layer of a Lakehouse or a KQL database.
2. Transformation/Denormalization: Applying logic (filtering, cleaning, joining) using PySpark, Spark SQL, T-SQL, or KQL.
3. Persistence: Saving the transformed, often denormalized, data into the Silver or Gold layer. 


// Example Code and Scenarios
1. Ingestion
PySpark (Notebook)
This loads data from an external source (e.g., a CSV file in OneLake) into a Spark DataFrame and then saves it as a Delta table in the Lakehouse. 

# Ingest data from a CSV file in the 'Files' section to a Delta table in the 'Tables' section
df = spark.read.format("csv").option("header", "true").load("Files/dimension_city/*.csv")

# Display count for verification
print(df.count())

# Write to a Delta table
df.write.mode("overwrite").format("delta").saveAsTable("wwilakehouse.dimension_city")



// KQL (KQL Queryset or Notebook)
This script creates a table with a defined schema and mapping, then pulls data from a public blob storage URL. 

// 1. Create the table and define schema mapping
.create table trips2 (
    BikepointID:string,
    Street:string,
    Neighbourhood:string,
    Latitude:real,
    Longitude:real,
    No_Bikes:long,
    No_Empty_Docks:long,
    Timestamp:datetime
)

// 2. Ingest data from a public blob
.ingest into table trips2 ('path.to.your') with (ignoreFirstRecord=true)



SQL (Warehouse or Lakehouse SQL endpoint)
Use the COPY statement in a Warehouse to ingest data from Azure Data Lake Storage Gen2 or Azure Blob storage. 

COPY INTO dbo.YourTableName
(col1, col2, col3)
FROM 'yourstorageaccount.blob.core.windows.net'
WITH (
    FILE_TYPE = 'PARQUET',
    -- Other options like FIELDTERMINATOR, ROWTERMINATOR can be specified for CSV
)


// 2. Transformation and Denormalization
PySpark (Notebook)
Join multiple related DataFrames (df_fact_sale, df_dimension_date, df_dimension_city) to denormalize the data into a single aggregated DataFrame. 


# Create DataFrames referencing existing Delta tables in the Lakehouse
df_fact_sale = spark.read.table("wwilakehouse.fact_sale")
df_dimension_date = spark.read.table("wwilakehouse.dimension_date")
df_dimension_city = spark.read.table("wwilakehouse.dimension_city")

# Denormalize/Join data to generate business aggregates
df_denormalized = df_fact_sale.join(df_dimension_date, ["date_id"]) \
                              .join(df_dimension_city, ["city_id"])

# Select relevant columns and perform transformations (e.g., uppercase a column)
from pyspark.sql.functions import upper
df_transformed = df_denormalized.selectExpr(
    "sale_id",
    "upper(city) as sale_city",
    "total_amount"
)

# Write the denormalized data to a new Gold layer Delta table
df_transformed.write.mode("overwrite").format("delta").saveAsTable("wwilakehouse.sales_gold")



// SQL (Spark SQL in Notebook or T-SQL in Warehouse/Lakehouse SQL endpoint)
Use standard JOIN operations to denormalize across tables. In a Fabric Notebook, use the %%sql magic command to run Spark SQL. 


%%sql
-- Denormalize data by joining multiple dimension tables to a fact table
SELECT
    vidg.game_id,
    vidg.title,
    gen.genre,
    pub.publisher
FROM
    wwilakehouse.dim_videogames_norm AS vidg
JOIN
    wwilakehouse.dim_genres AS gen ON vidg.genre_id = gen.genre_id
JOIN
    wwilakehouse.dim_publishers AS pub ON vidg.publisher_id = pub.publisher_id


// KQL (KQL Queryset or Notebook)
While KQL is optimized for real-time analytics and schema-on-read, you can use the join operator for denormalization within a query, though performance might vary compared to Spark/SQL for massive batch operations. KQL is more commonly used for real-time transformations via functions and update policies. 

// Define a KQL function for transformation logic
.create-or-alter function TransformRawData() {
    RawData
    | parse BikepointID with * "BikePoints_" BikepointID:int // Extract int from string
    | extend BikesToBeFilled = No_Empty_Docks - No_Bikes // Add calculated column
    | project BikepointID, Street, BikesToBeFilled // Select specific columns
}

// Query using the function and join (if another table exists)
TransformRawData()
| join (AnotherTable) on CommonId
| project Street, BikesToBeFilled, AnotherTable.Info




