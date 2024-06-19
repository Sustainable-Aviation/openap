import openap
from openap.traj import Generator
#from openap.aero import kts, fpm
import pandas as pd
import numpy as np
from openap import FuelFlow


actype = "A320"
mass0 = 66300
trajgen = Generator(actype)


data_cr = trajgen.cruise(dt=60, range_cr=1852, alt_cr=35000, m_cr=0.78)

#data_cr = trajgen.cruise(dt=1, random = True)

time = data_cr['t']
height = data_cr['h']
s = data_cr['s']
v = data_cr['v']
vs = data_cr['vs']
alt_cr = data_cr['alt_cr']
mach_cr = data_cr['mach_cr']

fuelflow = FuelFlow(ac='A320', eng='CFM56-5B4')

mass0 = 60000
mass = mass0


path_angles = np.degrees(np.arctan(to_fpm(vs) , v * 1.94384))


#time_series = pd.Series(time)

#time_deltas = time_series.diff().dt.total_seconds().fillna(0)
#time_deltas = np.ts.diff(periods=-1)
#time_deltas[-1] = time_deltas[-2]

#mass = mass0

for (dt, tas, alt, pa) in zip(time, v, height, path_angles):
    #print("dt:", dt, "tas", tas, "alt:", alt, "pa", pa)

    FF = fuelflow.enroute(mass=mass, tas=tas, alt=alt, path_angle=0)
    print("Current Fuel flow in Kg/s:", FF)
    mass -= FF * 60

fuelburn = mass0 - mass

print(fuelburn)