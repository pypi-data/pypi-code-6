"""
Utilities
=========
"""

__all__ = ['telemetry_to_gps_positions', 'filter_ardu_log', 'filtered_telemetry_to_gps_positions']

import string
import StringIO

import numpy as np
import utm


def telemetry_to_gps_positions(log_file, msl_float, gps_file=None, format="ardu", coord_sys="utm"):
    """
    Filters GPS positions from an Arudpilot log file into a text file
    NOTE: Mikro Currently Not Implemented

    :param file log_file: Telemetry Flight Log File (Comma-delimited etc.)
    :param float msl_float: lauch altitude (meters above mean sea level)
    :param file GPS Positions File: (Optional) Clean file to write GPS
     positions (UTM coordinates, meters, space-delimited, etc)
    :param string format: Telemetry log file format
    :param string coord_sys: GPS file output coordinate system

    :return: gps_array
    :rtype: np.array

    | **Example**
    | >>> log_file = open("path/to/log", 'r')
    | >>> gps_file = open("path/to/output/directory/GPS_positions.txt", 'w')
    | >>> msl = 50.6
    | >>> acquire.utilities.telemetry_to_gps_txt(log_file, msl, gps_file=gps_file)
    |
    | *Input File (log_file):*
    |
    | CTUN, 643, 0, 9787, 9800, 0, 0, 5, 422, 0
    | ATT, 0, 23, 0, 2, 0, 183, 0
    | NTUN, 29907, 0, 3, 26866, 0, 0, 230, -10
    | GPS, 232733000, 12, 38.8882963, -76.5585533, 98.0000, 99.8500, 244, 9388
    | CMD, 100, 85, 16, 1, 0, 14200, 388882720, -765593408
    | ...
    |
    | *Output File (GPS_positions.txt):*
    |
    | 364754.663 4305831.507 137.744
    | 364754.771 4305831.238 137.753
    | 364754.827 4305830.938 137.707
    | ...

    """
    if (format == "ardu"):
        filtered_log = StringIO.StringIO()  # Buffer to store filtered log
        filter_ardu_log(log_file, filtered_log)
        filtered_log.seek(0)  # Rewind buffer to beginning
        gps_array = filtered_telemetry_to_gps_positions(
            filtered_log, msl_float, gps_file=gps_file)

    elif (format == "mikro"):
        raise ValueError("Cannot process format other than Ardu")

    else:
        raise ValueError("Cannot process format other than Ardu")

    return gps_array


def filter_ardu_log(log_file, filt_log_file, types='CMD GPS'):
    '''
    Filteres data from log file

    :param file logfile: Original LOG File (FMT headers must be included)
    :param file filt_log_file: Clean file to write Filtered LOG File
    :param string types: (Optional) Space-delimited datalog types to include

    | **Example**
    | >>> log_file = open(filepath1, 'r')
    | >>> filt_log_file = open(filepath2, 'w')
    | >>> acquire.utilities.filter_ardu_log(log_file, filt_log_file)
    |
    | *Input File (flight.log):*
    | CTUN, 643, 0, 9787, 9800, 0, 0, 5, 422, 0
    | ATT, 0, 23, 0, 2, 0, 183, 0
    | NTUN, 29907, 0, 3, 26866, 0, 0, 230, -10
    | GPS, 232733000, 12, 38.8882963, -76.5585533, 98.0000, 99.8500, 244, 9388
    | CMD, 100, 85, 16, 1, 0, 14200, 388882720, -765593408
    | ...
    |
    | * Output File (filtered.log):*
    | GPS, 232733000, 12, 38.8882963, -76.5585533, 98.0000, 99.8500, 244, 9388
    | CMD, 100, 85, 16, 1, 0, 14200, 388882720, -765593408
    | ...


    '''
    datatypes = types.strip().split()

    for line in log_file:
        linesplit = string.split(line, ',')

        if ((linesplit[0] == 'FMT') and (linesplit[3].strip() in datatypes)):
            filt_log_file.write(line)

        elif ((linesplit[0] == 'FMT') and (linesplit[3].strip() == 'FMT')):
            filt_log_file.write(line)

        elif (linesplit[0] in datatypes):
            filt_log_file.write(line)

    return


def filtered_telemetry_to_gps_positions(filt_log_file, msl_float, gps_file=None, coord_sys="utm",debug=False):
    '''
    Converts filtered gps positions from telemetry into three-dimensional
    gps array

    UTM: <easting> <northing> <altitude> expressed in meters
    WGS84: Support not yet added

    :param file filt_log_file: Filtered LOG File
    :param float msl_float: lauch altitude (meters above mean sea level)
    :param file gps_file: (Optional) Clean file to write GPS coordinates
    :param string coord_sys: (Future capability of WGS84)

    :return: gps_array
    :rtype: np.array

    | *Notes*
    |
    | Default CMD Column Format:
    | CMD, CTot, CNum, CId, COpt, Prm1, Alt, Lat, Lng
    |
    | Default GPS Column Format:
    | GPS, Status, Time, NSats, HDop, Lat, Lng, RelAlt, Alt, Spd, GCrs
    |
    | See here for information on Arducopter datalogging:
    | http://copter.ardupilot.com/wiki/downloading-and-analyzing-data-logs-in-mission-planner/
    |
    | Find out meaning of these values: CMD: 16, 22
    '''
    dtype = 0
    offset = 4  # FMT Offset on where column keys begin

    # Default GPS Row Position Columns
    lat_column = 3
    lon_column = 4
    alt_column = 5

    # Default CMD Row Position Columns
    CId_col = 3

    for line in filt_log_file:
        entry_col = string.split(line, ',')

        if ((entry_col[dtype] == 'FMT') and (entry_col[3].strip() == 'GPS')):
            lat_column = entry_col.index('Lat') - offset
            lon_column = entry_col.index('Lng') - offset
            alt_column = entry_col.index('RelAlt') - offset

        if ((entry_col[dtype] == 'FMT') and (entry_col[3].strip() == 'CMD')):
            CId_col = entry_col.index('CId') - offset

    filt_log_file.seek(0)  # Rewind file to beginning

    # Begin Conversion
    GPS_array = []
    gatherFlag = 0
    pointCounter = 0

    for entry in filt_log_file:
        entry_col = string.split(entry, ', ')

        #  Takeoff Command (use this as a start)
        if ((gatherFlag == 0) and (entry_col[dtype] == 'CMD') and (int(entry_col[CId_col]) == 22)):
            gatherFlag += 1

        #  Waypoint Command
        if ((gatherFlag == 1 or gatherFlag == 2)
                and entry_col[dtype] == 'CMD' and int(entry_col[CId_col]) == 16):
            gatherFlag += 1

        #  Stalling from recording GPS commands
        if (gatherFlag >= 3 and gatherFlag <= 15):
            gatherFlag += 1

        #  Allows the recording of new GPS commands
        if (gatherFlag >= 15):
            #  What's going on here?
            if (entry_col[dtype] == 'GPS'):
                # Convert Lat/Lon to UTM
                lat = float(entry_col[lat_column])
                lon = float(entry_col[lon_column])
                point = utm.from_latlon(lat, lon)

                # Relative height
                alt = float(entry_col[alt_column])
                alt = (0.94 * (alt + msl_float)) + 1.2

                GPS_array.append([point[0], point[1], alt])

                pointCounter += 1

            #  What's going on here?
            if (entry_col[dtype] == 'CMD' and int(entry_col[CId_col]) == 16):
                pointCounter = 0

    del GPS_array[len(GPS_array) - pointCounter + 12:]

    gps_array = np.array(GPS_array)

    if gps_file:
        np.savetxt(gps_file, gps_array, fmt="%.3f", delimiter="\t")

    return gps_array
