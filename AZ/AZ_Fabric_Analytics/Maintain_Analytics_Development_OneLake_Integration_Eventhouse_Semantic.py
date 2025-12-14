Implementing OneLake integration involves enabling the feature in the respective service settings in the Fabric portal, after which the data becomes accessible in Delta Lake format via standard Azure Data Lake Storage (ADLS) APIs or specific Fabric Python libraries. 

Prerequisites
- Microsoft Fabric Capacity: You need a Power BI Premium P or Microsoft Fabric F SKU.
- Permissions: Appropriate workspace and item permissions (e.g., Contributor) are required.
- Enablement: OneLake integration must be explicitly enabled for the specific Eventhouse KQL database/table and for the semantic model in their respective settings. 

Eventhouse OneLake Integration

- Data in the Eventhouse, once OneLake availability is enabled, is exposed as Delta tables in OneLake. 

Enable Integration

- Navigate to your KQL database in the Fabric portal.
- In the item details pane, find the OneLake section and set Availability to Enabled. This can be done at the database or table level. 

Python Coding Example (Accessing data in a Fabric Notebook)

You can access the Eventhouse data from a Fabric Notebook using a Spark job and the OneLake ABFS (Azure Blob Filesystem) path. 


# Import necessary libraries (already available in Fabric notebooks runtime)
from pyspark.sql import SparkSession

# Replace placeholders with your actual workspace and item details
# The path format for KQL database in OneLake is specific
workspaceName = "<yourWorkspaceName>"
kqlDatabaseName = "<yourKQLDatabaseName>"
tableName = "<yourTableName>"

# Construct the OneLake path using the ABFS format
# Note: the kql database name is appended with '.KustoDatabase' in the path
delta_table_path = f"abfss://{workspaceName}@onelake.dfs.fabric.microsoft.com/{kqlDatabaseName}.KustoDatabase/Tables/{tableName}"

# Read the delta table into a Spark DataFrame
df = spark.read.format("delta").load(delta_table_path)

# Display the data
df.show()



Semantic Model OneLake Integration

For semantic models, the integration writes all import-mode tables to Delta tables in OneLake. 

Enable Integration
- In your Power BI semantic model settings in the Fabric workspace, expand OneLake integration.
- Click the slider to On and select Apply. 


Python Coding Example (Accessing data using semantic link in a Fabric Notebook) 

The most direct way to access an integrated semantic model in Python is by using the semantic link library in a Fabric Notebook, which can read the data directly from the underlying Delta tables in OneLake. 

# Import necessary libraries
import pandas as pd
from sempy.functions import read_table
from sempy import resolve_onelake_path

# Replace placeholders with your actual workspace and semantic model details
workspace_name = "<yourWorkspaceName>"
semantic_model_name = "<yourSemanticModelName>"
table_name = "<yourTableName>"

# Read the table directly from OneLake mode using semantic link
# This method uses the 'onelake' mode to read from the Delta tables in OneLake
df = read_table(semantic_model_name, table_name, workspace=workspace_name, mode="onelake")

# Display the first few rows of the DataFrame
print(df.head())





General OneLake Access (using ADLS Gen2 APIs):

You can also access data in OneLake as if it were an ADLS Gen2 storage account using the azure-storage-file-datalake library in any Python environment (requires authentication setup, such as DefaultAzureCredential). 

Below is a Python coding example demonstrating how to list files within a specified path in OneLake using ADLS Gen2 APIs. This example utilizes the azure.storage.file-datalake and azure.identity libraries, authenticating with DefaultAzureCredential. 

To demonstrate accessing OneLake using ADLS Gen2 APIs with Python, the following code snippet shows how to list files within a specified path. This example uses the azure-storage-file-datalake and azure.identity libraries for authentication and access. 
