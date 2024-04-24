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

Target_id = "190107-10182-AZU2585"

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
            # Make a definite copy if it's originally a slice
            matching_rows = matching_rows.copy()

            latitude = matching_rows['latitude']
            longitude = matching_rows['longitude']
            altitude = matching_rows['altitude_ft']
            seg_len_nmi = matching_rows['segment_length'] * 0.001 * 0.539957


            # Compute the elapsed time in seconds for each segment
            elapsed_time = calculate_elapsed_time(matching_rows['time'])

            # Insert zero at the start of the elapsed_time list
            elapsed_time.insert(0, 0)

            # Assign elapsed_time list to a new DataFrame column
            matching_rows['elapsed_time_seconds'] = elapsed_time

            #print("Elapsed time/segment (s): ", matching_rows['elapsed_time_seconds'].tolist())
            #print("Total flight time (s): ", sum(matching_rows['elapsed_time_seconds']))
            
            # Calculate cumulative distance in nautical miles
            # Avoid SettingWithCopyWarning by ensuring operations are done on a DataFrame, not a slice
            matching_rows.loc[:, 'segment_length_nmi'] = matching_rows['segment_length'] * 0.000539957
            matching_rows.loc[:, 'cumulative_distance_nmi'] = matching_rows['segment_length_nmi'].cumsum()

            total_segment_length = matching_rows['segment_length'].sum()
    
            print("Total segment length in nmi: ", total_segment_length * 0.001 * 0.539957)


            # Compute the rate of climb

            # Calculate the change in altitude (delta altitude)
            matching_rows['delta_altitude'] = matching_rows['altitude_ft'].diff()

            # Clean up the DataFrame by filling or removing NA values if necessary
            matching_rows.fillna(0, inplace=True)  # Optional: replace NA values with 0 if suitable for your context

            # Calculate the rate of climb in feet per minute (ft/min)
            # Prevent division by zero by replacing 0 with NaN in 'delta_time_seconds'
            matching_rows['rate_of_climb_fpm'] = (matching_rows['delta_altitude'] / matching_rows['elapsed_time_seconds'].replace(0, pd.NA)) * 60

            # Set the first entry of rate of climb to zero
            matching_rows['rate_of_climb_fpm'].iloc[0] = 0
            
            # If the last value of true airspeed is zero, drop the last row from the datafrae
            if matching_rows['true_airspeed'].iloc[-1] == 0:
                # Get the index of the last row
                last_row_index = matching_rows.index[-1]
                
                # Drop the last row by index
                matching_rows = matching_rows.drop(last_row_index)

            # Convert true airspeed from meters per second to knots
            matching_rows['true_airspeed_knots'] = matching_rows['true_airspeed'] * 1.94384

            # Ensure 'rate_of_climb_fpm' and 'true_airspeed_knots' columns are numeric
            matching_rows['rate_of_climb_fpm'] = pd.to_numeric(matching_rows['rate_of_climb_fpm'], errors='coerce')
            matching_rows['true_airspeed_knots'] = pd.to_numeric(matching_rows['true_airspeed_knots'], errors='coerce')   

            # Create a new column with the converted values
            matching_rows['true_airspeed_fpm'] = matching_rows['true_airspeed_knots'] * 101.3

            # Compute the path angle in radians
            matching_rows['path_angle_radians'] = np.arctan(matching_rows['rate_of_climb_fpm'] / matching_rows['true_airspeed_fpm'])

            # Optionally, convert the angle to degrees for easier interpretation
            matching_rows['path_angle_degrees'] = np.degrees(matching_rows['path_angle_radians'])

            airFrame = utl.fallback(airframe)

            fuel_burn = utl.compute_emissions(matching_rows, airFrame, 0.85)

            # Add the computed fuel burn to the DataFrame
            matching_rows['fuel_burn'] = fuel_burn

            matching_rows.to_csv("selected_waypoint.csv")
            print("Data saved to 'selected_waypoint.csv'.")
            print(matching_rows.head(5))

            pProc.plot_map_fuelburn(matching_rows)
            

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