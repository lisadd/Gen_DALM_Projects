In Microsoft Fabric, batch data ingestion, transformation, grouping, and aggregation can be accomplished using Data Pipelines, Notebooks (PySpark/Python), or the Warehouse (T-SQL/SQL). 

//Steps for Batch Data Processing
The high-level steps for batch data processing in Azure Data Fabric are:

1. Ingest Raw Data: Use a Data Pipeline's Copy activity to land raw data (e.g., from an Azure Blob storage) into the Bronze layer of a Lakehouse. Alternatively, the T-SQL COPY statement can be used to ingest data directly into a Warehouse table from an external source.

2. Transform and Refine: Use a Fabric Notebook with PySpark or a Dataflow Gen2 to apply transformation logic (e.g., cleaning, filtering, joining).

3. Group and Aggregate: Perform grouping and aggregation operations using PySpark, T-SQL, or KQL depending on your target destination (Lakehouse or Warehouse/KQL Database).

4. ALoad Curated Data: Save the transformed and aggregated data into a refined Delta table in the Lakehouse (Silver/Gold layers) or a Warehouse table for downstream analytics. 


Example Code

The following examples demonstrate grouping and aggregation using Python (PySpark), KQL, and SQL (T-SQL).
Python (PySpark)

In a Fabric Notebook, you can use PySpark to group and aggregate data. This example aggregates sales data by year and month. 

# Assuming 'orders_df' is a PySpark DataFrame loaded from a Lakehouse table
# Example: orders_df = spark.read.format("delta").load("abfss://<container>@<storage>.dfs.core.windows.net/orders_table")

sales_by_yearMonth = orders_df.groupBy("Year", "Month").agg(
    {"UnitPrice": "sum"}
).withColumnRenamed("sum(UnitPrice)", "Total_Unit_Price") #

# Display the result
sales_by_yearMonth.show()

# To save the result back to a new Delta table in the Lakehouse
# sales_by_yearMonth.write.format("delta").mode("overwrite").save("abfss://<container>@<storage>.dfs.core.windows.net/sales_agg_table")



// KQL (Kusto Query Language) 
In a KQL database, you use the summarize operator to group and aggregate data. This example counts total records grouped by state. 


// In the KQL Queryset, run this query:
Weather
| summarize TotalRecords = count() by State //
| project State, TotalRecords
| order by TotalRecords desc


// SQL (T-SQL)
In a Fabric Data Warehouse, you use standard T-SQL GROUP BY and aggregate functions. This example aggregates order data by year and month. 


-- In the Warehouse Query Editor, run this T-SQL query:

SELECT
    YEAR(OrderDate) AS OrderYear,
    MONTH(OrderDate) AS OrderMonth,
    COUNT(*) AS TotalOrders,
    SUM(UnitPrice) AS TotalUnitPrice
FROM
    dbo.orders --
GROUP BY
    YEAR(OrderDate),
    MONTH(OrderDate);

