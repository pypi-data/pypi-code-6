import subprocess

import rasterio


with rasterio.drivers():

    with rasterio.open('tests/data/shade.tif') as src:
        shade = src.read_band(1)
        meta = src.meta

    with rasterio.open('/tmp/colormap.tif', 'w', **meta) as dst:
        dst.write_band(1, shade)
        dst.write_colormap(
            1, {
                0: (255, 0, 0, 255), 
                255: (0, 0, 255, 255) })
        cmap = dst.read_colormap(1)
        # True
        assert cmap[0] == (255, 0, 0, 255)
        # True
        assert cmap[255] == (0, 0, 255, 255)

subprocess.call(['open', '/tmp/colormap.tif'])

