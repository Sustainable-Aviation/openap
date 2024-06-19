import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata
import matplotlib.font_manager as fm

def compute_relative_difference(file1, file2):
    """
    Computes the relative difference in fuel burn between two CSV files.

    Parameters:
    file1 (str): The path to the first CSV file.
    file2 (str): The path to the second CSV file.

    Returns:
    pd.DataFrame: DataFrame containing the relative difference in fuel burn.
    """
    try:
        # Read the CSV files
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)
    except Exception as e:
        print(f"Error reading CSV files: {e}")
        return None

    try:
        df1 = df1[df1['Aircraft IATA code'] == 'A319']
        df2 = df2[df2['Aircraft IATA code'] == 'A319']
        # Ensure the data is aligned
        df1 = df1.sort_values(by=['Total distance (nm) (FF)', 'Payload (Kg)'])
        df2 = df2.sort_values(by=['Total distance (nm) (FF)', 'Payload (Kg)'])

        # Merge the dataframes on 'Total distance (nm) (FF)' and 'Payload (Kg)'
        merged_df = pd.merge(df1, df2, on=['Total distance (nm) (FF)', 'Payload (Kg)'], suffixes=('_file1', '_file2'))

        # Compute the relative difference in fuel burn
        merged_df['Relative difference in fuel burn (%)'] = (
            (merged_df['Fuel_burnt (FF)_file2'] - merged_df['Fuel_burnt (FF)_file1']) / merged_df['Fuel_burnt (FF)_file1'] * 100
        )
        
        return merged_df[['Total distance (nm) (FF)', 'Payload (Kg)', 'Relative difference in fuel burn (%)']]

    except Exception as e:
        print(f"Error processing data: {e}")
        return None

def plot_relative_difference_contour(df, contour_limits):
    """
    Plots the relative difference in fuel burn as a filled contour plot.

    Parameters:
    df (pd.DataFrame): DataFrame containing the relative difference in fuel burn.
    """

    
    total_distance = df['Total distance (nm) (FF)'].values
    payload = df['Payload (Kg)'].values
    relative_difference = df['Relative difference in fuel burn (%)'].values

    # Create a grid of total_distance and payload values
    grid_x, grid_y = np.mgrid[total_distance.min():total_distance.max():100j, payload.min():payload.max():100j]

    # Interpolate the relative difference values on the grid
    grid_z = griddata((total_distance, payload), relative_difference, (grid_x, grid_y), method='linear')

    # Fill NaN values in the grid with the mean of the non-NaN values
    grid_z_filled = np.nan_to_num(grid_z, nan=np.nanmean(grid_z))

    # Create a filled contour plot
    fig, ax = plt.subplots()
    contourf = ax.contourf(grid_x, grid_y, grid_z_filled, levels=np.linspace(contour_limits[0], contour_limits[1], 100), cmap='viridis')
    cbar = plt.colorbar(contourf, ticks=np.linspace(contour_limits[0], contour_limits[1], 10))
    #contourf = ax.contourf(grid_x, grid_y, grid_z_filled, cmap='seismic')
    #cbar = plt.colorbar(contourf)
    cbar.set_label('Relative difference in fuel burnt (%)', fontsize=20, fontname="Times New Roman")
    

    # Add contour lines
    #contour_lines = ax.contour(grid_x, grid_y, grid_z_filled, levels=np.linspace(contour_limits[0], contour_limits[1], 10), colors='black', linewidths=0.1)
    contour_lines = ax.contour(grid_x, grid_y, grid_z_filled, levels=np.linspace(contour_limits[0], contour_limits[1], 30), colors='black', linewidths=0.1)
    # Add contour labels with customized font properties
    clabels = ax.clabel(contour_lines, fmt='%2.1f', colors='black', fontsize=12, inline=True)

    # Customize font properties for contour labels
    for label in clabels:
        label.set_fontname('Times New Roman')
        label.set_size(12)
        label.set_weight('bold')


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

    # Save the figure (uncomment the following line if you want to save the figure)
    plt.savefig('A319/Plots/RelDiff/Rel_Dif_FB_CTR_A319_133.png', dpi=300)

    plt.show()

# Define file paths
file1 = 'A319/data/A319_115_Emissions_Summary_Combined.csv'   # Reference airframe
file2 = 'A319/data/A319_133_Emissions_Summary_Combined.csv'

contour_limits = (-2, 14)

# Compute relative difference
relative_difference_df = compute_relative_difference(file1, file2)

# Plot relative difference contour if the computation was successful
if relative_difference_df is not None:
    plot_relative_difference_contour(relative_difference_df, contour_limits)




