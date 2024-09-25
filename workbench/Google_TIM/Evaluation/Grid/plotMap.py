import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np

# Create a figure and axis with the Robinson projection
fig = plt.figure(figsize=(10, 5))
ax = plt.axes(projection=ccrs.Robinson())

# Add coastlines for reference
ax.coastlines()

# Add gridlines with intervals of 2 degrees for both latitude and longitude
gl = ax.gridlines(draw_labels=True, crs=ccrs.PlateCarree(), linewidth=0.5, color='gray', linestyle='--')
gl.xlocator = plt.MultipleLocator(2)  # 2 degrees spacing for longitude
gl.ylocator = plt.MultipleLocator(2)  # 2 degrees spacing for latitude

# Turn off top and right labels
gl.top_labels = False
gl.right_labels = False

# Turn off x and y axis
ax.axis('off')

# Define the latitudes and longitudes for the grid cells
lat_grid = np.arange(-90, 90, 2)
lon_grid = np.arange(-180, 180, 2)

# Plot centroids of each grid cell
for lat in lat_grid + 1:  # Centroid latitude is the middle of the 2° grid cell
    for lon in lon_grid + 1:  # Centroid longitude is the middle of the 2° grid cell
        ax.plot(lon, lat, marker='o', color='red', transform=ccrs.PlateCarree())

# Display the map
plt.title('World Map with 2°x2° Grid and Centroids (Robinson Projection, Axes Off)')
plt.show()