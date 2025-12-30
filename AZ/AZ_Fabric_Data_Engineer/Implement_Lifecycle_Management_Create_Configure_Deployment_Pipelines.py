Implementing lifecycle management in Microsoft Fabric involves a combination of manual setup in the Fabric UI and automation via the Fabric REST APIs, which can be invoked using Python or PowerShell.


// Steps to Create and Configure Deployment Pipelines:
The initial setup is done in the Microsoft Fabric user interface. 


  1. Create Workspaces: In the Fabric UI, create separate workspaces for each stage of your lifecycle (e.g., Development, Test, Production). Ensure they are assigned to a Fabric Premium capacity.
  2. Create the Deployment Pipeline:
    - Navigate to the Deployment pipelines section in Fabric.
    - Select Create pipeline.
    - Name the pipeline and optionally add a description.
    - Define your stages (2 to 10 allowed). The default are Development, Test, and Production, which is a common practice.
  3. Assign Workspaces to Stages:
    - For each stage in the newly created pipeline, select Assign workspace.
    - Choose the corresponding workspace you created earlier (e.g., assign the 'Dev' workspace to the Development stage). A workspace can only be in one pipeline at a time.
  4. Develop and Deploy Content:
    - Develop your Fabric items (Lakehouse, Notebooks, Data Pipelines, etc.) in the Development workspace.
    - Once ready, select the Deploy button (a lightning bolt icon) at the top of the Development stage to move content to the Test stage. You can choose a full or selective deployment.
    - Repeat the deployment process from Test to Production after validation.

  5. Configure Deployment Rules (Optional):
   - Set specific configurations (like different database connections or parameters for data sources) that vary between stages using deployment rules. This ensures credentials or server names don't need manual changes during deployment. 


// Example Python Code for Automation:
  - For programmatic automation  (e.g., integrating with Azure DevOps or GitHub Actions), you can use the Fabric REST APIs. The example below uses a service principal for authentication and the requests library to trigger a deployment. 

  - This example assumes you have an Azure AD service principal with the necessary permissions and the requests Python library installed (pip install requests):

import requests
import json

# Configuration variables
TENANT_ID = "YOUR_TENANT_ID"
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
PIPELINE_ID = "YOUR_PIPELINE_ID"
SOURCE_STAGE_ID = "YOUR_SOURCE_STAGE_ID" # e.g., 'Development' stage ID
TARGET_STAGE_ID = "YOUR_TARGET_STAGE_ID" # e.g., 'Test' stage ID

# 1. Authenticate and get an access token
def get_access_token(tenant_id, client_id, client_secret):
    authority_url = f"login.microsoftonline.com{tenant_id}/oauth2/v2.0/token"
    scope = "api.fabric.microsoft.com"
    payload = {
        'client_id': client_id,
        'scope': scope,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    response = requests.post(authority_url, data=payload)
    response.raise_for_status()
    return response.json()['access_token']

# 2. Deploy content using the Fabric REST API
def deploy_pipeline_stage(token, pipeline_id, source_stage_id, target_stage_id, deployment_note="Automated deployment"):
    deploy_url = f"api.fabric.microsoft.com{pipeline_id}/deploy"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = {
        'sourceStageId': source_stage_id,
        'targetStageId': target_stage_id,
        'options': {
            'note': deployment_note
        }
    }
    
    response = requests.post(deploy_url, data=json.dumps(payload), headers=headers)
    response.raise_for_status()
    print(f"Deployment initiated successfully with status code: {response.status_code}")
    # You might need to poll a different endpoint to check the deployment status

# Main execution
if __name__ == "__main__":
    try:
        token = get_access_token(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
        print("Access token obtained successfully.")
        
        # Deploy from Development (Source Stage) to Test (Target Stage)
        deploy_pipeline_stage(token, PIPELINE_ID, SOURCE_STAGE_ID, TARGET_STAGE_ID, "Deploying latest dev changes to Test environment")
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


Reference: Automate deployment pipeline by using Fabric APIs (https://learn.microsoft.com/en-us/fabric/cicd/deployment-pipelines/pipeline-automation-fabric)
