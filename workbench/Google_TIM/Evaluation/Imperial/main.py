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

narrow_body = ["A319", "A320", "A321", "A20N", "B734", "B737", "B738", "B739", "E170", "E195", "E75L"]
wide_body = ["B789", "B788", "B77W", "B772", "B763", "A359", "A333", "A332", "A343"]


Target_id = "190114-72410-AFL106"

# List of flight IDs to exclude
excluded_flight_ids = ["190110-93704-ARG1844", "190114-77651-CES201",  "190111-69033-GCR7939", "190113-51219-CRL953", "190107-99735-ARG1141", "190115-24252-AEA023", "190112-45597-QFA107", "190114-72410-AFL106"]

debug = False
Limit = 199


# Payload factor
payload_factor = 0.70

# List to hold data for all flights for plotting
all_flights_data = []

# Initialize list to hold all emissions data
emissions_data = []

count  = 0
global_iter = 0
plot_fuel_burn = True
write_emissions = True

if plot_fuel_burn:
    # Loop through each unique flight_id in df_sum
    for index, row in df_sum.iterrows():
        flight_id = row['flight_id']

        if debug:
            if flight_id == Target_id:
                flight_data = df_sum[df_sum['flight_id'] == flight_id]
                airframe = flight_data['aircraft_type_icao'].iloc[0]
                matching_rows = df_wyp[df_wyp['flight_id'] == flight_id]

                if not matching_rows.empty:
                    matching_rows = matching_rows.copy()
                    processed_df = utl.processFlightdata(matching_rows)

            

                    # See if a fallback airframe is required (if not supported in openAP )
                    print("---------------------------------------------------------------------")
                    print("Current airframe: ", airframe)
                    airFrame = utl.fallback(airframe)

                
                    #print(flight_data['flight_id'])
                    processed_df.to_csv("Failing.csv")
                    fuel_burn, CO2, H2O, NOX, CO, HC = utl.compute_emissions_beta(processed_df, airFrame, payload_factor, debug)
                    processed_df['fuel_burn'] = fuel_burn


                    pProc.plot_map_fuelburn_total(processed_df)


        # Run in normal mode
        else:
            try:
                global_iter = global_iter + 1
                #if flight_id in excluded_flight_ids:
                #    continue  # Skip this loop iteration

                flight_data = df_sum[df_sum['flight_id'] == flight_id]

                if count > Limit:
                    break

                airframe = flight_data['aircraft_type_icao'].iloc[0]

                #if airframe == 'A332':
                #    continue  # Something is wrong with A332, skip for now.

                if airframe == 'A359':
                    continue  # Kinematic model not available

                if airframe == 'B772':
                    continue  #  Kinematic model not available

                if airframe == 'A20N':
                    continue  #  Kinematic model not available

                if airframe == 'A21N':
                    continue  #  Kinematic model not available

                if airframe == 'B734':
                    continue  #  Kinematic model not available

                if airframe == 'B763':
                    continue  #  Drag polar not available

                if airframe == 'E170':
                    continue  #  Drag polar not available

                if airframe == 'E195':
                    continue  #  Kinematic model not available

                if airframe == 'E75L':
                    continue  #  Kinematic model not available

                # Select matching waypoints data
                matching_rows = df_wyp[df_wyp['flight_id'] == flight_id]

                if not matching_rows.empty:
                    matching_rows = matching_rows.copy()
                    processed_df = utl.processFlightdata(matching_rows)

                    processed_df.to_csv("processed.csv")

                    

                    # See if a fallback airframe is required (if not supported in openAP)
                    print("---------------------------------------------------------------------")
                    print("Current airframe: ", airframe)
                    print("Global iter: ", global_iter)
                    #airFrame = utl.fallback(airframe)

               
                    fuel_burn, CO2, H2O, NOX, CO, HC, Reserve_fuel, Trip_fuel, Payload_weight, fuel_consumption_array, CO2_emissions_array, H2O_emissions_array, Nox_emissions_array = utl.compute_emissions_beta(processed_df, airframe, payload_factor, debug)  

                    # Append results to the list
                    emissions_data.append({
                        "flight_id": flight_id,
                        "Aircraft IATA code": airframe,
                        "Total distance (nm) (FF)": round(processed_df['cumulative_distance_nmi'].iloc[-1], 4),
                        "Reserve Fuel (Kg)": round(Reserve_fuel, 4),
                        "Trip Fuel (Kg)": round(Trip_fuel, 4),
                        "Payload (Kg)": round(Payload_weight,4),
                        "Fuel_burnt (FF)": round(fuel_burn,4),
                        "Forecast CO2 (Kg)": round(CO2,4),
                        "Forecast H2O (kg)": round(H2O,4),
                        "Forecast NOX (Kg)": round(NOX,4),
                        "Forecast CO (Kg)": round(CO,4),
                        "Forecast HC (Kg)": round(HC,4)
                        })

                    # Add the computed fuel burn to the DataFrame
                    processed_df['fuel_burn'] = fuel_consumption_array
                    processed_df['CO2'] =  CO2_emissions_array
                    processed_df['H2O'] =  H2O_emissions_array
                    processed_df['NOx'] =  Nox_emissions_array


                    all_flights_data.append(processed_df)

                count  = count + 1
            except ValueError as e:
                print("Failed to calculate fuel burn due to a ValueError:", e)
    # end df_sum loop   

            # Combine all data into a single DataFrame
            combined_data = pd.concat(all_flights_data, ignore_index=True)

            combined_data.to_csv('combined_data.csv')

    #pProc.plot_map_fuelburn_waypoint(combined_data)

    # Write emissions in EEA format for Google TIM
    if write_emissions:
        emissions_df = pd.DataFrame(emissions_data)
        emissions_df.to_csv("Output/Ver_2/No_Wind/A320/A320-111/Emissions_Summary_PF_0.7.csv", index=False)

    # Set global parameters
    #plt.rcParams['figure.figsize'] = (10, 10)  # width, height in inches
    #plt.rcParams['figure.dpi'] = 300
    #plt.rcParams['savefig.dpi'] = 300

    #pProc.plot_map_fuelburn_waypoint(combined_data)

    #pProc.plot_map_H2O_waypoint(combined_data)

    #pProc.plot_map_CO2_waypoint(combined_data)

#################
# Plot the altitude profile on world map
    #pProc.plot_map_altitude(df_sum, df_wyp)


# Plot the distance bin distribution
#pProc.plot_distance_bin(df_sum)

#pProc.plot_distance_bin_actype(df_sum, "B739")

#pProc.plot_distance_bin_class(df_sum)

#pProc.plot_aircraft_class_donut(df_sum)

#pProc.plot_map_groundTrack_total(df_sum)