import pandas as pd
import matplotlib.pyplot as plt

# Define file paths
file_path_1 = 'Data/EEA2019/ICL_EEA2019.csv'
file_path_2 = 'Data/OAP/Emissions_Summary_PF_0.1.csv'

plt.style.use('seaborn-deep')

# Load data into dataframes
df1 = pd.read_csv(file_path_1)
df2 = pd.read_csv(file_path_2)

# Filter dataframe 1 to include only rows with flight IDs present in dataframe 2
df1_filtered = df1[df1['flight_id'].isin(df2['flight_id'])]

# Define bins for 500 nm distance intervals up to 6000 nm
bins_500 = [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000]
labels_500 = ['0-500', '500-1000', '1000-1500', '1500-2000', '2000-2500', '2500-3000', '3000-3500', '3500-4000', '4000-4500', '4500-5000', '5000-5500', '5500-6000']

# Create bins for total distance in the filtered dataframe and dataframe 2
df1_filtered['Distance_bin'] = pd.cut(df1_filtered['Distance'], bins=bins_500, labels=labels_500, right=False)
df2['Distance_bin'] = pd.cut(df2['Total distance (nm) (FF)'], bins=bins_500, labels=labels_500, right=False)

# Convert fuel burnt values from Kg to tonnes
df1_filtered['Fuel_burnt (CCD) EEA'] = df1_filtered['Fuel_burnt (CCD) EEA'] / 1000
df2['Fuel_burnt (FF)'] = df2['Fuel_burnt (FF)'] / 1000

# Group by distance bin and calculate mean fuel burnt
mean_fuel_burnt_df1_500 = df1_filtered.groupby('Distance_bin')['Fuel_burnt (CCD) EEA'].mean()
mean_fuel_burnt_df2_500 = df2.groupby('Distance_bin')['Fuel_burnt (FF)'].mean()

# Calculate relative error
relative_error = abs(mean_fuel_burnt_df1_500 - mean_fuel_burnt_df2_500) / mean_fuel_burnt_df1_500

# Plotting the mean fuel burnt for each distance bin from both dataframes
fig1 = plt.figure()
ax1 = fig1.gca()

bar1 = plt.bar(mean_fuel_burnt_df1_500.index, mean_fuel_burnt_df1_500, width=0.4, align='center', label='EEA2019', edgecolor='black', color='dimgray')
bar2 = plt.bar(mean_fuel_burnt_df2_500.index, mean_fuel_burnt_df2_500, width=0.4, align='edge', label='OpenAP', edgecolor='black', color='steelblue')

# Annotate bars with relative error above df2 bars
for bar, err in zip(bar2, relative_error):
    height = bar.get_height()
    ax1.annotate(f'{err:.2%}',
                 xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 3),  # 3 points vertical offset
                 textcoords="offset points",
                 ha='center', va='bottom', fontsize=12, color='black', fontname="Times New Roman")

plt.xlabel('Distance Bin (nm)', fontname="Times New Roman", fontsize=20)
plt.ylabel('Mean Fuel Burnt (Tonnes)', fontname="Times New Roman", fontsize=20)
#plt.title('Mean Fuel Burnt for Different Distance Bins (500 nm)')

for axis in ['top', 'bottom', 'left', 'right']:
    ax1.spines[axis].set_linewidth(1.5)

plt.xticks(fontname="Times New Roman", fontsize=14, rotation=45)
plt.yticks(fontname="Times New Roman", fontsize=14)

plt.legend(prop={'family': 'Times New Roman', 'size': 14})

plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

F = plt.gcf()
Size = F.get_size_inches()
F.set_size_inches(Size[0]*1.7, Size[1]*1.5, forward=True)

plt.ylim([0, 120])

plt.tight_layout()
plt.show()
