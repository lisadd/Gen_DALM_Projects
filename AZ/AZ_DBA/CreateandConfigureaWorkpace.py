Use Python to interact with the Power BI REST API to manage workspaces and assets. This requires using libraries like requests to make HTTP calls to the API endpoints.

# 1. Create and Configure a Workspace (via Power BI REST API with Python)

import requests
import json

# Replace with your Power BI tenant and credentials/token
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"  # Obtain this via Azure AD app registration
API_BASE_URL = "https://api.powerbi.com/v1.0/myorg"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def create_workspace(name, description):
    url = f"{API_BASE_URL}/groups"
    payload = {
        "name": name,
        "description": description
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    print(f"Workspace '{name}' created successfully: {response.json()}")
    return response.json()["id"]

# Example usage:
# workspace_id = create_workspace("My New Python Workspace", "Workspace created via Python API")

