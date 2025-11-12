# Lab 3: Mapping, Indexing and Text Analysis

### Mapping and Indexing

Start by creating a new index for books

```
PUT /${username}-books4
```

Get the current mapping for the new index (should be empty).

```
GET /${username}-books4/_mapping
```

Add a document to the index.

```
POST /${username}-books4/_doc
{
  "id": 1,
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "year": 1925,
  "read": false
}
```

Check the mapping again. It shows different fields derived from first document. This is called dynamic mapping.

```
GET /${username}-books4/_mapping
```

Add another document with a new field

```
POST /${username}-books4/_doc
{
  "id": 2,
  "title": "Pride and Prejudice",
  "author": "Jane Austen",
  "year": 1813,
  "popularity": 8.2
}
```

Once more, check the mapping. Note, that the new field appears in the mapping as well.

```
GET /${username}-books4/_mapping
```

Let's see what happens to nested data

```
POST /${username}-books4/_doc
{
  "id": 3,
  "title": "The Catcher in the Rye",
  "author": "J.D. Salinger",
  "year": 1951,
  "editions": [
    {
      "year": 1951,
      "edition": 1,
      "sold": 10000
    },
    {
      "year": 1960,
      "edition": 2,
      "sold": 500000
    }
  ]
}
```

Retrieve the data

```
GET /${username}-books4/_search
{
  "fields": ["*"]
}
```

Note that the nested data is not stored (i.e. indexed) as an array of objects but as seperate arrays of strings. This means that the relationship between `year` and `sold` is lost in the index. You can see it by querying for all books which have an edition with `year < 1955` and `sold > 100000`. In our case there is no such book, but it is returned because the object was flattened.

```
GET /${username}-books4/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "range" : {
            "editions.sold": {
              "gt" : 100000
              }
          }
        },
        {
          "range" : {
            "editions.year": {
            "lt" : 1955
            }
          }
        }
      ]
    }
  }
}
```

In [lab 4](./lab-4.md) we will learn how to fix this issue with `nested` data. For now, let's play around with updates. First, add a new book to the index.

```
PUT /${username}-books4/_doc/5
{
  "id": 5,
  "title": "The Hobbit",
  "author": "J.R.R. Tolkien",
  "popularity": 9.3
}
```

Now try to update the popularity

```
PUT /${username}-books4/_doc/5
{
  "popularity": 1.1
}
```

Check the document

```
GET /${username}-books4/_doc/5
```

With this operation, we removed the rest of the document.
Redo the previous command and then update the same document using the [\_update API](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-update.html#_update_part_of_a_document).

```
POST /${username}-books4/_update/5
{
  "doc": {
  "popularity": 1.1
  }
}
```

Check the result

```
GET /${username}-books4/_doc/5
```

Now the partial update worked as expected. Let's try a scripted update. Instead of pushing field data to Elasticsearch, we provide a script which updates the value. The following call increases the popularity by 1.

```
POST /${username}-books4/_update/5
{
  "script" : "ctx._source.popularity += 1"
}
GET /${username}-books4/_doc/5
```

We can also update multiple documents with one request using the [\_update_by_query API](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-update-by-query.html). The following request adds the author name to the title field for all books that were published after 1900.

```
POST /${username}-books4/_update_by_query
{
  "query": {
    "range": {
      "year": {
        "gte": 1900
      }
    }
  },
  "script": {
    "source": "ctx._source.title += ' by '+ ctx._source.author"
  }
}
```

Get all books to verify your changes.

```
GET /${username}-books4/_search
```

Now create an index with explicit mapping. To enforce a data schema we set `"dynamic": "strict"`. Otherwise, explicit mappings still allow dynamic mapping.

```
PUT /${username}-myusers
  {
    "mappings": {
      "dynamic": "strict",
      "properties": {
        "name": {
          "type": "text"
        },
        "birthday": {
          "type": "date",
          "format": "strict_date_optional_time||epoch_millis"
      }
    }
  }
}
```

Add a document to the index. This works, as it complies with our previously defined schema.

```
POST /${username}-myusers/_doc
{
  "name": "Foo Bar",
  "birthday": "1990-04-27"
}
```

This next query will fail. Can you guess why?

```
POST /${username}-myusers/_doc
{
  "name": "John Doe",
  "birthday": true
}
```

Also this query will fail, as we try to introduce the new field `gender` which we didn't define previously.

```
POST /${username}-myusers/_doc
{
  "name": "Foo Bar",
  "birthday": "1990-04-27",
  "gender": "male"
}
```

Make sure only the first, valid document was added.

```
GET /${username}-myusers/_search
```

### Text analysis

Let's look into text analyzers in Elasticsearch. You can test different analyzers using the [\_analyze API](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-analyze.html).

```
GET /_analyze
{
  "analyzer": "standard",
  "text": "The quick brown fox jumped over the lazy dog."
}
```

Check the retrieved tokens. What is different from the source? Let's use an analyzer for `english` text. What changed?

```
GET /_analyze
{
  "analyzer": "english",
  "text": "The quick brown fox jumped over the lazy dog."
}
```

Compare the generated tokens using a `german` analyzer

```
GET /_analyze
{
  "analyzer": "german",
  "text": "The quick brown fox jumped over the lazy dog."
}
```

What does the `keyword` analyzer do?

```
GET /_analyze
{
  "analyzer": "keyword",
  "text": "The quick brown fox jumped over the lazy dog."
}
```

Finally, let's create our own analyzer. We only want to take words into account which have more than 4 characters. To create a new analyzer, we need to create a new index.

```
PUT /${username}-custom-analyzer-index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_word_length_analyzer": {
          "tokenizer": "standard",
          "filter": [
            "length_filter"
          ]
        }
      },
      "filter": {
        "length_filter": {
        "type": "length",
        "min": 4,
        "max": 100
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "sample": {
      "type": "text",
      "analyzer": "my_word_length_analyzer"
      }
    }
  }
}
```

Test the analyzer by calling `_analyze` on the index context.

```
GET /${username}-custom-analyzer-index/_analyze
{
  "text": "The quick brown fox jumped over the lazy dog.",
  "analyzer": "my_word_length_analyzer"
}
```

# Clean up

```
DELETE /${username}-books4
DELETE /${username}-myusers
DELETE /${username}-custom-analyzer-index
```
