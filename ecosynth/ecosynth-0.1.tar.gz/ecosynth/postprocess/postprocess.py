"""
Postprocess
===========
"""
import StringIO
import time

import numpy as np

from . import io
from . import transforms
from . import CloudRasterizer
from ecosynth.acquire.utilities import telemetry_to_gps_positions

__all__ = ['run']

def run(out_file, log_file, msl_float, cams_geo_file=None, ply_file=None, points_txt_file=None, gps_file=None, logger_file=None, dense_ply_file_in=None, dense_ply_file_out=None, helm_params_file=None):
    """
    Entry point for Post-Processing stage of automated pipeline

    :param file out_file: Bundler OUT file
    :param file log_file: LOG file from Acquisition stage
    :param float msl_float: lauch altitude (meters above mean sea level)
    :param cams_geo_file: (Optional) Clean file to write georeferenced cameras
    :param file ply_file: (Optional) Clean file to write georeferenced and
        noise-filtered PLY
    :param file points_txt_file: (Optional) Clean file to write georeferenced
        and noise-filtered points
    :param file gps_file: (Optional) Clean file to write GPS positions
    :param file logger_file: (Optional) File currently for debugging and point
        cloud statistics
    :param file dense_ply_file_in: (Optional) Dense PLY File to Transform
    :param file dense_ply_file_out: (Optional) Transformed Dense PLY File
    :param file helm_params_file: (Optional) Clean file to write Helmert parameters

    :return: cr_object
    :rtype: CloudRasterizer

    | **Notes**
    | here

    | **Example**
    | here

    """
    start = time.time()
    #  Setup
    if gps_file:
        gps_file_buf = gps_file
    else:
        gps_file_buf = StringIO.StringIO()

    gps_array = telemetry_to_gps_positions(
        log_file, msl_float, gps_file=gps_file_buf)

    if gps_file:
        np.savetxt(gps_file, gps_array)

    #  Input Data Conversion
    out_tuple = io.load_out(out_file)  # Load OUT File
    """
    # Success Metric Level 0 (>99 percent images used)
    """
    if logger_file:
        cams_total = out_tuple.cam_array[:, 0].size
        cams_used = out_tuple.cam_array_fixed[:, 0].size
        percent_cams = float(cams_used) / cams_total * 100
        if(percent_cams > 99):
            logger_file.write("\nEcosynther Quality Test Level 0: Success\n")
        else:
            logger_file.write("\nEcosynther Quality Test Level 0: Failure\n")
        logger_file.write("   Total Cameras: %i\n" % cams_total)
        logger_file.write("   Used Cameras: %i\n" % cams_used)
        logger_file.write("   %% Cameras Used : %f\n" % percent_cams)

    #  Georeference Primary Points
    xyzrgb_array_georef, params = transforms.georef_telemetry(
        out_tuple, gps_array, msl_float, logger=logger_file)

    if helm_params_file:
        for p in params:
            helm_params_file.write(str(p) + "\n")

    if cams_geo_file:
        # Transform camera coordinates
        cams_array_geo = transforms.apply_helmert(
            params, out_tuple.cam_array_fixed[:, 0:3])
        # Recombine coordinates with camera FKKe
        ffk_array = out_tuple.cam_array_fixed[:, 3]
        ffk_array = ffk_array.reshape(-1, 1)
        #cams_array_geo = np.hstack((
        #    cams_array_geo, ffk_array))

        np.savetxt(
            cams_geo_file, cams_array_geo, fmt=['%.3f', '%.3f', '%.3f'])  #, '%.3f'])

    # Georeference and Save Dense Points
    if (dense_ply_file_in and dense_ply_file_out):
        ply_tuple = io.load_ply(dense_ply_file_in)
        # Transform coordinates
        xyz_georef_array = transforms.apply_helmert(
            params, ply_tuple.xyzrgb_array[:, 0:3])
        # Recombine coordinates and colors
        dense_georef_array = np.hstack(
            xyz_georef_array, ply_tuple.xyzrgb_array[:, 3:])
        # Save file
        io.save_ply(dense_ply_file_out, dense_georef_array)

    #  Filter Noise from Primary
    cr_object = CloudRasterizer.CloudRasterizer(
        xyzrgb_array_georef, resolution=1)
    cr_object.filter_noise_z()

    """
    # Success Metric Level 1 (Part B)
        - mean pc density > 40 points per square-meter
        - std point cloud density <40 points per square-meter
    """
    # NOTE: ASSUMES 1 METER RESOLUTION
    if logger_file:
        pd_raster = cr_object.get_point_density_raster()
        mean_pd = pd_raster.mean()
        std_pd = pd_raster.std()
        if((mean_pd > 40) and (std_pd < 40)):
            logger_file.write("\nEcosynther Quality Test Level 1 (Part B): Success\n")
        else:
            logger_file.write("\nEcosynther Quality Test Level 1 (Part B): Failure\n")
        logger_file.write("   Mean Point Density: %f\n" % mean_pd)
        logger_file.write("   STD Point Density : %f\n" % std_pd)

    #  Save Primary Point Cloud to File
    if ply_file or points_txt_file:
        xyzrgb_array_geo_noise = cr_object.get_cloud_array()
        if ply_file:
            io.save_ply(ply_file, xyzrgb_array_geo_noise)
        if points_txt_file:
            print "xyzrgb_array_georef shape:", xyzrgb_array_geo_noise.shape
            np.savetxt(
                points_txt_file, xyzrgb_array_geo_noise.reshape(-1,6), fmt=['%.3f', '%.3f', '%.3f', '%i', '%i', '%i'])

    #  EcoBrowser

        print "   postprocess.run time:", time.time()-start
    return cr_object
