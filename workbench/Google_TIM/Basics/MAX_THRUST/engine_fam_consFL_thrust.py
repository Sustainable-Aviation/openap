import matplotlib.pyplot as plt
import csv
import matplotlib.ticker as tck
import matplotlib.ticker as ticker
import itertools  # For cycling through a list of markers and colors

#plt.style.use('seaborn-v0_8-deep')
plt.style.use('seaborn-dark-palette')
#plt.style.use('seaborn-deep')



# Define your CSV files paths here
csv_files = [
    '/Users/prateekranjan/Documents/Github/openap/workbench/Google_TIM/Basics/CR_THRUST/data/A319/cruise_thrust_A319-111.csv',
    #'/Users/prateekranjan/Documents/Github/openap/workbench/Google_TIM/Basics/data/A320/cruise_thrust_A320-211.csv',
    '/Users/prateekranjan/Documents/Github/openap/workbench/Google_TIM/Basics/CR_THRUST/data/A319/cruise_thrust_A319-112.csv',
    '/Users/prateekranjan/Documents/Github/openap/workbench/Google_TIM/Basics/CR_THRUST/data/A319/cruise_thrust_A319-113.csv',
    '/Users/prateekranjan/Documents/Github/openap/workbench/Google_TIM/Basics/CR_THRUST/data/A319/cruise_thrust_A319-114.csv',
    '/Users/prateekranjan/Documents/Github/openap/workbench/Google_TIM/Basics/CR_THRUST/data/A319/cruise_thrust_A319-115.csv',
    '/Users/prateekranjan/Documents/Github/openap/workbench/Google_TIM/Basics/CR_THRUST/data/A319/cruise_thrust_A319-131.csv',
    '/Users/prateekranjan/Documents/Github/openap/workbench/Google_TIM/Basics/CR_THRUST/data/A319/cruise_thrust_A319-132.csv',
    '/Users/prateekranjan/Documents/Github/openap/workbench/Google_TIM/Basics/CR_THRUST/data/A319/cruise_thrust_A319-133.csv',
    # Add more file paths as needed
]

labels = itertools.cycle(('CFM56-5B5','CFM56-5B6','CFM56-5A4','CFM56-5A5','CFM56-5B7','V2522-A5','V2524-A5','V2527M-A5'))

fl_specific = 35000  # Specify the Flight Level for which you want to plot the data

# Prepare markers and colors to differentiate between files in the plot
markers = itertools.cycle(('o', 's', '^', 'v', '>', '<', 'p', 'P', '*', 'X'))  # Example markers
#colors = itertools.cycle(('b', 'g', 'r', 'c', 'm', 'y', 'k'))  # Example colors

fig1 = plt.figure()
ax1 = fig1.gca()

for csv_file in csv_files:
    speeds = []
    thrusts = []

    with open(csv_file, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            fl = float(row['Altitude (ft)'])
            if fl == fl_specific:
                tas = float(row['TAS (kts)'])
                thrust = float(row['Cruise Thrust (N)'])
                speeds.append(tas/1)
                thrusts.append(thrust/1000)

    # Plotting for the current CSV file
    ax1.plot(speeds, thrusts, marker=next(markers),mec = 'black', linestyle='-',ms = 12, linewidth = 2, label=next(labels))

#plt.title(f'Altitude vs. cruise Thrust at TAS = {tas_specific} kts')
ax1.set_xlabel('Speed (knots)',fontsize = 22, fontname="Times New Roman")
ax1.set_ylabel('Max. Thrust (kN)',fontsize = 22, fontname="Times New Roman")
#plt.grid(True)
plt.legend(loc = 'upper right', frameon=True, fontsize = 14)
#plt.legend(loc='upper right', frameon=True, fontsize=14, ncol=8)


# Plot grid properties
ax1.grid(which='major', color='black', linestyle='-', linewidth='0.05')
ax1.minorticks_on()
ax1.grid(which='minor', color='black', linestyle=':', linewidth='0.05')

for axis in ['top','bottom','left','right']:
  ax1.spines[axis].set_linewidth(1.5)

# Modify axes ticks properties
plt.xticks(fontname = "Times New Roman", fontsize  = 20)
plt.yticks(fontname = "Times New Roman", fontsize = 20)

ax1.tick_params(bottom=True, top=True, left=True, right=True)
ax1.tick_params(labelbottom=True, labeltop=False, labelleft=True, labelright=False)

ax1.tick_params(which='major', length=10, width=1.2, direction='in')
ax1.tick_params(which='minor', length=5, width=1.2, direction='in')


F = plt.gcf()
Size = F.get_size_inches()
F.set_size_inches(Size[0]*1.5, Size[1]*1.5, forward=True) # Set forward to True to resize window along with plot in figure.



plt.xlim([320, 450])
plt.ylim([41,64])

#plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
#plt.tight_layout()
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.savefig('A319/A319_eng_family_consFL.png', dpi=300)  # Save the figure
plt.show()

# Desired speed in knots
desired_speed = 440

# Initialize lists to store thrust values at the desired speed
thrust_values_at_desired_speed = []

# Iterate over each CSV file to collect thrust data at the desired speed
for csv_file in csv_files:
    with open(csv_file, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            fl = float(row['Altitude (ft)'])
            if fl == fl_specific:
                tas = float(row['TAS (kts)'])
                thrust = float(row['Cruise Thrust (N)']) / 1000  # Converting to kN for consistency
                # Check if the speed matches the desired speed (you might want to allow some tolerance)
                if tas == desired_speed:
                    thrust_values_at_desired_speed.append(thrust)


# Compute max and min thrust values at the desired speed
if thrust_values_at_desired_speed:
    max_thrust = max(thrust_values_at_desired_speed)
    min_thrust = min(thrust_values_at_desired_speed)
    delta_thrust = max_thrust - min_thrust
    #print(f"Max thrust at {desired_speed} knots: {max_thrust} kN")
    #print(f"Min thrust at {desired_speed} knots: {min_thrust} kN")
    print("Delta_thrust: ", delta_thrust)
    
else:
    print(f"No thrust data found for {desired_speed} knots.")