import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


contour_limits = (0, 500)

# Load the data from the CSV file
file_path = 'combined_processed_A321.csv'  # Change this to your actual file path
df = pd.read_csv(file_path)

# Group the data by flight_id
grouped = df.groupby('flight_id')

# Create a colormap based on true_airspeed_knots
#norm = plt.Normalize(df['true_airspeed_knots'].min(), df['true_airspeed_knots'].max())
norm = plt.Normalize(contour_limits[0], contour_limits[1])
cmap = plt.get_cmap('coolwarm')

# Plot all flight paths in one plot
fig1 = plt.figure()
ax1 = fig1.gca()

# Create a plot for each flight_id
for flight_id, data in grouped:
    colors = cmap(norm(data['true_airspeed_knots']))
    for i in range(len(data) - 1):
        plt.plot(data['cumulative_distance_nmi'].iloc[i:i+2], data['altitude_ft'].iloc[i:i+2] / 100,
                 marker='o', color=colors[i], label=flight_id if i == 0 else "", ms=0, linewidth=2)

plt.xlabel('Distance (nmi)', fontname="Times New Roman", fontsize=20)
plt.ylabel('Flight Level', fontname="Times New Roman", fontsize=20)

ax1.spines['top'].set_linewidth(1.5)
ax1.spines['bottom'].set_linewidth(1.5)
ax1.spines['left'].set_linewidth(1.5)
ax1.spines['right'].set_linewidth(1.5)

# Axis limits
plt.xlim([-10, 2500])
plt.ylim([-10, 400])

# Add colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax1)
cbar.set_label('True Airspeed (knots)', fontname="Times New Roman", fontsize=20)

# Customize colorbar tick labels
cbar.ax.tick_params(labelsize=18)  # Set font size of the colorbar tick labels
for label in cbar.ax.get_yticklabels():
    label.set_family("Times New Roman")


F = plt.gcf()
Size = F.get_size_inches()
F.set_size_inches(Size[0]*1.5, Size[1]*1.5, forward=True)

plt.xticks(fontname="Times New Roman", fontsize=20)
plt.yticks(fontname="Times New Roman", fontsize=20)



plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300



plt.tight_layout()
plt.savefig('Plots/A321/A321_ICL_alt_Profile.png', dpi=300)
plt.show()
