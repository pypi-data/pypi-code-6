"""
IO
==

"""

__all__ = ['load_out', 'load_ply', 'save_ply',
            'txt_to_ply', 'ply_to_ecobrowser_point_cloud']

import collections

import numpy as np


def load_out(out_file):
    """
    :param file out_file: Bundler OUT file

    :return: out_tuple
    :rtype: Named Tuple

    | **Example**
    | >>> f = open(out_file, 'r')
    | >>> out_tuple = postprocess.io.load_out(f)
    |
    | Out Tuple Contents:
    |   out_tuple.cameras_total     <integer>
    |   out_tuple.cameras_used      <integer>
    |   out_tuple.cam_array         (Unknown Format) <numpy array>
    |   out_tuple.cam_array_fixed   (Unknown Format) <numpy array>
    |                                    used cameras correctly ordered and
    |                                    eliminates unused cameras
    |   out_tuple.points_total      <integer>
    |   out_tuple.xyzrgb_array      <numpy array>
    |
    | **Notes**
    | See here to learn more about the OUT file Format
    | http://www.cs.cornell.edu/~snavely/bundler/bundler-v0.3-manual.html

    """
    lines = out_file.readlines()

    # HEADER
    header = lines[1].rstrip().split(' ')
    cameras_total = int(header[0])
    points_total = int(header[1])

    # FILTER CAMERAS
    cam_offset = 2
    rows_per_camera = 5
    columns = 3

    cameras_section = lines[cam_offset: (cameras_total * rows_per_camera) + cam_offset]
    cameras_array = np.array([value for row in cameras_section for value in row.rstrip().split(' ')], dtype=float)
    cameras_array.resize((cameras_total * rows_per_camera, columns))

    camera_index = np.arange(cameras_total)
    camFKK = np.array([cameras_array[(rows_per_camera * i)] for i in camera_index])
    camRots = np.array([cameras_array[(rows_per_camera*i+1):(rows_per_camera*i+4)] for i in camera_index])
    camTrans = np.array([cameras_array[(rows_per_camera*i+4)] for i in camera_index])
    cameras = np.array([np.dot(-camRots[i].transpose(), camTrans[i].transpose())  for i in camera_index])
    cameras = np.vstack((cameras.transpose(), camFKK[:, 0])).transpose()

    # Find number of cameras used
    cameras_used = cameras_total
    for camera in cameras:
        if (camera[0] == 0) and (camera[1] == 0) and (camera[2] == 0):
            cameras_used -= 1

    cameras_fixed = _reorder_cameras(cameras)

    # FILTER POINTS
    rows_per_point = 3
    points_offset = cameras_total * rows_per_camera + cam_offset
    points_count = 0

    # iterate through the .out file for every point and grab
    # the XYZ, RGB, and Views return an XYZRGB list and a view list
    views_list = []
    xyz_list = []
    rgb_list = []

    while points_count < (points_total):
        pointIndex = points_offset + points_count * rows_per_point
        xyz_row = lines[pointIndex].rstrip('\n').split(' ')
        rgb_row = lines[pointIndex+1].rstrip('\n').split(' ')
        view_row = lines[pointIndex+2]
        xyz_list.append(xyz_row)
        rgb_list.append(rgb_row)
        views_list.append(view_row)
        points_count += 1

    xyz_array = np.array(xyz_list, dtype=float)
    rgb_array = np.array(rgb_list, dtype=int)
    xyzrgb_array = np.hstack((xyz_array, rgb_array))

    out = collections.namedtuple(
        'Out', ['cameras_total', 'cameras_used', 'cam_array', 'cam_array_fixed', 'points_total', 'xyzrgb_array'])

    out_tuple = out(cameras_total, cameras_used, cameras, cameras_fixed, points_total, xyzrgb_array)
    return out_tuple


def _reorder_cameras(cameras):
    """
    Solve issue with shifted camera sequence (FIND OUT MORE)

    :param np.array cameras: numpy array of cameras (MORE)

    :return: cameras_fixed
    :rtype: np.array

    """
    camerasOff = []
    camerasOff.append(cameras[-1])
    cameras = np.array(cameras)
    camerasOff = np.concatenate((np.array(camerasOff), cameras[:-1]))

    #average distance bewteen points
    camMeanX = np.mean(np.subtract(cameras[:, 0], camerasOff[:, 0]))
    camMeanY = np.mean(np.subtract(cameras[:, 1], camerasOff[:, 1]))
    #camMeanZ = np.mean(cameras[:, 2])

    #average distance bewteen points
    camSTDX = np.std(np.subtract(cameras[:, 0], camerasOff[:, 0]))
    camSTDY = np.std(np.subtract(cameras[:, 1], camerasOff[:, 1]))
    #camSTDZ = np.std(cameras[:, 2])

    moveToEnd = 0

    for i in range(len(cameras)):

        ZscoreX = (((cameras[i][0] - cameras[i - 1][0])) - camMeanX) / camSTDX
        ZscoreY = (((cameras[i][1] - cameras[i - 1][1])) - camMeanY) / camSTDY

        if (camerasOff[i][0] != cameras[i-1][0] or camerasOff[i][1] != cameras[i-1][1]):
            print "\nWarning: Cameras Off\n"

        if (abs(ZscoreY) >= 3 or abs(ZscoreX) >= 3):
            print "\nLoading OUT file: cam_array break found: ZscoreX: %f, ZscoreY: %f" % (ZscoreX, ZscoreY)
            break
        else:
            moveToEnd += 1

    camerasEnd = cameras[:moveToEnd]
    camerasBegin = cameras[moveToEnd:]

    cameras_fixed = np.concatenate((camerasBegin, camerasEnd))
    cameras_fixed = cameras_fixed[np.where(cameras_fixed[:, 0] != 0)]
    return cameras_fixed


def load_ply(ply_file, delim=' '):
    """
    Reads in PLY file and returns a PointCloud object

    :param file ply_file: PLY-formatted ascii file
    :param string delim: (Optional) delimiter for coordinate dimensions

    :return: ply_tuple
    :rtype: Named Tuple

    | PLY Tuple Contents:
    |   ply_tuple.header            <string>
    |   ply_tuple.points_total      <integer>
    |   ply_tuple.xyzrgb_array      <numpy array>
    |
    | **Example**
    | >>> f = open(filepath, 'r')
    | >>> ply_tuple = postprocess.io.load_ply(f)
    |

    """
    lines = ply_file.readlines()

    # HEADER
    header = ""
    count = 0
    while True:
        header = header + lines[count]

        if lines[count].strip().startswith('end_header'):
            count += 1
            break
        count += 1

    #points_total = int(header[1])
    coordinate_list = []
    for line in lines[count:]:
        point = line.strip().split(delim)
        if len(point) >= 6:
            coordinate_list.append([float(point[0]), float(point[1]), float(point[2]), float(point[3]), float(point[4]), float(point[5])])

    xyzrgb_array = np.array(coordinate_list)
    points_total = xyzrgb_array.shape[0]

    ply = collections.namedtuple(
        'ply', ['header', 'points_total', 'xyzrgb_array'])

    ply_tuple = ply(header, points_total, xyzrgb_array)
    return ply_tuple


def save_ply(ply_file, xyzrgb_array):
    """
    Saves a PLY named tuple as a PLY file

    :param file ply_file: file to save PLY formatted data
    :param np.array xyzrgb_array: PLY XYZRGB array

    | **Notes**
    | - Currently assumes the number of points in the file has not been
    |   changed since the PLY was loaded
    | - Currently saves all XYZRGB values to %.18e (--> larger file size)
    | - Future: Add support for creating PLY files from tuples without headers

    | **Example**
    | f = open(filepath, 'w')
    | postprocess.io.save_ply(f, ply_tuple.xyzrgb_array)
    | f.close()

    """
    # Generate Header
    header = """ply\nformat ascii 1.0\nelement face 0\nproperty\
 list uchar int vertex_indices\nelement vertex %i\n\
property float x\nproperty float y\nproperty float z\n\
property uchar diffuse_red\nproperty uchar diffuse_green\n\
property uchar diffuse_blue\nend_header\n"""

    ply_file.write(header % xyzrgb_array[:, 0].size)

    for line in xyzrgb_array:
        string = "%e %e %e %i %i %i\n" % (line[0], line[1], line[2], line[3], line[4], line[5])
        ply_file.write(string)

    return


def load_ascii_grid(ascii_file):
    """
    Loads an ascii grid as a named tuple

    :param file ascii_file:

    :return: ascii_tuple
    :rtype: named tuple

    | ASCII Grud Tuple Contents:
    |   ascii_tuple.rows        <int>
    |   ascii_tuple.cols        <int>
    |   ascii_tuple.xll         <int>
    |   ascii_tuple.yll         <int>
    |   ascii_tuple.resolution  <int>
    |   ascii_tuple.null        <int>
    |   ascii_tuple.grid        <numpy array>
    |
    | **Notes**
    | See here for more about the ASCII grid format:
    | http://daac.ornl.gov/MODIS/ASCII_Grid_Format_Description.html
    """
    ASCII = ascii_file.read()
    results = re.search("ncols\s*(?P<cols>-?\d+.?\d*)\s*nrows\s*(?P<rows>-?\d+.?\d*)\s*xllcorner\s*(?P<xCorner>-?\d+.?\d*)\s*yllcorner\s*(?P<yCorner>-?\d+.?\d*)\s*cellsize\s*(?P<cellSize>-?\d+.?\d*)\s*NODATA_value\s*(?P<noData>-?\d+.?\d*)", ASCII)

    ASCIIgrid = ASCII.splitlines()
    ASCIIgrid = np.array(ASCIIgrid)[6:]
    grid = []

    for line in ASCIIgrid:
        vals = line.strip().split(' ')
        vals = np.array(vals)
        tempList = []
        if (len(line) != []):
            for val in vals:
                if (len(val) > 0):
                #print val
                    tempList.append(float(val))
            if (len(tempList) > 0):
                grid.append(tempList)

    grid = np.rot90(grid)

    ascii_grid = collections.namedtuple(
        'ascii_grid', ['rows', 'cols', 'xll', 'yll', 'resolution', 'null', 'grid'])

    rows = float(results.group("cols"))
    cols = float(results.group("rows"))
    xll = float(results.group("xCorner"))
    yll = float(results.group("yCorner"))
    resolution = float(results.group("cellSize"))
    null = float(results.group("noData"))
    grid = np.array(grid)
    grid[grid == null] = np.nan  # sets null value to nan

    ascii_tuple = ascii_grid(
        rows, cols, xll, yll, resolution, null, grid)
    return ascii_tuple


def ply_to_ecobrowser_point_cloud():
    """
    This is a potential function

    :param str a: A string to be converted
    :param integ v: A string to be converted
    :param type b: optional parameter

    :return: the return
    :rtype: int

    :raises IndexError: if such and such

    | **Notes**
    | here

    | **Example**
    | here

    """

    pass
