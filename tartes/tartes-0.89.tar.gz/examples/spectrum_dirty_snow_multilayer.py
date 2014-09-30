import tartes
import tartes.impurities
from pylab import *


ssa = [40,30,20]      #
density = [300,300,300]
depth = [0.02,0.05,1000] 

wavelengths = arange(300,1000,10)*1e-9 # from 300 to 2500nm

# pure snow
albedo_pure = tartes.albedo(wavelengths,ssa,density,depth)

# with a profile of soot
albedo_soot = tartes.albedo(wavelengths,
                            ssa,density,depth,
                            impurities=[10e-9, 50e-9, 0])

# A profile of mixture soot+Hulis
impurities_content= [
    [10e-9,50e-9], # soot and HULIS in the first layer
    [30e-9, 100e-9],  # soot and HULIS in the second layer
    [0, 10e-9]  # soot and HULIS in the last layer
]

albedo_mixture = tartes.albedo(wavelengths,ssa,density,depth,
                               impurities=impurities_content,
                               impurities_type=[tartes.impurities.Soot,
                                                tartes.impurities.HULIS])


plot(wavelengths*1e9,albedo_pure,label='pure snow')
plot(wavelengths*1e9,albedo_soot,label='snow with a profile of soot')
plot(wavelengths*1e9,albedo_mixture,label='snow with soot and HULIS')
legend(loc='best')
show()
