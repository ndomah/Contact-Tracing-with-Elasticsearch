import pandas as pd
from pydantic import Json

# Load the previously created Parquet file containing business data.
# Parquet format is used for efficient data storage and retrieval.
dataset = pd.read_parquet("./data/businesses.parquet.gzip")

# (Commented out) Alternative way to load a dataset from a JSON file if needed.
# dataset = pd.read_json("./data/yelp_academic_dataset_business.json", lines=True)

# Print the dataset to verify its contents.
print(dataset)

# Print data types of each column for validation.
print(dataset.dtypes)

# Print the total number of elements in the dataset.
print(dataset.size)

# Count the occurrences of unique business names and print the most common one.
print(dataset.BUSINESS_NAME.value_counts().head(1))

# Extract the first row of the dataset.
my_st = dataset.head(1)

# Convert the extracted row into a JSON-formatted string.
my_json = my_st.to_json(orient='records')

# Print the JSON representation of the first row for verification.
print(my_json)