"""
Utilities
=========
"""

__all__ = ['interpolate_gps_positions_for_cams']

from ecosynth.acquire.utilities import telemetry_to_gps_positions

import os
import numpy as np


def interpolate_gps_positions_for_cams(log_file, msl_float, cam_filepath, cam_xyz_file):
    """
    This script interpolates the GPS position from a GPS list onto the camera
    list

    | (Change) Run this ?script? at a command line within the folder where all
    | the pictures are located. it requires one argument and that is the
    | trimmed GPS file in tab delimited format X Y Z with a header. that
    | can be used in Photoscan to estimate XYZ location for each camera
    | with format: '# <label>','<x>', '<y>','<z>'

    :param file log_file:
    :param float msl_float:
    :param string cam_filepath: Assumes .JPG extension is capitalized
        for all photos
    :param file cam_xyz_file:

    | **Notes**
    | This function assumes that the GPS_file.txt and list of pictures
    | are in the same order: i.e., that the first GPS point in the
    | GPS list corresponds to the first GPS flight of the main flight,
    | the last point is the last of the flight, and similarly that the
    | first photo (based on an alphabetical A-Z sort) is the first photo
    | in the main flight and the last is the last.

    | **Example**
    | >>> log_file = open(log_filepath, 'r')
    | >>> msl_float = 5.6
    | >>> cam_filepath = '/path/to/cams'
    | >>> cam_xyz_file = open(cam_xyz_filepath, 'w')
    | >>> generation.utilities.interpolate_gps_positions_for_cams(
    |   log_file, msl_float, cam_filepath, cam_xyz_file)

    | **Example Output**
    | # <label>   <x>    <y>   <z>
    | a.JPG     364754.663290    4305831.506730    136.543925
    | ...
    """
    gps_array = telemetry_to_gps_positions(log_file, msl_float)
    dirlist = os.listdir(cam_filepath)

    cam_array = np.array([i for i in dirlist if i[-3:] == 'JPG'], dtype=str)

    scaledGPSlist = np.array(_scaleList(
        gps_array, cam_array), dtype=np.float64)

    stackedList = [1]*(len(cam_array))

    for j, line in enumerate(stackedList):
        stackedList[j] = cam_array[j], scaledGPSlist[j][0], scaledGPSlist[j][1], scaledGPSlist[j][2]

    header = '# <label>     <x>    <y>    <z>'
    cam_xyz_file.write(header + '\n')
    for row in stackedList:
        cam_xyz_file.write('%s    %.6f    %.6f    %.6f\n' % (row))
    cam_xyz_file.close()

    return


def _scaleList(GPS_array, CAM_array):
    GPSlength = float(GPS_array.shape[0])
    CAMlength = float(CAM_array.shape[0])
    CAMIdx = np.arange(CAMlength)
    lengthScale = GPSlength/CAMlength
    CAMIdxScale = np.array(CAMIdx * lengthScale, dtype=int)
    scaledGPSlist = GPS_array[CAMIdxScale]

    return scaledGPSlist
