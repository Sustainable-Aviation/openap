from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from openap.traj import Generator

def read_parquet_header(file_path):
    # Read the parquet file
    df = pd.read_parquet(file_path, engine='pyarrow')

    return df


file_path_1 = '../ICCT_GAIA_Flight_Summary_Sample.pq'
file_path_2 = '../ICCT_GAIA_Flight_Waypoints_Sample.pq'

Target_Airframe = "A319"

# Obtain the dataframe
df_sum = read_parquet_header(file_path_1)  # Datadrame with flight summary
df_wyp = read_parquet_header(file_path_2)  # Dataframe with flight speed, waypoints

# Loop through and select unique flights
for index, row in df_sum.iterrows():
    flight_id = row['flight_id']

    # Extract flight data for a specific flight
    flight_data = df_sum[df_sum['flight_id'] == flight_id]

    # Identify the type of airframe
    airframe = flight_data['aircraft_type_icao'].iloc[0]
    
    if airframe == Target_Airframe:
        #print(" Flight ID:", flight_id, " Airframe ", airframe)

        # Select matching waypoints data
        matching_rows = df_wyp[df_wyp['flight_id'] == flight_id]

        if not matching_rows.empty:
            matching_rows = matching_rows.copy()
            print(matching_rows)



#end
#trajgen = Generator(ac='a319')

#trajgen.enable_noise()   # enable Gaussian noise in trajectory data

#data_all = trajgen.complete(dt=10, random=True)

#print("Keys:", data_all.keys())
