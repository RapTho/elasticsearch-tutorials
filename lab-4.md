#########################################
######## Lab 4: Search and Aggregation
#########################################

# Lets start by putting some recipes into an index
PUT /recipes
POST /recipes/_bulk
{"index":{"_index":"recipes","_id":"1"}}
{"name":"Classic Spaghetti Carbonara","ingredients":["spaghetti","eggs","pecorino cheese","guanciale"],"instructions":"1. Cook spaghetti in boiling salted water. 2. Whisk together eggs and cheese. 3. Fry guanciale. 4. Toss spaghetti with guanciale and egg mixture. 5. Serve with freshly cracked black pepper.","likes":123}
{"index":{"_index":"recipes","_id":"2"}}
{"name":"Beef Stroganoff","ingredients":["beef sirloin","onion","mushrooms","sour cream","beef broth"],"instructions":"1. Cut beef into strips. 2. Sauté beef and onion. 3. Add mushrooms and cook until tender. 4. Add beef broth and bring to a simmer. 5. Stir in sour cream. 6. Serve over noodles.","likes":12}
{"index":{"_index":"recipes","_id":"3"}}
{"name":"Chicken Alfredo","ingredients":["chicken breast","heavy cream","parmesan cheese","fettuccine"],"instructions":"1. Cook fettuccine in boiling salted water. 2. Cut chicken into strips and sauté until cooked through. 3. Add heavy cream and bring to a simmer. 4. Stir in parmesan cheese until melted. 5. Toss pasta with sauce and chicken. 6. Serve hot.","likes":3}
{"index":{"_index":"recipes","_id":"4"}}
{"name":"Beef Chili","ingredients":["ground beef","onion","red bell pepper","kidney beans","tomato sauce"],"instructions":"1. Sauté onion and red pepper. 2. Add ground beef and cook until browned. 3. Add kidney beans and tomato sauce. 4. Simmer for 30 minutes. 5. Serve hot.","likes":45}
{"index":{"_index":"recipes","_id":"5"}}
{"name":"Chicken Enchiladas","ingredients":["shredded chicken","enchilada sauce","flour tortillas","shredded cheddar cheese"],"instructions":"1. Preheat oven to 350 degrees. 2. Mix shredded chicken with enchilada sauce. 3. Place chicken mixture in center of tortillas and roll up. 4. Place enchiladas in a baking dish. 5. Cover with shredded cheese. 6. Bake for 20 minutes. 7. Serve hot.","likes":91}
{"index":{"_index":"recipes","_id":"6"}}
{"name":"Roast Pork Tenderloin","ingredients":["pork tenderloin","garlic","rosemary","olive oil"],"instructions":"1. Preheat oven to 375 degrees. 2. Combine garlic, rosemary, and olive oil in a small bowl. 3. Rub mixture over pork tenderloin. 4. Roast in the oven for 20-25 minutes. 5. Serve hot.","likes":1}
{"index":{"_index":"recipes","_id":"7"}}
{"name":"Baked Salmon","ingredients":["salmon fillet","lemon","garlic","butter"],"instructions":"1. Preheat oven to 350 degrees. 2. Place salmon fillet on a sheet of aluminum foil. 3. Squeeze lemon over salmon. 4. Melt butter and mix with garlic. 5. Pour butter mixture over salmon. 6. Bake for 20 minutes. 7. Serve hot.","likes":32}
{"index":{"_index":"recipes","_id":"8"}}
{"name":"Tacos","ingredients":["ground beef","taco seasoning","tortilla chips","shredded lettuce","diced tomatoes"],"instructions":"1. Brown ground beef in a skillet. 2. Add taco seasoning and cook according to package directions. 3. Serve over a bed of tortilla chips. 4. Top with shredded lettuce and diced tomatoes. 5. Serve hot.","likes":74}
{"index":{"_index":"recipes","_id":"9"}}
{"name":"Spicy Chicken Curry","ingredients":["chicken breast","curry powder","coconut milk","tomatoes","onion"],"instructions":"1. Cut chicken into cubes and sauté in a large pot. 2. Add onion and cook until translucent. 3. Add curry powder and cook for 1 minute. 4. Add diced tomatoes and coconut milk. 5. Simmer for 20 minutes. 6. Serve hot over rice.","likes":16}
{"index":{"_index":"recipes","_id":"10"}}
{"name":"Creamy Tomato Soup","ingredients":["tomatoes","onion","garlic","heavy cream"],"instructions":"1. Heat olive oil in a large pot. 2. Add chopped onion and garlic and sauté until softened. 3. Add chopped tomatoes and simmer for 15 minutes. 4. Blend soup until smooth. 5. Add heavy cream and simmer for an additional 5 minutes. 6. Serve hot. There is no chicken in tomato soup.","likes":17}

# Search for all recipes which have `chicken` in their name.
# For simplicity, we only return `name` and `ingredients`.
GET /recipes/_search
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

# Q: Why is `Spicy Chicken Curry` ranked lower than `Chicken Enchiladas`
#    Investigate the score using the _explain API
GET /recipes/_explain/3
{
  "query": {
    "match": {
      "name": "chicken"
    }
  }
}
GET /recipes/_explain/9
{
  "query": {
    "match": {
      "name": "chicken"
    }
  }
}

# Actually, there is one more recipe which talks about `chicken`.
# Lets also search on `instructions` for the provided query.
GET /recipes/_search
{
  "query": {
    "multi_match": {
      "query": "chicken",
      "fields": [
        "name", "instructions"
      ]
    }
  },
  "fields": [
    "name", "instructions"
  ],
  "_source": false
}

# Not everyone can spell `Enchiladas``. Fuzziness allows for spell errors.
# How wrong can you spell `Enchiladas` before it is not recognized anymore?
GET /recipes/_search
{
  "query": {
    "fuzzy": {
      "name": {
        "value": "enchiadas",
        "fuzziness": "AUTO"
      }
    }
  },
    "fields": [
    "name"
  ],
  "_source": false
}

# Lets have a closer look on scoring.
# When searching in field `name` only this field is used for scoring.
GET /recipes/_search
{
  "query": {
    "match": {
      "name": "chicken"
    }
  },
  "fields": [
    "name",
    "ingredients",
    "likes"
  ],
  "_source": false
}

# We want to boost results which have a high number of likes. This can be done
# using a `function_score` query. This takes a standard query (`query`) and calculates additional scors
# based on document data (in this case it adds the value of likes * 0.1).
GET /recipes/_search
{
  "query": {
    "function_score": {
      "field_value_factor": {
        "field": "likes",
        "factor": 0.1
      },
      "query": {
        "match": {
          "name": "chicken"
        }
      }
    }
  },
  "fields": [
    "name",
    "ingredients",
    "likes"
  ],
  "_source": false
}

# Remember the example from lab 3 using nested data. Lets have a look on this again.
PUT /books5
{}
POST /books5/_doc
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

# Lets get all editions which were published after 1955 and sold more than 100000 times.
# Actually there is none, so the result should be empty.
GET /books5/_search
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

# Wait what? What went wrong?
# A look on the field `edition` shows how Elasticsearch indexed the data internally.
GET /books5/_search
{
  "fields": [
    "editions.*"
  ],
  "_source": false
}

# It flattened the object, so instead of having an array of objects we have multiple arrays,
# one for each object value. Due to this we lost the relationship between `year` and `sold`
# within `editions`.

# To fix this, we have to declare the field as `nested`. When using `nested`, the object is treated
# as a seperate document in the index. Delete the index, create it with a mapping and do the steps above again.
DELETE /books5
PUT /books5
{
  "mappings": {
    "properties": {
      "editions": {
        "type": "nested"
      }
    }
  }
}

# The `nested` type allows us to create 1-to-many relationships in Elasticsearch. 

# Lets consider an online blog with posts which can be commented. Adding comments as `nested` might be a problem
# because each change in a comment (e.g. when number of likes changes) requires a reindex of the full document.
# For such usecases there is a parent-child join query in Elasticsearch. To use it, a field needs to be declared as `join`.
# Only one `join` field is allowed per index, but you can define multiple types of relations.
PUT posts
{
  "mappings":{
      "properties":{
        "author": {
           "type": "text"
         },
         "text": {
           "type": "text"
         },
         "likes": {
           "type": "integer"
         },
         "content_type":{
            "type": "join",
            "relations": {
               "post": "comment"
            }
         }
      }
   }
}

# Lets add a blog post to the index.
# Note that we hardcode the routing (just needs to be consistent between all)
# The reason for this is that related documents must end up in the same shard.
POST /posts/_doc/0?routing=xyz
{
  "author": "Mr. Author",
  "text": "This blogpost is about Elasticsearch and its amazing search capabilities",
  "likes": 10,
  "content_type": {
    "name": "post"
  }
}

# Now lets add a comment. The document must be in the same index as the parent document (also in same shard).
# Note that we provided the id of the parent element in `content_type`
POST /posts/_doc/1?routing=xyz
{
  "author": "Commentator 1",
  "text": "Isnt this also about aggregation?",
  "likes": 25,
  "content_type": {
    "name": "comment",
    "parent": "0"
  }
}

# Assume we want to get all posts which are about "aggregation".
# In our case, the post itself does not mention it but the comment does. So we want to also retrieve
# the post as it is somehow related to the term "aggregation" (through its comment).
# The following query gives us only the comment, because "aggregation" is not
# mentioned in the post itself.
GET /posts/_search
{
  "query": {
    "match": {
      "text": "aggregation"
    }
  }
}

# If we enforce to only get posts (by adding a logical AND)
# we end up with an empty result.
GET /posts/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "text": "aggregation"
          }
        },
        {
          "match": {
            "content_type": "post"
          }
        }
      ]
    }
  }
}

# But we want to get the blog post, because the comment is talking about "aggregation".
# So lets combine two queries with a logical OR:
# 1. search directly on posts
# 2. search on child documents (comments) but retrieve their associated parent document (post)
# This can be done using the `has_child` query. The query is executed against the children, but the parent is returned.
# You can also specify how many children need to match the query before you consider the parent element.
GET /posts/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "bool": {
            "must": [
              {
                "match": {
                  "text": "aggregation"
                }
              },
              {
                "match": {
                  "content_type": "post"
                }
              }
            ]
          }
        },
        {
          "has_child": {
            "type": "comment",
            "query": {
              "match": {
                "text": "aggregation"
              }
            },
            "min_children": 1
          }
        }
      ]
    }
  }
}

# This also works in the other direction. Lets get all comments which are on
# posts that have more than 10 likes (again, evaluated on parent but the children are returned).
GET /posts/_search
{
  "query": {
    "has_parent": {
      "parent_type": "post",
      "query": {
        "range": {
          "likes": {
            "gte": 10
          }
        }
      }
    }
  }
}

# Lets have a look on Elasticsearch Aggregation capabilities

# We start by adding orders to a new index. Note that we use the customer name as a keyword (like id)
PUT /orders
{
  "mappings": {
    "properties": {
      "customer_name": {
        "type": "keyword"
      }
    }
  }
}
POST /orders/_bulk
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

# Lets start simple: group all the orders by customer.
# Note that we dropped a query statement for simplicity, but usually you want to aggregate search results and not all documents.
# This is a bucket aggregation, the buckets are the different customers.
GET /orders/_search
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

# We can now perform another aggregation on these buckets.
# This is done by adding a nested `aggs` to the request which sums up all values in `total_priece`.
# This is a metric aggregation.
GET /orders/_search
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

# Lets have a look on another bucket aggregation. The following example groups the 
# documents by `order_date` and creates a histogram with a resolution of 1d.
GET /orders/_search
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

# Again, we can extend this by adding a metric aggregation to the bucket which calculates the total revenue for 
# each histogram bin. In addition, we can use `top_hits` aggregation to get the top items of each bucket
# (in our case based on total_price).
GET /orders/_search
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
            "sort": [
              {
                "total_price": {
                  "order": "desc"
                }
              }
            ],
            "size": 2
          }
        }
      }
    }
  }
}

# Top hits can be used also on top-level (outside of buckets), e.g. to 
# show the order with the highest `total_price`.
GET /orders/_search
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
        "sort": [
          {
            "total_price": {
              "order": "desc"
            }
          }
        ],
        "size": 1
      }
    }
  }
}

# Finally, we can also do pipeline aggregations (using the output of one aggregation for the next one).
# Lets assume we want to calculate the maximum average revenue per day for the past week.
# We start by calculating the average revenue for every day. For this we create again a histogram which 
# gives us a bucket with orders for each day. Now we aggregate each bucket by calculating the average.
# Next we use this outcome to get the maximum from it. For this step, we need the `avg_revenue_per_day` value for 
# each bucket from `orders_per_day`. This can be referenced using the `>` operator.
POST /orders/_search
{
  "size": 0,
  "aggs": {
    "orders_per_day": {
      "date_histogram": {
        "field": "order_date",
        "fixed_interval": "1d"
      },
      "aggs": {
        "avg_revenue_per_day": {
          "avg": {
            "field": "total_price"
          }
        }
      }
    },
    "max_avg_revenue_per_week": {
      "max_bucket": {
        "buckets_path": "orders_per_day>avg_revenue_per_day"
      }
    }
  }
}


# Remove data from lab 3
DELETE /recipes
DELETE /books5
DELETE /posts
DELETE /orders