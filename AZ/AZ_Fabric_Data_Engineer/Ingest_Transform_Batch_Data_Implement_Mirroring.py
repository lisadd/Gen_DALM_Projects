In Microsoft Fabric, batch data ingestion and transformation can be accomplished using Pipelines, Notebooks (Python/Spark/SQL), or Dataflows Gen2. Data mirroring is a distinct, low-latency replication feature configured through the Fabric portal without explicit code for the replication process itself. 

// Ingest and Transform Batch Data

// Option 1: Notebooks (Python, SQL, KQL)

Notebooks offer a flexible, code-first approach ideal for data engineers. You use Spark (PySpark, Spark SQL) for processing data within a Lakehouse or Warehouse. 


// Steps:
1. Create a Lakehouse or Warehouse in your Fabric workspace.
2. Create a new Notebook and attach it to your Lakehouse.
3. Ingest data into the raw layer (e.g., Bronze folder in OneLake) using Python/Spark.
4. Transform data using PySpark or Spark SQL.
5. Write transformed data to a curated layer (e.g., Silver/Gold tables). 

Example Python (PySpark) Code for Ingestion and Transformation:

# Assuming you have a source file (e.g., 'abfss://...')
# Ingest raw data into a Spark DataFrame
df_raw = spark.read.format("csv").option("header", "true").load("Files/raw_data.csv")

# Perform transformations (example: filtering and adding a calculated column)
# This example filters rows where 'value' > 10 and adds an 'is_valid' column
df_transformed = df_raw.filter(df_raw['value'] > 10).withColumn("is_valid", lit(True))

# Write the transformed data to a delta table in your Lakehouse
df_transformed.write.format("delta").mode("overwrite").save("Tables/transformed_data")


// Example SQL (Spark SQL) Code in a Notebook:
You can run SQL commands in a notebook cell by using %%sql magic command. 


%%sql
-- Create a new table from the transformed data stored in the delta format
CREATE TABLE default.final_data AS
SELECT id, name, value, is_valid
FROM default.transformed_data
WHERE is_valid = TRUE;



Example KQL for Transformation (within a KQL Database):
You can use KQL for real-time analytics data transformation. 


.create-or-alter function TransformRawData() {
    RawData
    | parse source_column with * "prefix_" transformed_id:int
    | extend BikesToBeFilled = No_Empty_Docks - No_Bikes
    | project transformed_id, BikesToBeFilled, source_column
}

// Apply the transformation using an update policy
// (This is a configuration setting, not a direct query execution for batch)






// Option 2: Data Pipelines
For a low-to-no-code experience, use Fabric Data Pipelines with the Copy Data assistant. 

Steps:

1. In your workspace, select + New > Pipeline under Data Factory.
2. Use the Copy data assistant to configure source and destination.
3. Select your data source (e.g., Azure SQL DB, blob storage) and a Fabric destination (Lakehouse, Warehouse).
4. Use Dataflows Gen2 (which uses Power Query) for intermediate data transformation if needed. 

// Implement Mirroring 

Mirroring in Fabric is a configuration feature to continuously replicate data from external sources (like Azure SQL Database, Snowflake, etc.) into OneLake in near real-time, avoiding traditional ETL. 

Steps (No Code Required):

1. Open the Fabric portal and navigate to your workspace.
2. Select + New > More options, then under the Data Warehouse section, select Mirrored Azure SQL Database (or other source type).
3. Enter a name for your mirrored database and select Create.
4. Configure connection details for your source database, ensuring necessary permissions and network settings (e.g., public access or data gateways for private networks) are in place.
5. Select the tables you want to mirror from the source.
The mirroring process starts, and data is automatically replicated to OneLake, where you can then query it using the SQL analytics endpoint or access via notebooks. 

Once mirrored, you can query the data using standard T-SQL in the SQL analytics endpoint, for example: 

-- Query the mirrored data using T-SQL
SELECT * FROM dbo.YourMirroredTable WHERE [some_condition];

