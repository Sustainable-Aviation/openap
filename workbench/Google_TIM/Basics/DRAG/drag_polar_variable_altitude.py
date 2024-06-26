from openap import prop, Thrust, Drag, WRAP
from openap.traj import Generator
import csv
from openap import Drag

import numpy as np
import matplotlib.pyplot as plt

# Import Airbus A321 with CFM-56
ac1 = prop.aircraft('A321')

#print(ac1)

# Get the MTOW for this airframe
MTOW =  ac1['limits']['MTOW']  # Kgs

#Factor = 0.10
#Mass = int(Factor * MTOW)

Mass = 50000 #Kgs

# Define range of aircraft cruise altitude
alts = range(30000, 41000, 500)  # Adjust step as needed
speeds = range(300, 450, 10)  # Adjust step as needed


# AIRCRAFT DRAG CALCULATION ----->
drag = Drag(ac = "A321")


# Open a CSV file to write the takeoff thrust data
with open('data/A321/cruise_drag_A321_fixed_mass01_multiple_altitude.csv', 'w', newline='') as csvfile:
    fieldnames = ['altitude', 'TAS (kts)', 'CL', 'CD']  # Define column names
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()  # Write the column names

    # Iterate over each altitude, compute the takeoff thrust, and write to CSV
    for alt in alts:
        for speed in speeds:
            CL, CD = drag.clean_CL_CD(mass=Mass, tas=speed, alt=alt, path_angle=0)  # Compute takeoff thrust at this altitude
            writer.writerow({'altitude': alt, 'TAS (kts)': speed, 'CL': CL, 'CD': CD})

print("Cruise polar data saved!.")


