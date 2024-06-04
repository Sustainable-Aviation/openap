import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import utils as utl
import numpy as np
import postProcess as pProc
from datetime import datetime

plt.style.use('seaborn-deep')

file_path = 'Output/Emissions_Summary_PF_0.5.csv'

df = pd.read_csv(file_path)

Fb_tot = df['Fuel_burnt (FF)'].sum()

CO2_tot = df['Forecast CO2 (Kg)'].sum()

H2O_tot = df['Forecast H2O (kg)'].sum()

NOX_tot = df['Forecast NOX (Kg)'].sum()


print('FB total:', Fb_tot/1000)
print('CO2 total:', CO2_tot/1000)
print('H2O total:', H2O_tot/1000)
print('NOX total:', NOX_tot/1000)


#pProc.plot_map_fuelburn_waypoint(df)

#pProc.plot_map_H2O_waypoint(df)

#pProc.plot_map_CO2_waypoint(df)

#pProc.plot_map_NOX_waypoint(df)