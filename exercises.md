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

   - [Generate an API key](https://www.elastic.co/guide/en/kibana/8.13/api-keys.html) using the Kibana console or API.
   - Securely save the API key for future use.

3. **Validation:**
   - Validate the API key by making a simple API call using a `curl` to list indexes or get cluster health.

### Exercise 2: Using curl to interact with the Elasticsearch API

**Objective:** Master the use of `curl` for Elasticsearch API interactions.

#### Tasks:

1. Create a new index with an explicit mapping that satisfies the following field / type criteria:

- Name = text
- Price = float
- Production Date = date of format `strict_date_optional_time` or `epoch_millis`
- Available = true
- Category = keyword
- Parts = Array of text

2. Add data to the newly created index using `curl`. Use the sample data below in a bulk request.

```
{ "index" : { "_index" : "bicycle_products", "_id" : "1" } }
{ "Name": "Speedster Road Bike", "Price": 850.00, "Production Date": "2024-04-01T00:00:00Z", "Available": false, "Category": "Road Bikes", "Parts": ["frame", "wheels", "brakes"] }
{ "index" : { "_index" : "bicycle_products", "_id" : "2" } }
{ "Name": "Mountain King Bicycle", "Price": 1200.00, "Production Date": "2024-04-02T00:00:00Z", "Available": false, "Category": "Mountain Bikes", "Parts": ["suspension", "off-road tires", "chain"] }
{ "index" : { "_index" : "bicycle_products", "_id" : "3" } }
{ "Name": "Urban Commuter 3000", "Price": 600.00, "Production Date": "2024-04-03T00:00:00Z", "Available": true, "Category": "City Bikes", "Parts": ["bell", "basket", "lights"] }
{ "index" : { "_index" : "bicycle_products", "_id" : "4" } }
{ "Name": "Trailblazer XC 29", "Price": 1100.00, "Production Date": "2024-04-04T00:00:00Z", "Available": true, "Category": "Cross Country", "Parts": ["helmet", "gloves", "handlebar"] }
{ "index" : { "_index" : "bicycle_products", "_id" : "5" } }
{ "Name": "Night Rider 500", "Price": 950.00, "Production Date": "2024-04-05T00:00:00Z", "Available": true, "Category": "Hybrid Bikes", "Parts": ["LED lights", "hybrid tires", "comfort seat"] }
{ "index" : { "_index" : "bicycle_products", "_id" : "6" } }
{ "Name": "Breeze Leisure Bike", "Price": 500.00, "Production Date": "2024-04-06T00:00:00Z", "Available": false, "Category": "Leisure Bikes", "Parts": ["basket", "wide seat", "cruise handlebars"] }
{ "index" : { "_index" : "bicycle_products", "_id" : "7" } }
{ "Name": "Thunder BMX", "Price": 300.00, "Production Date": "2024-04-07T00:00:00Z", "Available": true, "Category": "BMX Bikes", "Parts": ["stunt pegs", "reinforced frame", "BMX handlebar"] }
{ "index" : { "_index" : "bicycle_products", "_id" : "8" } }
{ "Name": "Glider 1000 Roadster", "Price": 650.00, "Production Date": "2024-04-08T00:00:00Z", "Available": true, "Category": "Road Bikes", "Parts": ["road tires", "aerodynamic frame", "racing saddle"] }
{ "index" : { "_index" : "bicycle_products", "_id" : "9" } }
{ "Name": "Cyclone Mountain Series", "Price": 1350.00, "Production Date": "2024-04-20T00:00:00Z", "Available": true, "Category": "Mountain Bikes", "Parts": ["all-terrain tires", "advanced suspension", "carbon frame"] }
{ "index" : { "_index" : "bicycle_products", "_id" : "10" } }
{ "Name": "Ranger Trail Expert", "Price": 1050.00, "Production Date": "2024-04-10T00:00:00Z", "Available": true, "Category": "Mountain Bikes", "Parts": ["shock absorbers", "trail tires", "durable pedals"] }
{ "index" : { "_index" : "bicycle_products", "_id" : "11" } }
{ "Name": "City Glide 700", "Price": 670.00, "Production Date": "2024-04-11T00:00:00Z", "Available": false, "Category": "City Bikes", "Parts": ["commuter frame", "mudguards", "chain lock"] }
{ "index" : { "_index" : "bicycle_products", "_id" : "12" } }
{ "Name": "Pinnacle Road Ace", "Price": 890.00, "Production Date": "2024-04-12T00:00:00Z", "Available": true, "Category": "Road Bikes", "Parts": ["carbon wheelset", "speedometer", "drop handlebars"] }
{ "index" : { "_index" : "bicycle_products", "_id" : "13" } }
{ "Name": "Sunset Cruiser Deluxe", "Price": 550.00, "Production Date": "2024-04-13T00:00:00Z", "Available": true, "Category": "Leisure Bikes", "Parts": ["leather seat", "wide handlebars", "cruiser tires"] }
{ "index" : { "_index" : "bicycle_products", "_id" : "14" } }
{ "Name": "Freewheel X2 BMX", "Price": 320.00, "Production Date": "2024-04-14T00:00:00Z", "Available": true, "Category": "BMX Bikes", "Parts": ["freestyle tires", "360-degree rotor", "BMX forks"] }
{ "index" : { "_index" : "bicycle_products", "_id" : "15" } }
{ "Name": "ElectroRide E-Bike", "Price": 1400.00, "Production Date": "2024-04-15T00:00:00Z", "Available": true, "Category": "Electric Bikes", "Parts": ["electric motor", "battery pack", "digital display"] }
{ "index" : { "_index" : "bicycle_products", "_id" : "16" } }
{ "Name": "Touring Explorer 2000", "Price": 950.00, "Production Date": "2024-04-16T00:00:00Z", "Available": true, "Category": "Touring Bikes", "Parts": ["pannier rack", "touring tires", "comfort saddle"] }
{ "index" : { "_index" : "bicycle_products", "_id" : "17" } }
{ "Name": "Trail Blazer XT", "Price": 1300.00, "Production Date": "2024-04-17T00:00:00Z", "Available": true, "Category": "Mountain Bikes", "Parts": ["full suspension", "trail-specific gearing", "aluminum frame"] }
{ "index" : { "_index" : "bicycle_products", "_id" : "18" } }
{ "Name": "City Pro Commuter", "Price": 720.00, "Production Date": "2024-04-18T00:00:00Z", "Available": false, "Category": "City Bikes", "Parts": ["urban tires", "fenders", "rear rack"] }
{ "index" : { "_index" : "bicycle_products", "_id" : "19" } }
{ "Name": "Rapid Racer 5000", "Price": 1100.00, "Production Date": "2024-04-19T00:00:00Z", "Available": true, "Category": "Road Bikes", "Parts": ["carbon fiber frame", "aero wheels", "performance brakes"] }
{ "index" : { "_index" : "bicycle_products", "_id" : "20" } }
{ "Name": "Kids' Adventure 20", "Price": 250.00, "Production Date": "2024-04-20T00:00:00Z", "Available": true, "Category": "Kids' Bikes", "Parts": ["training wheels", "child-friendly grips", "colorful frame"] }

```

3. Make sure no other fields are allowed by trying to index the following non-compliant document

```
{ "Name": "Racer Bicicletta", "Price": 1.00, "Production Date": "Fake Date", "Available": "maybe", "Category": 200, "Parts": true }
```

And how about the follwoing one with a new field?

```
{ "Name": "Kids' Adventure 20", "NEW": "FIELD", "Price": 250.00, "Production Date": "2024-04-20T00:00:00Z", "Available": true, "Category": "Kids' Bikes", "Parts": ["training wheels", "child-friendly grips", "colorful frame"] }
```

4. Find all bicycles matching the following criteria. There should only be **3**

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

### Exercise 4: Bucket and Metric Aggregations via Python

**Objective:** Utilize Elasticsearch's aggregation framework to summarize data.

#### Task:

Write a Python script that uses the `bicycle_products` index of the previous exercise to produce the following output:

```
The most expensive bike costs VARIABLE_MAX_PRICE, while the cheapest bike costs VARIABLE_MIN_PRICE. There are VARIABLE_NUMBER_OF_ROAD_BIKES road bikes available.
```

While:

- VARIABLE_MAX_PRICE is the resulting value of a metric aggregation querying the most expensive bike. The value should be **1400**
- VARIABLE_MIN_PRICE is the resulting value of a metric aggregation querying the cheapest bike. The value shoudl be **250**
- VARIABLE_NUMBER_OF_ROAD_BIKES is the resulting value of a combination of query on the `Available` field and bucket aggregation over `Category`. You will then display the value for the bucket `Road Bikes`. The value should be **3**

### Exercise 5: Crawl the web

**Objective:** Learn how to crawl websites

#### Task:

Use Elasticsearch's [Web Crawler](https://www.elastic.co/web-crawler) to gather data from the [https://hslu.ch](https://hslu.ch) website.

**HINT:** You find the Web Crawler in Kibana under Search -> Content

Ignore the listed jobs by adding a [disallow policy](https://www.elastic.co/guide/en/enterprise-search/current/crawler-managing.html#crawler-managing-crawl-rules) for everything that contains:

```
/hochschule-luzern/ueber-uns/jobs-und-karriere/
```

You should get about **23'500 documents**

### Exercise 6: Use Kibana to discover the data

**Objective:** Browse through the data using Kibana's Discover functionality

#### Tasks:

1. In Kibana open the menu, click on Analytics -> Discover
2. Look for data that contains `renewable` in the title field.
3. Open one of the documents and look at the document's structure
4. Now let's imagine you're a lonely guy and need to use Kibana to search for parties at your campus. Filter by `url_path_dir3` = `campus`and `body_content` = `Party`. Are there any?
