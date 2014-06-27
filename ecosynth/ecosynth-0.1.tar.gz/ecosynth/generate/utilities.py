"""
Utilities
=========
"""

__all__ = ['interpolate_gps_positions_for_cams']


def interpolate_gps_positions_for_cams(gps_file):
    """
    This script interpolates the GPS position from a GPS list onto the camera
    list

    | (Change) Run this ?script? at a command line within the folder where all
    | the pictures are located. it requires one argument and that is the
    | trimmed GPS file in tab delimited format X Y Z with a header. that
    | can be used in Photoscan to estimate XYZ location for each camera
    | with format: '# <label>','<x>', '<y>','<z>'

    :param file GPS Positions File: UTM, meters, read permissions

    :return: file named 'rough_camera_XYZ_from_GPS.txt'
    :rtype: file

    | **Notes**
    | This function assumes that the GPS_file.txt and list of pictures
    | are in the same order: i.e., that the first GPS point in the
    | GPS list corresponds to the first GPS flight of the main flight,
    | the last point is the last of the flight, and similarly that the
    | first photo (based on an alphabetical A-Z sort) is the first photo
    | in the main flight and the last is the last.

    | **Example**
    | >>> f1 = open(filepath, 'r')
    | >>> f2 = generation.utilities.interpolate_gps_positions_for_cams(f1)
    """

    pass
