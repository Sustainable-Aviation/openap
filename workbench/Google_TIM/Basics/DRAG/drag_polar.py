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


# AIRCRAFT DRAG CALCULATION ----->
drag = Drag(ac = ac1_family)

# Mass in Kg, TAS in knots, altitude in feet.
CL, CD = drag.clean_CL_CD(mass=10000, tas=200, alt=20000, path_angle=5)


print("CL:", CL)
print("CD:", CD)


# THRUST CALCULATION------->
#thrust = Thrust(ac=ac1_family, eng=eng1['name'])

# Takeoff thrust at this speed and altitude
# Define the altitude range from 0 to 14500 feet, in steps (e.g., every 500 feet)
#altitudes = range(32000, 41000, 500)  # Adjust step as needed
#speeds = range(330, 450, 10)  # Adjust step as needed

# Open a CSV file to write the takeoff thrust data
#with open('data/A320/cruise_thrust_A320-233.csv', 'w', newline='') as csvfile:
#    fieldnames = ['Altitude (ft)', 'TAS (kts)', 'Cruise Thrust (N)']  # Define column names
#    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#    writer.writeheader()  # Write the column names
    
#    # Iterate over each altitude, compute the takeoff thrust, and write to CSV
#    for alt in altitudes:
#        for speed in speeds:
#            T_TO = thrust.cruise(tas=speed, alt=alt)  # Compute takeoff thrust at this altitude
#            writer.writerow({'Altitude (ft)': alt, 'TAS (kts)': speed, 'Cruise Thrust (N)': T_TO})

#print("Cruise thrust data saved!.")




