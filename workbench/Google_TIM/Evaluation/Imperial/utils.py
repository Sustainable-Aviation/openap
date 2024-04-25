import pandas as pd
from openap import prop, FuelFlow
import numpy as np
import sys
from datetime import datetime

def compute_emissions(trajectory, actype, massfrac, debug):

    # Define fuel flow object with default engine (TODO add specifici with Cirium)
    ff = FuelFlow(actype)

    ac1 = prop.aircraft(actype)

    # Get mass design limits
    MTOW = ac1['limits']['MTOW']  # Kg

    # Get the MLW for this airframe
    MLW = ac1['limits']['MLW']  # Kg

    # Get the OEW for this airframe
    OEW = ac1['limits']['OEW']  # Kgs

    # Get the MFC for this airframe
    MFC = ac1['limits']['MFC']  # Kgs

    path_angles = trajectory.path_angle_radians
    
    # Time spent over each segment (in-between waypoints)
    time_deltas = trajectory.elapsed_time_seconds

    # Set the initial mass to "some fraction" of MTOW
    mass_init = massfrac * MTOW
    mass = mass_init

    # Determine the number of segments
    n = len(time_deltas)

    # Initialize a NumPy array of zeros with size n to store fuelflow*dt values
    fuel_consumption_array = np.zeros(n)

    for i, (dt, tas, alt, pa) in enumerate(zip(time_deltas, trajectory.true_airspeed_knots, trajectory.altitude_ft, path_angles)):
        if None in (dt, tas, alt, pa):
            print(f"Skipping index {i} due to missing data.")
            continue
        fuelflow = ff.enroute(mass, tas, alt, pa)
        # Here fuelflow is change in mass (fuel burn) over a segment
        mass -= fuelflow * dt

        if debug:
            if pd.isna(fuelflow * dt):
                print("Fuel burn calculation resulted in NAN, stopping execution")

                print("Aircraft: ", actype)
                print("Current dt:", dt)
                print("Current fuelflow:", fuelflow)
                print("Current mass:", mass)
                print("Current TAS:", tas)
                print("Current PA:", pa)
                print("Current alt:", alt)
                raise ValueError("Fuel burn is NaN")

        # Store the product of fuelflow and dt directly in the preallocated array
        fuel_consumption_array[i] = fuelflow * dt

    # Ensure that the final mass is less than or equal to design MLW
    if (mass > MLW):
        print("ERROR: Current mass fraction and mission profile reuslts in exceeding MLW")
        sys.exit()

    fuelburn = mass_init - mass

    print("Fuel burn: ", fuelburn)

    return fuel_consumption_array


def fallback(airframe):
    if airframe == "E195":
        print("E195 not supported, selecting A319 as fallback airframe \n")
        alt_airframe = "A319"

    if airframe == "A20N":
        print("A20N not supported, selecting A320 as fallback airframe \n")
        alt_airframe = "A320"
        return alt_airframe

    if airframe == "B734":
        print("B734 not supported, selecting B737 as fallback airframe \n")
        alt_airframe = "B737"
        return alt_airframe    
    
    else:
        return airframe


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

def processFlightdata(matching_rows):
    # Make a definite copy if it's originally a slice
    matching_rows = matching_rows.copy()
    latitude = matching_rows['latitude']
    longitude = matching_rows['longitude']
    altitude = matching_rows['altitude_ft']
    seg_len_nmi = matching_rows['segment_length'] * 0.001 * 0.539957

    # Compute the elapsed time in seconds for each segment
    elapsed_time = calculate_elapsed_time(matching_rows['time'])

    #print(elapsed_time)

    # Insert zero at the start of the elapsed_time list
    elapsed_time.insert(0, 0)

    # Assign elapsed_time list to a new DataFrame column
    matching_rows['elapsed_time_seconds'] = elapsed_time

    # Calculate cumulative distance in nautical miles
    # Avoid SettingWithCopyWarning by ensuring operations are done on a DataFrame, not a slice
    matching_rows.loc[:, 'segment_length_nmi'] = matching_rows['segment_length'] * 0.000539957
    matching_rows.loc[:, 'cumulative_distance_nmi'] = matching_rows['segment_length_nmi'].cumsum()

    total_segment_length = matching_rows['segment_length'].sum()
    #print("Total segment length in nmi: ", total_segment_length * 0.001 * 0.539957)

    # Compute the rate of climb
    # Calculate the change in altitude (delta altitude)
    matching_rows['delta_altitude'] = matching_rows['altitude_ft'].diff()

    # Clean up the DataFrame by filling or removing NA values if necessary
    matching_rows.fillna(0, inplace=True)  # Optional: replace NA values with 0 if suitable for your context

    # Calculate the rate of climb in feet per minute (ft/min)
    # Prevent division by zero by replacing 0 with NaN in 'delta_time_seconds'
    matching_rows['rate_of_climb_fpm'] = (matching_rows['delta_altitude'] / matching_rows['elapsed_time_seconds'].replace(0, pd.NA)) * 60

    # Set the first entry of rate of climb to the same as for the second entry
    matching_rows.loc[matching_rows.index[0], 'rate_of_climb_fpm'] = matching_rows['rate_of_climb_fpm'].iloc[1]

    # The time elaspsed for the first row is zero. Take it as half of the time elapsed of the next waypoint
    matching_rows.loc[matching_rows.index[0], 'elapsed_time_seconds'] = matching_rows['elapsed_time_seconds'].iloc[1] * 0.5

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

    # Processing complete, return the dataframe
    return matching_rows





