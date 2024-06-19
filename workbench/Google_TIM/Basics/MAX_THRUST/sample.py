from openap import prop, Thrust, Drag, WRAP
from openap.traj import Generator
import numpy as np
import matplotlib.pyplot as plt
import csv
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

ac1 = prop.aircraft('A359')

print(ac1)

