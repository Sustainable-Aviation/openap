import matplotlib.pyplot as plt
import numpy as np
import csv
from scipy.interpolate import griddata

# Path to the CSV file
#csv_file_path = '/Users/prateekranjan/Documents/Github/openap/workbench/Google_TIM/Basics/data/A320/takeoff_thrust_A320-214.csv'
csv_file_path = '/Users/prateekranjan/Documents/Github/openap/workbench/Google_TIM/Basics/data/A320/takeoff_thrust_A320-215.csv'
# Initialize empty lists for data
altitudes = []
speeds = []
thrusts = []

# Read data from CSV file
with open(csv_file_path, mode='r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header
    for row in reader:
        altitude, speed, thrust = row
        altitudes.append(float(altitude))
        speeds.append(float(speed))
        thrusts.append(float(thrust))

# Convert lists to numpy arrays and convert thrusts to kilo-Newtons for readability
altitudes = np.array(altitudes)
speeds = np.array(speeds)
thrusts = np.array(thrusts) * 1e-3  # Convert thrust to kN for better readability

# Create grid for contour plot
alt_grid, speed_grid = np.meshgrid(np.unique(altitudes), np.unique(speeds))

# Interpolate thrust values for the grid
thrust_grid = griddata((altitudes, speeds), thrusts, (alt_grid, speed_grid), method='cubic')

# Plot setup
fig1 = plt.figure()
ax1 = fig1.gca()

# Generate contour plot
contour = plt.contourf(alt_grid, speed_grid, thrust_grid, levels=50, cmap='coolwarm')

# Add colorbar and its title
cbar = plt.colorbar(contour)

cbar.set_label('Takeoff Thrust (kN)', fontsize=20, fontname="Times New Roman") #weight='bold')  # Colorbar title

# Customize colorbar tick labels
cbar.ax.tick_params(labelsize=18)  # Set font size of the colorbar tick labels
for label in cbar.ax.get_yticklabels():
    label.set_family("Times New Roman")
    #label.set_weight("bold")

# Contour line labels with black color
plt.clabel(contour, inline=True, fontsize=0, fmt='%1.0f', colors='k')  # Make contour labels black

# Further styling
for axis in ['top', 'bottom', 'left', 'right']:
    ax1.spines[axis].set_linewidth(1.5)

# Modify axes ticks properties
plt.xticks(fontname="Times New Roman", fontsize=20)
plt.yticks(fontname="Times New Roman", fontsize=20)

ax1.tick_params(bottom=True, top=True, left=True, right=True)
ax1.tick_params(labelbottom=True, labeltop=False, labelleft=True, labelright=False)
ax1.tick_params(which='major', length=10, width=1.2, direction='in')
ax1.tick_params(which='minor', length=5, width=1.2, direction='in')

# Adjust figure size
F = plt.gcf()
Size = F.get_size_inches()
F.set_size_inches(Size[0]*1.5, Size[1]*1.5, forward=True)

# High DPI for better image quality
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

# Axis limits
plt.xlim([0, 14000])
plt.ylim([110, 160])

# Titles and labels
#plt.title('Takeoff Thrust Contour Plot', fontsize=24, fontname="Times New Roman")
plt.xlabel('Altitude (ft)', fontsize=22, fontname="Times New Roman")
plt.ylabel('TAS (kts)', fontsize=22, fontname="Times New Roman")
#plt.savefig('data/A320/A320-214_TO_Contour.png', dpi=300)  # Save the figure
plt.savefig('data/A320/A320-215_TO_Contour.png', dpi=300)  # Save the figure
plt.show()
