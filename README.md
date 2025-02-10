# Contact Tracing with Elasticsearch: San Francisco Business & App Scan Data Pipeline

## Overview
This project simulates a contact tracing system using **Python, Elasticsearch, and Streamlit**. It generates, processes, and visualizes business scan data to track user interactions with businesses in San Francisco. The system allows for fast querying and visualization of user-business interactions using an interactive dashboard.

![Data Pipeline](https://github.com/ndomah/Contact-Tracing-with-Elasticsearch/blob/main/img/fig1-workflow.png)

**Key Features:**
- **Data Generation**: Creates **100,000 fake users** and combines them with **10,000 businesses** from a [San Francisco public dataset](https://www.kaggle.com/datasets/san-francisco/sf-registered-business-locations-san-francisco?select=registered-business-locations-san-francisco.csv).
- **Synthetic App Scans**: Simulates **1,000,000 app scans** over three days.
- **Data Processing & Storage**: Stores data efficiently in **Parquet format**.
- **Search & Retrieval**: Indexes data in **Elasticsearch** for fast querying.
- **Interactive Dashboard**: Uses **Streamlit** to visualize businesses, searches, and user scans.

**Tech Stack**
- **Python**: Data generation & processing
- **Pandas**: Data wrangling & transformation
- **Faker**: Generating synthetic user data
- **Elasticsearch**: Searchable datastore for app scans
- **Streamlit**: Interactive dashboard for data visualization
- **Docker**: Running Elasticsearch & Kibana in containers

## Data Schema

This project generates structured JSON data, indexing it in Elasticsearch. Below is the schema used:

![Elasticsearch Schema](https://github.com/ndomah/Contact-Tracing-with-Elasticsearch/blob/main/img/fig3-elasticsearch-schema.png)

## Workflow

**1. Prepare Business Data**
- Run [`01_prepare_sf_data.py`](https://github.com/ndomah/Contact-Tracing-with-Elasticsearch/blob/main/scripts/01_prepare_sf_data.py) to:
  - Load and preprocess San Francisco data from 10,000 businesses
  - Extract location data (latitude/longitude)
  - Filter and clean the dataset
  - Save the preprocessed data as a JSON file 

**2. Generate Fake Users and App Scans**
- Run [`02_create_fake_dataset.py`](https://github.com/ndomah/Contact-Tracing-with-Elasticsearch/blob/main/scripts/02_create_fake_dataset.py) to:
  - Generate 100,000 fake users with names, device IDs, and birthdates
  - Simulate 1,000,000 app scan events over a 3-day period
  - Join users with business data to create a realistic dataset
  - Save the dataset as a compressed Parquet file 

**3. Start Elasticsearch**
- Refer to [`docker-compose.yml`](https://github.com/ndomah/Contact-Tracing-with-Elasticsearch/blob/main/docker-compose.yml)
- Run:
```sh
docker-compose up -d
```

**4. Load Data into Elasticsearch**
- Run [`dev_elasticsearch_client.py`](https://github.com/ndomah/Contact-Tracing-with-Elasticsearch/blob/main/scripts/dev_elasticsearch_client.py) to:
  - Connect to an Elasticsearch instance
  - Upload the processed dataset into an Elasticsearch index (`my_app_scans`)
  - Run basic queries to verify data indexing 

**5. Verify Data**
- Run [`dev_read_fake_dataset.py`](https://github.com/ndomah/Contact-Tracing-with-Elasticsearch/blob/main/scripts/dev_read_fake_dataset.py) to:
  - Read and verify the Parquet dataset
  - Output sample data for validation

**6. Launch the Streamlit Dashboard**
- Run [`streamlit_app.py`](https://github.com/ndomah/Contact-Tracing-with-Elasticsearch/blob/main/scripts/streamlit_app.py) to:
  - Launch a Streamlit dashboard for searching and visualizing data
  - Allows searching by business name, ID, or device ID
  - Displays a map with business locations


## Streamlit Dashboard
This project includes a **fully interactive web-based UI** for exploring the dataset:

![](https://github.com/ndomah/Contact-Tracing-with-Elasticsearch/blob/main/img/streamlit%20app.PNG)

**Features:**
- Search by business name (e.g., "Burger")
- Search by business ID
- Search by device ID
- Map-based visualization of business & scans

## Future Improvements
- **Expand dataset** with more business categories & user behaviors
- **Enhance search features** (e.g., full-text search, geospatial filters)
- **Improve UI** with additional analytics & insights
- **Integrate machine learning** for business recommendations
