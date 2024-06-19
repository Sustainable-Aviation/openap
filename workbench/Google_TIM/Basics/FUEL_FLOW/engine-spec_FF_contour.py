import numpy as np
import matplotlib.pyplot as plt
from openap import prop, FuelFlow


ac1 = prop.aircraft('A321')

print(ac1)

# Get the MTOW for this airframe
MTOW = ac1['limits']['MTOW']  # Kgs

min_mass_fraction = 0.1
max_mass_fraction = 0.85

fuelflow = FuelFlow(ac='A320', eng='CFM56-5-A1')

# Fixed altitude
ALT = 35000

# Creating mass fractions directly for plotting
MASS = np.arange(min_mass_fraction, max_mass_fraction, 0.01)  # Steps in terms of fraction

SPEED = np.arange(300, 440, 10)

FF_values = np.zeros((len(MASS), len(SPEED)))

for i, mass_fraction in enumerate(MASS):
    mass = mass_fraction * MTOW  # Convert mass fraction back to kg for the calculation
    for j, speed in enumerate(SPEED):
        FF_values[i, j] = fuelflow.enroute(mass=mass, tas=speed, alt=ALT)

# Generating a meshgrid for plotting
MASS_grid, SPEED_grid = np.meshgrid(MASS, SPEED, indexing='ij')

# Create contour plot
# Plot setup
fig1 = plt.figure()
ax1 = fig1.gca()

contourf = plt.contourf(MASS_grid, SPEED_grid, FF_values, cmap='coolwarm', levels=100)
cbar = plt.colorbar(contourf)
cbar.set_label('Fuel-flow (Kg/s)', fontsize=20, fontname="Times New Roman")


# Customize colorbar tick labels
cbar.ax.tick_params(labelsize=18)  # Set font size of the colorbar tick labels
for label in cbar.ax.get_yticklabels():
    label.set_family("Times New Roman")
    #label.set_weight("bold")


# Label axes with mass fractions in decimals
plt.xlabel('Mass Fraction', fontsize=22, fontname="Times New Roman")
plt.ylabel('TAS (kts)', fontsize=22, fontname="Times New Roman")

plt.xticks(fontsize=20, fontname="Times New Roman")
plt.yticks(fontsize=20, fontname="Times New Roman")

# High DPI for better image quality
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300



# Adjust figure size
F = plt.gcf()
Size = F.get_size_inches()
F.set_size_inches(Size[0]*1.5, Size[1]*1.5, forward=True)

# Axis limits
plt.xlim([0.1, 0.84])
plt.ylim([300, 430])

plt.savefig("A321/A321_Baseline_FF.png")

plt.show()


