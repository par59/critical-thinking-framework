python map.py

import geopandas as gpd
import matplotlib.pyplot as plt

# Load the world map dataset
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Define a list of countries to highlight
highlight_countries = ["United States of America", "India", "Brazil"]

# Create a new column to mark highlighted countries
world["highlight"] = world["name"].apply(lambda x: "red" if x in highlight_countries else "lightblue")

# Plot the map
fig, ax = plt.subplots(figsize=(12, 7))
world.plot(ax=ax, edgecolor="black", color=world["highlight"])

# Add title and labels
ax.set_title("Highlighted Countries: USA, India, and Brazil", fontsize=14)
ax.set_xlabel("Longitude", fontsize=12)
ax.set_ylabel("Latitude", fontsize=12)

# Show the plot
plt.show()
