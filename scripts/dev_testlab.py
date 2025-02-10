from numpy import NaN
import pandas as pd
import json

# Function to safely convert a JSON-like string into a Python dictionary.
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
# This dataset is an error-prone version of the registered business locations dataset.
in_df = pd.read_csv("./data/registered-business-locations-san-francisco-error.csv", converters=converter)

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

# Print the normalized DataFrame for debugging.
print(normalized)

# Create a DataFrame for longitude and latitude extracted from the normalized data.
longlat_df = pd.DataFrame(normalized['coordinates'].to_list(), columns=['longitude', 'latitude'])

# Print extracted longitude and latitude information for verification.
print(longlat_df)

# Merge the original DataFrame with the extracted longitude and latitude information.
merged_df = pd.merge(cleaned_nonan_df, longlat_df, left_index=True, right_index=True)

# Print the shape of the merged DataFrame to verify proper merging.
print(merged_df.shape)

# Print the data types of the merged DataFrame for validation.
print(merged_df.dtypes)

# Print the original "Business Location" column for debugging.
print(in_df['Business Location'])

# Print the merged DataFrame to inspect the final output.
print(merged_df)