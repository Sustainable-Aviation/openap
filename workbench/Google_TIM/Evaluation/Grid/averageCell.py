import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
import pandas as pd

# Load the CSV data
file_path = 'data/gridded_flights_first_100000_rows.csv'  # Change this to your file path
data = pd.read_csv(file_path)

# Convert latitude and longitude from radians to degrees
data['latitude_deg'] = np.degrees(data['latitude_rad'])
data['longitude_deg'] = np.degrees(data['longitude_rad'])

# Conversion factor from meters to feet
meters_to_feet = 3.28084

# Discretize the world map into 1°x1° grid (instead of 2°x2°)
lat_grid = np.arange(-90, 90, 1)
lon_grid = np.arange(-180, 180, 1)

# Create a figure and axis with the Robinson projection
fig = plt.figure(figsize=(12, 6))
#ax = plt.axes(projection=ccrs.PlateCarree())  # Switch to PlateCarree for easier zooming
ax = plt.axes(projection=ccrs.PlateCarree())

# Add coastlines for reference
ax.coastlines()

# Add gridlines with intervals of 1 degree for both latitude and longitude
gl = ax.gridlines(draw_labels=False, crs=ccrs.PlateCarree(), linewidth=0.01, color='gray', linestyle='--')
gl.xlocator = plt.MultipleLocator(1)  # 1 degrees spacing for longitude
gl.ylocator = plt.MultipleLocator(1)  # 1 degrees spacing for latitude

# Turn off top and right labels
gl.top_labels = False
gl.right_labels = False

# Turn off x and y axis
ax.axis('off')

# Create a color map for altitudes
cmap = plt.cm.get_cmap('coolwarm')

# Create a list to store average altitudes for the colorbar
average_altitudes = []

# Compute average altitudes for all cells first, converting to feet
for lat in lat_grid:  # Latitude for each grid cell
    for lon in lon_grid:  # Longitude for each grid cell
        # Find all points within the current grid cell
        in_cell = data[
            (data['latitude_deg'] >= lat) & (data['latitude_deg'] < lat + 1) &
            (data['longitude_deg'] >= lon) & (data['longitude_deg'] < lon + 1)
        ]
        
        if len(in_cell) > 0:
            # Compute the average altitude in meters, then convert to feet
            average_altitude_meters = in_cell['altitude_AF_m'].mean()
            average_altitude_feet = average_altitude_meters * meters_to_feet
            average_altitudes.append(average_altitude_feet)
            
            # Debug: Print the latitude, longitude, and average altitude in feet
            print(f"Grid cell ({lat}, {lon}) - Avg Altitude: {average_altitude_feet:.2f} feet")

# Ensure there are no division by zero errors in normalization
if len(average_altitudes) > 0:
    altitude_min = min(average_altitudes)
    altitude_max = max(average_altitudes)
    altitude_range = altitude_max - altitude_min

    # Plot average altitude for each grid cell
    for lat in lat_grid:  # Latitude for each grid cell
        for lon in lon_grid:  # Longitude for each grid cell
            # Find all points within the current grid cell
            in_cell = data[
                (data['latitude_deg'] >= lat) & (data['latitude_deg'] < lat + 1) &
                (data['longitude_deg'] >= lon) & (data['longitude_deg'] < lon + 1)
            ]
            
            if len(in_cell) > 0:
                # Compute the average altitude in meters, then convert to feet
                average_altitude_meters = in_cell['altitude_AF_m'].mean()
                average_altitude_feet = average_altitude_meters * meters_to_feet
                
                # Normalize the value for color mapping
                if altitude_range != 0:
                    normalized_value = (average_altitude_feet - altitude_min) / altitude_range
                else:
                    normalized_value = 0.5  # Default to mid-range if all altitudes are the same
                
                color = cmap(normalized_value)
                
                # Plot the grid cell as a rectangle filled with the color corresponding to average altitude in feet
                ax.add_patch(plt.Rectangle((lon, lat), 1, 1, facecolor=color, edgecolor='none', transform=ccrs.PlateCarree()))

                # Add a marker at the center of the cell for better visibility
                #ax.plot(lon + 0.5, lat + 0.5, marker='o', color='black', markersize=2, transform=ccrs.PlateCarree())

    # Add a colorbar to the plot
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=altitude_min, vmax=altitude_max))
    sm.set_array([])  # Set a dummy array for colorbar
    cbar = plt.colorbar(sm, ax=ax, orientation='vertical', shrink=0.7, pad=0.05)
    cbar.set_label('Average Flight Altitude (feet)', rotation=90)

    # Zoom in to the region where data exists
    #ax.set_extent([-50, 30, -10, 30], crs=ccrs.PlateCarree())  # Adjust according to data points
    # Set the extent to global (show the entire world)
    ax.set_global()

    # Display the map
    plt.title('Average Flight Altitude per 1°x1° Grid Cell (Feet)')
    plt.show()

else:
    print("No valid altitude data found.")
