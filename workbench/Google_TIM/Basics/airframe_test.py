from openap.traj import Generator

trajgen = Generator(ac='b763')

trajgen.enable_noise()   # enable Gaussian noise in trajectory data

data_cl = trajgen.climb(dt=10, random=True)  # using random paramerters
data_cl = trajgen.climb(dt=10, cas_const_cl=280, mach_const_cl=0.78, alt_cr=35000)

data_de = trajgen.descent(dt=10, random=True)
data_de = trajgen.descent(dt=10, cas_const_de=280, mach_const_de=0.78, alt_cr=35000)

data_cr = trajgen.cruise(dt=60, random=True)
data_cr = trajgen.cruise(dt=60, range_cr=2000, alt_cr=35000, m_cr=0.78)

data_all = trajgen.complete(dt=10, random=True)
data_all = trajgen.complete(dt=10, alt_cr=35000, m_cr=0.78,
                            cas_const_cl=260, cas_const_de=260)