import pandas as pd
import matplotlib.pyplot as plt

# Define file paths
file_path_1 = 'Data/EEA2019/ICL_EEA2019.csv'
file_path_2 = 'Data/OAP/Emissions_Summary_PF_0.7.csv'

short_range = False

plt.style.use('seaborn-deep')

# Load data into dataframes
df1 = pd.read_csv(file_path_1)
df2 = pd.read_csv(file_path_2)

# Filter for a specific aircraft type
aircraft_type = 'B77W'
df2_filtered = df2[df2['Aircraft IATA code'] == aircraft_type]

# Filter dataframe 1 to include only rows with flight IDs present in dataframe 2
df1_filtered = df1[df1['flight_id'].isin(df2_filtered['flight_id'])]

if short_range:
    # Define bins for 500 nm distance intervals up to 2000 nm
    bins_500 = [0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000]
    labels_500 = ['0-250', '250-500', '500-750', '750-1000', '1000-1250', '1250-1500', '1500-1750', '1750-2000']
else:
    # Define bins for 500 nm distance intervals up to 6000 nm
    bins_500 = [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000]
    labels_500 = ['0-500', '500-1000', '1000-1500', '1500-2000', '2000-2500', '2500-3000', '3000-3500', '3500-4000', '4000-4500', '4500-5000', '5000-5500', '5500-6000']

# Create bins for total distance in the filtered dataframe and dataframe 2
df1_filtered['Distance_bin'] = pd.cut(df1_filtered['Distance'], bins=bins_500, labels=labels_500, right=False)
df2_filtered['Distance_bin'] = pd.cut(df2_filtered['Total distance (nm) (FF)'], bins=bins_500, labels=labels_500, right=False)

# Convert fuel burnt values from Kg to tonnes
df1_filtered['Fuel_burnt (CCD) EEA'] = df1_filtered['Fuel_burnt (CCD) EEA'] / 1000
df2_filtered['Fuel_burnt (FF)'] = df2_filtered['Fuel_burnt (FF)'] / 1000

# Group by distance bin and calculate mean fuel burnt
mean_fuel_burnt_df1_500 = df1_filtered.groupby('Distance_bin')['Fuel_burnt (CCD) EEA'].mean()
mean_fuel_burnt_df2_500 = df2_filtered.groupby('Distance_bin')['Fuel_burnt (FF)'].mean()

# Calculate relative error
relative_error = abs(mean_fuel_burnt_df1_500 - mean_fuel_burnt_df2_500) / mean_fuel_burnt_df1_500

print(relative_error)

# Combine relative error and distance bin into a DataFrame
relative_error_df = pd.DataFrame({
    'Distance_bin': relative_error.index,
    'Relative_error': relative_error.values
})

# Save the DataFrame to a CSV file
relative_error_df.to_csv('Output/B77W/RED_PF07.csv', index=False)

