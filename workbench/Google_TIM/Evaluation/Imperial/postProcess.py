import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import csv
from matplotlib.colors import Normalize

plt.style.use('seaborn-deep')

def plot_map_altitude(df_sum, df_wyp):

    """
    Plots a map visualization of flight paths with altitude data on a Robinson projection.

    This function takes two dataframes, one containing a summary of flights and another with waypoints including latitude, longitude, and altitude data. It iterates through the flight summary dataframe, filters waypoints for each flight, and plots them on a Robinson projection map with altitude data color-coded. The function also handles a large number of flights by breaking the loop after 200,000 iterations for debugging or performance reasons.

    Parameters:
    df_flight_summary (pd.DataFrame): A dataframe containing a summary of flights. Each row represents a flight and must include a 'flight_id'.
    df_flight_waypoint (pd.DataFrame): A dataframe containing waypoints data. Each row must include 'flight_id', 'latitude', 'longitude', and 'altitude_ft' for each waypoint.

    Returns:
    None: The function directly displays the plot and saves it as a PNG file.

    Side effects:
    - The plot is displayed using plt.show().
    - A PNG file is saved to 'Output/Plots/Map_altitude.png'.
    - Uses CartoPy for the map projection, which requires an active internet connection for map features.
    - Modifies matplotlib's global figure and savefig DPI settings which may affect other plots.

    Examples:
    >>> df_summary = pd.read_parquet('path/to/flight_summary.parquet')
    >>> df_waypoints = pd.read_parquet('path/to/flight_waypoints.parquet')
    >>> plot_map_altitude(df_summary, df_waypoints)
    """

    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())

    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    #ax.add_feature(cfeature.OCEAN, alpha=0.1)
    #ax.add_feature(cfeature.LAKES, alpha=0.5)
    #ax.add_feature(cfeature.RIVERS)

    # Remove bounding box/spines
    for spine in ax.spines.values():
        spine.set_visible(False)

    count = 0

    # Loop over each flight in the summary DataFrame
    for index, row in df_sum.iterrows():
        flight_id = row['flight_id']  # Adjust this line if the column name in your data is different

        # Toggle conditon for debug
        if count > 200000:
            break

        # Filter the waypoints DataFrame for rows where the flight_id matches
        matching_rows = df_wyp[df_wyp['flight_id'] == flight_id]

        if not matching_rows.empty:
            latitude = matching_rows['latitude']
            longitude = matching_rows['longitude']
            altitude = matching_rows['altitude_ft']

        # Normalize the altitude values to a range between 0 and 1 for coloring
        norm = plt.Normalize(altitude.min(), altitude.max())
        cmap = plt.cm.viridis  # Color map

        # Scatter plot for latitude and longitude data, color-coded by altitude
        sc = ax.scatter(longitude, latitude, c=altitude, cmap=cmap, norm=norm, transform=ccrs.Geodetic(), marker='o', s =1)

        count = count + 1
    #end for loop

    cbar = plt.colorbar(sc, ax=ax, orientation='vertical', fraction=0.02, pad=0.02)
    cbar.set_label('Altitude (feet)', fontsize=20, fontname = "Times New Roman")

    # Customize colorbar tick labels
    cbar.ax.tick_params(labelsize=18)  # Set font size of the colorbar tick labels

    for label in cbar.ax.get_yticklabels():
        label.set_family("Times New Roman")



    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['savefig.dpi'] = 300
    plt.savefig('Output/Plots/Map_altitude.png')

    plt.show()
#end


def plot_map_totalDistance(df_sum, df_wyp):

    """
    Plots a map visualization of flight paths with total ground track distance data on a Robinson projection.

    This function takes two dataframes, one containing a summary of flights and another with waypoints including latitude, longitude, and altitude data. It iterates through the flight summary dataframe, filters waypoints for each flight, and plots them on a Robinson projection map with altitude data color-coded. The function also handles a large number of flights by breaking the loop after 200,000 iterations for debugging or performance reasons.

    Parameters:
    df_flight_summary (pd.DataFrame): A dataframe containing a summary of flights. Each row represents a flight and must include a 'flight_id'.
    df_flight_waypoint (pd.DataFrame): A dataframe containing waypoints data. Each row must include 'flight_id', 'latitude', 'longitude', and 'altitude_ft' for each waypoint.

    Returns:
    None: The function directly displays the plot and saves it as a PNG file.

    Side effects:
    - The plot is displayed using plt.show().
    - A PNG file is saved to 'Output/Plots/Map_altitude.png'.
    - Uses CartoPy for the map projection, which requires an active internet connection for map features.
    - Modifies matplotlib's global figure and savefig DPI settings which may affect other plots.

    Examples:
    >>> df_summary = pd.read_parquet('path/to/flight_summary.parquet')
    >>> df_waypoints = pd.read_parquet('path/to/flight_waypoints.parquet')
    >>> plot_map_altitude(df_summary, df_waypoints)
    """

    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())

    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    #ax.add_feature(cfeature.OCEAN, alpha=0.1)
    #ax.add_feature(cfeature.LAKES, alpha=0.5)
    #ax.add_feature(cfeature.RIVERS)

    # Remove bounding box/spines
    for spine in ax.spines.values():
        spine.set_visible(False)

    count = 0

    # Loop over each flight in the summary DataFrame
    for index, row in df_sum.iterrows():
        flight_id = row['flight_id']  # Adjust this line if the column name in your data is different

        # Toggle conditon for debug
        if count > 200000:
            break

        # Filter the waypoints DataFrame for rows where the flight_id matches
        matching_rows = df_wyp[df_wyp['flight_id'] == flight_id]

        if not matching_rows.empty:
            latitude = matching_rows['latitude']
            longitude = matching_rows['longitude']
            altitude = matching_rows['altitude_ft']

        # Normalize the altitude values to a range between 0 and 1 for coloring
        norm = plt.Normalize(altitude.min(), altitude.max())
        cmap = plt.cm.viridis  # Color map

        # Scatter plot for latitude and longitude data, color-coded by altitude
        sc = ax.scatter(longitude, latitude, c=altitude, cmap=cmap, norm=norm, transform=ccrs.Geodetic(), marker='o', s =1)

        count = count + 1
    #end for loop

    cbar = plt.colorbar(sc, ax=ax, orientation='vertical', fraction=0.02, pad=0.02)
    cbar.set_label('Altitude (feet)', fontsize=20, fontname = "Times New Roman")

    # Customize colorbar tick labels
    cbar.ax.tick_params(labelsize=18)  # Set font size of the colorbar tick labels

    for label in cbar.ax.get_yticklabels():
        label.set_family("Times New Roman")



    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['savefig.dpi'] = 300
    plt.savefig('Output/Plots/Map_tractDistance.png')

    plt.show()
#end

def plot_distance_bin(df_sum):

    """
    Plot a histogram of the total distance traveled by flights, converted from kilometers to nautical miles.

    This function checks if the DataFrame `df_sum` contains a column named 'total_distance_km'. If present, it converts these distances into nautical miles and then plots a histogram of these distances. The plot customizes various visual elements for clarity and aesthetics, including font styles and sizes, spine thickness, and histogram color and edges. The resulting plot is saved as a high-resolution PNG file and also displayed.

    Parameters:
    df_sum (pd.DataFrame): DataFrame containing the flight summary data. Must include a column 'total_distance_km' which contains the distances traveled by flights in kilometers.

    Returns:
    None: This function does not return any values. It directly saves and displays a plot.

    Raises:
    KeyError: If 'total_distance_km' does not exist in df_sum, the function will not perform the conversion or plotting and will finish without altering the state.

    Side Effects:
    - Modifies the global matplotlib DPI settings which may affect other plots.
    - Saves a PNG file to 'Output/Plots/Distance_bin.png'.
    - Displays the plot using plt.show().

    Example:
    >>> df_summary = pd.read_parquet('path/to/flight_summary.parquet')
    >>> plot_distance_bin(df_summary)
    """

    if 'total_distance_km' in df_sum.columns:

        df_sum['total_distance_nm'] = df_sum['total_distance_km'] * 0.539957

        fig1 = plt.figure()
        ax1 = fig1.gca()

        plt.hist(df_sum['total_distance_nm'], bins=30, color='C0', edgecolor='black')
        #plt.title('Frequency Distribution of Total Distance Travelled by Flights')
        plt.xlabel('Distance (nmi)' ,fontname = "Times New Roman", fontsize = 20)
        plt.ylabel('Frequency',  fontname = "Times New Roman", fontsize = 20)

        for axis in ['top', 'bottom', 'left', 'right']:
            ax1.spines[axis].set_linewidth(1.5)

        # Modify axes ticks properties
        plt.xticks(fontname="Times New Roman", fontsize=20)
        plt.yticks(fontname="Times New Roman", fontsize=20)

        plt.xlim([0, 9000])

        F = plt.gcf()
        Size = F.get_size_inches()
        F.set_size_inches(Size[0]*1.7, Size[1]*1.5, forward=True)


        plt.rcParams['figure.dpi'] = 300
        plt.rcParams['savefig.dpi'] = 300
        plt.savefig('Output/Plots/Distance_bin.png')

        plt.show()


import pandas as pd
import matplotlib.pyplot as plt

def plot_distance_bin_actype(df_sum, actype):
    """
    Plot a histogram of the total distance traveled by flights, converted from kilometers to nautical miles,
    and plot a specific histogram for A319 aircraft type.

    Parameters:
    df_sum (pd.DataFrame): DataFrame containing the flight summary data. Must include columns 'total_distance_km' and 'aircraft_type'.

    Returns:
    None: This function does not return any values. It directly saves and displays a plot.

    Raises:
    KeyError: If 'total_distance_km' or 'aircraft_type' does not exist in df_sum, the function will not perform the conversion or plotting and will finish without altering the state.

    Side Effects:
    - Modifies the global matplotlib DPI settings which may affect other plots.
    - Saves a PNG file to 'Output/Plots/Distance_bin.png'.
    - Displays the plot using plt.show().
    """

    if 'total_distance_km' not in df_sum.columns or 'aircraft_type_icao' not in df_sum.columns:
        raise KeyError("DataFrame must include 'total_distance_km' and 'aircraft_type_icao' columns")

    # Convert kilometers to nautical miles
    df_sum['total_distance_nm'] = df_sum['total_distance_km'] * 0.539957

    unique_aircraft_types = df_sum['aircraft_type_icao'].unique()
    unique_aircraft_types_df = pd.DataFrame(unique_aircraft_types, columns=['aircraft_type_icao'])

    unique_aircraft_types_df.to_csv("Aircraft_type.csv")

    # Specific plot for A319
    actype_data = df_sum[df_sum['aircraft_type_icao'] == actype]


    if not actype_data.empty:
        fig1 = plt.figure()
        ax1 = fig1.gca()
        plt.hist(actype_data['total_distance_nm'], bins=30, color='C0', edgecolor='black')
        #plt.title('Frequency Distribution of Total Distance Travelled by A319 Flights')
        plt.xlabel('Ground track distance (nmi)', fontname="Times New Roman", fontsize=20)
        plt.ylabel('Frequency', fontname="Times New Roman", fontsize=20)
        for axis in ['top', 'bottom', 'left', 'right']:
            ax1.spines[axis].set_linewidth(1.5)
        plt.xticks(fontname="Times New Roman", fontsize=20)
        plt.yticks(fontname="Times New Roman", fontsize=20)

        plt.rcParams['figure.dpi'] = 300
        plt.rcParams['savefig.dpi'] = 300

        F = plt.gcf()
        Size = F.get_size_inches()
        F.set_size_inches(Size[0]*1.7, Size[1]*1.5, forward=True)

        plt.xlim([0, 9000])
        plt.ylim([0, 22])
        filename = f'Output/Plots/Aircraft_distance/{actype}_Distance_bin.png'
        plt.savefig(filename)
        plt.show()

def plot_distance_bin_class(df_sum):
    narrow_body = ["A319", "A320", "A321", "A20N", "B734", "B737", "B738", "B739", "E170", "E195", "E75L"]
    wide_body = ["B789", "B788", "B77W", "B772", "B763", "A359", "A333", "A332", "A343"]

    if 'total_distance_km' not in df_sum.columns or 'aircraft_type_icao' not in df_sum.columns:
        raise KeyError("DataFrame must include 'total_distance_km' and 'aircraft_type_icao' columns")

    # Convert kilometers to nautical miles
    df_sum['total_distance_nm'] = df_sum['total_distance_km'] * 0.539957

    # Filter data for narrow-body and wide-body
    df_narrow = df_sum[df_sum['aircraft_type_icao'].isin(narrow_body)]
    df_wide = df_sum[df_sum['aircraft_type_icao'].isin(wide_body)]

    fig1 = plt.figure()
    ax1 = fig1.gca()

    # Plotting
    plt.hist(df_narrow['total_distance_nm'], bins=30, alpha=0.7, label='Narrow Body', edgecolor='black', color = 'C0')
    plt.hist(df_wide['total_distance_nm'], bins=30, alpha=0.7, label='Wide Body', edgecolor='black', color = "C2")

    plt.xlabel('Ground track distance (nmi)', fontname="Times New Roman", fontsize=20)
    plt.ylabel('Frequency', fontname="Times New Roman", fontsize=20)
    plt.legend()
    
    for axis in ['top', 'bottom', 'left', 'right']:
            ax1.spines[axis].set_linewidth(1.5)

    plt.xticks(fontname="Times New Roman", fontsize=20)
    plt.yticks(fontname="Times New Roman", fontsize=20)

    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['savefig.dpi'] = 300

    F = plt.gcf()
    Size = F.get_size_inches()
    F.set_size_inches(Size[0]*1.7, Size[1]*1.5, forward=True)

    plt.xlim([0, 9000])
    plt.ylim([0, 300])
    plt.savefig("Output/Plots/Aircraft_distance/Class_frequency_dist.png")
    plt.show()


def plot_aircraft_class_donut(df_sum):
    narrow_body = ["A319", "A320", "A321", "A20N", "B734", "B737", "B738", "B739", "E170", "E195", "E75L"]
    wide_body = ["B789", "B788", "B77W", "B772", "B763", "A359", "A333", "A332", "A343"]


# Filter data for narrow-body and wide-body
    df_narrow = df_sum[df_sum['aircraft_type_icao'].isin(narrow_body)]
    df_wide = df_sum[df_sum['aircraft_type_icao'].isin(wide_body)]

    # Create a donut plot for narrow-body aircraft count
    airframe_counts = df_wide['aircraft_type_icao'].value_counts()

    fig1 = plt.figure()
    ax1 = fig1.gca()

    ax1.pie(airframe_counts, labels=airframe_counts.index, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 12, 'fontname': 'Times New Roman'})
    # Draw a circle at the center of pie to make it look like a donut
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig1.gca().add_artist(centre_circle)

    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['savefig.dpi'] = 300

    F = plt.gcf()
    Size = F.get_size_inches()
    F.set_size_inches(Size[0]*1.7, Size[1]*1.5, forward=True)

    plt.savefig("Output/Plots/Aircraft_type/Wide_body_donut.png")
    plt.show()


def plot_map_fuelburn_total(matching_rows):
    # Assuming matching_rows is a DataFrame
    if not isinstance(matching_rows, pd.DataFrame):
        raise ValueError("matching_rows must be a pandas DataFrame.")

    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())

    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.set_global()

    # Remove bounding box/spines
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Ensure columns exist
    if not {'latitude', 'longitude', 'fuel_burn'}.issubset(matching_rows.columns):
        raise ValueError("DataFrame must contain 'latitude', 'longitude', and 'fuel_burn' columns.")

    # Extracting the necessary columns
    latitude = matching_rows['latitude']
    longitude = matching_rows['longitude']
    fuel_burn = matching_rows['fuel_burn'] 

    # Normalize the fuel burn values for coloring
    norm = Normalize(vmin=fuel_burn.min(), vmax=fuel_burn.max())
    cmap = plt.cm.viridis  # Color map

    # Scatter plot for latitude and longitude data, color-coded by fuel burn
    sc = ax.scatter(longitude, latitude, c=fuel_burn, cmap=cmap, norm=norm, transform=ccrs.Geodetic(), marker='o', s=1)

    cbar = plt.colorbar(sc, ax=ax, orientation='vertical', fraction=0.02, pad=0.02)
    cbar.set_label('Fuel burn (Kg)', fontsize=20, fontname="Times New Roman")

    # Customize colorbar tick labels
    cbar.ax.tick_params(labelsize=18)  # Set font size of the colorbar tick labels
    for label in cbar.ax.get_yticklabels():
        label.set_family("Times New Roman")

    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['savefig.dpi'] = 300
    plt.savefig('Output/Plots/Map_Fuel_burn.png')

    plt.show()

def plot_map_groundTrack_total(df_sum):
    # Assuming matching_rows is a DataFrame
    if not isinstance(df_sum, pd.DataFrame):
        raise ValueError("matching_rows must be a pandas DataFrame.")

    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())

    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.set_global()

    # Remove bounding box/spines
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Ensure columns exist
    if not {'latitude', 'longitude', 'total_distance_km'}.issubset(df_sum.columns):
        raise ValueError("DataFrame must contain 'latitude', 'longitude', and 'total_distance_km' columns.")

    # Extracting the necessary columns
    latitude = df_sum['latitude']
    longitude = df_sum['longitude']
    # Kilometers to natical miles
    track_distance = df_sum['total_distance_km'] * 0.539957

    # Normalize the fuel burn values for coloring
    norm = Normalize(vmin=track_distance.min(), vmax=track_distance .max())
    cmap = plt.cm.viridis  # Color map

    # Scatter plot for latitude and longitude data, color-coded by fuel burn
    sc = ax.scatter(longitude, latitude, c=track_distance, cmap=cmap, norm=norm, transform=ccrs.Geodetic(), marker='o', s=1)

    cbar = plt.colorbar(sc, ax=ax, orientation='vertical', fraction=0.02, pad=0.02)
    cbar.set_label('Fuel burn (Kg)', fontsize=20, fontname="Times New Roman")

    # Customize colorbar tick labels
    cbar.ax.tick_params(labelsize=18)  # Set font size of the colorbar tick labels
    for label in cbar.ax.get_yticklabels():
        label.set_family("Times New Roman")

    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['savefig.dpi'] = 300
    plt.savefig('Output/Plots/Map_Track_Distance.png')

    plt.show()