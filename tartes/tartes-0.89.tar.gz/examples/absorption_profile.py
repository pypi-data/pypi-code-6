import tartes
from pylab import *

print(tartes)

nlayer = 200
ssa = [20]*nlayer # nlayer layers with the same SSA...
density = [300]*nlayer # and the same density
depth = [0.01]*nlayer # all the layer are 1cm deep, the snowpack is layer*1cm deep

wavelengths = [400e-9,500e-9,600e-9,700e-9,800e-9,900e-9]



for wl in wavelengths:
    z,absorption_profile = tartes.absorption_profile(wl,ssa,density,depth,soilalbedo=0.50)
    semilogx(absorption_profile,-z,label='%g nm' % (wl*1e9))

    albedo = tartes.albedo(wl,ssa,density,depth,soilalbedo=0.50)
    print(1 - sum(absorption_profile)," ",albedo)

ylabel('depth(m)')
xlabel('absorbed energy (for 1W/m2 incident)')
legend(loc='best')
show()
