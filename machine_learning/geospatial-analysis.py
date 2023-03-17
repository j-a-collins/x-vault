import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Read the UFO sightings data into a DataFrame
ufo_data = pd.read_csv('../ufo_sighting_data.csv', low_memory=False)

# Drop rows with missing latitude or longitude
ufo_data.dropna(subset=['latitude', 'longitude'], inplace=True)

# Extract latitude and longitude columns
lat_lon = ufo_data[['latitude', 'longitude']]

# Standardize the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(lat_lon)

# Perform K-means clustering
num_clusters = 5
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans_labels = kmeans.fit_predict(scaled_data)

# Add the cluster labels to the original DataFrame
ufo_data['cluster'] = kmeans_labels

# Save the updated DataFrame to a new CSV file
ufo_data.to_csv('../ufo_sighting_data_with_clusters.csv', index=False)
