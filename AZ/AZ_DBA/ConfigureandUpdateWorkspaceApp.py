# 2. Configure and Update a Workspace App (via Power BI REST API with Python)

def publish_app(workspace_id, app_name, app_description):
    url = f"{API_BASE_URL}/groups/{workspace_id}/PublishApp"
    payload = {
        "appProfile": {
            "name": app_name,
            "description": app_description,
            # Add more app settings as needed
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    print(f"App '{app_name}' published for workspace {workspace_id}: {response.json()}")

# Example usage:
# publish_app(workspace_id, "My Python App", "App published from Python workspace")



