# Lab 4: Search and Aggregation

### Searches

Let's start by creating a new index

```
PUT /${username}-recipes
```

Add data to the `recipes` index

```
POST /${username}-recipes/_bulk
{"index":{"_index":"${username}-recipes","_id":"1"}}
{"name":"Classic Spaghetti Carbonara","ingredients":["spaghetti","eggs","pecorino cheese","guanciale"],"instructions":"1. Cook spaghetti in boiling salted water. 2. Whisk together eggs and cheese. 3. Fry guanciale. 4. Toss spaghetti with guanciale and egg mixture. 5. Serve with freshly cracked black pepper.","likes":123}
{"index":{"_index":"${username}-recipes","_id":"2"}}
{"name":"Beef Stroganoff","ingredients":["beef sirloin","onion","mushrooms","sour cream","beef broth"],"instructions":"1. Cut beef into strips. 2. Sauté beef and onion. 3. Add mushrooms and cook until tender. 4. Add beef broth and bring to a simmer. 5. Stir in sour cream. 6. Serve over noodles.","likes":12}
{"index":{"_index":"${username}-recipes","_id":"3"}}
{"name":"Chicken Alfredo","ingredients":["chicken breast","heavy cream","parmesan cheese","fettuccine"],"instructions":"1. Cook fettuccine in boiling salted water. 2. Cut chicken into strips and sauté until cooked through. 3. Add heavy cream and bring to a simmer. 4. Stir in parmesan cheese until melted. 5. Toss pasta with sauce and chicken. 6. Serve hot.","likes":3}
{"index":{"_index":"${username}-recipes","_id":"4"}}
{"name":"Beef Chili","ingredients":["ground beef","onion","red bell pepper","kidney beans","tomato sauce"],"instructions":"1. Sauté onion and red pepper. 2. Add ground beef and cook until browned. 3. Add kidney beans and tomato sauce. 4. Simmer for 30 minutes. 5. Serve hot.","likes":45}
{"index":{"_index":"${username}-recipes","_id":"5"}}
{"name":"Chicken Enchiladas","ingredients":["shredded chicken","enchilada sauce","flour tortillas","shredded cheddar cheese"],"instructions":"1. Preheat oven to 350 degrees. 2. Mix shredded chicken with enchilada sauce. 3. Place chicken mixture in center of tortillas and roll up. 4. Place enchiladas in a baking dish. 5. Cover with shredded cheese. 6. Bake for 20 minutes. 7. Serve hot.","likes":91}
{"index":{"_index":"${username}-recipes","_id":"6"}}
{"name":"Roast Pork Tenderloin","ingredients":["pork tenderloin","garlic","rosemary","olive oil"],"instructions":"1. Preheat oven to 375 degrees. 2. Combine garlic, rosemary, and olive oil in a small bowl. 3. Rub mixture over pork tenderloin. 4. Roast in the oven for 20-25 minutes. 5. Serve hot.","likes":1}
{"index":{"_index":"${username}-recipes","_id":"7"}}
{"name":"Baked Salmon","ingredients":["salmon fillet","lemon","garlic","butter"],"instructions":"1. Preheat oven to 350 degrees. 2. Place salmon fillet on a sheet of aluminum foil. 3. Squeeze lemon over salmon. 4. Melt butter and mix with garlic. 5. Pour butter mixture over salmon. 6. Bake for 20 minutes. 7. Serve hot.","likes":32}
{"index":{"_index":"${username}-recipes","_id":"8"}}
{"name":"Tacos","ingredients":["ground beef","taco seasoning","tortilla chips","shredded lettuce","diced tomatoes"],"instructions":"1. Brown ground beef in a skillet. 2. Add taco seasoning and cook according to package directions. 3. Serve over a bed of tortilla chips. 4. Top with shredded lettuce and diced tomatoes. 5. Serve hot.","likes":74}
{"index":{"_index":"${username}-recipes","_id":"9"}}
{"name":"Spicy Chicken Curry","ingredients":["chicken breast","curry powder","coconut milk","tomatoes","onion"],"instructions":"1. Cut chicken into cubes and sauté in a large pot. 2. Add onion and cook until translucent. 3. Add curry powder and cook for 1 minute. 4. Add diced tomatoes and coconut milk. 5. Simmer for 20 minutes. 6. Serve hot over rice.","likes":16}
{"index":{"_index":"${username}-recipes","_id":"10"}}
{"name":"Creamy Tomato Soup","ingredients":["tomatoes","onion","garlic","heavy cream"],"instructions":"1. Heat olive oil in a large pot. 2. Add chopped onion and garlic and sauté until softened. 3. Add chopped tomatoes and simmer for 15 minutes. 4. Blend soup until smooth. 5. Add heavy cream and simmer for an additional 5 minutes. 6. Serve hot. There is no chicken in tomato soup.","likes":17}
```

Search for all recipes which have `chicken` in their name and limit the response to the `name` and `ingredients` fields. Use the [\_source option](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-fields.html#search-fields) to avoid retrieving the whole document.

```
GET /${username}-recipes/_search
{
  "query": {
    "match": {
      "name": "chicken"
    }
  },
  "fields": [
    "name",
    "ingredients"
  ],
  "_source": false
}
```

Actually, there is one more recipe which contains `chicken`. Let's also include `instructions` in our search query.

```
GET /${username}-recipes/_search
{
  "query": {
    "multi_match": {
      "query": "chicken",
      "fields": ["name", "instructions"]
    }
  },
  "fields": ["name", "instructions"],
  "_source": false
}
```

Not everyone can spell `Enchiladas` correctly. Fuzziness respects spelling errors in your search string. How wrong can you spell `Enchiladas` before it is not recognized anymore?

```
GET /${username}-recipes/_search
{
  "query": {
    "fuzzy": {
      "name": {
        "value": "enchiadas",
        "fuzziness": "AUTO"
      }
    }
  },
  "fields": ["name"],
  "_source": false
}
```

Remember the query with nested data from lab 3? Lets have a look at this again and start by creating an index.

```
PUT /${username}-books5
```

Let's add a new book

```
POST /${username}-books5/_doc
{
  "id": 1,
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

Now try to get all editions which were published after `1955` and sold more than `100000` copies. Actually there is none, so the result should be empty.

```
GET /${username}-books5/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "range": {
            "editions.sold": {
              "gt": 100000
            }
          }
        },
        {
          "range": {
            "editions.year": {
              "lt": 1955
            }
          }
        }
      ]
    }
  }
}
```

What went wrong? A closer look at the `editions` field shows how Elasticsearch indexed the data internally.

```
GET /${username}-books5/_search
{
  "fields": ["editions.*"],
  "_source": false
}
```

It flattened the object, so instead of having an array of objects we have multiple arrays, one for each object value. That's why we lost the relationship between `year` and `sold` within the `editions` array. To fix this, we have to declare the field as `nested`. When using `nested`, the object is treated as a seperate document in the index. Delete the index, recreate it with an explicit mapping and do the steps above again.

```
DELETE /${username}-books5
```

```
PUT /${username}-books5
{
  "mappings": {
    "properties": {
      "editions": {
        "type": "nested"
      }
    }
  }
}
```

The `nested` type allows us to create 1-to-many relationships in Elasticsearch.

### Aggregations

Let's look at Elasticsearch's aggregation capabilities. We start by adding orders to a new index. Note that we declare the `customer_name` as a `keyword`.

```
PUT /${username}-orders
{
  "mappings": {
    "properties": {
      "customer_name": {
        "type": "keyword"
      }
    }
  }
}
```

```
POST /${username}-orders/_bulk
{ "index": { "_id": 1 }}
{ "customer_name": "John Doe", "order_date": "2022-01-01", "total_price": 100, "items": ["T-shirt", "Jeans"] }
{ "index": { "_id": 2 }}
{ "customer_name": "Jane Smith", "order_date": "2022-01-01", "total_price": 100, "items": ["Socks"] }
{ "index": { "_id": 3 }}
{ "customer_name": "Tom Smith", "order_date": "2022-01-01", "total_price": 50, "items": ["Socks"] }
{ "index": { "_id": 4 }}
{ "customer_name": "Jane Smith", "order_date": "2022-01-02", "total_price": 150, "items": ["Shoes", "Sweater"] }
{ "index": { "_id": 5 }}
{ "customer_name": "Tom Smith", "order_date": "2022-01-02", "total_price": 50, "items": ["Socks"] }
{ "index": { "_id": 6 }}
{ "customer_name": "John Doe", "order_date": "2022-01-03", "total_price": 75, "items": ["Hat", "Gloves"] }
{ "index": { "_id": 7 }}
{ "customer_name": "Jane Smith", "order_date": "2022-01-04", "total_price": 200, "items": ["Coat"] }
{ "index": { "_id": 8 }}
{ "customer_name": "Tom Smith", "order_date": "2022-01-05", "total_price": 50, "items": ["Socks"] }
{ "index": { "_id": 9 }}
{ "customer_name": "John Doe", "order_date": "2022-01-05", "total_price": 25, "items": ["T-shirt", "Hat"] }
{ "index": { "_id": 10 }}
{ "customer_name": "Jane Smith", "order_date": "2022-01-05", "total_price": 90, "items": ["Gloves"] }
```

Now group all the orders by `customer_name`. Note that the following bucket aggregation skips the query statement in the aggregation query. Usually you want to filter the aggregation results and not aggregate over all documents.

```
GET /${username}-orders/_search
{
  "size": 0,
  "aggs": {
    "customers": {
      "terms": {
        "field": "customer_name"
      }
    }
  }
}
```

We can now perform a metric aggregation on these buckets. This is done by adding a nested `aggs` to the request which sums up all values in `total_price`.

```
GET /${username}-orders/_search
{
  "size": 0,
  "aggs": {
    "customers": {
      "terms": {
        "field": "customer_name"
      },
      "aggs": {
        "total_revenue": {
          "sum": {
            "field": "total_price"
          }
        }
      }
    }
  }
}
```

Let's look at another bucket aggregation. The following example groups the documents by `order_date` and creates a histogram with a resolution of 1d.

```
GET /${username}-orders/_search
{
  "size": 0,
  "aggs": {
    "orders_per_day": {
      "date_histogram": {
        "field": "order_date",
        "fixed_interval": "1d"
      }
    }
  }
}
```

Again, we can extend this by adding a metric aggregation to each bucket to calculate the total revenue for each histogram. Also, we can use the `top_hits` aggregation to get the top items of each bucket.

```
GET /${username}-orders/_search
{
  "size": 0,
  "aggs": {
    "orders_per_day": {
      "date_histogram": {
        "field": "order_date",
        "fixed_interval": "1d"
      },
      "aggs": {
        "total_revenue": {
          "sum": {
            "field": "total_price"
          }
        },
        "highest_orders": {
          "top_hits": {
            "size": 2,
            "sort": [
              {
                "total_price": {
                  "order": "desc"
                }
              }
            ]
          }
        }
      }
    }
  }
}
```

The `top_hits` aggregation can also be used on the top-level to show the order with the highest `total_price`.

```
GET /${username}-orders/_search
{
  "size": 0,
  "aggs": {
    "max_price": {
      "max": {
        "field": "total_price"
      }
    },
    "highest_orders": {
      "top_hits": {
        "size": 1,
        "sort": [
          {
            "total_price": {
              "order": "desc"
            }
          }
        ]
      }
    }
  }
}
```

That's it :)

# Clean up

```
DELETE /${username}-recipes
DELETE /${username}-books5
DELETE /${username}-orders
```
