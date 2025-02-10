from numpy import NaN
import pandas as pd
import json

# Function to safely convert a JSON string into a Python dictionary.
# If conversion fails, it returns NaN instead of raising an error.
def my_convert_json(value):
    try:
        return json.loads(value)
    except:
        return NaN

# Define a dictionary of converters for reading the CSV file.
# The "Business Location" field contains JSON-like strings but uses single quotes (' instead of ").
# This converter replaces single quotes with double quotes to make it valid JSON.
converter = {"Business Location": lambda x: x.replace("\'", "\"")}

# Read the CSV file while applying the converter to the "Business Location" column.
in_df = pd.read_csv("./data/registered-business-locations-san-francisco-original.csv", converters=converter)

# Convert the "Business Location" column from a JSON-like string to an actual JSON object.
# This is necessary for later normalization.
in_df['Business Location'] = in_df['Business Location'].map(lambda x: my_convert_json(x))

# Select only relevant columns from the dataset.
filtered_df = in_df[['Location Id', 'DBA Name', 'Street Address', 'City', 'Source Zipcode', 'Business Location']]

# Remove rows that contain NaN values and reset the index to maintain proper alignment.
cleaned_nonan_df = filtered_df.dropna().reset_index()

# Normalize the "Business Location" JSON field to extract latitude and longitude.
normalized = pd.json_normalize(cleaned_nonan_df['Business Location'], max_level=1)

# Print the data types of the normalized columns to verify correct processing.
print(normalized.dtypes)

# Create a DataFrame for longitude and latitude extracted from the normalized data.
longlat_df = pd.DataFrame(normalized['coordinates'].to_list(), columns=['longitude', 'latitude'])

# Print data types again for verification.
print(normalized.dtypes)

# Merge the original DataFrame with the extracted longitude and latitude information.
merged_df = pd.merge(cleaned_nonan_df, longlat_df, left_index=True, right_index=True)

# Keep only the necessary columns, including the extracted latitude and longitude.
filtered_df = merged_df[['Location Id', 'DBA Name', 'Street Address', 'City', 'Source Zipcode', 'latitude', 'longitude']]

# Display a count of businesses by city to verify data integrity.
print(filtered_df['City'].value_counts())

# Filter only businesses located in San Francisco.
sf_data = filtered_df.loc[filtered_df['City'] == 'San Francisco']

# Randomly select 10,000 businesses from the dataset.
sf_data = sf_data.sample(n=10000)

# Rename columns to standardize naming conventions.
ex_df = sf_data.rename(columns={
    'Location Id': 'business_id',
    'DBA Name': 'business_name',
    'Street Address': 'business_address',
    'City': 'city',
    'Source Zipcode': 'zip',
})

# Print the final processed DataFrame for verification.
print(ex_df)

# Save the cleaned data to a JSON file in a line-separated format.
ex_df.to_json('./data/sf_businesses.json', lines=True, orient='records')