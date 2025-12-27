Configuring Microsoft Fabric workspace settings programmatically is primarily achieved using the Fabric CLI (Command Line Interface) and REST APIs, which can be invoked from Python scripts or PowerShell. KQL and SQL are used for data querying and manipulation within a KQL database or Data Warehouse item, not for managing overall workspace settings. 

//Python (via Fabric CLI)

You can use the Fabric CLI from within a Python script to automate workspace operations. First, ensure you have the CLI installed using pip: pip install MS-fabric-CLI. 

The following Python script uses the os library to execute Fabric CLI commands. This example creates a workspace and a Lakehouse within it:

import os

# Authenticate to Fabric via CLI (interactive login)
# You would typically run 'fab login' in your terminal first and authenticate interactively
# For automation, service principal authentication is recommended.
# os.system("fab login --method ServicePrincipal --client-id <client_id> --secret <secret> --tenant-id <tenant_id>")

workspace_name = "MyAutomatedWorkspace"
lakehouse_name = "MyLakehouse"

# Create a new workspace
print(f"Creating workspace: {workspace_name}")
os.system(f'fab workspace create --name "{workspace_name}"')

# Create a new Lakehouse in the workspace
print(f"Creating lakehouse: {lakehouse_name} in {workspace_name}")
os.system(f'fab lakehouse create --workspace "{workspace_name}" --name "{lakehouse_name}"')

# List workspaces to verify
print("Listing all workspaces:")
os.system("fab ls")



NOTE: For production automation, service principal authentication is used to avoid interactive logins. Reference: https://www.google.com/url?sa=i&source=web&rct=j&url=https://learn.microsoft.com/en-us/rest/api/fabric/articles/fabric-command-line-interface&ved=2ahUKEwilk5SO096RAxVFF2IAHdtuI4wQy_kOegQIBhAB&opi=89978449&cd&psig=AOvVaw3FR46T0uP1ab8QTQ9fU_fB&ust=1766955176192000


// REST API (Python Example)
You can also use Python to call the Fabric REST APIs directly for more granular control. This requires obtaining a Microsoft Entra ID token. 


import requests
import json

# Replace with your actual access token and capacity ID
ACCESS_TOKEN = "<Your_Access_Token>"
CAPACITY_ID = "<Your_Capacity_ID>" 
WORKSPACE_NAME = "NewWorkspaceViaAPI"

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# The endpoint for creating a workspace
# The API for creating a workspace includes a parameter for the capacity ID.
api_url = "api.fabric.microsoft.com"

# Data payload for the new workspace, assigning it to a capacity
payload = {
    "displayName": WORKSPACE_NAME,
    "capacityId": CAPACITY_ID
}

try:
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    print(f"Workspace '{WORKSPACE_NAME}' created successfully.")
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")



NOTE: For information on obtaining the required access token, refer to the --> Fabric API Quickstart guide - https://www.google.com/url?sa=i&source=web&rct=j&url=https://learn.microsoft.com/en-us/rest/api/fabric/articles/get-started/fabric-api-quickstart&ved=2ahUKEwilk5SO096RAxVFF2IAHdtuI4wQy_kOegQIChAB&opi=89978449&cd&psig=AOvVaw3FR46T0uP1ab8QTQ9fU_fB&ust=1766955176192000

/// KQL and SQL
KQL and SQL are declarative query languages used to interact with data within specific Fabric items (KQL databases or Data Warehouses). They are not designed for managing core administrative workspace settings like capacity assignment, access control, or general configuration. 

- KQL Example (reading data in a Notebook):


%%kusto
# Replace <yourKQLdatabaseURI> and <tablename>
let kustoQuery = "['<tablename>'] | take 10"; 
let kustoUri = "https://<yourKQLdatabaseURI>.kusto.data.microsoft.com"; 
let database = "DocsDatabase"; 
# The actual configuration is done in the UI or via connection string/magic commands



- SQL Example (querying a Data Warehouse in a Notebook):

%%sql -artifact <databasename> -type SQLDatabase
SELECT * FROM SalesLT.Customer LIMIT 10;




