import numpy
import rasterio

with rasterio.open('tests/data/RGB.byte.tif') as src:
    
    # The following asserts that all bands have the same block/stripe structure.
    assert len(set(src.block_shapes)) == 1
    
    # As they do, we can iterate over the first band's block windows.
    for ji, window in src.block_windows(1):

        # Get data in this window for each band as a Numpy masked array.
        bands = [
            numpy.ma.masked_equal(
                src.read_band(src.indexes[i]),
                src.nodatavals[i])
            for i in range(src.count)]

        # Break out after the first block.
        break

# Let's look at the first, blue band.
b = bands[0]
print(b)
print(b.mask)
print(b.fill_value)
print(b.min(), b.max(), b.mean())
