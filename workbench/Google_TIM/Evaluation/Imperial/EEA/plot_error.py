import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('seaborn-deep')

# Load the datasets
file_path_1 = 'Output/B77W/RED_PF01.csv'
file_path_2 = 'Output/B77W/RED_PF02.csv'
file_path_3 = 'Output/B77W/RED_PF03.csv'
file_path_4 = 'Output/B77W/RED_PF04.csv'
file_path_5 = 'Output/B77W/RED_PF05.csv'
file_path_6 = 'Output/B77W/RED_PF06.csv'
file_path_7 = 'Output/B77W/RED_PF07.csv'
#file_path_8 = 'Output/B77W/RED_PF08.csv'

data_1 = pd.read_csv(file_path_1).dropna()
data_2 = pd.read_csv(file_path_2).dropna()
data_3 = pd.read_csv(file_path_3).dropna()
data_4 = pd.read_csv(file_path_4).dropna()
data_5 = pd.read_csv(file_path_5).dropna()
data_6 = pd.read_csv(file_path_6).dropna()
data_7 = pd.read_csv(file_path_7).dropna()
#data_8 = pd.read_csv(file_path_8).dropna()

# Multiply the relative error by 100
data_1['Relative_error'] *= 100
data_2['Relative_error'] *= 100
data_3['Relative_error'] *= 100
data_4['Relative_error'] *= 100
data_5['Relative_error'] *= 100
data_6['Relative_error'] *= 100
data_7['Relative_error'] *= 100
#data_8['Relative_error'] *= 100

# Combine data into a list for easier processing
datasets = [data_1, data_2, data_3, data_4, data_5, data_6, data_7]
labels = ['PF: 0.1', 'PF: 0.2', 'PF: 0.3', 'PF: 0.4', 'PF: 0.5', 'PF: 0.6', 'PF: 0.7']
pf_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]

# Plotting the combined bar chart
fig1 = plt.figure()
ax1 = fig1.gca()

# Set background colors
#fig1.patch.set_facecolor('C0')  # Set the figure background color
#ax1.set_facecolor('gray')  # Set the axes background color

# Width of each bar
bar_width = 0.1

# Positions of the bars on the x-axis
r = np.arange(len(data_1['Distance_bin']))
positions = [r + bar_width * i for i in range(len(datasets))]

# Using a colormap
cmap = plt.cm.Blues
colors = cmap(np.linspace(0, 1, len(datasets)))

# Creating the bars
for pos, data, color, label in zip(positions, datasets, colors, labels):
    plt.bar(pos, data['Relative_error'], color=color, width=bar_width, edgecolor='gray', label=label)
    #plt.bar(pos, data['Relative_error'], color=color, width=bar_width, label=label)

# Adding labels and title
plt.xlabel('Distance Bin (nmi)', fontname="Times New Roman", fontsize=20)
plt.ylabel('Relative Error (%)', fontname="Times New Roman", fontsize=20)
#plt.title('Relative Error for Each Distance Bin (Comparison)', fontweight='bold')

for axis in ['top', 'bottom', 'left', 'right']:
    ax1.spines[axis].set_linewidth(1.0)

# Adding the distance bin labels at the center of the bars
plt.xticks([r + bar_width * 1.5 for r in range(len(data_1['Distance_bin']))], data_1['Distance_bin'], rotation=45, fontname="Times New Roman", fontsize=14)
plt.yticks(fontname="Times New Roman", fontsize=14)

# Adding the colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=min(pf_values), vmax=max(pf_values)))
sm.set_array([])
cbar = plt.colorbar(sm)
cbar.set_label('Payload fraction', rotation=270, labelpad=25, fontname="Times New Roman", fontsize=20)

# Increase colorbar tick labels size
cbar.ax.tick_params(labelsize=16)

#plt.ylim([0, 30])  # short range
plt.ylim([0, 80])  # short range

plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

F = plt.gcf()
Size = F.get_size_inches()
F.set_size_inches(Size[0]*1.7, Size[1]*1.5, forward=True)

plt.tight_layout()
plt.savefig('Output/B77W/Relative_Error/B77W_MultiPF_Rel_Error.png',dpi=300)

# Show the plot
plt.show()

