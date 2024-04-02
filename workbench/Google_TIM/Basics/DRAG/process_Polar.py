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
    '/Users/prateekranjan/Documents/Github/openap/workbench/Google_TIM/Basics/DRAG/data/A320/cruise_drag_A320-111.csv',
    #'/Users/prateekranjan/Documents/Github/openap/workbench/Google_TIM/Basics/data/A320/cruise_drag_A320-211.csv',
    '/Users/prateekranjan/Documents/Github/openap/workbench/Google_TIM/Basics/DRAG/data/A320/cruise_drag_A320-212.csv',
    '/Users/prateekranjan/Documents/Github/openap/workbench/Google_TIM/Basics/DRAG/data/A320/cruise_drag_A320-214.csv',
    '/Users/prateekranjan/Documents/Github/openap/workbench/Google_TIM/Basics/DRAG/data/A320/cruise_drag_A320-215.csv',
    '/Users/prateekranjan/Documents/Github/openap/workbench/Google_TIM/Basics/DRAG/data/A320/cruise_drag_A320-216.csv',
    '/Users/prateekranjan/Documents/Github/openap/workbench/Google_TIM/Basics/DRAG/data/A320/cruise_drag_A320-231.csv',
    '/Users/prateekranjan/Documents/Github/openap/workbench/Google_TIM/Basics/DRAG/data/A320/cruise_drag_A320-232.csv',
    '/Users/prateekranjan/Documents/Github/openap/workbench/Google_TIM/Basics/DRAG/data/A320/cruise_drag_A320-233.csv',
    # Add more file paths as needed
]

labels = itertools.cycle(('A320-111','A320-212','A320-214','A320-215','A320-216','A320-231','A320-232','A320-233'))

tas_specific = 420

# Prepare markers and colors to differentiate between files in the plot
markers = itertools.cycle(('o', 's', '^', 'v', '>', '<', 'p', 'P', '*', 'X'))  # Example markers
#colors = itertools.cycle(('b', 'g', 'r', 'c', 'm', 'y', 'k'))  # Example colors

fig1 = plt.figure()
ax1 = fig1.gca()

for csv_file in csv_files:
    CL = []
    CD = []

    with open(csv_file, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tas = float(row['TAS (kts)'])
            if tas == tas_specific:
                cl = float(row['CL'])
                cd = float(row['CD'])
                CL.append(cl)
                CD.append(cd)

    # Plotting for the current CSV file
    ax1.plot(CL, CD, marker=next(markers),mec = 'black', linestyle='-',ms = 8, linewidth = 2, label=next(labels))

#plt.title(f'Altitude vs. cruise Thrust at TAS = {tas_specific} kts')
ax1.set_xlabel(r'$C_L$',fontsize = 22, fontname="Times New Roman")
ax1.set_ylabel(r'$C_D$',fontsize = 22, fontname="Times New Roman")
#plt.grid(True)
plt.legend(loc = 'upper left', frameon=True, fontsize = 14)

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



plt.xlim([0.015, 1])
plt.ylim([0.015,0.046])

#plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
#plt.tight_layout()
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.savefig('data/A320/A320_CR_420.png', dpi=300)  # Save the figure
plt.show()
