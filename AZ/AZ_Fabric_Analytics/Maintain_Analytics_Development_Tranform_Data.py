# In Microsoft Fabric, data transformations and star schema implementation are primarily achieved using PySpark/Spark SQL in Notebooks for Lakehouses and T-SQL for Warehouses. KQL (Kusto Query Language) is used for real-time analytics scenarios and can leverage update policies for transformation. 
Transform and Enrich Data (Python/PySpark)

// In a Microsoft Fabric Lakehouse, Python (PySpark) is the primary language for data engineering transformations within a Notebook environment. The code below demonstrates loading data into a Spark DataFrame, enriching it with a new column, and saving it as a Delta table (a common format in Fabric lakehouses). 


# Import necessary libraries
from pyspark.sql import functions as F

# Assuming 'raw_data_table' is a table in your Lakehouse (e.g., in the "Bronze" layer)
df = spark.read.table("raw_data_table")

# --- Transform data: Filter out null values in a key column ---
df_cleaned = df.filter(df["some_key_column"].isNotNull())

# --- Enrich data: Add a new calculated column (e.g., 'TotalAmount' from 'Quantity' and 'UnitPrice') ---
df_enriched = df_cleaned.withColumn("TotalAmount", df_cleaned["Quantity"] * df_cleaned["UnitPrice"])

# --- Save the transformed and enriched data to a new Delta table (e.g., in the "Silver" layer) ---
# Make sure the 'Tables' folder in your Lakehouse is the target
df_enriched.write.format("delta").mode("overwrite").saveAsTable("enriched_silver_table")



// B. Implement a Star Schema (SQL): 

In a Microsoft Fabric Warehouse, T-SQL is used to define and populate the star schema (fact and dimension tables). You can run the following SQL scripts in a SQL Query Editor in your Warehouse. 

1. Create Dimension Table (T-SQL)
The following code creates a DimProduct dimension table with a surrogate key. 


CREATE TABLE DimProduct (
    ProductKey INT IDENTITY(1,1) PRIMARY KEY NONCLUSTERED NOT ENFORCED, -- Use IDENTITY for surrogate keys
    ProductID INT NOT NULL,
    ProductName NVARCHAR(100),
    Category NVARCHAR(50),
    -- Other dimension attributes
) WITH (
    DISTRIBUTION = REPLICATE -- Replicate distribution is often efficient for smaller dimension tables
);



# Note that while PRIMARY KEY is supported for performance optimization, constraints are not enforced in the Synapse SQL engine within Fabric. Data integrity must be managed during the ETL process. 


// 2. Create Fact Table (T-SQL):
The following code creates a FactSales table, including foreign keys to dimension tables and measurable facts. 


CREATE TABLE FactSales (
    SaleKey BIGINT IDENTITY(1,1),
    DateKey INT NOT NULL,
    ProductKey INT NOT NULL, -- Foreign key to DimProduct
    CustomerKey INT NOT NULL, -- Foreign key to DimCustomer
    SalesAmount DECIMAL(18, 2),
    Quantity INT,
    -- Other measures
) WITH (
    DISTRIBUTION = HASH(ProductKey) -- Hash distribution is typically good for large fact tables
);



// 3. Populate Tables (T-SQL):
You can populate these tables using INSERT INTO ... SELECT statements, potentially using cross-database queries if the source data is in a different Lakehouse or Warehouse within the same workspace. 


-- Example: Populate DimProduct from a staging table (e.g., 'Staging_Products')
INSERT INTO DimProduct (ProductID, ProductName, Category)
SELECT ProductID, ProductName, Category
FROM Staging_Products
WHERE ProductID IS NOT NULL;



// Transform Data (KQL):

In a KQL Database, you can use update policies to automatically transform and enrich data. The policy runs a KQL query on the source table and ingests the results into a destination table. 


// Define the function that performs the transformation
.create function with (docstring = 'A function that enriches raw data', folder = 'Enrichment') 
TransformRawData() {
    RawDataTable
    | where quantity > 0
    | project 
        timestamp,
        product_id,
        customer_id,
        total_price = quantity * price, // Enrich with a new column
        event_city = city
}

// Create an update policy to run this function automatically
.alter table TransformedDataTable policy update on TransformedData 
@'[{"Source": "RawDataTable", "Query": "TransformRawData()", "IsEnabled": true, "Is a snapshot": false}]'



This KQL update policy automatically transforms data in RawDataTable and loads the enriched results into TransformedDataTable







