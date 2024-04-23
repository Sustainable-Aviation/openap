import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

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


def plot_map_singleFlight(long, lat, altitude):


    # Normalize the altitude values to a range between 0 and 1 for coloring
    norm = plt.Normalize(altitude.min(), altitude.max())
    cmap = plt.cm.viridis  # Color map

    fig, ax = plt.subplots(figsize=(20, 10), subplot_kw={'projection': ccrs.Robinson()})
    ax.set_global()  # Ensure the entire globe is displayed
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    #ax.add_feature(cfeature.OCEAN, alpha=0.1)
    #ax.add_feature(cfeature.LAKES, alpha=0.5)
    #ax.add_feature(cfeature.RIVERS)

    # Scatter plot for latitude and longitude data, color-coded by altitude
    sc = ax.scatter(long, lat, c=altitude, cmap=cmap, norm=norm, transform=ccrs.Geodetic(), marker='o', s =6)

    cbar = plt.colorbar(sc, ax=ax, orientation='vertical', fraction=0.02, pad=0.02)
    cbar.set_label('Altitude (feet)', fontsize=20, fontname = "Times New Roman")

    cbar.ax.tick_params(labelsize=18)  # Set font size of the colorbar tick labels


    for label in cbar.ax.get_yticklabels():
        label.set_family("Times New Roman")

    plt.show()    

