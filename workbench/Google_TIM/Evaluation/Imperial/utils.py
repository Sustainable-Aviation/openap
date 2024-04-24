import pandas as pd
from openap import prop, FuelFlow
import numpy as np
import sys


def compute_emissions(trajectory, actype, massfrac):

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
        return alt_airframe
    else:
        return airframe