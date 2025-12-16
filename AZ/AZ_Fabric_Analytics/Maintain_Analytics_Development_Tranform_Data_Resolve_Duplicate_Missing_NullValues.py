In Microsoft Fabric, data transformation and cleansing for missing or duplicate values can be achieved using PySpark in notebooks, SQL with the Lakehouse/Warehouse endpoint, or KQL in a KQL database. 

///  Python (PySpark) Examples

These examples are for use within a Microsoft Fabric Notebook, typically operating on a Spark DataFrame. 

#Identify missing data: You can use the .info() method to see null counts, or filter explicitly:

# Identify rows with nulls in a specific column
rows_with_null = df.filter(df['column_name'].isNull())
rows_with_null.show()



# Resolve missing data (fill nulls): The .fillna() method is used to replace null values with a specified value:

# Fill missing values in a specific column with a default value (e.g., 'Unknown' or 0)
df_filled = df.fillna({'column_name': 'Unknown'})

# Fill all integer columns with 0
df_filled_all_ints = df.fillna(0)



# Resolve missing data (drop rows): The .dropna() method removes rows containing nulls:

# Drop rows where any value is null
df_dropped_any = df.dropna()

# Drop rows only if all values are null
df_dropped_all = df.dropna(how='all')

# Drop rows with nulls in a specific column
df_dropped_col = df.dropna(subset=['column_name'])



# Identify and resolve duplicate data: The .dropDuplicates() method removes duplicate rows:

# Remove rows that are duplicates across all columns
df_distinct = df.dropDuplicates()

# Remove rows that are duplicates based on specific columns (e.g., 'ID', 'Name')
df_distinct_subset = df.dropDuplicates(['ID', 'Name'])




// SQL Examples
These SQL commands are for use in the SQL Analytics endpoint of a Lakehouse or in a Data Warehouse, operating on tables.


# Identify missing data:

-- Select rows with a NULL value in 'column_name'
SELECT *
FROM TableName
WHERE column_name IS NULL;


# Resolve missing data (update or filter):

-- Update NULL values to a default value (e.g., 'N/A')
UPDATE TableName
SET column_name = 'N/A'
WHERE column_name IS NULL;

-- Alternatively, filter them out when selecting data
SELECT *
FROM TableName
WHERE column_name IS NOT NULL;


# Identify and resolve duplicate data: Duplicates are often handled using DISTINCT or window functions, as directly deleting duplicates can be complex:

-- Select distinct rows (effectively removing exact duplicates)
SELECT DISTINCT *
FROM TableName;

-- Using a CTE and ROW_NUMBER() to delete duplicates while keeping one instance
WITH CTE AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY column1, column2, column3 -- Specify columns that define a duplicate
            ORDER BY some_timestamp_column DESC    -- Keep the latest or first record
        ) AS rn
    FROM TableName
)
DELETE FROM CTE
WHERE rn > 1;






/// KQL (Kusto Query Language) Examples
These examples are for use within a KQL Queryset in a Microsoft Fabric KQL database. 


# Identify missing data:

-- Find records where 'column_name' is null
TableName
| where isnull(column_name)


#  Resolve missing data: The replace_string or coalesce functions can substitute values during a query, or you can filter them out:

-- Replace nulls in 'column_name' with a default value 'Unknown' during the query
TableName
| extend column_name = coalesce(column_name, 'Unknown')

-- Filter out records with nulls
TableName
| where isnotnull(column_name)



# Identify and resolve duplicate data: The distinct or arg_max / arg_min operators are useful for deduplication:

-- Return distinct rows based on all columns
TableName
| distinct *

-- Deduplicate based on specific columns, keeping the record with the latest timestamp
TableName
| summarize arg_max(timestamp_column, *) by column1, column2






