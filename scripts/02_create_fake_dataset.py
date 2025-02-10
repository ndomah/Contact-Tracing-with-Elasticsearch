import faker
import pandas as pd
import numpy as np
from random import randrange
import datetime as datetime
from datetime import timedelta

# Initialize the Faker library to generate synthetic data
Faker = faker.Factory().create
fake = Faker()

# Define the number of fake users to generate (100,000)
n = 100000

# Generate a DataFrame of fake user data, including:
# - Name
# - State
# - Birth date (between ages 18 and 65)
# - Device ID (MSISDN, a mobile identifier)
faker_data = pd.DataFrame([
    [fake.name(), 
     fake.state(),
     fake.date_of_birth(minimum_age=18, maximum_age=65),
     fake.msisdn()
    ] 
    for _ in range(n)
], columns=['user_name', 'user_state', 'user_birth_date', 'deviceID'])

# Assign a unique user_id to each generated user
faker_data['user_id'] = range(1, 1+len(faker_data))

# Display the first 30 rows and the data types for verification
print(faker_data.head(30))
print(faker_data.dtypes)

# Convert the DataFrame to appropriate data types
faker_data = faker_data.convert_dtypes()

# Ensure user_id is stored as an integer
faker_data = faker_data.astype({'user_id': 'int64'})

# Convert birth date to a proper datetime format
faker_data['user_birth_date'] = pd.to_datetime(faker_data['user_birth_date'])
print(faker_data.dtypes)

# Read the businesses dataset generated in `01_prepare_sf_data.py` (contains 10,000 rows)
businesses = pd.read_json("./data/sf_businesses.json", lines=True)

# Display the businesses dataset and its data types for verification
print(businesses)
print(businesses.dtypes)

# Replicate the businesses dataset 100 times to create 1,000,000 records
# This simulates multiple user interactions with businesses
df_repeated = pd.concat([businesses] * 100, ignore_index=True)

# Display the shape of the new dataset to confirm the expansion
print(df_repeated.shape)

# Assign each row a random user_id between 1 and 100,000
df_repeated['user_id'] = np.random.randint(1, 100000, df_repeated.shape[0])

# Display data types and contents of the repeated dataset
print(df_repeated.dtypes)
print(df_repeated)

# Join the user data with the business dataset based on user_id
df_repeated2 = df_repeated.merge(faker_data, on="user_id", how='left')

# Display the merged dataset for verification
print(df_repeated2)
print(df_repeated2.dtypes)

# Function to generate a random timestamp within a given range (January 1-3, 2022)
def random_date():
    """
    This function returns a random datetime between two specified datetime objects.
    """
    start = datetime.datetime.strptime('2022-01-01 12:00 AM', '%Y-%m-%d %I:%M %p')
    end = datetime.datetime.strptime('2022-01-03 11:55 PM', '%Y-%m-%d %I:%M %p')

    # Compute the total duration in seconds
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds

    # Generate a random second within the range
    random_second = randrange(int_delta)

    return start + timedelta(seconds=random_second)

# Assign a random scan timestamp to each business scan event
df_repeated2['scan_timestamp'] = df_repeated2['business_name'].apply(lambda s: random_date())

# Display the dataset after adding the timestamp
print(df_repeated2)

# Drop the user_id column as it is no longer needed after merging
df_repeated2 = df_repeated2.drop('user_id', axis=1)

# Display the updated data types for verification
print(df_repeated2.dtypes)

# Print a single row as a JSON object for debugging
print(df_repeated2.head(1).to_json())

# Save the dataset as a compressed Parquet file for efficient storage and retrieval
df_repeated2.to_parquet('./data/sf_appscans.parquet.gzip', compression='gzip')

# Optional: Save the dataset in JSON format if needed
# df_repeated2.to_json('./data/sf_fakedataset.json', lines=True, orient='records')