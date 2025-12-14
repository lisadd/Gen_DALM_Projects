In Microsoft Fabric, the choice between a Lakehouse, Warehouse, or Eventhouse depends on your data's structure, speed, and the tasks (e.g., data engineering, BI, real-time analytics) you intend to perform with it. 


# Choosing the Right Fabric Item:
Feature 	Lakehouse	Warehouse	Eventhouse

- Primary Use Case	Data Engineering, Data Science, ML, raw data storage	Enterprise Data Warehousing, BI, structured reporting	Real-time analytics, time-series, IoT/telemetry data

- Data Types	Structured, semi-structured, unstructured	Structured (primarily)	Structured, semi-structured, unstructured (event streams)

- Primary Language	Python, PySpark, Spark SQL, R, Scala	T-SQL	KQL, limited T-SQL

- Ingestion Speed	Batch, near real-time	High-throughput batch	High-velocity real-time

- Access	Spark notebooks, SQL analytics endpoint	SQL endpoint, T-SQL queries	KQL queryset, Real Time Dashboards


# Data Ingestion and Access in Python
Data in all three items is stored in the open Delta Parquet format in OneLake, which simplifies data sharing. Ingestion is often done via Data Pipelines or Eventstreams, but Python can be used within Fabric notebooks for data preparation and loading. 


// 1. Ingest Data into a Lakehouse using Python (PySpark in a Fabric Notebook) 
You can use Spark within a Fabric notebook to read data from a source (like an external blob storage) and write it into your Lakehouse as a Delta table. 

# Ingest data from an external source (e.g., Azure Blob Storage) into the Lakehouse
# Assumes data is in CSV format and a linked service is configured

# Define the source path (using ABFS path format)
source_path = "abfss://<container_name>@<storage_account_name>.dfs.core.windows.net/<path_to_file.csv>"

# Read data into a Spark DataFrame
df = spark.read.format("csv").option("header", "true").load(source_path)

# Perform transformations (optional)
# For example, display the first few rows
display(df.limit(5))

# Write the DataFrame to the 'Tables' section of the default Lakehouse as a Delta table
# The table will be available in the SQL Analytics Endpoint
table_name = "MyLakehouseTable"
df.write.format("delta").mode("overwrite").saveAsTable(table_name)
print(f"Data successfully written to Lakehouse table: {table_name}")
 


// 2. Access Data from a Lakehouse using Python (Pandas in a Fabric Notebook) 
Inside a Fabric notebook, the default Lakehouse is automatically mounted at /lakehouse/default/, allowing easy access using file paths. 

import pandas as pd

# Read a Delta table from the Lakehouse into a Pandas DataFrame
# Data is physically stored in OneLake in delta format
df_pandas = spark.read.format("delta").load("/lakehouse/default/Tables/MyLakehouseTable").toPandas()

# Display the data
print(df_pandas.head())

# Alternatively, read a file from the 'Files' section of the lakehouse
file_df = pd.read_csv("/lakehouse/default/Files/my_uploaded_file.csv")
print(file_df.head())
 


// 3. Access Data from a Warehouse using Python (PyODBC/T-SQL Magic Command) 
For Warehouses, Python access usually involves connecting to the SQL endpoint using the pyodbc library or using the %%tsql magic command within a Fabric Notebook. This is best for structured data and analytical queries. 

# Use T-SQL magic command in a Fabric Notebook to query a Warehouse
# The results are bound to a Python Pandas DataFrame
# Replace 'Contoso' with your Warehouse name

%%tsql -artifact Contoso -type Warehouse -bind df_warehouse
SELECT * FROM dbo.DimDate;

# Display the resulting Pandas DataFrame
print(df_warehouse.head())
 


// 4. Ingest data into an Eventhouse 
Eventhouses are primarily designed for high-velocity, real-time streaming data. Ingestion is typically configured via Eventstreams within the Fabric UI, which can pull data from sources like Azure Event Hubs and route it automatically to the Eventhouse KQL database. While Python can manage the creation of these connections using the Azure SDKs, the actual data flow is managed by the Fabric service. Data access is primarily via KQL. 
