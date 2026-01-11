In Microsoft Fabric, streaming data is primarily handled through the Eventstream feature and processed using the built-in, no-code event processor, or with Python/Spark Structured Streaming and KQL for more complex scenarios. 

// Choose an Appropriate Streaming Engine

The choice of streaming engine depends on your needs: 

- Microsoft Fabric Eventstream (No-Code Editor): Best for simple ingestion, basic transformations (filtering, managing fields, basic aggregation), and routing to destinations like a KQL database or Lakehouse. It offers a user-friendly, drag-and-drop interface.

- KQL (Kusto Query Language) in a KQL Database: Ideal for advanced, real-time analytics, complex event processing (CEP), and implementing automated transformation via update policies within the database itself.

- Apache Spark (via Fabric Notebooks): Use for complex data transformations, machine learning pipelines on streaming data, and large-scale, deep integration with Delta Lake. This approach uses Python/Scala/SQL code within a notebook environment.
- Azure Stream Analytics: A fully managed external service for real-time analytics with a SQL-based query language, suitable for simple processing tasks where a dedicated, external managed solution is preferred. 


// Ingest and Transform Streaming Data 
The following steps and examples demonstrate the common methods using Fabric Eventstream and KQL.

///Step 1: Ingest Data via Eventstream (UI-based)
1. Create an Eventstream: In your Fabric workspace, navigate to the Real-Time Intelligence experience and create a new Eventstream item.

2. Add a Source: In the eventstream editor, select Get Data or Add source. Choose your source (e.g., Azure Event Hubs, Custom App, Sample data).

3.Configure Source: Follow the prompts to provide connection details and credentials. This process creates a data stream in your Real-Time hub.

4. Define Transformations (No-Code): Use the event processor editor (drag-and-drop interface) to apply built-in transformations like Filter, Manage fields, or Aggregate as needed.

5. Add a Destination: Select Add destination (e.g., KQL Database, Lakehouse). Configure the destination table and ingestion mode (direct or with processing).

6. Publish: Save and publish the eventstream to start the flow. 

// Step 2: Transform Data with KQL Update Policy (KQL Example)
Once data is in a KQL database "SourceTable", an update policy can automatically transform and save it to a "TransformedTable". 


// Create the target table (TransformedTable)
.create table TransformedTable (Timestamp:datetime, StationID:string, BikeCount:long)

// Define a function with the transformation logic
.create function with (docstring = "Calculates bike counts", folder = "MyFunctions")
 fn_transform_bicycles() {
    SourceTable
    | where Timestamp > ago(1h) // Example: filter recent data
    | summarize BikeCount = count() by StationID, bin(Timestamp, 15m) // Example: aggregate by station and time window
    | project Timestamp, StationID, BikeCount
}

// Apply an update policy to the source table to trigger the function
.alter table SourceTable policy update 
 @'[{"IsEnabled": true, "Source": "SourceTable", "Target": "TransformedTable", "Query": "fn_transform_bicycles()", "Is and to source": false, "CreationTime": "2025-01-01T00:00:00Z"}]'



// Step 3: Ingest and Transform with Python (Code Example - Producer) 

For code-based ingestion, you can use Python client libraries (e.g., azure-eventhub) to act as a data producer to the Eventstream's custom endpoint. Transformations can be done within the Python code before sending or using Spark Structured Streaming in a Fabric Notebook. 

Python Producer Example (sends data to Eventstream):
You will need an Eventstream connection string from the "Custom app" source details in Fabric. 

import time
import json
import asyncio
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData

# Eventstream connection string and name (replace with your details)
EVENTHUB_CONNECTION_STR = "Endpoint=sb://<your_namespace>.eventhub.windows.net/..."
EVENTHUB_NAME = "<your_eventstream_name>"

async def run():
    producer = EventHubProducerClient.from_connection_string(
        conn_str=EVENTHUB_CONNECTION_STR,
        eventhub_name=EVENTHUB_NAME
    )
    async with producer:
        while True:
            # Example data (replace with your actual data source logic)
            data = {
                "id": time.time(),
                "value": "sample_data",
                "timestamp": str(datetime.now())
            }
            event_data = EventData(json.dumps(data))
            await producer.send_batch([event_data])
            print(f"Sent event: {data}")
            await asyncio.sleep(5) # Send every 5 seconds

if __name__ == "__main__":
    from datetime import datetime
    asyncio.run(run())



The data is then ingested into Fabric, where you can apply further transformations using the methods mentioned above. 

// Step 4: Query Streaming Data with SQL or KQL

Once the data lands in a KQL database table, you can query it using KQL or T-SQL (via the KQL queryset). 
KQL Query Example:

TransformedTable
| where BikeCount > 10
| project StationID, BikeCount, Timestamp
| render timechart 



// SQL Query Example (in a KQL Queryset set to T-SQL mode):

SELECT
    StationID,
    BikeCount,
    Timestamp
FROM
    TransformedTable
WHERE
    BikeCount > 10;

