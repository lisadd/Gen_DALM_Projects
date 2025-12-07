# 3. Publish, Import, or Update Items in a Workspace (Reports, Datasets - via Power BI REST API with Python)

def publish_pbix_to_workspace(workspace_id, pbix_file_path, dataset_display_name):
    url = f"{API_BASE_URL}/groups/{workspace_id}/imports?datasetDisplayName={dataset_display_name}"
    with open(pbix_file_path, 'rb') as f:
        files = {'file': (pbix_file_path, f, 'application/octet-stream')}
        response = requests.post(url, headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}, files=files)
    response.raise_for_status()
    print(f"PBIX file '{pbix_file_path}' published to workspace {workspace_id}: {response.json()}")

# Example usage:
# publish_pbix_to_workspace(workspace_id, "my_report.pbix", "My Report Dataset")



