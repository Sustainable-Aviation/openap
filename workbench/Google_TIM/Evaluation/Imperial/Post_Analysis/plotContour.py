import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata

def plot_fuel_burnt_contour(file_paths, aircraft_name):
    """
    Generates a filled contour plot for fuel burnt as a function of payload and total distance travelled
    for a specified aircraft, using data from the provided CSV files.

    Parameters:
    file_paths (list of str): List of file paths to the CSV files containing the emissions data.
    aircraft_name (str): The IATA code of the aircraft (e.g., 'A319').

    The CSV files are expected to have the following columns:
    - 'Aircraft IATA code': The aircraft code (e.g., 'A319')
    - 'Total distance (nm) (FF)': The total distance travelled in nautical miles
    - 'Payload (Kg)': The payload in kilograms
    - 'Fuel_burnt (FF)': The fuel burnt

    The function performs the following steps:
    1. Loads and concatenates data from all provided CSV files.
    2. Filters the data to include only rows where the aircraft type matches the specified aircraft name.
    3. Extracts the relevant columns (total distance, payload, and fuel burnt) and drops any rows with missing values.
    4. Interpolates the fuel burnt values over a grid of total distance and payload values.
    5. Creates a filled contour plot with the 'coolwarm' colormap.
    6. Adds labels and a color bar to the plot.
    7. Displays the plot.

    Example usage:
    file_paths = [
        '/path/to/Emissions_Summary_PF_0.1.csv',
        '/path/to/Emissions_Summary_PF_0.2.csv',
        ...
    ]
    aircraft_name = 'A319'
    plot_fuel_burnt_contour(file_paths, aircraft_name)
    """
    # Load and concatenate data from all files
    all_data = pd.concat([pd.read_csv(file) for file in file_paths])

    # Filter data for the specified aircraft
    aircraft_data = all_data[all_data['Aircraft IATA code'] == aircraft_name]

    # Extract relevant columns and drop rows with missing values
    aircraft_data = aircraft_data[['Total distance (nm) (FF)', 'Payload (Kg)', 'Fuel_burnt (FF)']].dropna()

    total_distance = aircraft_data['Total distance (nm) (FF)'].values
    payload = aircraft_data['Payload (Kg)'].values
    fuel_burnt = aircraft_data['Fuel_burnt (FF)'].values

    # Create a grid of total_distance and payload values
    grid_x, grid_y = np.mgrid[total_distance.min():total_distance.max():100j, payload.min():payload.max():100j]

    # Interpolate the fuel burnt values on the grid
    grid_z = griddata((total_distance, payload), fuel_burnt, (grid_x, grid_y), method='linear')

    # Create a filled contour plot
    # 2D Contour plotting
    fig1 = plt.figure()
    ax1 = fig1.gca()

    contourf = plt.contourf(grid_x, grid_y, grid_z, 50, cmap='coolwarm')
    cbar = plt.colorbar(contourf)
    cbar.set_label('Fuel burnt (kg)', fontsize=20, fontname="Times New Roman")

    # Customize colorbar tick labels
    cbar.ax.tick_params(labelsize=18)  # Set font size of the colorbar tick labels
    for label in cbar.ax.get_yticklabels():
        label.set_family("Times New Roman")

    for axis in ['top', 'bottom', 'left', 'right']:
        ax1.spines[axis].set_linewidth(1.5)

    # Modify axes ticks properties
    plt.xticks(fontname="Times New Roman", fontsize=20)
    plt.yticks(fontname="Times New Roman", fontsize=20)

    ax1.tick_params(bottom=True, top=True, left=True, right=True)
    ax1.tick_params(labelbottom=True, labeltop=False, labelleft=True, labelright=False)
    ax1.tick_params(which='major', length=10, width=1.2, direction='in')
    ax1.tick_params(which='minor', length=5, width=1.2, direction='in')

    # Axis limits
    plt.xlim([total_distance.min(),total_distance.max() ])
    plt.ylim([payload.min()/1,payload.max()/1 ])

    # High DPI for better image quality
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['savefig.dpi'] = 300

    # Add labels and a color bar
    plt.xlabel('Total Distance (nm)', fontsize = 22, fontname = "Times New Roman")
    plt.ylabel('Payload (Kg)', fontsize = 22, fontname = "Times New Roman")

    F = plt.gcf()
    Size = F.get_size_inches()
    F.set_size_inches(Size[0]*1.5, Size[1]*1.5, forward=True)

    plt.savefig('Contours/A319/A319_115.png', dpi=300)  # Save the figure
    # Show the plot
    plt.show()

# Example usage
file_paths = [
    '../Output/Ver_2/No_Wind/Emissions_Summary_PF_0.1.csv',
    '../Output/Ver_2/No_Wind/Emissions_Summary_PF_0.2.csv',
    '../Output/Ver_2/No_Wind/Emissions_Summary_PF_0.3.csv',
    '../Output/Ver_2/No_Wind/Emissions_Summary_PF_0.4.csv',
    '../Output/Ver_2/No_Wind/Emissions_Summary_PF_0.5.csv',
    '../Output/Ver_2/No_Wind/Emissions_Summary_PF_0.6.csv',
    '../Output/Ver_2/No_Wind/Emissions_Summary_PF_0.7.csv',
    '../Output/Ver_2/No_Wind/Emissions_Summary_PF_0.8.csv'
]
aircraft_name = 'A319'
plot_fuel_burnt_contour(file_paths, aircraft_name)
