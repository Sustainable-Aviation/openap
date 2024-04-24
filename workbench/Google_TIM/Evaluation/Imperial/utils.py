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

    mass0 = massfrac * MTOW

    path_angles = trajectory.path_angle_radians
    
    time_deltas = trajectory.elapsed_time_seconds

    mass = mass0

    for (dt, tas, alt, pa) in zip(time_deltas, trajectory.true_airspeed_knots, trajectory.altitude_ft, path_angles):
        fuelflow = ff.enroute(mass, tas, alt, pa)
        mass -= fuelflow * dt
    

    # Ensure that the final mass is less than or equal to design MLW
    if (mass > MLW):
        print("ERROR: Current mass fraction and mission profile reuslts in exceeding MLW")
        sys.exit()

    fuel = mass0 - mass

    print("Fuel burn: ", fuel)


