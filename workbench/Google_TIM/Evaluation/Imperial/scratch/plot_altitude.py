import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the CSV file
file_path = 'combined_processed_A319.csv'  # Change this to your actual file path
df = pd.read_csv(file_path)

# Group the data by flight_id
grouped = df.groupby('flight_id')

# Plot all flight paths in one plot
    # Start plotting
fig1 = plt.figure()
ax1 = fig1.gca()

# Create a plot for each flight_id
for flight_id, data in grouped:
    plt.plot(data['cumulative_distance_nmi'], data['altitude_ft']/100, marker='o', color = 'gray', label=flight_id, ms = 0, linewidth = 2)

plt.xlabel('Distance (nmi)',fontname="Times New Roman", fontsize=20)
plt.ylabel('Flight Level',fontname="Times New Roman", fontsize=20)

ax1.spines['top'].set_linewidth(1.5)
ax1.spines['bottom'].set_linewidth(1.5)
ax1.spines['left'].set_linewidth(1.5)
ax1.spines['right'].set_linewidth(1.5)

F = plt.gcf()
Size = F.get_size_inches()
F.set_size_inches(Size[0]*1.5, Size[1]*1.5, forward=True)

plt.xticks(fontname="Times New Roman", fontsize=20)
plt.yticks(fontname="Times New Roman", fontsize=20)

plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300


plt.show()
