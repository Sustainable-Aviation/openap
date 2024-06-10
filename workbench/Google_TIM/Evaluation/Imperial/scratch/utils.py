import pandas as pd
from openap import prop, FuelFlow, Emission
import numpy as np
import sys
from datetime import datetime

def getMaxPayload(MTOW , MFW ,OEW):

    # Max Payload Weight = Max. take off weight - Max fuel weight - empty weight
    MPW = MTOW - MFW - OEW

    return MPW

def getMaxPayloadBADA(airframe):

    # Return maximum payload (kg) based on BADA OPF files
    if airframe == 'A319':
        return 1.70E+04
    
    if airframe == 'A320':
        return 2.15E+04
    
    if airframe == 'A321':
        return 2.17E+04
    
    if airframe == 'B737':
        return 1.69E+04
    
    if airframe == 'B738':
        return 2.03E+04
    
    if airframe == 'B739':
        return 2.30E+04
    
    if airframe == 'B752':
        return 2.13E+04
    
    if airframe == 'A332':
        return 4.74E+04
    
    if airframe == 'A333':
        return 4.79E+04
    
    if airframe == 'A343':
        return 4.70E+04
    
    if airframe == 'B77W':
        return 6.99E+04
    
    if airframe == 'B788':
        return 4.31E+04
    
    if airframe == 'B789':
        return 6.36E+04
    
    else:
        print("ERROR: Airframe not found. Cannot assign payload")
    
    


def computute_mission_weight(actype, payload_factor, fuel_factor, diagnostics):

    # Get aircraft type
    ac1 = prop.aircraft(actype)

    # Get the maximum fuel capacity (liters)
    MFC = ac1['limits']['MFC']

    # Fuel weight breakdown
    Trip_Fuel = MFC * fuel_factor

    # Reserve fuel (assume x % of maximum fuel)
    Reserve_Fuel = MFC * 0.05

    # Compute the fuel weight (Max. Fuel Mass)
    MFW = MFC * 0.804   # Jet A density 0.8 kg/liter
    
    # Get mass design limits
    MTOW = ac1['limits']['MTOW']  # Kg

    # Get OEW
    OEW = ac1['limits']['OEW']  # Kgs

    # Get mass design limits
    MLW = ac1['limits']['MLW']  # Kg

    MPW = getMaxPayload(MTOW , MFW ,OEW)
   
    # Eval mission weight = operating empty weight + payload weight*factor + fuel weight
    MW = OEW + (MPW * payload_factor) + Trip_Fuel + Reserve_Fuel

    if diagnostics:
        print("MTOW:", MTOW)
        print("OEW:", OEW)
        print("Fuel weight:", Trip_Fuel + Reserve_Fuel)
        print("Payload weight:", MPW * payload_factor)
  
    return MW, MTOW, MLW, OEW, Trip_Fuel, Reserve_Fuel, MPW * payload_factor




def compute_emissions(trajectory, actype, payload_factor, fuel_factor, debug):

    # Define fuel flow object with default engine (TODO add specifici with Cirium)
    ff = FuelFlow(actype)
    emission = Emission(actype)
    
    # Get the mission weight (Mass) (fuel + payload + OEW)
    Mass_ini, MTOW, MLW, OEW, Trip_Fuel, Reserve_Fuel, Payload_weight = computute_mission_weight(actype, payload_factor, fuel_factor, False)

    path_angles = trajectory.path_angle_radians
    
    # Time spent over each segment (in-between waypoints)
    time_deltas = trajectory.elapsed_time_seconds

    # Mission mass cannot be less than operational empty weight - 
    if Trip_Fuel  == 0:
        print("Trip fuel weight cannot be zero")
        sys.exit()

    mass = Mass_ini

    if mass > (1.25*MTOW):
        print("Mission weight is greater than MTOW!")
        print("Design MTOW: ", MTOW)
        print("Mission weight: ", mass)
        computute_mission_weight(actype, payload_factor, fuel_factor, True)
        sys.exit()

    # Determine the number of segments
    n = len(time_deltas)

    # Initialize an array of zeros with size n to store fuelflow*dt values
    fuel_consumption_array = np.zeros(n)

    # Initialize emissions array
    CO2_emissions_array = np.zeros(n)
    H2O_emissions_array = np.zeros(n)
    Nox_emissions_array = np.zeros(n)
    CO_emissions_array = np.zeros(n)
    HC_emissions_array = np.zeros(n)



    for i, (dt, tas, alt, pa) in enumerate(zip(time_deltas, trajectory.true_airspeed_knots, trajectory.altitude_ft, path_angles)):
        if None in (dt, tas, alt, pa):
            print(f"Skipping index {i} due to missing data.")
            continue
        fuelflow = ff.enroute(mass, tas, alt, pa)
        # Here fuelflow is change in mass (fuel burn) over a segment (Kg/s over segment)
        mass -= fuelflow * dt

        if mass < (OEW + Payload_weight + Reserve_Fuel):
            print("Current mission weight is less than  OEW + Payload + Reserve_Fuel")
            print("Not enough fuel to complete mission under normal conditions")
            print("Available mission fuel weight: ", Trip_Fuel)
            sys.exit()

        if debug:
            # Exit if fuel burn invalid 
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

        # Compute emissions
        CO2_emissions_array[i] = emission.co2(fuelflow)
        H2O_emissions_array[i] = emission.h2o(fuelflow)
        Nox_emissions_array[i] = emission.nox(fuelflow)
        CO_emissions_array[i] = emission.co(fuelflow)
        HC_emissions_array[i] = HC = emission.hc(fuelflow)
        
    # Compute total fuel burn over entire mission
    fuelburn = Mass_ini - mass
    # Ensure that the final mass is less than or equal to design MLW
    if (mass > MLW):
        print("ERROR: Final mass exceeds maximum design landing weight")
        print("Final mission mass: ", mass)
        print("Max. landing weight: ", MLW)
        print("Initial fuel weight:", )
        print("Fuel burn: ", fuelburn)

        sys.exit()

    

    print("Fuel burn: ", fuelburn)

    return fuel_consumption_array


def fallback(airframe):
    if airframe == "E195":
        print("E195 not supported, selecting B737 as fallback airframe \n")
        alt_airframe = "B737"

    if airframe == "A20N":
        print("A20N not supported, selecting A319 as fallback airframe \n")
        alt_airframe = "A319"
        return alt_airframe

    if airframe == "B734":
        print("B734 not supported, selecting B738 as fallback airframe \n")
        alt_airframe = "B738"
        return alt_airframe
    
    if airframe == "B772":
        print("B772 not supported, selecting B77W as fallback airframe \n")
        alt_airframe = "B77W"
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



def getfuelBurn(actype, payload_factor, trajectory,MTOW, MFC, MLW, OEW, fuel_factor, Payload_weight, debug):

    # For now, target A319 only and switch engine to CFM56-5B5
    if actype =="A319":
        print("Setting user-defined engine for A319")
        ff = FuelFlow(actype, eng = 'CFM56-5B5')
    else:
        # Define fuel flow object with default engine (TODO add specific engine with Cirium)
        ff = FuelFlow(actype)

    # Define emissions object
    emission = Emission(actype)

    # Fuel weight breakdown
    Trip_Fuel = MFC * fuel_factor

    # Reserve fuel (assume 5 % of maximum fuel capacity)
    Reserve_Fuel = MFC * 0.05

    # Eval mission weight = operating empty weight + payload weight_factor + fuel weight
    Mass_ini = OEW + Payload_weight + Trip_Fuel + Reserve_Fuel

    # Initial mass
    mass = Mass_ini

    # Mission weight cannot be greater than MTOW
    if mass > MTOW:
        print("Mission weight is greater than MTOW!")
        print("Design MTOW: ", MTOW)
        print("Mission weight: ", mass)
        computute_mission_weight(actype, payload_factor, fuel_factor, True)

        raise ValueError("Mission weight is greater than MTOW!")
    
    if Trip_Fuel == 0:
        raise ValueError("Trip fuel is zero, cannot start mission on reserves")
    
    if Trip_Fuel > MFC:
        raise ValueError("Required trip fuel is greater than maximum fuel capacity")

    # Compute path angles from trajectory
    path_angles = trajectory.path_angle_radians

    # Time spent over each segment (in-between waypoints)
    time_deltas = trajectory.elapsed_time_seconds

    # Determine the number of segments
    n = len(time_deltas)

    # Initialize a NumPy array of zeros with size n to store fuelflow*dt values
    fuel_consumption_array = np.zeros(n)

    # Initialize emissions array
    CO2_emissions_array = np.zeros(n)
    H2O_emissions_array = np.zeros(n)
    Nox_emissions_array = np.zeros(n)
    CO_emissions_array = np.zeros(n)
    HC_emissions_array = np.zeros(n)

    for i, (dt, tas, alt, pa) in enumerate(zip(time_deltas, trajectory.true_airspeed_knots, trajectory.altitude_ft, path_angles)):
            
        if None in (dt, tas, alt, pa):
            print(f"Skipping index {i} due to missing data.")
            continue

        # If in LTO mode, use takeoff fuelflow setting
        if ((alt < 3000) and (pa > 0.001)):
            fuelflow = ff.takeoff(tas, alt, throttle = 1)

        if (alt > 3000):
            fuelflow = ff.enroute(mass, tas, alt, pa)

        # If in LTO mode, use takeoff fuelflow setting
        if ((alt < 3000) and (pa < 0.001)):
            #fuelflow = ff.takeoff(tas, alt, throttle = 0.25)
            fuelflow = ff.enroute(mass, tas, alt, pa)
    
        # Here fuelflow is change in mass (fuel burn) over a segment (Kg/s over segment)
        mass -= fuelflow * dt

        if mass < (OEW + Payload_weight + Reserve_Fuel):
            #print("Current mission weight: ", mass)
            #print("Current Fuel weight: ", (OEW + Payload_weight + Reserve_Fuel)-mass )
            #print("Trip fuel weight: ", Trip_Fuel)
            raise ValueError("Not enough trip fuel to complete the mission")

        if debug:
            if pd.isna(fuelflow * dt):
                raise ValueError("Fuel burn calculation resulted in NaN")

        # If all checks passed, append the fuel_consumption array     
        fuel_consumption_array[i] = fuelflow * dt

        # Compute emissions
        CO2_emissions_array[i] = emission.co2(fuelflow)
        H2O_emissions_array[i] = emission.h2o(fuelflow)
        Nox_emissions_array[i] = emission.nox(fuelflow, tas, alt)
        CO_emissions_array[i] = emission.co(fuelflow, tas, alt)
        HC_emissions_array[i] =  emission.hc(fuelflow, tas, alt)

    # Fuel burn Caclulation ends

    # Check if the final mass does not exceed maximum landing weight
    if mass > MLW:
        raise ValueError("Final mass exceeds maximum design landing weight")

    # Total fuel burn
    fuelBurn = Mass_ini - mass

    # Total Emissions
    CO2 = np.sum(CO2_emissions_array)
    H2O = np.sum(H2O_emissions_array)
    NOX = np.sum(Nox_emissions_array)
    CO = np.sum(CO_emissions_array)
    HC = np.sum(HC_emissions_array)

    print("Fuel burn:", fuelBurn)
    print("---------------------------------------------------------------------")

    return fuelBurn, CO2, H2O, NOX, CO, HC, Reserve_Fuel, Trip_Fuel, Payload_weight, fuel_consumption_array, CO2_emissions_array, H2O_emissions_array, Nox_emissions_array


def compute_emissions_beta(trajectory, actype, payload_factor, debug):
    # Define fuel flow object with default engine (TODO add specifici with Cirium)
    ff = FuelFlow(actype)

    # Get aircraft type
    ac1 = prop.aircraft(actype)


    # Get the maximum fuel capacity (liters)
    MFC = ac1['limits']['MFC']

    # Compute the fuel weight (Max. Fuel Mass)
    MFW = MFC * 0.80   # Jet A density 0.8 kg/liter
    
    # Get mass design limits
    MTOW = ac1['limits']['MTOW']  # Kg

    # Get OEW
    OEW = ac1['limits']['OEW']  # Kgs

    # Get mass design limits
    MLW = ac1['limits']['MLW']  # Kg

    # Get the maximum payload weight (kg) from BADA OPF
    MPW = getMaxPayloadBADA(actype)

    # Payload weight is some fraction of total payload capacity
    Payload_weight = MPW * payload_factor

    # Set initial fuel_factor/ fraction
    fuel_factor = 0.1

    max_tries = 100  # Maximum number of tries including the initial attempt
    increment = 0.01


    for attempt in range(max_tries):
        try:
            #print(f"Attempt {attempt + 1} with fuel factor {fuel_factor:.2f}")
            fuel_burn, CO2, H2O, NOX, CO, HC, Reserve_fuel, Trip_fuel, Pyload_weight, fuel_consumption_array, CO2_emissions_array, H2O_emissions_array, Nox_emissions_array  =  getfuelBurn(actype, payload_factor, trajectory, MTOW, MFC, MLW, OEW, fuel_factor, Payload_weight, debug)
            return fuel_burn, CO2, H2O, NOX, CO, HC, Reserve_fuel, Trip_fuel, Pyload_weight, fuel_consumption_array, CO2_emissions_array, H2O_emissions_array, Nox_emissions_array
        except ValueError as e:
            #print(f"Attempt {attempt + 1} with fuel factor {fuel_factor:.2f}: {e}")
            fuel_factor += increment  # Increase the fuel factor for the next attempt

            if attempt == max_tries - 1:
                #print("Max retries reached. Unable to calculate emissions with the given parameters.")
                #print("Flight ID : ", trajectory['flight_id'])
                #print("Current mission distance: ", trajectory['cumulative_distance_nmi'])
                raise  # Re-raise the last exception to indicate failure after all retries

  

