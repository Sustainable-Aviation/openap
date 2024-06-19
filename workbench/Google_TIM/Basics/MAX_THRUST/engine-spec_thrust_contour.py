from openap import prop, Thrust, Drag, WRAP
from openap.traj import Generator
import numpy as np
import matplotlib.pyplot as plt
import csv
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata


import numpy as np
import matplotlib.pyplot as plt

# Import Airbus A320 with CFM-56
ac1 = prop.aircraft('A320')


eng1 = prop.engine('CFM56-5-A1')

ac1_name = ac1['aircraft']
ac1_family = ac1_name.replace("Airbus ", "")  # Including the space after "Airbus" to remove it as well


# Determine your desired vmin and vmax values for the colormap
vmin_value = 64
vmax_value = 220

#Take off conditions -> Assume TO at sea level, all the way upto 14000 feet
#                    -> Assume TO speeds from 130 kts to 220 kts 
TO_alt = range(0, 14000, 300)
TO_spid = range(130, 220, 10)

#Climb conditions -> Assume CLB range from 3000 feet to 16000 feet
#                 -> Assume TO speeds from 220 kts to 280 kts 
CL_alt = range(3000, 20000, 300)
CL_spid = range(220, 280, 10)

# Cruise conditions -> Assume CR range from 3000 feet to 16000 feet
#                   -> Assume TO speeds from 220 kts to 280 kts 
CR_alt = range(20000, 40000, 300)
CR_spid = range(280, 440, 10)

# THRUST CALCULATION------->
thrust = Thrust(ac=ac1_family, eng=eng1['name'])

# Initialize a 2D numpy array to store the thrust values
TO_thrust_values = np.zeros((len(TO_alt), len(TO_spid)))
CL_thrust_values = np.zeros((len(CL_alt), len(CL_spid)))
CR_thrust_values = np.zeros((len(CR_alt), len(CR_spid)))


for i, alt in enumerate(TO_alt):
    for j, speed in enumerate(TO_spid):
        # Compute takeoff thrust
        THRUST_TO = thrust.takeoff(tas=speed, alt=alt)
        TO_thrust_values[i, j] = THRUST_TO

for i, alt in enumerate(CL_alt):
    for j, speed in enumerate(CL_spid):
        # Compute takeoff thrust
        THRUST_CL = thrust.climb(tas=speed, alt=alt, roc = 1000)
        CL_thrust_values[i, j] = THRUST_CL

for i, alt in enumerate(CR_alt):
    for j, speed in enumerate(CR_spid):
        # Compute takeoff thrust
        CRUISE_CL = thrust.cruise(tas=speed, alt=alt)
        CR_thrust_values[i, j] = THRUST_CL        


# Converting range objects to numpy arrays
TO_alt_array = np.array(TO_alt)
TO_spid_array = np.array(TO_spid)

CL_alt_array = np.array(CL_alt)
CL_spid_array = np.array(CL_spid)

CR_alt_array = np.array(CR_alt)
CR_spid_array = np.array(CR_spid)


# Combining altitude and speed arrays
all_alt = np.concatenate((TO_alt_array, CL_alt_array, CR_alt_array))
all_spd = np.concatenate((TO_spid_array, CL_spid_array, CR_spid_array))


# Preparing data for 2D interpolation
unique_alt = np.unique(all_alt)
unique_spd = np.unique(all_spd)
grid_alt, grid_spd = np.meshgrid(unique_alt, unique_spd, indexing='ij')
flat_alt = np.concatenate([np.tile(TO_alt_array, len(TO_spid_array)), np.tile(CL_alt_array, len(CL_spid_array)), np.tile(CR_alt_array, len(CR_spid_array))])
flat_spd = np.concatenate([np.repeat(TO_spid_array, len(TO_alt_array)), np.repeat(CL_spid_array, len(CL_alt_array)), np.repeat(CR_spid_array, len(CR_alt_array))])
flat_thrust = np.concatenate([TO_thrust_values.flatten(), CL_thrust_values.flatten(), CR_thrust_values.flatten()])

# Interpolating thrust values over the grid
grid_thrust = griddata((flat_alt, flat_spd), flat_thrust/1000, (grid_alt, grid_spd), method='linear')

# 2D Contour plotting
fig1 = plt.figure()
ax1 = fig1.gca()

contourf = plt.contourf(unique_spd, unique_alt/100, grid_thrust, cmap='coolwarm', vmin=vmin_value, vmax=vmax_value, levels=50)
cbar = plt.colorbar(contourf)
cbar.set_label('Max. Thrust (kN)', fontsize=20, fontname="Times New Roman")

# Customize colorbar tick labels
cbar.ax.tick_params(labelsize=18)  # Set font size of the colorbar tick labels
for label in cbar.ax.get_yticklabels():
    label.set_family("Times New Roman")
    #label.set_weight("bold")

for axis in ['top', 'bottom', 'left', 'right']:
    ax1.spines[axis].set_linewidth(1.5)

# Modify axes ticks properties
plt.xticks(fontname="Times New Roman", fontsize=20)
plt.yticks(fontname="Times New Roman", fontsize=20)

ax1.tick_params(bottom=True, top=True, left=True, right=True)
ax1.tick_params(labelbottom=True, labeltop=False, labelleft=True, labelright=False)
ax1.tick_params(which='major', length=10, width=1.2, direction='in')
ax1.tick_params(which='minor', length=5, width=1.2, direction='in')

F = plt.gcf()
Size = F.get_size_inches()
F.set_size_inches(Size[0]*1.5, Size[1]*1.5, forward=True)

# Axis limits
plt.xlim([all_spd.min(),all_spd.max() ])
plt.ylim([all_alt.min()/100,all_alt.max()/100 ])





# High DPI for better image quality
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

plt.title('Max. Thrust for CFM56-5-A1 engine', fontsize = 22, fontname = "Times New Roman")
plt.xlabel('Speed (knots)', fontsize = 22, fontname = "Times New Roman")
plt.ylabel('Flight Level', fontsize = 22, fontname = "Times New Roman")

plt.savefig('A320/CFM56-5-A1.png', dpi=300)  # Save the figure
plt.show()

