import rasterio
import subprocess

with rasterio.open('tests/data/RGB.byte.tif') as src:
    r = src.read_band(1)
    g = src.read_band(2)
    b = src.read_band(3)

window = (30, 269), (50, 313)

with rasterio.open(
        '/tmp/example.tif', 'w',
        driver='GTiff', width=500, height=300, count=3,
        dtype=r.dtype) as dst:
    dst.write_band(1, r, window=window) 
    dst.write_band(2, g, window=window)
    dst.write_band(3, b, window=window)

subprocess.call(['open', '/tmp/example.tif'])

read_window = (350, 410), (350, 450)

with rasterio.open('tests/data/RGB.byte.tif') as src:
    r = src.read_band(1, window=read_window)
    g = src.read_band(2, window=read_window)
    b = src.read_band(3, window=read_window)

write_window = (-240, None), (-400, None)

with rasterio.open(
        '/tmp/example2.tif', 'w',
        driver='GTiff', width=500, height=300, count=3,
        dtype=r.dtype) as dst:
    dst.write_band(1, r, window=write_window) 
    dst.write_band(2, g, window=write_window)
    dst.write_band(3, b, window=write_window)

subprocess.call(['open', '/tmp/example2.tif'])


