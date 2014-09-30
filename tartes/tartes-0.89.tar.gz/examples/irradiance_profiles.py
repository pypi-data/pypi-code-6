import tartes
from pylab import *

# semi-infinite medium
ssa = [40,15]
density = [300,350]
depth= [0.3, 1]

# depth at which the calculation is performed
z = arange(0,100,5)*1e-2 # from 0 to 1m depth every cm

wavelengths = [400e-9,600e-9,800e-9]

for wl in wavelengths:
    down_irr_profile,up_irr_profile = tartes.irradiance_profiles(wl,z,ssa,density,depth)
    semilogx(up_irr_profile,-z,label='upwelling %g nm' % (wl*1e9))
    semilogx(down_irr_profile,-z,label='downwelling %g nm' % (wl*1e9))

xlabel('depth (m)')
ylabel('irradiance (W/m^2)')
legend(loc='best')
show()
