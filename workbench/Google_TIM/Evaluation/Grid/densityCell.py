import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
import pandas as pd
import seaborn as sns

cmap = sns.color_palette("YlOrBr", as_cmap=True)

# Load the CSV data
file_path = 'data/gridded_flights_first_100000_rows.csv'  # Change this to your file path
data = pd.read_csv(file_path)

# Convert latitude and longitude from radians to degrees
data['latitude_deg'] = np.degrees(data['latitude_rad'])
data['longitude_deg'] = np.degrees(data['longitude_rad'])

# Discretize the world map into 1°x1° grid using pandas cut
lat_bins = np.arange(-90, 91, 1)
lon_bins = np.arange(-180, 181, 1)

# Assign grid cell labels for latitude and longitude using pd.cut
data['lat_bin'] = pd.cut(data['latitude_deg'], bins=lat_bins, labels=lat_bins[:-1])
data['lon_bin'] = pd.cut(data['longitude_deg'], bins=lon_bins, labels=lon_bins[:-1])

# Count unique flight IDs in each grid cell
flight_density = data.groupby(['lat_bin', 'lon_bin'])['flight_id'].nunique().unstack(fill_value=0)

# Create a figure and axis with the Robinson projection
fig = plt.figure(figsize=(14, 7))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())

# Add coastlines for reference
ax.coastlines()

# Plot flight density on the map
lat_grid, lon_grid = np.meshgrid(lat_bins[:-1], lon_bins[:-1], indexing='ij')

for i in range(flight_density.shape[0]):
    for j in range(flight_density.shape[1]):
        density_value = flight_density.iloc[i, j]
        if density_value > 0:
            normalized_density_value = (density_value - flight_density.min().min()) / (flight_density.max().max() - flight_density.min().min())
            color_density = cmap(normalized_density_value)
            
            # Plot the grid cell as a rectangle filled with the color corresponding to flight density
            ax.add_patch(plt.Rectangle((lon_grid[i, j], lat_grid[i, j]), 1, 1, facecolor=color_density, edgecolor='none', transform=ccrs.PlateCarree()))

# Add colorbar for flight density
sm_density = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=flight_density.min().min(), vmax=flight_density.max().max()))
sm_density.set_array([])
cbar_density = plt.colorbar(sm_density, ax=ax, orientation='vertical', shrink=0.7, pad=0.05)
cbar_density.set_label('Flight Density', rotation=90, fontsize=16, fontname='Times New Roman')

cbar_density.ax.yaxis.set_tick_params(labelsize=16)
for label in cbar_density.ax.get_yticklabels():
    label.set_fontname('Times New Roman')

# Set the extent to global
ax.set_global()

for spine in ax.spines.values():
    spine.set_visible(False)

plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.show()
