import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn-deep')

# Load the Excel file
file_path = 'Data/ImperialTIMJan2019.xlsx'
xls = pd.ExcelFile(file_path)

# Load the "Aircraft Detail" sheet
aircraft_detail_df = pd.read_excel(xls, sheet_name='Aircraft Detail')

# Filter the dataset for 737 Max 8 series
max8_df = aircraft_detail_df[aircraft_detail_df['Series'] == '757-200']

# Plot the frequency distribution for the 'Number of Seats' column
fig1 = plt.figure()
ax1 = fig1.gca()


plt.hist(max8_df['Number of Seats'].dropna(), bins=30, color = 'C2', edgecolor='black')
plt.title('Frequency Distribution of Number of Seats for B757-200 Series',fontname = "Times New Roman", fontsize = 20)
plt.xlabel('Number of Seats',fontname = "Times New Roman", fontsize = 20)
plt.ylabel('Frequency', fontname = "Times New Roman", fontsize = 20)

for axis in ['top', 'bottom', 'left', 'right']:
            ax1.spines[axis].set_linewidth(1.5)

# Modify axes ticks properties
plt.xticks(fontname="Times New Roman", fontsize=20)
plt.yticks(fontname="Times New Roman", fontsize=20)

F = plt.gcf()
Size = F.get_size_inches()
F.set_size_inches(Size[0]*1.7, Size[1]*1.5, forward=True)

#plt.xlim([100, 200])

plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.savefig('Output/Plots/Seats/B752_bin.png')

# Show the plot
plt.show()
