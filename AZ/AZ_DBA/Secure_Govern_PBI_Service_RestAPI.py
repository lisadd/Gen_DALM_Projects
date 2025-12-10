
/*  Securing and governing Power BI items with Python, particularly for advanced features like row-level security (RLS) and sensitivity labels, primarily involves interacting with the Power BI Service REST API. While Power BI Desktop handles the initial setup of RLS roles and sensitivity labels, Python can be used to automate the assignment of users to these roles and the application of labels at scale.
*/


#Prerequisites:  You must have an Azure AD app registration (Service Principal), client ID, tenant ID, and client secret, and grant the necessary API permissions in Azure AD and the Power BI Admin portal.



# Install Prereqs:

pip install msal requests



# 1. Implementing Row-Level Security (RLS) Roles (Power BI Desktop): RLS roles are defined within Power BI Desktop. This is a manual process within the modeling tab.

#Example A:
// Example DAX filter for a role named "SalesManagers"
// This filter assumes a 'Region' column in your 'Sales' table
[Region] = "East" || [Region] = "West"


#Example B:

import msal
import requests
import json

# Configuration
TENANT_ID = "YOUR_TENANT_ID"
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
AUTHORITY_URL = f"login.microsoftonline.com{TENANT_ID}"
SCOPE = ["analysis.windows.net"] # Scope for Power BI Service
API_URL = "api.powerbi.com"

# Acquire token
app = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY_URL, client_credential=CLIENT_SECRET)
result = app.acquire_token_for_client(scopes=SCOPE)

if "access_token" in result:
    access_token = result["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    print("Authentication successful.")
else:
    raise Exception(f"Authentication failed: {result.get('error_description', 'No token found')}")



# 2. Assigning Workspace Roles (Power BI Service via Python): You can use the Power BI Service REST API to manage workspace roles. This requires authentication and understanding of the API endpoints.

#Example A: 


import requests
import json

# Replace with your Power BI Service details and access token
POWER_BI_API_URL = "https://api.powerbi.com/v1.0/myorg"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN" # Obtain this via Azure AD authentication
WORKSPACE_ID = "YOUR_WORKSPACE_ID"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Example: Add a user to a workspace as a 'Member'
user_email = "user@example.com"
role = "Member"

add_user_payload = {
    "identifier": user_email,
    "principalType": "User",
    "groupUserAccessRight": role
}

response = requests.post(f"{POWER_BI_API_URL}/groups/{WORKSPACE_ID}/users", headers=headers, data=json.dumps(add_user_payload))

if response.status_code == 200:
    print(f"User {user_email} added to workspace as {role}")
else:
    print(f"Error adding user: {response.text}")



#Example B:

def assign_workspace_role(workspace_id, principal_id, role="Viewer"):
    """
    Assigns a specified role to a principal (user/group) in a workspace.
    Principal ID can be user UPN or security group ID.
    """
    endpoint = f"{API_URL}/admin/workspaces/{workspace_id}/users"
    payload = {
        "principalType": "User", # Or "Group"
        "principalId": principal_id,
        "role": role # e.g., "Admin", "Member", "Contributor", "Viewer"
    }
    # Note: Using the Admin API requires Fabric Administrator privileges
    response = requests.post(endpoint, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"Successfully assigned role '{role}' to {principal_id} in workspace {workspace_id}.")
    else:
        print(f"Failed to assign role: {response.content}")
    # Call the refresh user permissions API afterwards for immediate effect
    requests.post(f"{API_URL}/RefreshUserPermissions", headers=headers)

# Example usage:
# assign_workspace_role("YOUR_WORKSPACE_ID", "USER_PRINCIPAL_NAME_OR_GROUP_ID", "Member")




# 3. Configuring Item-Level Access and Access to Semantic Models (Power BI Service via Python): Similar to workspace roles, you can manage access to specific reports, dashboards, and semantic models using the Power BI Service REST API.

# Example A: Grant 'Read' access to a report for a user
REPORT_ID = "YOUR_REPORT_ID"
grant_access_payload = {
    "identifier": user_email,
    "principalType": "User",
    "datasetUserAccessRight": "Read" # Or "ReadWrite", "Reshare" etc.
}

response = requests.post(f"{POWER_BI_API_URL}/reports/{REPORT_ID}/users", headers=headers, data=json.dumps(grant_access_payload))

if response.status_code == 200:
    print(f"User {user_email} granted 'Read' access to report {REPORT_ID}")
else:
    print(f"Error granting report access: {response.text}")



# Example B: Adds user access to a specific semantic model.

def add_semantic_model_user(workspace_id, semantic_model_id, user_email, access_right="Read"):
    """
    Grants specific access rights to a user for a semantic model.
    Access Rights: Read, ReadWrite, ReadExplore, ReadWriteExplore, Reshare, Owner.
    """
    endpoint = f"{API_URL}/workspaces/{workspace_id}/datasets/{semantic_model_id}/users"
    payload = {
        "grantTo": "Users",
        "members": [
            {
                "id": user_email,
                "principalType": "User"
            }
        ],
        "accessRights": [access_right]
    }
    response = requests.post(endpoint, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"Granted '{access_right}' access to {user_email} for semantic model {semantic_model_id}.")
    else:
        print(f"Failed to grant semantic model access: {response.content}")

# Example usage:
# add_semantic_model_user("YOUR_WORKSPACE_ID", "YOUR_DATASET_ID", "user@example.com", "ReadWrite")




# 4. Configuring Row-Level Security Group Membership (Power BI Service via Python): After defining RLS roles in Power BI Desktop, you assign users or security groups to these roles in the Power BI Service. Python can automate this assignment for semantic models.


def add_rls_group_member(workspace_id, semantic_model_id, role_name, principal_id):
    """
    Adds a user or security group to a pre-defined RLS role in a published semantic model.
    """
    endpoint = f"{API_URL}/workspaces/{workspace_id}/datasets/{semantic_model_id}/users"
    payload = {
        "principalType": "User", # Or "Group"
        "principalId": principal_id,
        "role": role_name
    }
    # This uses a different endpoint for RLS role assignments
    rls_endpoint = f"{API_URL}/datasets/{semantic_model_id}/security/rls"

    response = requests.post(rls_endpoint, headers=headers, json=payload)

    # The documentation for this API call is likely within specific SDKs or Admin APIs.
    # The general REST API documentation might have a different method.
    # A known correct endpoint is for *adding* group users to a dataset security role:
    endpoint_add_group_user = f"{API_URL}/datasets/{semantic_model_id}/AddGroupUser"
    payload_add_group_user = {
        "groupOrUser": principal_id,
        "roleName": role_name
    }

    response = requests.post(endpoint_add_group_user, headers=headers, json=payload_add_group_user)
    if response.status_code == 200:
        print(f"Added {principal_id} to RLS role '{role_name}' for semantic model {semantic_model_id}.")
    else:
        print(f"Failed to add RLS member: {response.content}")

# Example usage (Ensure 'SalesRole' is a role defined in your PBIX file):
# add_rls_group_member("YOUR_WORKSPACE_ID", "YOUR_DATASET_ID", "SalesRole", "sales_group_id")



# 5. Applying Sensitivity Labels (Microsoft Purview Information Protection SDK): Applying sensitivity labels programmatically requires interaction with Microsoft Purview Information Protection SDK, not directly with the Power BI Service REST API. This involves using the SDK to interact with the Microsoft Information Protection (MIP) service to apply labels to Power BI items.

### The user must be a Fabric Admin to use these admin APIs, and the label ID used must be part of their label policy


def set_sensitivity_label(item_type, item_id, label_id):
    """
    Applies a sensitivity label to a Power BI item (e.g., Report, Dashboard, Dataset).
    Requires Fabric Admin role and Tenant.ReadWrite.All scope.
    """
    # Item type can be 'reports', 'dashboards', 'datasets', etc.
    # Note: This is an Admin API endpoint.
    endpoint = f"{API_URL}/admin/InformationProtection/SetLabelsAsAdmin"
    payload = {
        "label": {
            "labelId": label_id
        },
        "artifacts": [
            {
                "artifactId": item_id,
                "artifactType": item_type
            }
        ]
    }
    response = requests.post(endpoint, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"Successfully applied sensitivity label {label_id} to {item_type} {item_id}.")
    else:
        print(f"Failed to apply label: {response.content}")

# Example usage:
# set_sensitivity_label("Report", "YOUR_REPORT_GUID", "YOUR_SENSITIVITY_LABEL_GUID")



