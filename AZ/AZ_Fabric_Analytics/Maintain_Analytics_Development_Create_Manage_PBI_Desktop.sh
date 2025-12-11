# // Create and manage a Power BI Desktop project (.pbip) 


#The .pbip format is a file-based representation of a Power BI project that enables source control integration by saving components (reports, datasets) as readable JSON and other text files. This is done within Power BI Desktop via the Save as option. 

# Management (Git command line examples on local machine):
# After saving as a .pbip project in Power BI Desktop, you use standard Git commands to manage the files on your local machine and push them to a remote repository:


# Initialize a local Git repository:

git init

# Stage changes (e.g., the report.json and definition.json files):

git add .


# Commit changes:

git commit -m "Initial commit of Power BI project files"


# Push to a remote repository (e.g., Azure DevOps or GitHub):

git remote add origin <remote_repo_url>
git push -u origin main




//# Create and Open a .pbip Project

To Create (Convert from .pbix)
	1. Open your existing .pbix file in Power BI Desktop.
	2. Go to File > Save as.
	3. In the "Save As" dialog, choose Power BI project files (*.pbip) as the file type.
	4. Select a folder location and save. 
This action creates a folder containing several files and subfolders, including:

	- <project_name>.Report folder: Contains report definition files (e.g., definition.pbir, report.json).
	- <project_name>.Dataset folder: Contains dataset definition files (e.g., model.bim, which is a Tabular Model Definition Language (TMDL) file).
	- <project_name>.pbip file: A small JSON file that acts as a pointer to the report and dataset folders. 

   # An example of the content within a simple <project_name>.pbip file looks like this: 


{
  "version": "1.0",
  "artifacts": [
    {
      "report": {
        "path": "YourProjectName.Report"
      }
    }
  ],
  "settings": {
    "enableAutoRecovery": true
  }
}





