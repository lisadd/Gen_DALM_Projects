### 
1. Connecting to a Power BI Semantic Model in Power BI Desktop (Live Connection):
This is not a code sample but a procedural description as Power BI Desktop provides a user interface for this. 

Open Power BI Desktop.
Select "Get Data" > "Power BI semantic models."
Browse and select the desired semantic model from your workspaces.
Choose "Connect live" to establish a live connection, allowing you to build reports without importing data. ###

###
EXAMPLE 1 Sample Code: Connecting to Azure SQL Database using Python (pyodbc):
This code sample demonstrates connecting to an Azure SQL Database from Python using the pyodbc library. ### 

import pyodbc

try:
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=your_server_name.database.windows.net;'
        'DATABASE=your_database_name;'
        'UID=your_username;'
        'PWD=your_password'
    )
    cursor = cnxn.cursor()
    cursor.execute("SELECT @@SERVERNAME")
    row = cursor.fetchone()
    if row:
        print(f"Successfully connected to: {row[0]}")
    else:
        print("Connection successful, but could not retrieve server name.")

except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print(f"Error connecting to Azure SQL Database: {sqlstate}")

finally:
    if 'cnxn' in locals() and cnxn:
        cnxn.close()

