import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import utils as utl
import numpy as np
import postProcess as pProc
from datetime import datetime

plt.style.use('seaborn-deep')

def read_parquet_header(file_path):
    # Read the parquet file
    df = pd.read_parquet(file_path, engine='pyarrow')

    return df

def calculate_elapsed_time(timestamps):
    # Ensure all timestamps are in datetime format
    datetime_objects = []
    for ts in timestamps:
        if isinstance(ts, str):
            dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
        elif isinstance(ts, pd.Timestamp):  # handle pandas Timestamp
            dt = ts.to_pydatetime()
        else:
            raise ValueError("Unsupported timestamp format")

        datetime_objects.append(dt)

    # Calculate the differences between consecutive timestamps
    time_differences = [datetime_objects[i + 1] - datetime_objects[i] for i in range(len(datetime_objects) - 1)]

    # Convert time differences to seconds
    elapsed_seconds = [td.total_seconds() for td in time_differences]

    return elapsed_seconds




# Replace 'yourfile.parquet' with the path to your Parquet file
#file_path = 'Data/ICCT_GAIA_Flight_Waypoints_Sample.pq'
file_path_1 = 'Data/ICCT_GAIA_Flight_Summary_Sample.pq'
file_path_2 = 'Data/ICCT_GAIA_Flight_Waypoints_Sample.pq'

# Obtain the dataframe
df_sum = read_parquet_header(file_path_1)  # Datadrame with flight summary
df_wyp = read_parquet_header(file_path_2)  # Dataframe with flight speed, waypoints

#Target_id = "190107-10182-AZU2585"
Target_id = "190114-20090-AAL1294"

for index, row in df_sum.iterrows():

    # Get current Flight id 
    flight_id = row["flight_id"]

    if flight_id == Target_id:

        print("Origin airport: ", row['origin_airport'])
        print("Destination airport: ", row['destination_airport'])
        #print(" Aircraft type: ", row['aircraft_type_icao'])
        # Check if this matches with target flight ID
        matching_rows = df_wyp[df_wyp['flight_id'] == Target_id]
        airframe = row['aircraft_type_icao']
        
        if not matching_rows.empty:

            # Compute the elapsed time in seconds for each segment
            #elapsed_time = calculate_elapsed_time(matching_rows['time'])

            #print(elapsed_time)
            processed_df = utl.processFlightdata(matching_rows)

            # See if a fallback airframe is required (if not supported in openAP )
            airFrame = utl.fallback(airframe)

            fuel_burn = utl.compute_emissions(processed_df, airFrame, 0.75)

            # Add the computed fuel burn to the DataFrame
            processed_df['fuel_burn'] = fuel_burn

            processed_df.to_csv("selected_waypoint.csv")
            print("Data saved to 'selected_waypoint.csv'.")
            print(processed_df.head(5))

            pProc.plot_map_fuelburn(processed_df)
            

            #print(time)
    
            #fig, ax = plt.subplots(figsize=(10, 5))
            #ax.plot(matching_rows['cumulative_distance_nmi'], matching_rows['altitude_ft'], marker='o', linestyle='-', color='blue')
            #plt.show()



            #pProc.plot_map_singleFlight(longitude, latitude, altitude)









#################
# Plot the altitude profile on world map
# pProc.plot_map_altitude(df_sum, df_wyp)


# Plot the distance bin distribution
#pProc.plot_distance_bin(df_sum)