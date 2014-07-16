s = SixS()
s.altitudes.set_sensor_satellite_level()

def set_param(s, aot):
    s.aot550 = aot

    return s

# Create a function to be called by the map
def f(aot):
    s.outputs = None
    a = copy.deepcopy(s)
    set_param(a, aot)
    a.run()
    if output_name is None:
        return a.outputs
    else:
        return getattr(a.outputs, output_name)

# Run the map
from multiprocessing.dummy import Pool

if n is None:
    pool = Pool()
else:
    pool = Pool(n)

print "Running for many wavelengths - this may take a long time"
results = pool.map(f, wavelengths)

try:
    if len(wavelengths[0]) == 4:
        cleaned_wavelengths = map(lambda x: x[:3], wavelengths)
        return np.array(cleaned_wavelengths), np.array(results)
    else:
        return np.array(wavelengths), np.array(results)
except:
    return np.array(wavelengths), np.array(results)