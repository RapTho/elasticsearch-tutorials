#########################################
######## Lab 3: Mapping and Indexing
#########################################

# Start by creating a new index for books
PUT /books4
{}

# Get the current mapping for the new index (should be empty).
GET /books4/_mapping

# Start by adding a document to the index.
POST /books4/_doc
{
  "id": 1,
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "year": 1925,
  "read": false
}

# Check the mapping again. It shows different fields deduced from first document.
# This is called dynamic mapping.
GET /books4/_mapping

# Add a new document with an additional field
POST /books4/_doc
{
  "id": 2,
  "title": "Pride and Prejudice",
  "author": "Jane Austen",
  "year": 1813,
  "popularity": 8.2
}

# Once more, check the mapping. Note, that the new field appears in the mapping as well.
GET /books4/_mapping

# Lets see what happens to nested data
POST /books4/_doc
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

# Retrieve the data
GET /books4/_search
{
  "fields": [
    "*"
  ]
}

# Note that the nested data is not stored (i.e. indexed) as an array of objects
# but as seperate arrays of strings. This means that the relationship between `year` and 
# `sold` are lost in the index. You can see it by querying for all books which have an edition
# with `year < 1955` and `sold > 100000`. In our case there is no such book, but it is returned because
# the object was flattened.
GET /books4/_search
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

# You can fix this behaviour with `nested` (see later).



# Lets play around with updates. First add a new book to the index.
PUT /books4/_doc/5
{
  "id": 5,
  "title": "The Hobbit",
  "author": "J.R.R. Tolkien",
  "popularity": 9.3
}

# Lets try to update the popularity...
POST /books4/_doc/5
{
  "popularity": 1.1
}
# ... and check the document
GET /books4/_doc/5

# With this operation, we deleted the rest of the document. Add it back by running the PUT command above again.
# Instead, lets use the dedicated _update API...
POST /books4/_update/5
{
  "doc": {
    "popularity": 1.1
  }
  
}
# ... and check the document
GET /books4/_doc/5

# Now the partial update worked as expected. Lets try a scripted update.
# Instead of pushing field data to Elasticsearch, we provide a script which updates the value.
# The following call increases the popularity by 1
POST /books4/_update/5
{
  "script" : "ctx._source.popularity += 1"
}
GET /books4/_doc/5

# We can also update multiple documents with one request using the `_update_with_query` API.
# The following request adds the author name to the title field for all books that were published after 1900.
POST /books4/_update_by_query
{
  "query": {
    "range": {
      "year": {
        "gte": 1900
      }
    }
  },
  "script": {
    "source": "ctx._source.title += ' by '+ctx._source.author"
  }
}
# Get all books to verify your changes.
GET /books4/_search



# Now create an index with explicit mapping.
# To enforce a data schema we set dynamic: strict.
# Otherwise, explit mapping is supplemented by dynamic mapping.
PUT /myusers
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
# Add a document to the index. This should work fine.
POST /myusers/_doc
{
  "name": "Foo Bar",
  "birthday": "1990-04-27"
}
# Adding this document will fail. Why?
POST /myusers/_doc
{
  "name": "John Doe",
  "birthday": true
}
# Adding this document will fail as well. Why?
POST /myusers/_doc
{
  "name": "Foo Bar",
  "birthday": "1990-04-27",
  "gender": "male"
}
# Make sure only the first, valid document was added.
GET /myusers/_search

# Finally, lets use a runtime field which is calculated during runtime.
# In our case we create a scripted runtime field which calculates the age of a user
# based on its birthday. Remember to add the field name to the list of output fields.
GET /myusers/_search
{
  "runtime_mappings": {
    "age": {
      "type": "double",
      "script": {
        "source": """
          long nowDate = new Date().getTime();
          long docDate = doc['birthday'].value.toEpochMilli();
          long millisecondsPerYear = 31536000000L;
          double age = 1.0*(nowDate - docDate)/millisecondsPerYear;
          emit(age);
        """
      }
    }
  },
  "query": {
    "match_all": {}
  },
  "fields": [
    "name", "age"
  ]
}

# Lets play around with text analyzers in Elasticsearch.
# You can test different analyzers using the _analyze endpoint.
GET /_analyze
{
  "analyzer": "standard",
  "text": "The quick brown fox jumped over the lazy dog."
}

# Check the retrieved tokens. What is different from the source?

# Lets use an analyzer for english text. What did change now?
GET /_analyze
{
  "analyzer": "english",
  "text": "The quick brown fox jumped over the lazy dog."
}

# In contrast, compare the generated tokens using a german analyzer
GET /_analyze
{
  "analyzer": "german",
  "text": "The quick brown fox jumped over the lazy dog."
}

# What does the keyword analyzer do?
GET /_analyze
{
  "analyzer": "keyword",
  "text": "The quick brown fox jumped over the lazy dog."
}

# Finally, lets create our own analyzer. 
# We only want to take words into account which have more than 4 characters.
# To create a new analyzer, we need to create a new index.
PUT /custom-analyzer-index
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

# Test the analyzer by calling _analyze on the index context.
GET /custom-analyzer-index/_analyze
{
  "text": "The quick brown fox jumped over the lazy dog.",
  "analyzer": "my_word_length_analyzer"
}


# Remove data from lab 3
DELETE /books4
DELETE /myusers
DELETE /custom-analyzer-index