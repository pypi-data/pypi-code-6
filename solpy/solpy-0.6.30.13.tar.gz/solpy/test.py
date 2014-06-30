import design
import inverters
import modules
module = "Mage Solar : USA Powertec Plus 250-6 MNCS"
inverter = "SMA America: SB7000US-11 277V"
inverter = "SMA America: SB5000TL-US-22 (240V) 240V"

i = design.generateOptions(inverter,module,'17601')
print i
#fillArray(inverter, zipcode, acDcRatio = 1.2, mount="Roof", stationClass = 1, \
#        Vmax = 600, bipolar= True)
