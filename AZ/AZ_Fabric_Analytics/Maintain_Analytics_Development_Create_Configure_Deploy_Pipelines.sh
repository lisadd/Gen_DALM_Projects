# //Create and configure deployment pipelines:

# Deployment pipelines are configured in the Fabric Portal UI to manage the promotion of content between stages (Development, Test, Production). 

# Automation of pipeline configuration can be done using the Fabric REST APIs, such as the Create deployment pipeline API call. The following is a conceptual curl command example to create a pipeline: 


# REST API Example (conceptual curl command):


curl -X POST "api.fabric.microsoft.com{workspaceId}/deploymentPipelines" \
-H "Authorization: Bearer <your_PAT_token>" \
-H "Content-Type: application/json" \
-d '{
  "displayName": "MyAnalyticsPipeline",
  "description": "Pipeline for my analytics project",
  "stages": [
    {"stageId": "1", "displayName": "Development"},
    {"stageId": "2", "displayName": "Test"},
    {"stageId": "3", "displayName": "Production"}
  ]
}'



# Once the pipeline is created and workspaces are assigned in the UI, you can use the APIs to deploy content. You can also define deployment rules for specific items (like changing a notebook's default lakehouse connection for the Test environment) within the UI. 


/*

In Microsoft Fabric, deployment pipelines provide a simple, wizard-driven user interface for managing the development life cycle of SQL database items and PySpark notebooks through development, test, and production stages. 

Prerequisites
An existing Fabric capacity.
At least two Fabric workspaces (e.g., "Dev" and "Test"), with content (SQL databases, notebooks) to manage.
Admin access to the workspaces. 

Step-by-Step Guide
// 1. Create a Deployment Pipeline
You can create a pipeline from the global Fabric interface or directly from an existing workspace. 
- From the Workspaces flyout menu, select Deployment pipelines.
- Select Create pipeline or + New pipeline.
- Enter a Name and optional Description for the pipeline.
- Define the number and names of your stages (e.g., Development, Test, Production). You must have at least two stages and a maximum of ten.

Select Create or Create and continue. 


// 2. Assign Workspaces to Stages
Link your actual Fabric workspaces to the defined pipeline stages. 
- In a pipeline stage (e.g., "Development"), select Assign a workspace.
- Choose the desired workspace from the list and select Assign.
- Repeat this process for your other stages (e.g., assign "Test" workspace to "Test" stage). 


// 3. Deploy Content
Once workspaces are assigned, you can deploy items (SQL databases, notebooks, etc.) from an earlier stage to a later stage. 
- In the source stage (e.g., Development), select the Deploy button (usually a forward arrow icon) to move content to the next stage (e.g., Test).
- You can choose between a Full deployment or Selective deployment (choose specific items).
- Review the deployment summary and add an optional note.
- Select Deploy. Fabric calculates the necessary T-SQL to update the target database to match the source's desired state. 


// 4. Configure Deployment Rules (Optional but Recommended) 
Deployment rules allow you to parameterize settings, such as connecting notebooks to a different Lakehouse in the target environment, without changing the code itself. 
- Before deploying, select Deployment rules next to the target stage.
- For PySpark notebooks or Spark Job Definitions, you can set rules to overwrite the default Lakehouse binding.
- Specify the target Lakehouse using one of the available options (e.g., "other Lakehouse"). 


// 5. Monitor and Iterate
After deployment, you can view the deployment history and compare content between stages to see differences (indicated by a badge icon). As you make changes in your development workspace, the pipeline will show that items have changed, allowing you to trigger subsequent deployments. 
For more advanced CI/CD, you can also integrate your Fabric workspace with Git (Azure DevOps or GitHub) to manage source control alongside the deployment pipelines.  

*/
