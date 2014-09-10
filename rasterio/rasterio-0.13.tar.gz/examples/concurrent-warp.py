"""concurrent-warp.py

Warp a raster dataset window-by-window using a ThreadPoolExecutor.

Simulates a CPU-bound thread situation where multiple threads can improve
performance.

With -j 4, the program returns in about 1/4 the time as with -j 1.
"""

import concurrent.futures
import multiprocessing
import time

import numpy

import rasterio
from rasterio.warp import reproject, RESAMPLING


def main(infile, outfile, dst_crs, dst_bounds, dst_shape, num_workers=4):
    """Use process_window() to process a file in parallel."""

    with rasterio.drivers():

        # Open the source dataset.
        with rasterio.open(infile) as src:

            source_bands = src.read()

            # Create a destination dataset based on source params.
            # The destination will be tiled, and we'll "process" the tiles
            # concurrently.
            meta = src.meta
            meta.update(blockxsize=256, blockysize=256, tiled='yes')
            
            meta.update(crs=dst_crs, height=dst_shape[0], width=dst_shape[1])
            
            left, bottom, right, top = dst_bounds
            dx = (right - left)/dst_shape[1]
            dy = (bottom - top)/dst_shape[0]
            meta.update(transform=rasterio.Affine(dx, 0, left, 0, dy, top))
            
            with rasterio.open(outfile, 'w', **meta) as dst:

                def warp_window(window):
                    
                    a, b, c, d, e, f, _, _, _ = dst.transform
                    c += window[1][0]*a
                    f += window[0][0]*e
                    dst_transform = rasterio.Affine(a, b, c, d, e, f)

                    results = []
                    for i, source in enumerate(source_bands):
                        destination = numpy.zeros(
                                        rasterio.window_shape(window),
                                        rasterio.uint8)
                        reproject(
                            source,
                            destination,
                            src_transform=src.transform,
                            src_crs=src.crs,
                            dst_transform=dst_transform,
                            dst_crs=dst.crs,
                            resampling=RESAMPLING.cubic)
                        results.append(destination)
                    return results

                # Submit the jobs to the thread pool executor.
                with concurrent.futures.ThreadPoolExecutor(
                        max_workers=num_workers) as executor:
                    
                    # Map the futures returned from executor.submit()
                    # to their destination windows.
                    future_to_window = {
                        executor.submit(warp_window, window): window
                        for ij, window in dst.block_windows(1)}
                    
                    # As the processing jobs are completed, get the
                    # results and write the data to the appropriate
                    # destination window.
                    for future in concurrent.futures.as_completed(
                            future_to_window):
                        
                        window = future_to_window[future]

                        data = future.result()

                        # Since there's no multiband write() method yet in
                        # Rasterio, we use write_band for each part of the
                        # 3D data array.
                        for i, arr in enumerate(data, 1):
                            dst.write_band(i, arr, window=window)


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
        '--destination-crs',
        required=True,
        metavar='CRS',
        help="Destination coordinate reference system")
    parser.add_argument(
        '--destination-bounds',
        required=True,
        metavar='BOUNDS',
        help="Destination bounds: left,bottom,right,top")
    parser.add_argument(
        '--destination-shape',
        required=True,
        metavar='SHAPE',
        help="Destination shape: height,width")
    parser.add_argument(
        '-j', 
        metavar='NUM_JOBS',
        type=int,
        default=multiprocessing.cpu_count(),
        help="Number of concurrent jobs")
    args = parser.parse_args()

    crs_arg = args.destination_crs.lower()
    if crs_arg.startswith('epsg:'):
        crs = {'init': crs_arg}
    else:
        crs = crs_arg
    bounds = tuple(map(float, args.destination_bounds.split(',')))
    shape = tuple(map(int, args.destination_shape.split(',')))
    
    main(args.input, args.output, crs, bounds, shape, args.j)

