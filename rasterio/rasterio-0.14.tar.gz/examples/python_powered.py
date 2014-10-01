# python_powered.py
#
# Turns the 15 features in the Python logo
#
#   http://www.python.org/community/logos/python-powered-h-140x182.png
#
# into a GeoJSON feature collection.

import json

import rasterio
from rasterio.features import shapes
from rasterio.transform import Affine as A


with rasterio.drivers():
    
    with rasterio.open('python-powered-h-140x182.png') as src:
        blue = src.read_band(3)
    
    # Set every non-background pixel to 0 and then mask out the
    # white background.
    blue[blue < 255] = 0
    mask = blue == 255

    # transform to world coordinates so that we can map it
    transform = A.translation(-35.0, 40.5) * A.scale(0.5, -0.5)

    results = ({
            'type': 'Feature', 
            'properties': {'raster_val': v}, 
            'geometry': s }
        for i, (s, v) 
        in enumerate(
            shapes(blue, mask=mask, transform=transform) ))
    
    collection = {
        'type': 'FeatureCollection', 
        'features': list(results) }

with open('python-powered.json', 'w') as dst:
    json.dump(collection, dst)

