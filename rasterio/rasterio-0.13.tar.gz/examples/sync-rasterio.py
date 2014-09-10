"""async-rasterio.py

Operate on a raster dataset window-by-window using asyncio's event loop
and thread executor.

Simulates a CPU-bound thread situation where multiple threads can improve
performance.
"""

import asyncio
import time

import rasterio


def main(infile, outfile):
    
    with rasterio.drivers():

        # Open the source dataset.
        with rasterio.open(infile) as src:

            # Create a destination dataset based on source params. The
            # destination will be tiled, and we'll "process" the tiles
            # concurrently.

            meta = src.meta
            del meta['transform']
            meta.update(affine=src.affine)
            meta.update(blockxsize=256, blockysize=256, tiled='yes')
            with rasterio.open(outfile, 'w', **meta) as dst:

                def compute(data):
                    # Fake a CPU-intensive computation.
                    dtype = data.dtype
                    tmp_data = data.astype(rasterio.float32)
                    for j in range(100):
                        tmp_data *= 2.0
                    tmp_data /= 180.0
                    tmp_data = data.astype(dtype.type)
                    # Reverse the bands just for fun.
                    return tmp_data[::-1]

                def process_window(window):
                    
                    # Read a window of data.
                    data = src.read(window=window)
                    
                    result = compute(data)
                    
                    # Write the result.
                    for i, arr in enumerate(result, 1):
                        dst.write_band(i, arr, window=window)

                for ij, window in dst.block_windows(1):
                    process_window(window)
                

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(
        description="Concurrent raster processing demo")
    parser.add_argument(
        'input',
        metavar='INPUT',
        help="Input file name")
    parser.add_argument(
        'output',
        metavar='OUTPUT',
        help="Output file name")
    args = parser.parse_args()
    
    main(args.input, args.output)


