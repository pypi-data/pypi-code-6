import tartes

ssa = 20      # in kg/m2
density = 300 # the result should be independent of the density for a semi-infinite medium

wavelength = 850e-9

albedo = tartes.albedo(wavelength,ssa,density,dir_frac=1,theta_inc=30)

print(albedo)

