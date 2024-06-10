import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata

plt.style.use('seaborn-deep')

def plot_fuel_burnt_contour(file_paths, contour_limits):
    """
    Generates a filled contour plot for fuel burnt as a function of payload and total distance travelled
    for a specified aircraft, using data from the provided CSV files.

    Parameters:
    file_paths (list of str): List of file paths to the CSV files containing the emissions data.
    contour_limits (tuple): The min and max limits for the contour levels.

    The CSV files are expected to have the following columns:
    - 'Aircraft IATA code': The aircraft code (e.g., 'A319')
    - 'Total distance (nm) (FF)': The total distance travelled in nautical miles
    - 'Payload (Kg)': The payload in kilograms
    - 'Fuel_burnt (FF)': The fuel burnt

    The function performs the following steps:
    1. Loads and concatenates data from all provided CSV files.
    2. Extracts the relevant columns (total distance, payload, and fuel burnt) and drops any rows with missing values.
    3. Interpolates the fuel burnt values over a grid of total distance and payload values.
    4. Creates a filled contour plot with the specified colormap and contour limits.
    5. Adds labels and a color bar to the plot.
    6. Displays the plot.
    """
    # Load and concatenate data from all files
    all_data = pd.concat([pd.read_csv(file) for file in file_paths])

    # Extract relevant columns and drop rows with missing values
    all_data = all_data[['Total distance (nm) (FF)', 'Payload (Kg)', 'Fuel_burnt (FF)']].dropna()

    total_distance = all_data['Total distance (nm) (FF)'].values
    payload = all_data['Payload (Kg)'].values
    fuel_burnt = all_data['Fuel_burnt (FF)'].values

    # Create a grid of total_distance and payload values
    grid_x, grid_y = np.mgrid[total_distance.min():total_distance.max():100j, payload.min():payload.max():100j]

    # Interpolate the fuel burnt values on the grid
    grid_z = griddata((total_distance, payload), fuel_burnt, (grid_x, grid_y), method='linear')

    # Create a filled contour plot with fixed limits and colors
    fig, ax = plt.subplots()
    contourf = ax.contourf(grid_x, grid_y, grid_z, levels=np.linspace(contour_limits[0], contour_limits[1], 100), cmap='magma')
    cbar = plt.colorbar(contourf, ticks=np.linspace(contour_limits[0], contour_limits[1], 10))
    cbar.set_label('Fuel burnt (kg)', fontsize=20, fontname="Times New Roman")

    # Customize colorbar tick labels
    cbar.ax.tick_params(labelsize=18)  # Set font size of the colorbar tick labels
    for label in cbar.ax.get_yticklabels():
        label.set_family("Times New Roman")

    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(1.5)

    # Modify axes ticks properties
    plt.xticks(fontname="Times New Roman", fontsize=20)
    plt.yticks(fontname="Times New Roman", fontsize=20)

    ax.tick_params(bottom=True, top=True, left=True, right=True)
    ax.tick_params(labelbottom=True, labeltop=False, labelleft=True, labelright=False)
    ax.tick_params(which='major', length=10, width=1.2, direction='in')
    ax.tick_params(which='minor', length=5, width=1.2, direction='in')

    # Axis limits
    plt.xlim([total_distance.min(), total_distance.max()])
    plt.ylim([payload.min(), payload.max()])

    # High DPI for better image quality
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['savefig.dpi'] = 300

    # Add labels and a color bar
    plt.xlabel('Total Distance (nm)', fontsize=22, fontname="Times New Roman")
    plt.ylabel('Payload (Kg)', fontsize=22, fontname="Times New Roman")

    

    fig.set_size_inches(fig.get_size_inches()[0]*1.5, fig.get_size_inches()[1]*1.5, forward=True)
    plt.tight_layout()
    plt.savefig('A319/Plots/A319_111.png', dpi=300)  # Save the figure
    plt.show()


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

def plot_fuel_burnt_scatter(file_paths, payload_value):
    """
    Generates a scatter plot of fuel burnt as a function of total distance for a given payload value.
    
    Parameters:
    file_paths (list of str): List of file paths to the CSV files containing the emissions data.
    payload_value (float): The payload value for which the scatter plot is to be generated.
    
    The CSV files are expected to have the following columns:
    - 'Total distance (nm) (FF)': The total distance travelled in nautical miles
    - 'Payload (Kg)': The payload in kilograms
    - 'Fuel_burnt (FF)': The fuel burnt
    
    The function performs the following steps:
    1. Loads and concatenates data from all provided CSV files.
    2. Filters the data for the specified payload value.
    3. Plots the scatter plot of fuel burnt as a function of total distance.
    4. Adds a trend line to the plot.
    5. Adds labels and displays the plot.
    """
    # Load and concatenate data from all files
    all_data = pd.concat([pd.read_csv(file) for file in file_paths])

    # Extract relevant columns and drop rows with missing values
    all_data = all_data[['Total distance (nm) (FF)', 'Payload (Kg)', 'Fuel_burnt (FF)']].dropna()

    # Filter data for the specified payload value
    filtered_data = all_data[all_data['Payload (Kg)'] == payload_value]

    if filtered_data.empty:
        print(f"No data found for payload value: {payload_value} Kg")
        return

    total_distance = filtered_data['Total distance (nm) (FF)'].values
    fuel_burnt = filtered_data['Fuel_burnt (FF)'].values

    # Create a scatter plot
    fig, ax = plt.subplots()
    ax.plot(total_distance, fuel_burnt, color='C0', alpha=1, linewidth=0.0, ms=12, mec='black', mfc='C0', marker="P")

    # Add labels and title
    plt.xlabel('Total Distance (nm)', fontsize=22, fontname="Times New Roman")
    plt.ylabel('Fuel Burnt (Kg)', fontsize=22, fontname="Times New Roman")

    # High DPI for better image quality
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['savefig.dpi'] = 300

    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(1.5)

    # Modify axes ticks properties
    plt.xticks(fontname="Times New Roman", fontsize=20)
    plt.yticks(fontname="Times New Roman", fontsize=20)

    ax.tick_params(bottom=True, top=True, left=True, right=True)
    ax.tick_params(labelbottom=True, labeltop=False, labelleft=True, labelright=False)
    ax.tick_params(which='major', length=10, width=1.2, direction='in')
    ax.tick_params(which='minor', length=5, width=1.2, direction='in')

    # Plot grid properties
    ax.grid(which='major', color='black', linestyle='-', linewidth='0.05')
    ax.minorticks_on()
    ax.grid(which='minor', color='black', linestyle=':', linewidth='0.05')

    # Fit a linear regression model to the data
    slope, intercept, r_value, p_value, std_err = linregress(total_distance, fuel_burnt)
    trend_line = slope * total_distance + intercept
    ax.plot(total_distance, trend_line, color='C2', linestyle='--', linewidth=2.5, label=f'(R² = {r_value**2:.2f})')

    # Add legend
    plt.legend(loc='upper left', bbox_to_anchor=(0, 1), ncol=2, prop={'family': 'Times New Roman', 'size': 14})

    plt.xlim([100, 2200])
    plt.ylim([500, 14000])
    fig.set_size_inches(fig.get_size_inches()[0]*1.5, fig.get_size_inches()[1]*1.5, forward=True)

    plt.tight_layout()
    plt.savefig('A319/Plots/Fixed_Payload_Scatter/A319_115_PF_010.png', dpi=300)  # Save the figure
    plt.show()


Plot_contour = False
Plot_scatter = True

file_paths = [
    'A319/data/A319_111_Emissions_Summary_Combined.csv',
]


if Plot_contour:
    contour_limits = (750, 14400)  # Replace with appropriate min and max values for your data

    plot_fuel_burnt_contour(file_paths, contour_limits)

if Plot_scatter:
    # Example usage
    #payload_value = 11900 # 70 %
    #payload_value = 8500  # 50 %
    #payload_value = 5100  # 30 %
    payload_value = 1700  # 10 %
    plot_fuel_burnt_scatter(file_paths, payload_value)