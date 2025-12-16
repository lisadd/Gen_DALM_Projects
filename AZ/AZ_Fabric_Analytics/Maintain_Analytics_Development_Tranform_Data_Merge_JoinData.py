In Azure Data Fabric, data transformation, merging, and joining can be accomplished using Python (PySpark), Kusto Query Language (KQL), and T-SQL depending on the service (e.g., Spark Notebooks, KQL databases, Data Warehouses). 

// Python (PySpark)

In Fabric notebooks using PySpark, data manipulation is typically done using DataFrame operations. 

#Transform (Aggregation example): The following code aggregates data by year and month and calculates the sum of UnitPrice:

sales_by_yearMonth = orders_df.groupBy("Year", "Month").agg({"UnitPrice": "sum"}).withColumnRenamed("sum(UnitPrice)", "Unit_Price")
sales_by_yearMonth.show()


# Join Data (Conceptual): You would use the join method on DataFrames:

# Assuming 'df1' and 'df2' are your DataFrames and 'ID' is the common column
joined_df = df1.join(df2, df1["ID"] == df2["ID"], "inner")
joined_df.show()


# Merge Data (Union example): To merge dataframes with compatible schemas (similar to a SQL UNION), you can use the union method.

# Assuming 'df1' and 'df2' have identical schemas
merged_df = df1.union(df2)
merged_df.show()


// Kusto Query Language (KQL)
In a Fabric KQL database, you use KQL operators for data manipulation and the join or lookup operator for combining data. 

# Transform (Summarize and Extend example): The following KQL script filters events, summarizes records by state, and extends a table with a new calculated column.


// Filter and aggregate data
StormEvents
| where State == "GEORGIA"
| summarize TotalRecords = count() by State, bin(StartTime, 1d)
| render timechart title = "Trend"

// Extend table with a new column
RawData
| extend BikesToBeFilled = No_Empty_Docks - No_Bikes
| extend Action = iff(BikesToBeFilled > 0, tostring(BikesToBeFilled), "NA")



# Join/Merge Data: The join operator combines rows from two tables based on a match in key columns. lookup is a specific optimization of leftouter or inner join for enriching a fact table with a dimension table.

// Inner join example
SalesFact 
| join kind=inner Products on ProductID
| summarize TotalSales = sum(Quantity) by ProductCategory



// SQL (T-SQL):

In a Fabric Data Warehouse or Synapse SQL environment, standard T-SQL is used for data operations. 

# Transform (Aggregate example): The following T-SQL code aggregates and groups data:


SELECT 
    YEAR(OrderDate) AS OrderYear, 
    MONTH(OrderDate) AS OrderMonth, 
    COUNT(*) AS TotalOrders, 
    SUM(UnitPrice) AS TotalUnitPrice
FROM 
    dbo.orders
GROUP BY 
    YEAR(OrderDate), 
    MONTH(OrderDate);


# Join Data: Standard SQL JOIN syntax is supported:

SELECT 
    T1.column1, 
    T2.column2
FROM 
    Table1 AS T1
INNER JOIN 
    Table2 AS T2 ON T1.ID = T2.ID;



# Merge Data: The MERGE statement in T-SQL performs inserts, updates, and deletes in a single command based on conditions between a source and target table:

MERGE TargetTable AS T
USING SourceTable AS S
    ON T.ID = S.ID
WHEN MATCHED THEN
    UPDATE SET T.Value = S.Value
WHEN NOT MATCHED BY TARGET THEN
    INSERT (ID, Value) VALUES (S.ID, S.Value);



