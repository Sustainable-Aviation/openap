from openap import prop, Thrust, Drag, WRAP, FlightPhase
from openap.traj import Generator
import csv

def dict_to_latex_table(dict_obj):
    latex_str = "\\begin{tabular}{l|l}\n"
    latex_str += "\\textbf{Key} & \\textbf{Value} \\\\ \\hline\n"
    for key, value in dict_obj.items():
        latex_str += f"{key} & {value} \\\\ \n"
    latex_str += "\\end{tabular}"
    return latex_str

import numpy as np
import matplotlib.pyplot as plt

# Import Airbus A320 with CFM-56
ac1 = prop.aircraft('A321')

print (ac1)
eng1 = prop.engine('V2527E-A5')

ac1_name = ac1['aircraft']
ac1_family = ac1_name.replace("Airbus ", "")  # Including the space after "Airbus" to remove it as well


#latex_table = dict_to_latex_table(eng1)
#print(latex_table)

# THRUST CALCULATION------->
thrust = Thrust(ac=ac1_family, eng=eng1['name'])

# Takeoff thrust at this speed and altitude
# Define the altitude range from 0 to 14500 feet, in steps (e.g., every 500 feet)
altitudes = range(0, 14501, 500)  # Adjust step as needed
speeds = range(110, 170, 10)  # Adjust step as needed

# Open a CSV file to write the takeoff thrust data
with open('data/A321/takeoff_thrust_A320-233.csv', 'w', newline='') as csvfile:
    fieldnames = ['Altitude (ft)', 'TAS (kts)', 'Takeoff Thrust (N)']  # Define column names
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()  # Write the column names
    
    # Iterate over each altitude, compute the takeoff thrust, and write to CSV
    for alt in altitudes:
        for speed in speeds:
            T_TO = thrust.takeoff(tas=speed, alt=alt)  # Compute takeoff thrust at this altitude
            writer.writerow({'Altitude (ft)': alt, 'TAS (kts)': speed, 'Takeoff Thrust (N)': T_TO})

print("Takeoff thrust data saved!.")




