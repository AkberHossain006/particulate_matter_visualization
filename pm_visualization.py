import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

# Sample data (latitude, longitude, PM values)
data = {
    'latitude': [28.6517178, 18.9387711, 31.2253441, 40.7128, 34.0522, 51.5074],  # Example latitudes (New York, Los Angeles, London)
    'longitude': [77.2219388, 72.8353355, 121.4888922, -74.0060, -118.2437, -0.1278],  # Example longitudes
    'PM': [20, 15, 25, 11, 17,13],  # Example PM values
    'city': ['Delhi', 'Mumbai', 'Shanghai', 'New York', 'Los Angeles', 'London']  # City names
}

# Create a GeoDataFrame
geometry = [Point(lon, lat) for lat, lon in zip(data['latitude'], data['longitude'])]
gdf = gpd.GeoDataFrame(data, geometry=geometry)

# Create a Matplotlib figure and subplots
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(6, 10))

# Plot the geographical points on the first subplot (map)
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))  # Load world map data
world.plot(ax=ax1, color='yellow')  # Plot world map
gdf.plot(ax=ax1, color='blue', markersize=gdf['PM'] * 5, marker='*', alpha=0.8)  # Plot points with adjusted marker size based on PM values
ax1.set_title('Geographical Points with PM Data')
ax1.set_xlabel('Longitude')
ax1.set_ylabel('Latitude')

# Plot the PM values on the second subplot (graph)
ax2.bar(data['city'], data['PM'], color='green')  # Plot PM values as a bar graph with city names as x-axis tick labels
ax2.set_title('PM Values')
ax2.set_xlabel('City')
ax2.set_ylabel('PM')

# Rotate x-axis labels for better visibility
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Adjust layout
plt.tight_layout()

# Show the plot
plt.show()
