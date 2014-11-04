
import os
import shutil
import subprocess
import tempfile

import numpy
import rasterio

tempdir = tempfile.mkdtemp()
tiffname = os.path.join(tempdir, 'example.tif')

with rasterio.drivers(GDAL_TIFF_INTERNAL_MASK=True):

    with rasterio.open(
            tiffname,
            'w', 
            driver='GTiff', 
            count=1, 
            dtype=rasterio.uint8, 
            width=10, 
            height=10) as dst:
        
        dst.write_band(1, numpy.ones(dst.shape, dtype=rasterio.uint8))

        mask = numpy.zeros(dst.shape, rasterio.uint8)
        mask[5:,5:] = 255
        dst.write_mask(mask)

print os.listdir(tempdir)
print subprocess.check_output(['gdalinfo', tiffname])

shutil.rmtree(tempdir)

