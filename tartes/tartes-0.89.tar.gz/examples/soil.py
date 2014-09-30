import tartes
from pylab import *

ssa = 20
density = 250

wavelength = 550

depth = arange(5,30,5)*1e-2
wavelengths = arange(300,1100,10)*1e-9 # from 300 to 1100nm

for d in depth:
    albedo = tartes.albedo(wavelengths,ssa,density,d,soilalbedo=0.2)
    plot(wavelengths*1e9,albedo,label='%gcm' % (d*100))

legend(loc='best')
show()
