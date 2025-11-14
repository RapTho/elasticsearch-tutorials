# DIY Elasticsearch

Now it's your turn to use what you practiced before. Can you solve all the challenges below?

### Exercise 1: Creating an API Key

**Objective:** Learn to create and manage API keys for secure API interactions.

#### Tasks:

1. **Introduction to API Keys:**

   - Discuss the importance of API keys for security.
   - Review the documentation on Elasticsearch API keys.
   - Introduction to `curl` syntax and options.

2. **Create an API Key:**

   - [Generate an API key](https://www.elastic.co/guide/en/kibana/8.15/api-keys.html) using the Kibana console or API.
   - Securely save the API key for future use.

3. **Validation:**
   - Validate the API key by making a simple API call using a `curl` to list indexes or get cluster health. Check [how to authenticate](https://www.elastic.co/guide/en/elasticsearch/reference/current/http-clients.html) towards the Elasticsearch API using API Keys.

### Exercise 2: Using curl to interact with the Elasticsearch API

**Objective:** Master the use of `curl` for Elasticsearch API interactions.

#### Tasks:

1. Set the `KIBANA_USERNAME` environment variable in your shell:

**macOS/Linux:**

```bash
export KIBANA_USERNAME="your_username_here"
```

**Windows PowerShell:**

```powershell
$env:KIBANA_USERNAME="your_username_here"
```

2. Create a new index called `${KIBANA_USERNAME}-bicycle_products` with an explicit mapping that satisfies the following field / type criteria:

- Name = text
- Price = float
- Production Date = date of format `strict_date_optional_time` or `epoch_millis`
- Available = true
- Category = keyword
- Parts = Array of text

**Windows user only**:
If you face issues with your `curl` requests, check the [troubleshooting section](#troubleshooting-curl-on-windows)

3. Add data to the newly created index using a [bulk request](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html) to the `${KIBANA_USERNAME}-bicycle_products/_bulk` endpoint.

**IMPORTANT:** Replace `${KIBANA_USERNAME}` with your actual username in the endpoint URL, or use the `KIBANA_USERNAME` shell variable as described above.

**Hint: for curl:** Save the data above to a file (e.g., `bulk_data.json`) and use the `--data-binary` flag.

```
{ "index" : { "_id" : "1" } }
{ "Name": "Speedster Road Bike", "Price": 850.00, "Production Date": "2024-04-01T00:00:00Z", "Available": false, "Category": "Road Bikes", "Parts": ["frame", "wheels", "brakes"] }
{ "index" : { "_id" : "2" } }
{ "Name": "Mountain King Bicycle", "Price": 1200.00, "Production Date": "2024-04-02T00:00:00Z", "Available": false, "Category": "Mountain Bikes", "Parts": ["suspension", "off-road tires", "chain"] }
{ "index" : { "_id" : "3" } }
{ "Name": "Urban Commuter 3000", "Price": 600.00, "Production Date": "2024-04-03T00:00:00Z", "Available": true, "Category": "City Bikes", "Parts": ["bell", "basket", "lights"] }
{ "index" : { "_id" : "4" } }
{ "Name": "Trailblazer XC 29", "Price": 1100.00, "Production Date": "2024-04-04T00:00:00Z", "Available": true, "Category": "Cross Country", "Parts": ["helmet", "gloves", "handlebar"] }
{ "index" : { "_id" : "5" } }
{ "Name": "Night Rider 500", "Price": 950.00, "Production Date": "2024-04-05T00:00:00Z", "Available": true, "Category": "Hybrid Bikes", "Parts": ["LED lights", "hybrid tires", "comfort seat"] }
{ "index" : { "_id" : "6" } }
{ "Name": "Breeze Leisure Bike", "Price": 500.00, "Production Date": "2024-04-06T00:00:00Z", "Available": false, "Category": "Leisure Bikes", "Parts": ["basket", "wide seat", "cruise handlebars"] }
{ "index" : { "_id" : "7" } }
{ "Name": "Thunder BMX", "Price": 300.00, "Production Date": "2024-04-07T00:00:00Z", "Available": true, "Category": "BMX Bikes", "Parts": ["stunt pegs", "reinforced frame", "BMX handlebar"] }
{ "index" : { "_id" : "8" } }
{ "Name": "Glider 1000 Roadster", "Price": 650.00, "Production Date": "2024-04-08T00:00:00Z", "Available": true, "Category": "Road Bikes", "Parts": ["road tires", "aerodynamic frame", "racing saddle"] }
{ "index" : { "_id" : "9" } }
{ "Name": "Cyclone Mountain Series", "Price": 1350.00, "Production Date": "2024-04-20T00:00:00Z", "Available": true, "Category": "Mountain Bikes", "Parts": ["all-terrain tires", "advanced suspension", "carbon frame"] }
{ "index" : { "_id" : "10" } }
{ "Name": "Ranger Trail Expert", "Price": 1050.00, "Production Date": "2024-04-10T00:00:00Z", "Available": true, "Category": "Mountain Bikes", "Parts": ["shock absorbers", "trail tires", "durable pedals"] }
{ "index" : { "_id" : "11" } }
{ "Name": "City Glide 700", "Price": 670.00, "Production Date": "2024-04-11T00:00:00Z", "Available": false, "Category": "City Bikes", "Parts": ["commuter frame", "mudguards", "chain lock"] }
{ "index" : { "_id" : "12" } }
{ "Name": "Pinnacle Road Ace", "Price": 890.00, "Production Date": "2024-04-12T00:00:00Z", "Available": true, "Category": "Road Bikes", "Parts": ["carbon wheelset", "speedometer", "drop handlebars"] }
{ "index" : { "_id" : "13" } }
{ "Name": "Sunset Cruiser Deluxe", "Price": 550.00, "Production Date": "2024-04-13T00:00:00Z", "Available": true, "Category": "Leisure Bikes", "Parts": ["leather seat", "wide handlebars", "cruiser tires"] }
{ "index" : { "_id" : "14" } }
{ "Name": "Freewheel X2 BMX", "Price": 320.00, "Production Date": "2024-04-14T00:00:00Z", "Available": true, "Category": "BMX Bikes", "Parts": ["freestyle tires", "360-degree rotor", "BMX forks"] }
{ "index" : { "_id" : "15" } }
{ "Name": "ElectroRide E-Bike", "Price": 1400.00, "Production Date": "2024-04-15T00:00:00Z", "Available": true, "Category": "Electric Bikes", "Parts": ["electric motor", "battery pack", "digital display"] }
{ "index" : { "_id" : "16" } }
{ "Name": "Touring Explorer 2000", "Price": 950.00, "Production Date": "2024-04-16T00:00:00Z", "Available": true, "Category": "Touring Bikes", "Parts": ["pannier rack", "touring tires", "comfort saddle"] }
{ "index" : { "_id" : "17" } }
{ "Name": "Trail Blazer XT", "Price": 1300.00, "Production Date": "2024-04-17T00:00:00Z", "Available": true, "Category": "Mountain Bikes", "Parts": ["full suspension", "trail-specific gearing", "aluminum frame"] }
{ "index" : { "_id" : "18" } }
{ "Name": "City Pro Commuter", "Price": 720.00, "Production Date": "2024-04-18T00:00:00Z", "Available": false, "Category": "City Bikes", "Parts": ["urban tires", "fenders", "rear rack"] }
{ "index" : { "_id" : "19" } }
{ "Name": "Rapid Racer 5000", "Price": 1100.00, "Production Date": "2024-04-19T00:00:00Z", "Available": true, "Category": "Road Bikes", "Parts": ["carbon fiber frame", "aero wheels", "performance brakes"] }
{ "index" : { "_id" : "20" } }
{ "Name": "Kids' Adventure 20", "Price": 250.00, "Production Date": "2024-04-20T00:00:00Z", "Available": true, "Category": "Kids' Bikes", "Parts": ["training wheels", "child-friendly grips", "colorful frame"] }
```

4. Make sure the correct data type of each field is enforced by trying to index the following non-compliant document

```
{ "Name": "Racer Bicicletta", "Price": 1.00, "Production Date": "Fake Date", "Available": "maybe", "Category": 200, "Parts": true }
```

And how about the following one with a new field?

```
{ "Name": "Kids' Adventure 20", "NEW": "FIELD", "Price": 250.00, "Production Date": "2024-04-20T00:00:00Z", "Available": true, "Category": "Kids' Bikes", "Parts": ["training wheels", "child-friendly grips", "colorful frame"] }
```

5. Find all bicycles matching the following criteria. There should only be **2**

- Availability = true
- Category = Road Bikes
- Price <= 1000

You might want to check out [bool](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html) and [filter](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-filter-context.html) queries.

### Exercise 3: Use Python to execute queries against Elasticsearch

**Objective:** Execute an Elasticsearch query from a Python script

#### Tasks:

**OPTIONAL:** Use [virtual environments](https://virtualenv.pypa.io/en/latest/user_guide.html)

1. Setup a new Pyhton project and get familiar with the [requests](https://pypi.org/project/requests/) library.
2. Send a query to get the cluster health and print the response

### Exercise 4: Use template Python app to interact with Elasticsearch

**Objective:** Learn how to use Python in combination with Elasticsearch.

#### Tasks:

**OPTIONAL:** Use [virtual environments](https://virtualenv.pypa.io/en/latest/user_guide.html)

**IMPORTANT:** For Python exercises, you'll need to set the `KIBANA_USERNAME` environment variable before running your scripts:

**macOS/Linux:**

```bash
export KIBANA_USERNAME="your_username_here"
```

**Windows PowerShell:**

```powershell
$env:KIBANA_USERNAME="your_username_here"
```

Then in your Python code, retrieve it using:

```python
import os
KIBANA_USERNAME = os.environ.get('KIBANA_USERNAME')
index_name = f"{KIBANA_USERNAME}-bicycle_products"
```

1. Write a Python script that uses the `${KIBANA_USERNAME}-bicycle_products` index of the previous exercise to produce the following output:

```
The most expensive bike costs VARIABLE_MAX_PRICE, while the cheapest bike costs VARIABLE_MIN_PRICE. There are VARIABLE_NUMBER_OF_ROAD_BIKES road bikes available.
```

Variables description:

- VARIABLE_MAX_PRICE is the resulting value of a metric aggregation querying the most expensive bike. The value should be **1400**
- VARIABLE_MIN_PRICE is the resulting value of a metric aggregation querying the cheapest bike. The value shoudl be **250**
- VARIABLE_NUMBER_OF_ROAD_BIKES is the resulting value of a combination of query on the `Available` field and bucket aggregation over `Category`. You will then display the value for the bucket `Road Bikes`. The value should be **3**
  <br>
  <br>

2. Use the [Python sample app](./python/) and send all the logs it produces to a new Elasticsearch index named `${KIBANA_USERNAME}-app-logs`.

3. Continue working on the Python app and update it so it correctly queries Elasticsearch and returns the result in the user interface.

### Troubleshooting curl on Windows

`curl` on Windows parses JSON data differently than on MacOS or Linux. Thus, there might be issues with the body section of your requests. If you receive an error related to `Compressor detection can only be called on some xcontent bytes` you can do the following.<br>

1. Extract the body section of your request into a file e.g. `data.json`
2. Reference this file in your curl request with the `-d @data.json` flag

```
curl -X PUT -H "Content-Type: application/json" -H "Authorization: ApiKey ..." -d @data.json "https://...cloud.es.io:443/myindex"
```

The data.json file could then look like the following

```json
{
  "mappings": {
    "properties": {
      "Name": {
        "type": "text"
      }
    }
  }
}
```
