import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from csv import DictReader, DictWriter

def read_pm_coordinates():
  with open('/content/pm_data (3).csv', "r") as f:
        return list(DictReader(f))

data=read_pm_coordinates()



# Create a GeoDataFrame

for entry in data:
    entry['PM'] = float(entry['PM'])

# Create geometry points
geometry = [Point(float(entry['Longitude']), float(entry['Latitude'])) for entry in data]

# Create a GeoDataFrame
gdf = gpd.GeoDataFrame(data, geometry=geometry)

# Create a Matplotlib figure and subplots
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(6, 10))

# Plot the geographical points on the first subplot (map)
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))  # Load world map data
world.plot(ax=ax1, color='yellow')  # Plot world map
gdf.plot(ax=ax1, color='blue', markersize=gdf['PM'] * 1, marker='*', alpha=0.8)  # Plot points with adjusted marker size based on PM values
ax1.set_title('Geographical Points with PM Data')
ax1.set_xlabel('Longitude')
ax1.set_ylabel('Latitude')

# Plot the PM values on the second subplot (graph)
ax2.bar([entry['City'] for entry in data], [entry['PM'] for entry in data], color='green')  # Plot PM values as a bar graph with city names as x-axis tick labels
ax2.set_title('PM Values')
ax2.set_xlabel('City')
ax2.set_ylabel('PM')

# Rotate x-axis labels for better visibility
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Adjust layout
plt.tight_layout()

# Show the plot
plt.show()



