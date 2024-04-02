from openap import prop, Thrust, Drag, WRAP, FlightPhase
from openap.traj import Generator
import matplotlib.pyplot as plt

# Import Airbus A320 with CFM-56

ac1 = prop.aircraft('A320')
eng1 = prop.engine('CFM56-5B4')

ac1_name = ac1['aircraft']
ac1_family = ac1_name.replace("Airbus ", "")  # Including the space after "Airbus" to remove it as well

trajgen = Generator(ac=ac1_family)

# Enable Gaussian noise in trajectory data
trajgen.enable_noise()   

# CLIMB TRAJECTORY
data_cl = trajgen.climb(dt=10, cas_const_cl=280, mach_const_cl=0.78, alt_cr=35000)

# FULL TRAJECTORY
data_all = trajgen.complete(dt=1, alt_cr=35000, m_cr=0.78,
                            cas_const_cl=260, cas_const_de=260)

# Print all the keys

keys = data_all.keys()
print(keys)

time = data_all['t']
alt  = data_all['h']

# Create the plot
#plt.figure(dpi=300)
plt.plot(data_all['t'], data_all['vs'], label='Altitude vs. Time')
plt.xlabel('Time')
plt.ylabel('Altitude')
plt.title('Altitude over Time')
plt.legend()

# Show the plot
plt.show()


