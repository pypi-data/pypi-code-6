"""
Utilities
=========
"""

__all__ = ['interpolate_gps_positions_for_cams']

from ecosynth.acquire.utilities import telemetry_to_gps_positions

import os
import re
import numpy as np


def interpolate_gps_positions_for_cams(log_file, msl_float, cam_filepath, pscan_cam_xyz_file=None, ecosynther_xyz_file=None):
    """
    This script interpolates the GPS position from a GPS list onto the camera
    list

    :param file log_file:
    :param float msl_float:
    :param string cam_filepath: Assumes .JPG extensions are capitalized
        for all photos
    :param file pscan_cam_xyz_file: (Optional) Photoscan output file with header and JPG names
    :param file ecosynther_xyz_file: (Optional) Ecosynther output file with just xyz dimensions

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
    | >>> generate.utilities.interpolate_gps_positions_for_cams(
    |   log_file, msl_float, cam_filepath, pscan_cam_xyz_file=cam_xyz_file)
    | >>> cam_xyz_file.close()

    | **Example pscan_cam_xyz_file Output**
    | # <label>   <x>    <y>   <z>
    | a.JPG     364754.663290    4305831.506730    136.543925
    | ...

    | **Example ecosynther_xyz_file Output (no header)**
    | 364754.663290    4305831.506730    136.543925
    | ...
    """
    gps_array = telemetry_to_gps_positions(log_file, msl_float)
    dirlist = os.listdir(cam_filepath)
    dirlist = sorted(dirlist, key=_sort_numerically)

    cam_array = np.array([i for i in dirlist if i[-3:] == 'JPG'], dtype=str)

    scaledGPSlist = np.array(_scaleList(
        gps_array, cam_array), dtype=np.float64)

    stackedList = [1]*(len(cam_array))

    for j, line in enumerate(stackedList):
        stackedList[j] = cam_array[j], scaledGPSlist[j][0], scaledGPSlist[j][1], scaledGPSlist[j][2]

    if pscan_cam_xyz_file:
        header = '# <label>     <x>    <y>    <z>'
        pscan_cam_xyz_file.write(header + '\n')
        for row in stackedList:
            pscan_cam_xyz_file.write('%s    %.6f    %.6f    %.6f\n' % (row))

    if ecosynther_xyz_file:
        for row in stackedList:
            ecosynther_xyz_file.write('%.6f    %.6f    %.6f\n' % (row[1:]))

    return


def _scaleList(GPS_array, CAM_array):
    GPSlength = float(GPS_array.shape[0])
    CAMlength = float(CAM_array.shape[0])
    CAMIdx = np.arange(CAMlength)
    lengthScale = GPSlength/CAMlength
    CAMIdxScale = np.array(CAMIdx * lengthScale, dtype=int)
    scaledGPSlist = GPS_array[CAMIdxScale]

    return scaledGPSlist


def _sort_numerically(string_list):
    r = re.compile('(\d+)')
    reg_list = r.split(string_list)
    return [int(name) if name.isdigit() else name for name in reg_list]
