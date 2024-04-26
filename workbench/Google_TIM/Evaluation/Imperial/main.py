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


# Replace 'yourfile.parquet' with the path to your Parquet file
#file_path = 'Data/ICCT_GAIA_Flight_Waypoints_Sample.pq'
file_path_1 = 'Data/ICCT_GAIA_Flight_Summary_Sample.pq'
file_path_2 = 'Data/ICCT_GAIA_Flight_Waypoints_Sample.pq'

# Obtain the dataframe
df_sum = read_parquet_header(file_path_1)  # Datadrame with flight summary
df_wyp = read_parquet_header(file_path_2)  # Dataframe with flight speed, waypoints

#Target_id = "190107-10182-AZU2585"
#Target_id = "190114-20090-AAL1294"
Target_id = "190107-72701-IBE32HL"

debug = False
Limit = 2

# Fuel load factor
fuel_factor = 0.001

# Payload factor
payload_factor = 0.90

# List to hold data for all flights for plotting
all_flights_data = []

count  = 0

# Loop through each unique flight_id in df_sum
for flight_id in df_sum['flight_id'].unique():
    if debug:
        if flight_id == Target_id:
            flight_data = df_sum[df_sum['flight_id'] == flight_id]
        
    else:
        flight_data = df_sum[df_sum['flight_id'] == flight_id]

        if count > Limit:
            break

        airframe = flight_data['aircraft_type_icao'].iloc[0]

        # Select matching waypoints data
        matching_rows = df_wyp[df_wyp['flight_id'] == flight_id]

        if not matching_rows.empty:
            matching_rows = matching_rows.copy()
            processed_df = utl.processFlightdata(matching_rows)

            # See if a fallback airframe is required (if not supported in openAP )
            print("Current airframe: ", airframe)
            airFrame = utl.fallback(airframe)

            if debug:
                print(flight_data['flight_id'])
                processed_df.to_csv("Failing.csv")
                fuel_burn = utl.compute_emissions(processed_df, airFrame, payload_factor, fuel_factor, debug)

            else:

                fuel_burn = utl.compute_emissions(processed_df, airFrame, payload_factor, fuel_factor, debug)       


                # Add the computed fuel burn to the DataFrame
                processed_df['fuel_burn'] = fuel_burn

                all_flights_data.append(processed_df)

                #print(matching_rows.head(5))

        count  = count + 1

 # end df_sum loop   

# Combine all data into a single DataFrame
combined_data = pd.concat(all_flights_data, ignore_index=True)

pProc.plot_map_fuelburn(combined_data)

#################
# Plot the altitude profile on world map
# pProc.plot_map_altitude(df_sum, df_wyp)


# Plot the distance bin distribution
#pProc.plot_distance_bin(df_sum)