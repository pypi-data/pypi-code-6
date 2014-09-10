import logging
import numpy
import os
import subprocess
import sys

import rasterio

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def test_read_mask():
    with rasterio.open('tests/data/RGB.byte.tif') as src:
        mask = src.read_mask()
        assert not mask.all()
        assert mask.any()

def test_write_mask_ints(tmpdir):
    tiffname = str(tmpdir.join('foo.tif'))
    with rasterio.open(
            tiffname, 
            'w', 
            driver='GTiff', 
            count=1, 
            dtype=rasterio.uint8, 
            width=10, 
            height=10) as dst:

        dst.write_band(1, 255*numpy.ones((10, 10), dtype=numpy.uint8))
        dst.write_mask(numpy.zeros((10, 10), dtype=numpy.uint8))

    with rasterio.open(tiffname) as src:
        mask = src.read_mask()
        assert not mask.any()
        assert 'foo.tif.msk' in os.listdir(str(tmpdir))

def test_write_mask_bools(tmpdir):
    tiffname = str(tmpdir.join('foo.tif'))
    with rasterio.open(
            tiffname, 
            'w', 
            driver='GTiff', 
            count=1, 
            dtype=rasterio.uint8, 
            width=10, 
            height=10) as dst:
        
        dst.write_band(1, 255*numpy.ones((10, 10), dtype=numpy.uint8))

        arr = numpy.ones((10, 10))
        mask = arr != 1.0
        dst.write_mask(mask)

    with rasterio.open(tiffname) as src:
        mask = src.read_mask()
        assert not mask.any()
        assert 'foo.tif.msk' in os.listdir(str(tmpdir))

