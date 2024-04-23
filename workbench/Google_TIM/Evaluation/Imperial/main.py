import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

import postProcess as pProc

plt.style.use('seaborn-deep')

def read_parquet_header(file_path):
    # Read the parquet file
    df = pd.read_parquet(file_path, engine='pyarrow')

    return df



# Replace 'yourfile.parquet' with the path to your Parquet file
#file_path = 'Data/ICCT_GAIA_Flight_Waypoints_Sample.pq'
file_path_1 = 'Data/ICCT_GAIA_Flight_Summary_Sample.pq'
file_path_2 = 'Data/ICCT_GAIA_Flight_Waypoints_Sample.pq'

# Obtain the dataframe
df_sum = read_parquet_header(file_path_1)  # Datadrame with flight summary
df_wyp = read_parquet_header(file_path_2)  # Dataframe with flight speed, waypoints

Target_id = "190107-10182-AZU2585"

for index, row in df_sum.iterrows():

    # Get current Flight id 
    flight_id = row["flight_id"]

    if flight_id == Target_id:

        print("Origin airport: ", row['origin_airport'])
        print("Destination airport: ", row['destination_airport'])
        print(" Aircraft type: ", row['aircraft_type_icao'])
        # Check if this matches with target flight ID
        matching_rows = df_wyp[df_wyp['flight_id'] == Target_id]
        
        
        if not matching_rows.empty:
            latitude = matching_rows['latitude']
            longitude = matching_rows['longitude']
            altitude = matching_rows['altitude_ft']
            seg_len_nmi = matching_rows['segment_length'] * 0.001 * 0.539957
            
            # Calculate cumulative distance in nautical miles
            # Avoid SettingWithCopyWarning by ensuring operations are done on a DataFrame, not a slice
            matching_rows.loc[:, 'segment_length_nmi'] = matching_rows['segment_length'] * 0.000539957
            matching_rows.loc[:, 'cumulative_distance_nmi'] = matching_rows['segment_length_nmi'].cumsum()

            total_segment_length = matching_rows['segment_length'].sum()


    
            print("Total segment length in nmi: ", total_segment_length * 0.001 * 0.539957)

            #print(time)
    
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(matching_rows['cumulative_distance_nmi'], matching_rows['altitude_ft'], marker='o', linestyle='-', color='blue')
            plt.show()
    

            #pProc.plot_map_singleFlight(longitude, latitude, altitude)









#################
# Plot the altitude profile on world map
# pProc.plot_map_altitude(df_sum, df_wyp)


# Plot the distance bin distribution
#pProc.plot_distance_bin(df_sum)