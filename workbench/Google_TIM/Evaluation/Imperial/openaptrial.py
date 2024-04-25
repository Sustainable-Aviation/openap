import numpy as np
import matplotlib.pyplot as plt
from openap import prop, FuelFlow

#actype = "a20n"

ac1 = prop.aircraft("a20n")

ff = FuelFlow("a20n")

# Get the MTOW for this airframe
MTOW = ac1['limits']['MTOW']  # Kgs

ac1 = prop.aircraft("a20n")

# Get the MLW for this airframe
MLW = ac1['limits']['MLW']  # Kgs

# Get the OEW for this airframe
OEW = ac1['limits']['OEW']  # Kgs

# Get the MFC for this airframe
MFC = ac1['limits']['MFC']  # Kgs

print("Aircraft MTOW: ", MTOW)
print("Aircraft MLW: ", MLW)
print("Aircraft OEW: ", OEW)
print("Aircraft MFC: ", MFC)

