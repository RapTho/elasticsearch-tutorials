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
PUT /books
```

Add some documents to the new index using the `_bulk` API

```
POST /books/_bulk
{"index": { "_id": 1}}
{"id": 1, "title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "Fantasy", "year": 1937}
{"index": { "_id": 2}}
{"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Classics", "year": 1960}
{"index": { "_id": 3}}
{"id": 3, "title": "The Catcher in the Rye", "author": "J.D. Salinger", "genre": "Classics", "year": 1951}
```

Let's check if all books were added.

```
GET /books/_search
{
  "query": {
  "match_all": {}
  }
}
```

Retrieve some details of the new index. Adding `books` to the path allows us to retrieve data related to our `books` index only.

```
GET /_cat/indices/books?v
```

Inspect the newly created shards. Adding `books` to the path retrieves only the shards belonging to the `books` index.

```
GET /_cat/shards/books?v
```

### Replication

Let's increase the number of replicas. It's a setting of the index so we need to update the index settings.

```
PUT /books/_settings
{
  "index" : {
  "number_of_replicas" : 2
  }
}
```

Let's check if the new replicas were deployed.

```
GET /_cat/shards/books?v
```

- Q: What is the problem with the new replica?

```
GET _cluster/allocation/explain
{
  "index": "books",
  "shard": 0,
  "primary": false
}
```

Reset the `number_of_replicas` to `1`

```
PUT /books/_settings
{
  "index" : {
  "number_of_replicas" : 1
  }
}
```

### Shards

In order to change the number of primary shards we need to copy the data to a new index. For this, we first need to disable write operations to the index `books`.

```
PUT /books/_settings
{
  "index.blocks.write": true
}
```

Now to use the [Split API](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-split-index.html) to create new index with two shards.

```
POST /books/_split/books2
{
  "settings": {
  "index.number_of_shards": 2
  }
}
```

Finally, enable write operations to original index again.

```
PUT /books/_settings
{
  "index.blocks.write": null
}
```

Inspect the shards for the newly created index.

```
GET /_cat/shards/books2?v
```

### Aliases

Another approach to increase the number of shards is to combine multiple indices by using an [alias](https://www.elastic.co/guide/en/elasticsearch/reference/current/aliases.html).

Let's try it out. First we create a new index called `books3`...

```
PUT /books3
```

Then we add some data to it

```
PUT /books3/_doc/4
{
  "id": 4,
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "genre": "Classics",
  "year": 1925
}
PUT /books3/_doc/5
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
        "index": "books",
        "alias": "booksa"
      }
    },
      {
      "add": {
        "index": "books3",
        "alias": "booksa"
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
GET /_cat/shards/booksa?v
```

We can also use the alias to query data. The query is executed on both underlying indices.

```
GET /booksa/_search
{
  "query": {
  "match_all": {}
  }
}
```

### Data Streams

The alias approach is suitable for a continous data flow, but managing the underlying indices can be cumbersome. [Datastreams](https://www.elastic.co/guide/en/elasticsearch/reference/current/data-streams.html) take the same approach but make the management of underlying indices much easier by integrating with the Index Lifecycle Manager (ILM). Data streams are commonly used for logs, observability metrics and other time-series data.

First of all, we increase the interval of the ILM. For a production setup several minutes should be enough!

```
PUT _cluster/settings
{
  "transient": {
    "indices.lifecycle.poll_interval": "10s"
  }
}
```

Let's add a new lifecycle policy within the ILM. For this you need to specify the minimum age and actions for the different [lifecycle phases](https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-index-lifecycle.html) `hot`, `warm`, `cold` and `frozen`.

```
PUT _ilm/policy/mylog-lifecycle-policy
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_docs": 2
          }
        }
      },
      "warm": {
        "min_age": "30s",
        "actions": {}
      },
      "cold": {
        "min_age": "60s",
        "actions": {}
      },
      "delete": {
        "min_age": "120s",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

The ILM will dynamically create new indices which requires a template. We first create an index template for the mapping section to define the index's fields.

```
PUT _component_template/mylog-mappings
{
  "template": {
    "mappings": {
      "properties": {
        "@timestamp": {
          "type": "date",
          "format": "date_optional_time||epoch_millis"
        },
        "message": {
        "type": "wildcard"
        }
      }
    }
  }
}
```

In the index template's settings section we reference the previously created ILM policy

```
PUT _component_template/mylog-settings
{
  "template": {
    "settings": {
      "index.lifecycle.name": "mylog-lifecycle-policy"
    }
  }
}
```

Finally, we combine the two component templates to create a new [index template](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-templates.html). Note that `index_patterns` defines the future data stream naming pattern.

```
PUT _index_template/mylog-index-template
{
  "index_patterns": ["mylog-data-stream*"],
  "data_stream": { },
  "composed_of": [ "mylog-mappings", "mylog-settings" ]
}
```

That's it. We can now start adding data!

### Adding data

As no data stream exists yet, Elasticsearch will create the stream and the underlying index automatically. As the naming convention matches our `index_pattern`, our previously created index template will be used.

```
POST /mylog-data-stream/_doc
{
  "@timestamp": "2023-04-24T17:01:15.000Z",
  "message": "192.168.0.2 - Hello World 1"
}
```

Let's add more data

```
POST /mylog-data-stream/_bulk
{ "index": {} }
{ "@timestamp": "2023-04-24T17:02:15.000Z", "message": "192.168.0.2 - Hello World 2"}
{ "index": {} }
{ "@timestamp": "2023-04-24T17:03:15.000Z", "message": "192.168.0.2 - Hello World 3"}
{ "index": {} }
{ "@timestamp": "2023-04-24T17:04:15.000Z", "message": "192.168.0.2 - Hello World 4"}
{ "index": {} }
{ "@timestamp": "2023-04-24T17:05:15.000Z", "message": "192.168.0.2 - Hello World 5"}
```

Observe the underlying indices. The results might be different depending on how long you waited between posting data.

```
GET _cat/indices/.ds-mylog*?v
```

You can also display its settings and mappings

```
GET .ds-mylog*/_settings
GET .ds-mylog*/_mappings
```

## Clean up

Undo what we did in this lab

```
DELETE books*
DELETE _data_stream/mylog-data-stream
DELETE _index_template/mylog-index-template
DELETE _component_template/mylog*
DELETE _ilm/policy/mylog-lifecycle-policy
```
