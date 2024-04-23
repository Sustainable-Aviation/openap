import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

import postProcess as pProc

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

pProc.plot_map_altitude(df_sum, df_wyp)


