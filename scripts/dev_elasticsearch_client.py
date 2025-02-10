from elasticsearch import Elasticsearch
import pandas as pd
from pandas import DataFrame
import json
import datetime as datetime

# Initialize a connection to the Elasticsearch instance running locally
es = Elasticsearch("http://localhost:9200")

# Define a search query using "match" to find a business by its business_id
business = {
  "query": {
    "match": {
      "business_id": "1059819-03-161"
    }
  }
}

# Alternative query using "simple_query_string" for a more flexible search
business2 = {
  "query": {
    "simple_query_string": {
      "query": "1059819-03-161",
      "fields": ["business_id"],
      "default_operator": "AND"
    }
  }
}

# Execute the search query on the "my_app_scans" index
res = es.search(index="my_app_scans", body=business2, size=9999)

# Convert the search results into a pandas DataFrame
df = DataFrame.from_dict(res['hits']['hits'])

# Print the shape (number of rows, columns) of the DataFrame
print(df.shape)

'''
# Get the list of all existing indices in Elasticsearch
print(es.indices.get_alias().keys())

# Delete an index (commented out for safety)
# es.indices.delete(index='test-index', ignore=[400, 404])
# print(es.indices.get_alias().keys())

# Retrieve index details
# print(client.indices.get(index="*"))
'''

# Define a query to search for records by "deviceID"
query_body = {
    "query": {
        "match": {
            "deviceID": 5167915669906
        } 
    } 
}

# Execute the search query on the "my_app_scans" index
res = es.search(index="my_app_scans", body=query_body)

# Convert the search results into a normalized pandas DataFrame
df = pd.json_normalize(res['hits']['hits'])

# Print the DataFrame and its data types for verification
print(df)
print(df.dtypes)

# Extract and print latitude from the search results
print(df.iloc[0]['_source.latitude'])

# Convert a Unix timestamp to a readable datetime format
time = datetime.datetime.fromtimestamp(867974400000000 / 1000000)
print(time)

#################################
# Additional Elasticsearch query to find businesses by postal code

my_query = {
    "match": {
        "postal_code": "30340"
    } 
}

# Execute the search query on the "my_app_scans" index
res = es.search(index="my_app_scans", query=my_query, size=9999)

# Convert the search results into a normalized pandas DataFrame
df = pd.json_normalize(res['hits']['hits'])

# Remove duplicate business entries based on business_id
df = df.drop_duplicates(subset=['_source.business_id'])

# Print the cleaned DataFrame
print(df)

'''
# Query for retrieving all postal codes (commented out for now)
res = es.search(index="my_app_scans", body=all_postal_codes, size=9999)

df_zip = pd.json_normalize(res['hits']['hits'])

print(df_zip['_source.postal_code'])
'''