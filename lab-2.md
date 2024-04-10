#########################################
######## Lab 2: Manage Indices and Shards
#########################################

# Lets start with getting detailed information about the cluster
GET /_cluster/state

# Instead of dealing with JSON format we can get a readable table format
# using the _cat endpoints. Add query parameter `v` to increase verbosity.
GET /_cat/nodes?v

# Q: What are the assigned roles?
# Q: What is the purpose of a dedicated tie-breaker node?
#    To answer this you might want to read about resiliency considerations in small clusters
#    https://www.elastic.co/guide/en/elasticsearch/reference/current/high-availability-cluster-design.html

# Get an overview on available indices.
GET /_cat/indices?v

# Get an overview of deployed shards.
GET /_cat/shards?v

# Lets add a new index with some data to dive deeper into shards.
# First, lets create a new index `books1`
PUT /books1
{}

# Add some documents to the new index
PUT /books1/_doc/1
{
  "id": 1,
  "title": "The Hobbit",
  "author": "J.R.R. Tolkien",
  "genre": "Fantasy",
  "year": 1937
}
PUT /books1/_doc/2
{
  "id": 2,
  "title": "To Kill a Mockingbird",
  "author": "Harper Lee",
  "genre": "Classics",
  "year": 1960
}
PUT /books1/_doc/3
{
  "id": 3,
  "title": "The Catcher in the Rye",
  "author": "J.D. Salinger",
  "genre": "Classics",
  "year": 1951
}

# Lets check if all books were added.
GET /books1/_search
{
    "query": {
        "match_all": {}
    }
}

# Retrieve some details on the new index.
# Adding `books1` to the path filters all indices for `books1`
GET /_cat/indices/books1?v

# Inspect the newly created shards.
# Adding `books1` to the path filters all indices for `books1`
GET /_cat/shards/books1?v

# Lets increase the number of replicas. Its a setting of the index so we need to update index settings.
PUT /books1/_settings
{
  "index" : {
    "number_of_replicas" : 2
  }
}

# Lets check if the new replicas were deployed.
GET /_cat/shards/books1?v

# Q: What is the problem with the new replica?
#    After answering reset the `number_of_replicas`` to 1

# Assume our database is growing and we want to change the number of shards.

# Q: Why is it not possible to just add a new primary shard to an existing index?
#    Use https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-split-index.html to answer this question.

# In order to change the number of primary shards we need to copy the data to a new index.
# For this, we first need to disable write operations to index `books1`.
PUT /books1/_settings
{
  "index.blocks.write": true
}
# Now use Split API to create new index with two shards.
POST /books1/_split/books2
{
  "settings": {
    "index.number_of_shards": 2
  }
}
# Finally, enable write operations to original index again.
PUT /books1/_settings
{
  "index.blocks.write": null
}

# Inspect shards for newly created index.
GET /_cat/shards/books2?v

# Another approach is to combine multiple indices, so new shards can be added
# by adding new indices to the combination. This can be done using `alias`.

# Lets try it out. First we create a new index `books3`...
PUT /books3
{}
# ... and add some data to it
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

# Now we can create an alias called `books` which points to both indices: `books1` and `books3`
POST /_aliases
{
  "actions": [
    {
      "add": {
        "index": "books1",
        "alias": "books"
      }
    },
    {
      "add": {
        "index": "books3",
        "alias": "books"
      }
    }
  ]
}

# Do we see the alias as an index?
GET /_cat/indices

# However, we can retrieve it by querying aliases.
GET /_cat/aliases?v

# The alias can be used like any other index. For example, we can retrieve corresponding charts
GET /_cat/shards/books?v

# We can also use the alias to query data. The query is executed on both underlying/baking indices.
GET /books/_search
{
    "query": {
        "match_all": {}
    }
}

# This approach is suitable for a continous data flow, but managing the underlying indices can be cumbersome.
# Datastreams take the same approach but make the management of underlying indices much easier by integrating with
# Index Lifecycle Manager (ILM). They are commonly used e.g. for logs, observability metrics and other time-series data.

# First of all, we increase the interval of ILM. For a production setup several minutes should be enough!
PUT _cluster/settings
{
  "transient": {
    "indices.lifecycle.poll_interval": "10s"
  }
}

# Lets add a new lifecycle policy within ILM. For this you need to specify minimum age and actions for
# the different lifecycle phases `hot`, `warm`, `cold` and `frozen`.
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
      "frozen": {
        "min_age": "90s",
        "actions": {
          "searchable_snapshot": {
            "snapshot_repository": "found-snapshots"
          }
        }
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

# ILM we dynamically create new indices which requires a template.
# For reusability we first create a template for index mapping (see later)...
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
# ..., then for index settings (here we reference the ILM policy)
PUT _component_template/mylog-settings
{
  "template": {
    "settings": {
      "index.lifecycle.name": "mylog-lifecycle-policy"
    }
  }
}
# ... and finally we put these two templates together to a new index template.
# Note that the index_patterns references the datastream name (which does not yet exists).
PUT _index_template/mylog-index-template
{
  "index_patterns": ["mylog-data-stream*"],
  "data_stream": { },
  "composed_of": [ "mylog-mappings", "mylog-settings" ]
}

# Thats it. We can now start adding data.
# Because nothing is there yet, Elasticsearch will create the stream and the underlying index automatically.
POST /mylog-data-stream/_doc
{
  "@timestamp": "2023-04-24T17:01:15.000Z",
  "message": "192.168.0.2 - Hello World 1"
}
# Lets add more data...
POST /mylog-data-stream/_doc
{
  "@timestamp": "2023-04-24T17:02:15.000Z",
  "message": "192.168.0.2 - Hello World 2"
}
# ... and more data...
POST /mylog-data-stream/_doc
{
  "@timestamp": "2023-04-24T17:03:15.000Z",
  "message": "192.168.0.2 - Hello World 3"
}
POST /mylog-data-stream/_doc
{
  "@timestamp": "2023-04-24T17:04:15.000Z",
  "message": "192.168.0.2 - Hello World 4"
}
POST /mylog-data-stream/_doc
{
  "@timestamp": "2023-04-24T17:05:15.000Z",
  "message": "192.168.0.2 - Hello World 5"
}

# Observe the underlying indices. The results might be different depending on how long you waited between posting data.
GET /_cat/indices/.ds-mylog*?v



# Remove data from lab 2
DELETE /books1
DELETE /books2
DELETE /books3
DELETE /_data_stream/mylog-data-stream