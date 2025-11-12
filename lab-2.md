# Lab 2: Manage Indices and Shards

## Overview

Lets start with getting detailed information about the cluster by executing

```
GET /_cluster/state
```

Instead of dealing with JSON format we can get a readable table format using the **\_cat** endpoints. Add query parameter **`v`** to increase verbosity.

```
GET /_cat/nodes?v
```

- Q: What are the assigned [roles](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-node.html#node-roles)?
- Q: What is the purpose of a dedicated tiebreaker node?
- A: read about [resiliency considerations in small clusters](https://www.elastic.co/guide/en/elasticsearch/reference/current/high-availability-cluster-small-clusters.html#high-availability-cluster-design-two-nodes-plus)

Get an overview of the available indices.

```
GET /_cat/indices?v
```

Get an overview of the deployed shards. [This page](https://www.elastic.co/guide/en/elasticsearch/reference/current/cat-shards.html#cat-shards-query-params) tells you what each of the columns mean.

```
GET /_cat/shards?v
```

## Indices

Let's add a new index with some data to dive deeper into shards. First, let's create a new index called `books`

```
PUT /${username}-books
```

Add some documents to the new index using the `_bulk` API

```
POST /${username}-books/_bulk
{"index": { "_id": 1}}
{"id": 1, "title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "Fantasy", "year": 1937}
{"index": { "_id": 2}}
{"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Classics", "year": 1960}
{"index": { "_id": 3}}
{"id": 3, "title": "The Catcher in the Rye", "author": "J.D. Salinger", "genre": "Classics", "year": 1951}
```

Let's check if all books were added.

```
GET /${username}-books/_search
{
  "query": {
  "match_all": {}
  }
}
```

Retrieve some details of the new index. Adding `books` to the path allows us to retrieve data related to our `books` index only.

```
GET /_cat/indices/${username}-books?v
```

Inspect the newly created shards. Adding `books` to the path retrieves only the shards belonging to the `books` index.

```
GET /_cat/shards/${username}-books?v
```

### Replication

Let's increase the number of replicas. It's a setting of the index so we need to update the index settings.

```
PUT /${username}-books/_settings
{
  "index" : {
  "number_of_replicas" : 2
  }
}
```

Let's check if the new replicas were deployed.

```
GET /_cat/shards/${username}-books?v
```

- Q: What is the problem with the new replica?

```
GET _cluster/allocation/explain
{
  "index": "${username}-books",
  "shard": 0,
  "primary": false
}
```

Reset the `number_of_replicas` to `1`

```
PUT /${username}-books/_settings
{
  "index" : {
  "number_of_replicas" : 1
  }
}
```

### Shards

In order to change the number of primary shards we need to copy the data to a new index. For this, we first need to disable write operations to the index `books`.

```
PUT /${username}-books/_settings
{
  "index.blocks.write": true
}
```

Now to use the [Split API](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-split-index.html) to create new index with two shards.

```
POST /${username}-books/_split/${username}-books2
{
  "settings": {
  "index.number_of_shards": 2
  }
}
```

Finally, enable write operations to original index again.

```
PUT /${username}-books/_settings
{
  "index.blocks.write": null
}
```

Inspect the shards for the newly created index.

```
GET /_cat/shards/${username}-books2?v
```

### Aliases

Another approach to increase the number of shards is to combine multiple indices by using an [alias](https://www.elastic.co/guide/en/elasticsearch/reference/current/aliases.html).

Let's try it out. First we create a new index called `books3`...

```
PUT /${username}-books3
```

Then we add some data to it

```
PUT /${username}-books3/_doc/4
{
  "id": 4,
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "genre": "Classics",
  "year": 1925
}
PUT /${username}-books3/_doc/5
{
  "id": 5,
  "title": "Pride and Prejudice",
  "author": "Jane Austen",
  "genre": "Romance",
  "year": 1813
}
```

Now we can create an alias called `booksa` which points to both indices: `books` and `books3`

```
POST /_aliases
{
  "actions": [
    {
      "add": {
        "index": "${username}-books",
        "alias": "${username}-booksa"
      }
    },
      {
      "add": {
        "index": "${username}-books3",
        "alias": "${username}-booksa"
      }
    }
  ]
}
```

Do we see the alias as an index?

```
GET /_cat/indices
```

No, but we can retrieve a list of aliases.

```
GET /_cat/aliases?v
```

The alias can be used like any other index. For example, we can retrieve corresponding shards

```
GET /_cat/shards/${username}-booksa?v
```

We can also use the alias to query data. The query is executed on both underlying indices.

```
GET /${username}-booksa/_search
{
  "query": {
  "match_all": {}
  }
}
```

### Data Streams

The alias approach is suitable for a continuous data flow, but managing the underlying indices can be cumbersome. [Data streams](https://www.elastic.co/guide/en/elasticsearch/reference/current/data-streams.html) take the same approach but make the management of underlying indices much easier by integrating with the Index Lifecycle Manager (ILM). Data streams are commonly used for logs, observability metrics and other time-series data.

First, let's speed up the ILM polling interval for demonstration purposes.

```
PUT _cluster/settings
{
  "transient": {
    "indices.lifecycle.poll_interval": "10s"
  }
}
```

#### Create ILM Policy

Let's create a comprehensive lifecycle policy that demonstrates all phases with actions available in the basic license:

```
PUT _ilm/policy/${username}-sensor-data-policy
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_primary_shard_size": "50mb",
            "max_age": "1d",
            "max_docs": 5
          }
        }
      },
      "warm": {
        "min_age": "30s",
        "actions": {
          "readonly": {}
        }
      },
      "delete": {
        "min_age": "90s",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

**What each action does:**

- `rollover`: Creates a new index when conditions are met (5 docs for demo, typically size/age in production)
- `readonly`: Makes index read-only to prevent accidental writes
- `delete`: Removes the index

#### Create Component Templates

Create a component template for mappings that defines our sensor data structure:

```
PUT _component_template/${username}-sensor-mappings
{
  "template": {
    "mappings": {
      "properties": {
        "@timestamp": {
          "type": "date",
          "format": "date_optional_time||epoch_millis"
        },
        "sensor_id": {
          "type": "keyword"
        },
        "temperature": {
          "type": "float"
        },
        "humidity": {
          "type": "float"
        },
        "location": {
          "type": "geo_point"
        },
        "status": {
          "type": "keyword"
        }
      }
    }
  }
}
```

Create a component template for settings that references our ILM policy:

```
PUT _component_template/${username}-sensor-settings
{
  "template": {
    "settings": {
      "index.lifecycle.name": "${username}-sensor-data-policy",
      "index.number_of_shards": 2,
      "index.number_of_replicas": 1
    }
  }
}
```

#### Create Index Template

Combine the component templates into an [index template](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-templates.html) for our data stream:

```
PUT _index_template/${username}-sensor-data-template
{
  "index_patterns": ["${username}-sensor-data*"],
  "data_stream": {},
  "composed_of": ["${username}-sensor-mappings", "${username}-sensor-settings"],
  "priority": 500
}
```

#### Add Data to the Data Stream

Now we can start ingesting data. The data stream and its first backing index will be created automatically:

```
POST /${username}-sensor-data/_doc
{
  "@timestamp": "2024-01-15T10:00:00.000Z",
  "sensor_id": "sensor-001",
  "temperature": 22.5,
  "humidity": 45.2,
  "location": {
    "lat": 40.7128,
    "lon": -74.0060
  },
  "status": "active"
}
```

Add more sensor readings to trigger a rollover (we set max_docs to 5):

```
POST /${username}-sensor-data/_bulk
{ "create": {} }
{ "@timestamp": "2024-01-15T10:05:00.000Z", "sensor_id": "sensor-001", "temperature": 22.8, "humidity": 44.8, "location": {"lat": 40.7128, "lon": -74.0060}, "status": "active"}
{ "create": {} }
{ "@timestamp": "2024-01-15T10:10:00.000Z", "sensor_id": "sensor-002", "temperature": 21.3, "humidity": 48.5, "location": {"lat": 40.7589, "lon": -73.9851}, "status": "active"}
{ "create": {} }
{ "@timestamp": "2024-01-15T10:15:00.000Z", "sensor_id": "sensor-003", "temperature": 23.1, "humidity": 43.2, "location": {"lat": 40.7614, "lon": -73.9776}, "status": "active"}
{ "create": {} }
{ "@timestamp": "2024-01-15T10:20:00.000Z", "sensor_id": "sensor-001", "temperature": 23.5, "humidity": 42.9, "location": {"lat": 40.7128, "lon": -74.0060}, "status": "active"}
{ "create": {} }
{ "@timestamp": "2024-01-15T10:25:00.000Z", "sensor_id": "sensor-002", "temperature": 21.8, "humidity": 47.3, "location": {"lat": 40.7589, "lon": -73.9851}, "status": "active"}
```

#### Monitor the Data Stream

View the data stream information:

```
GET _data_stream/${username}-sensor-data
```

#### Observe ILM Phase Transitions

Wait about 30 seconds and check the ILM status to see indices moving to the warm phase:

```
GET .ds-${username}-sensor-data*/_ilm/explain
```

You should see:

- Older indices in the **warm** phase (read-only)
- The current write index in the **hot** phase
- After 90 seconds, the oldest indices will be deleted.

## Clean up

Undo what we did in this lab:

```
DELETE ${username}-books
DELETE ${username}-books2
DELETE ${username}-books3
DELETE _data_stream/${username}-sensor-data
DELETE _index_template/${username}-sensor-data-template
DELETE _component_template/${username}-sensor-mappings
DELETE _component_template/${username}-sensor-settings
DELETE _ilm/policy/${username}-sensor-data-policy
```

Reset the ILM polling interval to default:

```
PUT _cluster/settings
{
  "transient": {
    "indices.lifecycle.poll_interval": null
  }
}
```
