In Microsoft Fabric, you can use Python (via Spark DataFrames), Kusto Query Language (KQL), or SQL to convert data types and filter data. The following examples demonstrate common operations for each language, assuming you are working within a Fabric Notebook or respective editor (KQL Queryset, SQL Query editor). 

Python (Spark DataFrames in a Fabric Notebook)

When working in a Fabric notebook, data is often loaded into a Spark DataFrame (e.g., df). 

// Filter data: Use the filter() or where() methods on a DataFrame:

# Filter data to select rows where the 'State' column is 'FLORIDA'
filtered_df = df.filter(df['State'] == 'FLORIDA')
filtered_df.show()



// Convert column data types: Use the withColumn() method combined with type conversion functions like cast() from pyspark.sql.functions

from pyspark.sql.functions import col

# Convert the 'DamageProperty' column from its original type to an integer type
df_transformed = df.withColumn('DamageProperty_Int', col('DamageProperty').cast('integer'))

# Display the new schema and some data
df_transformed.printSchema()
df_transformed.show()



// KQL (Kusto Query Language):

KQL is primarily used in Real-Time Analytics within Microsoft Fabric. Queries are executed against KQL databases. 


Filter data: Use the where operator to filter records based on a condition:

StormEvents
| where State == "FLORIDA"
| where DamageProperty > 5000
| take 10


// Convert column data types: Use the extend operator with a type conversion function (e.g., tostring(), toint()) to create a new column with the desired type. Note that you typically create a new column rather than altering the original column's type within a query, though management commands exist to alter the underlying table schema if needed.


StormEvents
| extend DamageProperty_Str = tostring(DamageProperty)
| extend StartTime_Date = todatetime(StartTime)
| project State, DamageProperty_Str, StartTime_Date
| take 10


*** SQL (Data Warehouse in Microsoft Fabric) 
T-SQL (Transact-SQL) is used for querying the SQL endpoint of a Lakehouse or a Fabric Data Warehouse. 

// Filter data: Use the WHERE clause in a SELECT statement:

SELECT
    *
FROM
    dbo.StormEvents
WHERE
    State = 'FLORIDA' AND DamageProperty > 5000;


// Convert column data types: Use the CAST() or CONVERT() functions within your query:

SELECT
    State,
    CAST(DamageProperty AS INT) AS DamageProperty_Int,
    CONVERT(DATE, StartTime) AS StartTime_Date
FROM
    dbo.StormEvents;



