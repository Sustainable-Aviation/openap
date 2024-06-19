from openap import prop, Thrust, Drag, WRAP
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
ac1 = prop.aircraft('A319')
eng1 = prop.engine('V2527M-A5')

ac1_name = ac1['aircraft']
ac1_family = ac1_name.replace("Airbus ", "")  # Including the space after "Airbus" to remove it as well


#latex_table = dict_to_latex_table(eng1)
#print(latex_table)

# THRUST CALCULATION------->
thrust = Thrust(ac=ac1_family, eng=eng1['name'])

# Takeoff thrust at this speed and altitude
# Define the altitude range from 0 to 14500 feet, in steps (e.g., every 500 feet)
altitudes = range(32000, 41000, 500)  # Adjust step as needed
speeds = range(330, 450, 10)  # Adjust step as needed

# Open a CSV file to write the takeoff thrust data
with open('data/A319/cruise_thrust_A319-133.csv', 'w', newline='') as csvfile:
    fieldnames = ['Altitude (ft)', 'TAS (kts)', 'Cruise Thrust (N)']  # Define column names
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()  # Write the column names
    
    # Iterate over each altitude, compute the takeoff thrust, and write to CSV
    for alt in altitudes:
        for speed in speeds:
            T_TO = thrust.cruise(tas=speed, alt=alt)  # Compute takeoff thrust at this altitude
            writer.writerow({'Altitude (ft)': alt, 'TAS (kts)': speed, 'Cruise Thrust (N)': T_TO})

print("Cruise thrust data saved!.")




