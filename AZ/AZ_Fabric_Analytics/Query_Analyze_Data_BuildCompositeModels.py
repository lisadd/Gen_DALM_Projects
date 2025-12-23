Designing and building composite models in Azure Power BI and Fabric is primarily a user interface-driven process within Power BI Desktop or the Fabric web modeling experience. 



// Steps to Design and Build a Composite Model
  1. Open Power BI Desktop or use the web modeling experience in the Fabric workspace.
  2. Connect to your initial data source. This can be a SQL database, KQL database, Lakehouse, or other source. Choose your initial storage mode (Import, DirectQuery, or Direct Lake).
  3. Add a second data source from a different source group (e.g., add an Excel file to a model already connected to a SQL database, or connect to another Power BI semantic model/Analysis Services model).
    - Adding a second source automatically converts the model into a composite model. If connecting to a Power BI semantic model, you will be prompted to convert the live connection to a DirectQuery connection.
  4. Define the storage mode for each table in your model.
    - Import: Data is loaded into memory for high performance.
    - DirectQuery: Queries run against the source at runtime, providing near real-time data.
    - Dual: The engine decides the best mode (Import or DirectQuery) on a query-by-query basis, often used for dimension tables.
  5. Create relationships between tables from different source groups in the Model view.
  6. Add measures, calculated columns, and hierarchies using Data Analysis Expressions (DAX) to enrich the model.
  7. Publish the report to your Azure Fabric workspace. 

// Query and Analyze Data Examples
Once your composite model is built, you can query and analyze the resulting semantic model using the following language examples:
 - Python: The sempy library in a Fabric notebook allows you to interact with the semantic model (dataset) using Python code.
 
# Import the required library
import sempy.fabric as fabric

# Authenticate (handled automatically in Fabric notebooks)
# List available semantic models
display(fabric.list_semantic_models())

# Load data from a specific semantic model and table
df = fabric.read_table(semantic_model="YourCompositeSemanticModelName", table_name="YourTableName")
display(df.head())

# Execute a DAX query against the model
dax_query = """
EVALUATE
SUMMARIZECOLUMNS (
    'Date'[Calendar Year],
    "Total Sales", SUM('Sales'[Sales Amount])
)
"""
dax_df = fabric.evaluate_dax(semantic_model="YourCompositeSemanticModelName", dax_query=dax_query)
display(dax_df)


// SQL: You can query the data using T-SQL by connecting to the SQL analytics endpoint of your Lakehouse or Warehouse in Fabric.


-- Connect to the SQL analytics endpoint of your Warehouse/Lakehouse
-- In a SQL Query editor in Fabric or SSMS

SELECT
    d.[Calendar Year],
    SUM(f.[Sales Amount]) AS [Total Sales]
FROM
    [dbo].[FactSales] AS f
INNER JOIN
    [dbo].[DimDate] AS d ON f.[DateKey] = d.[DateKey]
GROUP BY
    d.[Calendar Year]
ORDER BY
    [Total Sales] DESC;


// KQL: For data stored in a KQL database, you can use a KQL queryset in Fabric.

-- Connect to your KQL database in the KQL queryset
-- Query and analyze data

YourKQLTableName
| summarize TotalSales = sum(SalesAmount) by tostring(Year)
| order by TotalSales desc

