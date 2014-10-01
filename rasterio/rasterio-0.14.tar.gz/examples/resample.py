import rasterio
import subprocess

# Read raster bands directly to Numpy arrays.
with rasterio.open('rasterio/tests/data/RGB.byte.tif') as src:
    r = src.read_band(1)
    g = src.read_band(2)
    b = src.read_band(3)
    assert [b.dtype.type for b in (r, g, b)] == src.dtypes

with rasterio.open(
        '/tmp/resample.tif', 'w',
        **dict(
            src.meta, 
            **{'dtype': rasterio.uint8, 'count': 3, 'width': src.width/4, 'height': src.height/4, 'photometric': 'RGB'})
        ) as dst:
    
    dst.write_band(1, r)
    dst.write_band(2, g)
    dst.write_band(3, b)

# Dump out gdalinfo's report card.
info = subprocess.check_output(['gdalinfo', '-stats', '/tmp/resample.tif'])
print(info)

