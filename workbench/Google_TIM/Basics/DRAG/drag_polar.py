from openap import prop, Thrust, Drag, WRAP, FlightPhase
from openap.traj import Generator
import csv
from openap import Drag

import numpy as np
import matplotlib.pyplot as plt

# Import Airbus A320 with CFM-56
ac1 = prop.aircraft('A320')
eng1 = prop.engine('V2527E-A5')

ac1_name = ac1['aircraft']
ac1_family = ac1_name.replace("Airbus ", "")  # Including the space after "Airbus" to remove it as well

MTOW =  ac1['limits']['MTOW']  # Kgs

Min_mass = int(0.25 * MTOW)
Max_mass = int(0.75 * MTOW)


# Define range of aircraft mass
masses = range(Min_mass, Max_mass, 500)  # Adjust step as needed
speeds = range(330, 430, 10)  # Adjust step as needed


# AIRCRAFT DRAG CALCULATION ----->
drag = Drag(ac = ac1_family)


# Open a CSV file to write the takeoff thrust data
with open('data/A320/cruise_drag_A320-233.csv', 'w', newline='') as csvfile:
    fieldnames = ['Mass (kg)', 'TAS (kts)', 'CL', 'CD']  # Define column names
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()  # Write the column names

    # Iterate over each altitude, compute the takeoff thrust, and write to CSV
    for mass in masses:
        for speed in speeds:
            CL, CD = drag.clean_CL_CD(mass=mass, tas=speed, alt=35000, path_angle=0)  # Compute takeoff thrust at this altitude
            writer.writerow({'Mass (kg)': mass, 'TAS (kts)': speed, 'CL': CL, 'CD': CD})

print("Cruise polar data saved!.")




