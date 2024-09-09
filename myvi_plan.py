import requests
import pandas as pd
import numpy as np

# URL to scrape
url = "https://www.myvi.in/bin/vodafoneideadigital/servlet/Etopup/pack.0014.json"

# Step 1: Fetch data from the URL
response = requests.get(url)
data = response.json()  # Parse JSON data

# Step 2: Convert JSON data to pandas DataFrame
# Assuming the JSON is a list of dictionaries
df = pd.DataFrame(data)

# Step 3: Display the DataFrame
print(df.head())  # Display the first few rows

# Convert UNIT_COST to numeric (handling strings)
df = pd.DataFrame(data)
df['UNIT_COST'] = pd.to_numeric(df['UNIT_COST'], errors='coerce')

# Step 1: Clean the 'WEB-VALIDITY' column
def clean_validity(val):
    if 'Month' in val:
        return 28  # Assuming 1 Month = 28 Days
    elif 'Days' in val or 'days' in val or 'Day' in val:
        return int(val.split()[0])  # Extract the numeric part
    else:
        return np.nan  # Set NA as NaN

# Apply the function to clean the validity column
df['validity_days'] = df['WEB-VALIDITY'].apply(clean_validity)

# Step 2: Calculate cost per day (ignore NaN validity)
df['cost_per_day'] = df['UNIT_COST'] / df['validity_days']

# Step 3: Sort by 'cost_per_day'
df_sorted = df.sort_values(by='cost_per_day')
df_sorted.to_csv('myvi_sorted.csv', index=False)

# import matplotlib.pyplot as plt

# # Select columns for visualization
# x = df_sorted['UNIT_COST']
# y = df_sorted['validity_days']

# # Create a scatter plot
# plt.figure(figsize=(10, 6))  # Adjust figure size as needed
# plt.scatter(x, y)
# plt.xlabel('UNIT_COST')
# plt.ylabel('validity_days')
# plt.title('Scatter Plot of UNIT_COST vs validity_days')
# plt.grid(True)
# plt.show()