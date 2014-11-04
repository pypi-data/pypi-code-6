from itertools import izip

import rasterio

def sync_block_windows(src, *bidx):
    for batch in izip(*list(src.block_windows(b) for b in bidx)):
        unique = set(batch)
        if len(unique) == 1: # all are in sync
            yield unique.pop()
        else:
            raise ValueError("band blocks do not match and can not be sync'd")

with rasterio.open('tests/data/RGB.byte.tif') as src:
    for ji, rw in sync_block_windows(src, 1, 2, 3):
        r = src.read_band(1, window=rw)
        g = src.read_band(2, window=rw)
        b = src.read_band(3, window=bw)
        print(r.shape, g.shape, b.shape)
        break

