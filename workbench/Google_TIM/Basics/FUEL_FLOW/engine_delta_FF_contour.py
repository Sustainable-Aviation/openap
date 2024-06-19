import numpy as np
import matplotlib.pyplot as plt
from openap import prop, FuelFlow

# Define the aircraft
ac = 'A321'
alt = 35000  # Fixed altitude

# Import aircraft data
ac1 = prop.aircraft('A321')

# Get the MTOW for this airframe
MTOW = ac1['limits']['MTOW']  # Kgs

min_mass_fraction = 0.1
max_mass_fraction = 0.85

# Define engines
engine1 = 'CFM56-5B1'
engine2 = 'V2530-A5'  # Second engine for comparison

fuelflow1 = FuelFlow(ac=ac, eng=engine1)
fuelflow2 = FuelFlow(ac=ac, eng=engine2)

# Creating mass fractions directly for plotting
mass = np.arange(min_mass_fraction, max_mass_fraction, 0.01)  # Steps in terms of fraction
speed = np.arange(300, 440, 10)

# Initialize arrays to store fuel flow values for each engine
FF_values1 = np.zeros((len(mass), len(speed)))
FF_values2 = np.zeros((len(mass), len(speed)))

# Calculate fuel flow for each engine
for i, mass_fraction in enumerate(mass):
    m = mass_fraction * MTOW  # Convert mass fraction back to kg for the calculation
    for j, s in enumerate(speed):
        FF_values1[i, j] = fuelflow1.enroute(mass=m, tas=s, alt=alt)
        FF_values2[i, j] = fuelflow2.enroute(mass=m, tas=s, alt=alt)

# Compute the relative difference in fuel flow (engine2 - engine1) / engine1
relative_difference = ((FF_values2 - FF_values1) / FF_values1) * 100

# Generate a meshgrid for plotting
mass_grid, speed_grid = np.meshgrid(mass, speed, indexing='ij')

# Plotting the relative difference
fig1 = plt.figure()
ax1 = fig1.gca()

contourf = plt.contourf(mass_grid, speed_grid, relative_difference, cmap='coolwarm', levels=100)
cbar = plt.colorbar(contourf)
cbar.set_label(r'Fuel-flow $\Delta_{rel}$ (%)', fontsize=20, fontname="Times New Roman")

# Customize colorbar tick labels
cbar.ax.tick_params(labelsize=18)  # Set font size of the colorbar tick labels
for label in cbar.ax.get_yticklabels():
    label.set_family("Times New Roman")
    #label.set_weight("bold")

# Label axes
plt.xlabel('Mass Fraction', fontsize=22, fontname="Times New Roman")
plt.ylabel('TAS (kts)', fontsize=22, fontname="Times New Roman")

plt.xticks(fontsize=20, fontname="Times New Roman")
plt.yticks(fontsize=20, fontname="Times New Roman")

# High DPI for better image quality
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

plt.xlim([0.1, 0.84])
plt.ylim([300, 430])

# Adjust figure size
F = plt.gcf()
Size = F.get_size_inches()
F.set_size_inches(Size[0]*1.5, Size[1]*1.5, forward=True)

# Axis limits


plt.savefig("A321/A321_V2530-A5.png")

#plt.title(f'Relative Difference in Fuel Flow: {engine2} vs. {engine1}', fontsize=22, fontname="Times New Roman")

plt.show()

