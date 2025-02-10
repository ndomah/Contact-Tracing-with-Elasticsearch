import streamlit as st
import pandas as pd
from elasticsearch import Elasticsearch
from pandas.io.json import json_normalize
from streamlit_folium import folium_static
import folium
import datetime as datetime

# Connect to the Elasticsearch instance running locally
es = Elasticsearch("http://localhost:9200")

# Configure Streamlit layout to use the full width of the screen
st.set_page_config(layout="wide")

# Add a title to the sidebar
st.sidebar.title('San Francisco App Scan Tracker')

######################## Free Text Search ########################

# Input field for free text search in the sidebar
text = st.sidebar.text_input("Free Text Search")

# If the user enters text, execute the search
if text:
    # Define a query that searches across all fields using a simple query string
    query_body = {
        "query": {
            "simple_query_string": {
                "query": text
            }
        }
    }

    # Perform the search on the Elasticsearch index "my_app_scans"
    res = es.search(index="my_app_scans", body=query_body, size=1000)

    # Convert search results into a DataFrame
    df = pd.json_normalize(res['hits']['hits'])

    # Remove duplicate businesses based on "business_id"
    df = df.drop_duplicates(subset=['_source.business_id'])

    # Rename latitude and longitude columns for mapping
    df = df.rename(columns={"_source.latitude": "latitude", "_source.longitude": "longitude"})

    # Select relevant columns for display
    df = df.filter(items=['_source.business_id', '_source.business_name', '_source.business_address', 'latitude', 'longitude', '_source.zip'])

    # Display search results as a table with a header
    st.header(f"Businesses for search: {text}")

    # Format table with readable column names
    table_df = df.rename(columns={
        "_source.business_id": "Business ID",
        "_source.business_name": "Name",
        "_source.business_address": "Address",
        "_source.zip": "Postal Code"
    })

    # Show the table in Streamlit
    st.dataframe(data=table_df)

    # Display an interactive map with business locations
    map = folium.Map(location=[df.iloc[0]['latitude'], df.iloc[0]['longitude']], zoom_start=13)

    # Add markers for each business on the map
    for index, row in df.iterrows():
        folium.Marker(
            [row['latitude'], row['longitude']],
            popup=f"{row['_source.business_name']} <br> ID= {row['_source.business_id']}"
        ).add_to(map)

    # Render the map in Streamlit
    folium_static(map)

######################## Search by Postal Code ########################

# Input field for searching businesses by postal code
postal_code = st.sidebar.text_input("Zip Code")

# Display a link to all San Francisco zip codes
link = "[All San Francisco Zip codes](https://www.usmapguide.com/california/san-francisco-zip-code-map/)"
st.sidebar.markdown(link, unsafe_allow_html=False)

# Add a separator in the sidebar
st.sidebar.markdown("---", unsafe_allow_html=False)

# If a postal code is entered, execute the search
if postal_code:
    # Define a query that searches for businesses by zip code
    query_body = {
        "query": {
            "match": {
                "zip": postal_code
            }
        }
    }

    # Perform the search on Elasticsearch
    res = es.search(index="my_app_scans", body=query_body, size=1000)

    # Convert search results into a DataFrame
    df = pd.json_normalize(res['hits']['hits'])

    # Remove duplicate businesses based on "business_id"
    df = df.drop_duplicates(subset=['_source.business_id'])

    # Rename latitude and longitude columns for mapping
    df = df.rename(columns={"_source.latitude": "latitude", "_source.longitude": "longitude"})

    # Select relevant columns for display
    df = df.filter(items=['_source.business_id', '_source.business_name', '_source.business_address', 'latitude', 'longitude', '_source.zip'])

    # Display search results as a table
    st.header("Businesses in Postal Code")

    # Format table with readable column names
    table_df = df.rename(columns={
        "_source.business_id": "Business ID",
        "_source.business_name": "Name",
        "_source.business_address": "Address",
        "_source.zip": "Postal Code"
    })

    # Show the table in Streamlit
    st.dataframe(data=table_df)

    # Display an interactive map with business locations
    m = folium.Map(location=[df.iloc[0]['latitude'], df.iloc[0]['longitude']], zoom_start=13)

    # Add markers for each business on the map
    for index, row in df.iterrows():
        folium.Marker(
            [row['latitude'], row['longitude']],
            popup=f"{row['_source.business_name']} <br> ID= {row['_source.business_id']}"
        ).add_to(m)

    # Render the map in Streamlit
    folium_static(m)

######################## Search by Business ID ########################

# Input field for searching a business by its ID
business_id = st.sidebar.text_input("Business ID")

if business_id:
    # Define a query to search for businesses by business_id
    query_body = {
        "query": {
            "simple_query_string": {
                "query": business_id,
                "fields": ["business_id"],
                "default_operator": "AND"
            }
        }
    }

    # Perform the search on Elasticsearch
    res = es.search(index="my_app_scans", body=query_body, size=10000)

    # Convert search results into a DataFrame
    df = pd.json_normalize(res['hits']['hits'])

    # Select relevant columns for display
    table_df = df.filter(items=['_source.scan_timestamp', '_source.deviceID', '_source.user_name', '_source.user_birth_date'])

    # Convert Unix timestamps to human-readable format
    table_df['_source.user_birth_date'] = table_df['_source.user_birth_date'].apply(lambda s: datetime.datetime.fromtimestamp(s / 1000000).strftime("%Y/%m/%d"))
    table_df['_source.scan_timestamp'] = table_df['_source.scan_timestamp'].apply(lambda s: datetime.datetime.fromtimestamp(s / 1000000).strftime("%Y/%m/%d %H:%M:%S"))

    # Sort scan events by timestamp
    table_df = table_df.sort_values(by=['_source.scan_timestamp'])

    # Format table with readable column names
    table_df = table_df.rename(columns={
        "_source.scan_timestamp": "Scan Timestamp",
        "_source.deviceID": "Device ID",
        "_source.user_name": "User Name",
        "_source.user_birth_date": "Birth Date"
    })

    # Display search results as a table
    st.header(f"Users scanned at this business: {business_id}")
    st.dataframe(data=table_df)

######################## Search by Device ID ########################

# Input field for searching user activity by device ID
device_id = st.sidebar.text_input("Device ID")

if device_id:
    # Define a query to search for scans by device ID
    query_body = {
        "query": {
            "match": {
                "deviceID": device_id
            }
        }
    }

    # Perform the search on Elasticsearch
    res = es.search(index="my_app_scans", body=query_body, size=1000)

    # Convert search results into a DataFrame
    df = pd.json_normalize(res['hits']['hits'])

    # Rename latitude and longitude columns for mapping
    df = df.rename(columns={"_source.latitude": "latitude", "_source.longitude": "longitude"})

    # Convert timestamps to human-readable format
    df['_source.scan_timestamp'] = df['_source.scan_timestamp'].apply(lambda s: datetime.datetime.fromtimestamp(s / 1000000).strftime("%Y/%m/%d %H:%M:%S"))

    # Select relevant columns for display
    table_df = df.filter(items=['_source.scan_timestamp', '_source.business_id', '_source.business_name', '_source.business_address', 'longitude', 'latitude'])

    # Sort scan events by timestamp
    table_df = table_df.sort_values('_source.scan_timestamp')

    # Display results as a table
    st.header(f"User scans for user: {device_id}")
    st.dataframe(data=table_df)