import logging
import sys

import rasterio

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

with rasterio.drivers():
    with rasterio.drivers():
        pass
    with rasterio.open('rasterio/tests/data/RGB.byte.tif') as f:
        pass
