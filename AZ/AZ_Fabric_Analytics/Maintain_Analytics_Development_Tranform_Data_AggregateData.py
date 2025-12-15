In Microsoft Fabric, data transformation and aggregation can be accomplished using Python (PySpark/Pandas), Kusto Query Language (KQL), and SQL (T-SQL), primarily within Notebooks or Data Warehouse query editors. 


/// Python (PySpark/Pandas) Examples

Python in Fabric often uses PySpark dataframes for large-scale processing. You can run Python code in notebooks, and use kqlmagic to combine Python and KQL. 

# Transform (Filter) Data using Pandas (after KQL query):

%%kql
StormEvents 
| summarize max(DamageProperty) by State 
| order by max_DamageProperty desc 
| take 10

# After running the KQL above, the result is available as a pandas dataframe
df = _kql_raw_result_.to_dataframe()
statefilter = df.loc[0].State
print(f"Top state is: {statefilter}")

# Use the Python variable in a subsequent KQL query
%%kql
let _state = statefilter;
StormEvents | where State in (_state) | count 



# Aggregate Data using PySpark:

# orders_df is an existing PySpark DataFrame
sales_by_yearMonth = orders_df.groupBy("Year", "Month").agg({"UnitPrice": "sum"}).withColumnRenamed("sum(UnitPrice)", "Unit_Price")
sales_by_yearMonth.show()



/// Kusto Query Language (KQL) Examples:

KQL is powerful for real-time analytics and fast data exploration within a KQL database. 

Transform Data (using an update policy function):
You can define a function that performs transformations, which is then automated via an update policy.


// Create a function that adds two new calculated columns
.create function Bikepoint_light() {
    SourceTable
    | project BikepointID, Street, Neighbourhood, Latitude, Longitude, No_Bikes, No_Empty_Docks, Timestamp, 
    BikesToBeFilled = No_Empty_Docks - No_Bikes, 
    Action = iff(No_Empty_Docks > No_Bikes, "more docks", "more bikes")
}



# Aggregate Data:

// Use summarize operator to count total storms by state
StormEvents 
| summarize TotalStorms = count() by State
// You can also aggregate other functions like sum, avg, max, min
StormEvents
| summarize max(DamageProperty), avg(DamageProperty) by State



// SQL (T-SQL) Examples
T-SQL is used for data warehousing scenarios in Microsoft Fabric, allowing you to query and transform data in a Warehouse or its associated SQL analytics endpoint. 

# Transform Data (using a stored procedure):
You can execute a stored procedure to perform complex transformations and aggregations.

-- Execute a stored procedure to create and load aggregated data
EXEC [dbo].[populate_aggregate_sale_by_city];


# Aggregate Data:

-- Aggregate and group data by year and month
SELECT 
    YEAR(OrderDate) as OrderYear, 
    MONTH(OrderDate) as OrderMonth, 
    count(*) as TotalOrders, 
    SUM(UnitPrice) as TotalUnitPrice
FROM 
    dbo.orders
GROUP BY 
    YEAR(OrderDate), 
    MONTH(OrderDate);




