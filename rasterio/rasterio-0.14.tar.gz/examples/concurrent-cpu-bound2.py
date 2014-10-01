"""concurrent-cpu-bound.py

Operate on a raster dataset window-by-window using a ThreadPoolExecutor.

Simulates a CPU-bound thread situation where multiple threads can improve performance.

With -j 4, the program returns in about 1/4 the time as with -j 1.
"""

import concurrent.futures
import multiprocessing
import time

import rasterio



def main(infile, outfile, num_workers=4):
    """Use process_window() to process a file in parallel."""

    with rasterio.drivers():

        # Open the source dataset.
        with rasterio.open(infile) as src:

            # Create a destination dataset based on source params.
            # The destination will be tiled, and we'll "process" the tiles
            # concurrently.
            meta = src.meta
            del meta['transform']
            meta.update(affine=src.affine)
            meta.update(blockxsize=256, blockysize=256, tiled='yes')
            with rasterio.open(outfile, 'w', **meta) as dst:

                def process_window(args):
                    ij, window = args
                    # Fake an expensive computation.
                    time.sleep(0.1)
                    # Reverse the bands just for fun.
                    data = src.read(window=window)
                    data[:] = data[::-1]
                    for i, arr in enumerate(data, 1):
                        dst.write_band(i, arr, window=window)

                # Submit the jobs to the thread pool executor.
                with concurrent.futures.ThreadPoolExecutor(
                        max_workers=num_workers) as executor:
                    
                    executor.map(process_window, dst.block_windows(1))


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
    parser.add_argument(
        '-j',
        metavar='NUM_JOBS',
        type=int,
        default=multiprocessing.cpu_count(),
        help="Number of concurrent jobs")
    args = parser.parse_args()

    main(args.input, args.output, args.j)

