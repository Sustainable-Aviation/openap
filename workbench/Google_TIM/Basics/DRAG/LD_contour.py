import matplotlib.pyplot as plt
import numpy as np
import csv
from scipy.interpolate import griddata

# Path to the CSV file
csv_file_path = '/Users/prateekranjan/Documents/Github/openap/workbench/Google_TIM/Basics/DRAG/data/A359/cruise_drag_A359_fixed_mass01_multiple_altitude.csv'
#csv_file_path = '/Users/prateekranjan/Documents/Github/openap/workbench/Google_TIM/Basics/CR_THRUST/data/A359/cruise_thrust_A359-215.csv'
# Initialize empty lists for data
Altitude = []
Speed = []
CL = []
CD = []

# Read data from CSV file
with open(csv_file_path, mode='r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header
    for row in reader:
        altitude, speed, cl, cd = row
        Altitude.append(float(altitude))
        Speed.append(float(speed))
        CL.append(float(cl))
        CD.append(float(cd))

# Convert lists to numpy arrays and convert thrusts to kilo-Newtons for readability
Altitude = np.array(Altitude) * 0.01
Speed = np.array(Speed)
CL = np.array(CL)  
CD = np.array(CD) 
LoD = CL/CD
# Create grid for contour plot
altitude_grid, speed_grid = np.meshgrid(np.unique(Altitude), np.unique(Speed))

# Interpolate LoD values for the grid
LoD_grid = griddata((Altitude, Speed), LoD, (altitude_grid, speed_grid), method='cubic')

# Plot setup
fig1 = plt.figure()
ax1 = fig1.gca()


# Determine your desired vmin and vmax values for the colormap
vmin_value = 5
vmax_value = 18



# Generate contour plot
contourf = plt.contourf(altitude_grid, speed_grid, LoD_grid, levels=30, cmap='coolwarm',vmin=vmin_value, vmax=vmax_value)

# Generate contour lines on top of the filled contour
contour = plt.contour(altitude_grid, speed_grid, LoD_grid, levels=30, colors='black' ,vmin=vmin_value, vmax=vmax_value)

# Label the contour lines
texts = plt.clabel(contour, inline=True, fontsize=10, fmt='%1.1f')

# Set the weight to bold for all Text objects
#for text in texts:
#    text.set_weight('bold')

# Add colorbar and its title
cbar = plt.colorbar(contourf)

# Set custom tick values
#tick_values = np.linspace(vmin_value, vmax_value, num=8)  #  6 evenly spaced ticks from vmin to vmax
#cbar.set_ticks(tick_values)

# Set label of the colorbar
cbar.set_label('L/D', fontsize=20, fontname="Times New Roman") #weight='bold')  # Colorbar title

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
plt.xlim([300, 405])
plt.ylim([301, 405])

# Titles and labels
#plt.title('Takeoff Thrust Contour Plot', fontsize=24, fontname="Times New Roman")
plt.xlabel('Flight Level', fontsize=22, fontname="Times New Roman")
plt.ylabel('TAS (kts)', fontsize=22, fontname="Times New Roman")
plt.savefig('data/A359/A359_CRZ_M50T_LoD.png', dpi=300)  # Save the figure
plt.show()
