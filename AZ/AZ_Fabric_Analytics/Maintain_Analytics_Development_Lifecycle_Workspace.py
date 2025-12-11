# // Maintain the analytics development lifecycle:

#Maintaining the lifecycle involves best practices, such as using parameters for environment-specific configurations and using separate workspaces for different stages (development, test, production). Code snippets relate to parameterizing items like notebooks to work across stages. 


# PySpark Code (in a Fabric Notebook) for Parameterization:

# Example of using a parameter for the default lakehouse name,
# which can be changed by a deployment rule.

# Assume a 'target_lakehouse_name' parameter is defined in the notebook/environment
# and configured via deployment pipeline rules.
try:
    target_lakehouse_name = mssparkutils.env.get झीलParam("target_lakehouse_name")
except:
    # Default to 'DevelopmentLakehouse' if no parameter is provided (e.g., local dev)
    target_lakehouse_name = "DevelopmentLakehouse"

print(f"Using lakehouse: {target_lakehouse_name}")

# Mount the lakehouse using the variable
mssparkutils.fs.mount(
    f"abfss://{target_lakehouse_name}@onelake.info.fabric.microsoft.com",
    f"/lakehouse/{target_lakehouse_name}"
)

# Use the mounted path in subsequent PySpark operations
df = spark.read.format("delta").load(f"/lakehouse/{target_lakehouse_name}/Tables/MyTableName")
df.show()



# // Configure Version Control for Workspace:

# Version control (Git integration) is primarily configured through the Workspace settings UI in the Fabric portal. Once configured, changes can be committed and synced to an Azure DevOps or GitHub repository.
 
# While the configuration is a UI task, automation can be achieved using the Fabric REST APIs. The following is a conceptual example of how you might use a Python script with the fabric_cicd SDK to connect to a Git repository, as part of an automated setup: 


# This is a conceptual Python example using the fabric_cicd library for automation.
# The actual script runs within an Azure Pipeline and requires specific authentication setup.
import os
from azure.identity import DefaultAzureCredential
from fabric_cicd import GitConnection

# Assumes environment variables are set for authentication and workspace details
workspace_id = os.environ["WORKSPACE_ID"]
repo_url = "dev.azure.com"
branch_name = "main"
folder_path = "/" # The folder in the repo to sync with the workspace

# Authenticate
credential = DefaultAzureCredential()

# Connect to Git using the API/SDK
git_connection = GitConnection(
    workspace_id=workspace_id,
    remote_repo_url=repo_url,
    branch=branch_name,
    folder=folder_path,
    token_credential=credential
)

# Call the connect and sync method (abstracted by the SDK)
# git_connection.connect_and_sync()
print(f"Workspace {workspace_id} configured for Git integration with {repo_url} on branch {branch_name}")




