from openap import prop, Thrust, Drag, WRAP, FlightPhase
from openap.traj import Generator

# Import Airbus A320 with CFM-56

ac1 = prop.aircraft('A320')
eng1 = prop.engine('CFM56-5B4')

ac1_name = ac1['aircraft']
ac1_family = ac1_name.replace("Airbus ", "")  # Including the space after "Airbus" to remove it as well

print("Aircraft Family details")
print(ac1)
print(eng1)

# THRUST CALCULATION------->
thrust = Thrust(ac=ac1_family, eng=eng1['name'])

# Takeoff thrust
T_TO = thrust.takeoff(tas=100, alt=0)

# Climb thrust
T_CMB = thrust.climb(tas=200, alt=20000, roc=1000)

# Cruist thrust
T_CR = thrust.cruise(tas=230, alt=32000)

print("Takeoff thrust: ",T_TO)
print("Climb thrust: ",T_CMB)
print("Cruise thrust: ",T_CR)

# THRUST CALCULATION-------END

# DRAG CALCULATION------->

drag = Drag(ac=ac1_family)

D_clean = drag.clean(mass=60000, tas=200, alt=20000, path_angle=5)

D_landing = drag.nonclean(mass=60000, tas=150, alt=100, flap_angle=20,
                  path_angle=10, landing_gear=True)

print("Clean Drag:", D_clean)
print("Landing Drag:", D_landing)

# DRAG CALCULATION-------END

# KINEMATIC MODEL param_1ETER---->

wrap = WRAP(ac=ac1_family)

#param_1 = wrap.takeoff_speed()
#param_1 = wrap.takeoff_distance()
#param_1 = wrap.takeoff_acceleration()
#param_1 = wrap.initclimb_vcas()
#param_1 = wrap.initclimb_vs()
#param_1 = wrap.climb_range()
#param_1 = wrap.climb_const_vcas()
param_1 = wrap.climb_const_mach()
#param_1 = wrap.climb_cross_alt_concas()
#param_1 = wrap.climb_cross_alt_conmach()
#param_1 = wrap.climb_vs_pre_concas()
#param_1 = wrap.climb_vs_concas()
#param_1 = wrap.climb_vs_conmach()
#param_1 = wrap.cruise_range()
#param_1 = wrap.cruise_alt()
#param_1 = wrap.cruise_init_alt()
#param_1 = wrap.cruise_mach()
#param_1 = wrap.descent_range()
#param_1 = wrap.descent_const_mach()
#param_1 = wrap.descent_const_vcas()
#param_1 = wrap.descent_cross_alt_conmach()
#param_1 = wrap.descent_cross_alt_concas()
#param_1 = wrap.descent_vs_conmach()
#param_1 = wrap.descent_vs_concas()
#param_1 = wrap.descent_vs_post_concas()
#param_1 = wrap.finalapp_vcas()
#param_1 = wrap.finalapp_vs()
#param_1 = wrap.landing_speed()
#param_1 = wrap.landing_distance()
#param_1 = wrap.landing_acceleration()

print(param_1)

# KINEMATIC MODEL param_1ETER----END







