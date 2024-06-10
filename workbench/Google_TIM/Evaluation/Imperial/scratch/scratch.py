import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import utils as utl
from datetime import datetime

def read_parquet_header(file_path):
    # Read the parquet file
    df = pd.read_parquet(file_path, engine='pyarrow')
    return df

file_path_1 = '..//Data/ICCT_GAIA_Flight_Summary_Sample.pq'
file_path_2 = '..//Data/ICCT_GAIA_Flight_Waypoints_Sample.pq'

# Obtain the dataframe
df_sum = read_parquet_header(file_path_1)  # DataFrame with flight summary
df_wyp = read_parquet_header(file_path_2)  # DataFrame with flight speed, waypoints

# Initialize an empty DataFrame for appending processed data
combined_df = pd.DataFrame()

for index, row in df_sum.iterrows():
    flight_id = row['flight_id']

    flight_data = df_sum[df_sum['flight_id'] == flight_id]
    airframe = flight_data['aircraft_type_icao'].iloc[0]

    # Perform analysis only for A319
    if airframe == 'B77W':
        # Select matching waypoints data
        matching_rows = df_wyp[df_wyp['flight_id'] == flight_id]

        print("Current airframe: ", airframe)
        print("Current flight ID: ", flight_id)

        if not matching_rows.empty:
            matching_rows = matching_rows.copy()
            processed_df = utl.processFlightdata(matching_rows)
            
            # Append the processed data to the combined DataFrame using pd.concat
            combined_df = pd.concat([combined_df, processed_df], ignore_index=True)

# Save the combined DataFrame to a CSV file
combined_df.to_csv("combined_processed_B77W.csv", index=False)

print("Analysis Complete!")







