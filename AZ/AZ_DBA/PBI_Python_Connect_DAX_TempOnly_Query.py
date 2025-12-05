# You need to install the necessary library: 

pip install pyadomd pandas


## Python Example Code (using pyadomd)
## This code connects to a Power BI dataset (or AAS model) and executes a DAX query that uses DEFINE MEASURE to create a temporary calculation for that specific query execution. 

import pandas as pd
from pyadomd import Pyadomd

# Connection details
SERVER = "powerbi://api.powerbi.com"
DATASET_NAME = "YourDatasetName"
CONN_STR = f'Provider=MSOLAP;Data Source={SERVER};Initial Catalog={DATASET_NAME};Integrated Security=SSPI;'

DAX_QUERY = """
DEFINE MEASURE 'Sales'[Total Sales] = SUM(Sales[Sales Amount])
EVALUATE
SUMMARIZECOLUMNS
(
    'Date'[Calendar Year],
    "Sum of Sales", 'Sales'[Total Sales]
)
"""

try:
    with Pyadomd(CONN_STR) as conn:
        with conn.cursor().execute(DAX_QUERY) as cur:
            df = pd.DataFrame(cur.fetchall(), columns=[i.name.split('[')[-1].split(']')[0] for i in cur.description])
            print(df.head())

except Exception as e:
    print(f"An error occurred: {e}")




