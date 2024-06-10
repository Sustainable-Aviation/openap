import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import postProcess as pProc

Airframe = 'B738'

# Load the data from different files
file_paths = [
    'Output/Ver_2/No_Wind/Emissions_Summary_PF_0.1.csv',
    'Output/Ver_2/No_Wind/Emissions_Summary_PF_0.3.csv',
    'Output/Ver_2/No_Wind/Emissions_Summary_PF_0.5.csv',  # Assuming these should be different; corrected in case it's a typo
    'Output/Ver_2/No_Wind/Emissions_Summary_PF_0.7.csv',  # Changed assuming different file paths
    #'Output/Ver_2/No_Wind/Emissions_Summary_PF_0.9.csv'   # Changed assuming different file paths
]

dataframes = [pd.read_csv(fp) for fp in file_paths]

# Filter for A319 aircraft only and where Fuel Burnt is greater than zero
filtered_data = [
    df[(df['Aircraft IATA code'] == Airframe) & (df['Fuel_burnt (FF)'] > 0)]
    for df in dataframes
]


pProc.plot_FB_Payload_Distance(filtered_data)