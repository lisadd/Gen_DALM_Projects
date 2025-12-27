Configuring Microsoft Fabric domain and workspace settings is primarily performed through the Fabric Admin portal UI or the Microsoft Fabric REST APIs, as there are no direct KQL, SQL, or specific Python SDK commands for these administrative actions within a notebook environment. The available APIs often require a Python script to make the necessary HTTP requests. 

// Configuration via the Admin Portal (UI) 

The standard and most common method is using the web interface: 

 1. Sign in to Microsoft Fabric as a Fabric admin.
 2. Navigate to the Admin portal.
 3. Select the Domains tab to manage domains or the Workspaces tab to manage specific workspace settings (such as assigning a workspace to a domain, managing Spark settings, or configuring network security).
 4. Within the relevant settings page, you can define data classification, assign roles, manage access, and configure other domain or workspace-specific properties. 

// Configuration via REST API (Python Example) 
For automation or programmatic management, you can use the Microsoft Fabric REST APIs. This involves making authenticated HTTP requests using a language like Python. The examples below show how to get an access token and then use an API to set a workspace domain. 

/// Prerequisites for API Usage:
- A Microsoft Entra ID (Azure AD) application with service principal enabled for Admin APIs.
- The Client ID, Tenant ID, and Client Secret of the registered application.
- The Fabric Admin tenant settings must allow service principals to access admin APIs. 


/// Python Example: Assigning a Workspace to a Domain:

This Python code snippet uses the requests library to assign a specific workspace to a domain using the Fabric REST API. 


import requests
import json

# --- Configuration Variables ---
# Replace with your actual IDs and secret
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
TENANT_ID = "YOUR_TENANT_ID"
WORKSPACE_ID = "YOUR_WORKSPACE_ID" # The GUID of the workspace
DOMAIN_ID = "YOUR_DOMAIN_ID"       # The GUID of the domain

# The API endpoint URL for assigning a domain to a workspace
url = f"https://api.fabric.microsoft.com/v1/workspaces/{WORKSPACE_ID}/domain"

# --- Authentication: Get an access token ---
# The resource URL for Fabric management APIs
authority_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
scope = "api.fabric.microsoft.com"

payload = {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'scope': scope
}

# Request the token
token_response = requests.post(authority_url, data=payload)
token_response.raise_for_status()
access_token = token_response.json().get("access_token")

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# --- API Call: Assign the domain ---
# The body of the request containing the domain ID to assign
data = {
    "domainId": DOMAIN_ID
}

# Make the PATCH request to assign the domain
response = requests.patch(url, data=json.dumps(data), headers=headers)

# Check the response status
if response.status_code == 200 or response.status_code == 204:
    print(f"Successfully assigned workspace {WORKSPACE_ID} to domain {DOMAIN_ID}.")
elif response.status_code == 404:
    print("Error: Workspace or domain not found. Check your IDs.")
elif response.status_code == 403:
    print("Error: Forbidden. Check your service principal permissions and tenant settings.")
else:
    print(f"An error occurred: {response.status_code} - {response.text}")


Reference: https://community.fabric.microsoft.com/t5/Service/Setting-workspace-domain-via-API/td-p/3276128&ved=2ahUKEwizzvLd1N6RAxX1FmIAHUWyNoUQy_kOegQIDBAB&opi=89978449&cd&psig=AOvVaw3nM3Hf2Mes5pj9Wf-X2caG&ust=1766955611850000


