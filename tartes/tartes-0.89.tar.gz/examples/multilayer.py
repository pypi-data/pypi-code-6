import tartes
from pylab import *


ssa = [20,15,10]
density = [200,250,300]
depth = [0.01,0.10,1000] # depth of each layer in meter
wavelengths = arange(300,2500,10)*1e-9 # from 300 to 2500 nm

albedo_3layers = tartes.albedo(wavelengths,ssa,density,depth)

ssa = 20  
density = 300
albedo_semiinfinite = tartes.albedo(wavelengths,ssa,density)



# alpha controls the transparency of the curves
plot(wavelengths*1e9,albedo_semiinfinite,alpha=0.7)
plot(wavelengths*1e9,albedo_3layers,alpha=0.7)
show()
