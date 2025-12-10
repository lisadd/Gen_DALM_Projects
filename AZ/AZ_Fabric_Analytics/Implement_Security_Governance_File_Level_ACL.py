# Azure SDK (Python) example demonstrating how to manage file-level permissions (ACLs) within Azure Data Lake Storage Gen2.This example focuses on setting and retrieving ACLs for a specific file.


from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient

# --- Configuration ---
storage_account_name = "yourdlgen2account"  # Replace with your ADLS Gen2 account name
filesystem_name = "yourfilesystem"        # Replace with your filesystem name
file_name = "yourfile.txt"                # Replace with the target file name

# --- Authentication ---
# Authenticate using DefaultAzureCredential (recommended for production)
# This will try various credential types, including environment variables,
# managed identity, and Azure CLI.
credential = DefaultAzureCredential()

# Construct the DataLakeServiceClient
account_url = f"https://{storage_account_name}.dfs.core.windows.net"
service_client = DataLakeServiceClient(account_url, credential=credential)

# --- ACL Operations ---

try:
    # Get a file client
    file_client = service_client.get_file_client(filesystem_name, file_name)

    # 1. Get current ACLs for the file
    print(f"Getting ACLs for file: {file_name}")
    acl_properties = file_client.get_access_control()
    print("Current ACLs:")
    print(f"  Owner: {acl_properties.owner}")
    print(f"  Group: {acl_properties.group}")
    print(f"  ACL: {acl_properties.acl}")

    # 2. Set new ACLs for the file
    # Example: Grant read, write, and execute to owning user,
    # read and execute to owning group, and read to others.
    new_acl = "user::rwx,group::rx,other::r"
    print(f"\nSetting new ACLs for file to: {new_acl}")
    file_client.set_access_control(acl=new_acl)
    print("ACLs updated successfully.")

    # 3. Verify the updated ACLs
    print(f"\nVerifying updated ACLs for file: {file_name}")
    acl_properties_after_update = file_client.get_access_control()
    print("Updated ACLs:")
    print(f"  ACL: {acl_properties_after_update.acl}")

except Exception as e:
    print(f"An error occurred: {e}")



