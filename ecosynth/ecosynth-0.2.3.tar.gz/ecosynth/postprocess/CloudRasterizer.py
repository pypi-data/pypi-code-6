"""
CloudRasterizer
==============
"""

__all__ = ['CloudRasterizer']

import time

import numpy as np
import pylab as pl
import scipy.stats as stats


class CloudRasterizer(object):
    """
    CloudRasterizer Class for processing Point Cloud and enabling 2D analysis

    :param np.array xyzrgb_array: XYZRGB numpy array
    :param int resolution: (Optional) grid size relative to units of
        point cloud (assumed to be meters)
    :pararm list aoi: (Optional) [xMin, xMax, yMin, yMax, zMin, zMax]

    :var int resolution: grid size relative to units of point cloud
    :var np.array cloud_array: points in given AOI
    :var int xMin:
    :var int yMin:
    :var int zMin:
    :var np.array grid: 2D grid of arrays filled with XYZRGB points

    | **Notes**
    | here

    | **Example**
    | here

    """
    def __init__(self, xyzrgb_array, resolution=1):
        """

        """
        self.aoi = self.get_aoi(xyzrgb_array=xyzrgb_array)
        self.resolution = resolution
        self.cloud_array = self.subset_cloud_array(xyzrgb_array, self.aoi)
        self.grid = self.cloud_to_grid(self.cloud_array, resolution)

    def subset_cloud_array(self, xyzrgb_array, aoi=None):
        """
        Filters points outside given Area of Interest

        :param np.array xyzrgb_array:
        :param list aoi: (Optional) [xMin, xMax, yMin, yMax, zMin, zMax]

        :return: xyzrgb_array_filtered
        :rtype: np.array
        """
        start = time.time()
        if not aoi:
            print "   subset_cloud_array time:", time.time()-start
            return xyzrgb_array
        else:
            subset = []
            for point in xyzrgb_array:
                if ((aoi[0] <= point[0]) and (aoi[1] + 1 >= point[0])):
                    if ((aoi[2] <= point[1]) and (aoi[3] + 1 >= point[1])):
                            subset.append(point)

            xyzrgb_array_filtered = np.array(subset)
            print "   subset_cloud_array time:", time.time()-start
            return xyzrgb_array_filtered

    def _build_empty_grid():
        pass

    def _fill_grid():
        pass

    def cloud_to_grid(self, xyzrgb_array, resolution):
        """
        Sorts points into an XYZ grid and returns grid

        :param np.array xyzrgb_array:
        :param int resolution:

        :return: grid
        :rtype: np.array
        """
        start = time.time()
        aoi = self.get_aoi(xyzrgb_array=xyzrgb_array)

        if not aoi:
            Xmin = 0
            Xmax = 0
            Ymin = 0
            Ymax = 0
            Zmin = 0
            Zmax = 0

        else:
            Xmin = aoi[0]
            Xmax = aoi[1]
            Ymin = aoi[2]
            Ymax = aoi[3]
            Zmin = aoi[4]
            Zmax = aoi[5]

        # Build empty grid
        grid = []
        buff = int(1/resolution)

        if buff < 1:
            buff = 1

        for x in range(buff + int(int(Xmax - Xmin)/resolution)):
            grid.append([])
            for y in range(buff + int(int(Ymax - Ymin)/resolution)):
                grid[x].append([])

        # Fill Grid
        for i in range(len(xyzrgb_array)):
            x = int((xyzrgb_array[i][0] - Xmin)/resolution)
            y = int((xyzrgb_array[i][1] - Ymin)/resolution)

            grid[x][y].append(xyzrgb_array[i])

        print "   cloud_to_grid time:", time.time()-start
        return np.array(grid)

    def grid_to_cloud(self):
        """
        Takes points from a grid and builds an array

        :param list grid:

        :return: cloud_array
        :rtype: np.array
        """
        start = time.time()
        cloud_list = []
        x_len = len(self.grid)
        y_len = len(self.grid[0])

        for x in range(x_len):
            for y in range(y_len):
                z_col_array = self.get_z_column(x, y)
                if (z_col_array is None) or (not z_col_array.any()):
                    pass
                else:
                    for point in z_col_array:
                        cloud_list.append(point)

        cloud_array = np.array(cloud_list)
        print "   grid_to_cloud time:", time.time()-start
        return cloud_array

#Filter Functions
    def filter_noise_z(self, z_score_cutoff_global=3, z_score_cutoff_local=3):
        """
        Filters height noise above and below a given number of z-scores

        Filters points from a grid that have heights (z-dim) greater than
        the given number of standard deviations away from standard score.
        The filter is first applied over the cloud and then locally in
        z-columns with x and y dimensions equal to the grid resolution.

        :param float z_score_cutoff_global: (Optional)
        :param float z_score_cutoff_local: (Optional)
        """
        # Global Filter
        self._filter_noise_z_global(z_score_cutoff_global)

        # Local Filter
        self._filter_noise_z_local(z_score_cutoff_local)

    def _filter_noise_z_global(self, z_score_cutoff):
        """
        Filters global height noise

        :param float z_score_cutoff:
        """
        start = time.time()
        # Find z-scores
        indices = np.where(abs(
            stats.zscore(self.cloud_array[:, 2])) < z_score_cutoff)

        # Filter array
        filtered_cloud_array = self.cloud_array[indices]

        # Update object data
        self.cloud_array = filtered_cloud_array
        self.grid = self.cloud_to_grid(
            filtered_cloud_array, resolution=self.resolution)
        self.aoi = self.get_aoi(xyzrgb_array=filtered_cloud_array)

        print "   filter noise z global time:", time.time()-start
        return

    def _filter_noise_z_local(self, z_score_cutoff):
        """
        Filters local height noise

        :param float z_score_cutoff:
        """
        start = time.time()

        x_len = len(self.grid)
        y_len = len(self.grid[0])

        for x in range(x_len):
            for y in range(y_len):
                z_col_array = self.get_z_column(x, y)
                if (z_col_array is None) or (not z_col_array.any()):
                    pass
                else:
                    indices = np.where(abs(
                        stats.zscore(z_col_array[:, 2])) < z_score_cutoff)
                    filtered_col = z_col_array[indices]

                    self.set_z_column(x, y, filtered_col)

        # Update object data
        filtered_cloud_array = self.grid_to_cloud()

        self.cloud_array = filtered_cloud_array

        self.grid = self.cloud_to_grid(
            filtered_cloud_array, resolution=self.resolution)

        self.aoi = self.get_aoi(xyzrgb_array=filtered_cloud_array)



        print "   filter noise z local time:", time.time()-start
        return

    def filter_points_below_height(self, raster):
        """
        (Unimplemented)
        Filters points in grid that are below the corresponding value in
        the given raster

        :param np.array raster: (Note: np.arry or list or ?)

        :return: cv_object
        :rtype: CloudRasterizer
        """
        # For loop
            # Fetch z-column array

            # Filter

            # Append to new array

        # Rebuild grid from array

        pass

    def filter_points_above_height(self, raster):
        """
        (Unimplemented)
        Filters points in grid that are above the corresponding value in
        the given raster

        :param np.array raster: (Note: np.arry or list or ?)

        :return: cv_object
        :rtype: CloudRasterizer
        """
        # Filter array

        # Rebuild grid

        pass

#Get CloudRasterizer Functions
    def get_aoi(self, xyzrgb_array=None):
        """
        Searches own point_cloud and returns boundary points in physical space

        :return: aoi
        :rtype: list of integers
            [eastMin, eastMax, northMin, northMax, elevMin, elevMax]

        | *Example*
        | [35321, 35357, 46542, 46987, 10, 50]
        """
        start = time.time()
        aoi = []

        if (xyzrgb_array == None):
            aoi.append(int(np.amin(self.cloud_array[:, 0])))
            aoi.append(int(np.amax(self.cloud_array[:, 0])))
            aoi.append(int(np.amin(self.cloud_array[:, 1])))
            aoi.append(int(np.amax(self.cloud_array[:, 1])))
            aoi.append(int(np.amin(self.cloud_array[:, 2])))
            aoi.append(int(np.amax(self.cloud_array[:, 2])))

        elif not xyzrgb_array.any():
            pass

        else:
            aoi.append(int(np.amin(xyzrgb_array[:, 0])))
            aoi.append(int(np.amax(xyzrgb_array[:, 0])))
            aoi.append(int(np.amin(xyzrgb_array[:, 1])))
            aoi.append(int(np.amax(xyzrgb_array[:, 1])))
            aoi.append(int(np.amin(xyzrgb_array[:, 2])))
            aoi.append(int(np.amax(xyzrgb_array[:, 2])))

        print "   get_aoi time:", time.time()-start
        return aoi

    def get_shape(self):
        """
        Returns grid shape

        :return: grid_shape (X, Y)
        :rtype: tuple of integers

        | *Example*
        | >>> shape = cv.get_shape()
        | >>> print shape
        |   (10, 10)

        """
        grid_shape = [0, 0]
        grid_shape[0] = len(self.grid)
        grid_shape[1] = len(self.grid[0])

        grid_shape = tuple(grid_shape)
        return grid_shape

    def get_cloud_array(self):
        """
        Returns a copy of the cloud_array, with the option of subsetting it

        :return: cloud_array
        :rtype: np.array
        """
        return np.copy(self.cloud_array)

    def get_xyzrgb_array(self):
        """
        Returns a copy of the cloud_array, with the option of subsetting it

        :return: xyzrgb_array
        :rtype: np.array
        """
        return np.copy(self.cloud_array[:, 0:6])

    def get_xyz_grid(self, aoi=None):
        """
        Returns a copy of an XYZ grid, with the option of subsetting it

        :param list aoi: [xMin, xMax, yMin, yMax, zMin, zMax]

        :return: 2D grid
        :rtype: list
        """
        # Check for subset      if subset:
        if aoi:
            a = self.subset_cloud_array(self.cloud_array)
            g = self.cloud_to_grid(a, self.resolution)
        else:
            g = np.copy(self.grid)

        # Else just make copy of grid
        return g

    def get_xy_plane(self, z_index, subset=None):
        """
        (Unimplemented)
        Returns a copy of an XY grid at a given index in the Z dimension

        :param int z_index: height index
        :param list subset: aoi [xMin, xMax, yMin, yMax, zMin, zMax]

        :return: 2D grid
        :rtype: list
        """
        pass

    def get_xz_plane(self, subset=None):
        """
        (Unimplemented)
        """
        pass

    def get_yz_plane(self, subset=None):
        """
        (Unimplemented)
        """
        pass

    def get_x_column(self, x, y):
        """
        (Unimplemented)
        """
        pass

    def get_y_column(self, x, y):
        """
        (Unimplemented)
        """
        pass

    def get_z_column(self, x, y):
        """
        Fetches all cells at a given XY index and returns as a
        single array

        :param int x: Index (Check on this)
        :param int y: Index (Check on this)

        :return: z_column_array
        :rtype: np.array
        """
        in_bounds = self.is_in_grid_bounds(x, y, None)
        if not in_bounds:
            return None

        z_col = self.grid[x][y]

        return np.copy(z_col)

    def is_in_grid_bounds(self, x, y, z):
        """
        Boolean function that checks whether a given set of indices falls
        within the grid bounds

        :return: in_grid_bounds
        :rtype: boolean (True or False)
        """
        if (x and ((x < 0) or (x > len(self.grid) - 1))):
            return False
        if (y and ((y < 0) or (y > len(self.grid[0]) - 1))):
            return False
        if (z and ((z < 0) or (z > len(self.grid[0][0]) - 1))):
            return False

        return True

    def get_cell(self, x, y, z):
        """
        (Unimplemented)
        Fetches points of a given XYZ cell and returns as an array

        :param int x: Easting index (Check on this)
        :param int y: Northing index (Check on this)
        :param int z: Height index

        :return: cell_array
        :rtype: np.array
        """
        #z_col = self.get_z_column(x, y)
        #  Find points that match with z
        pass

#Set CloudRasterizer Functions
    def set_z_column(self, x, y, z_column_array):
        """
        Creates a list of cells and replaces grid cells in z column with given
        x and y indices

        :param int x:
        :param int y:
        :param np.array z_column_array:
        """
        in_bounds = self.is_in_grid_bounds(x, y, None)
        if not in_bounds:
            raise ValueError

        self.grid[x][y] = z_column_array

        return

#Analysis Functions
    def get_cv_elevation_raster(self):
        """
        Returns XY raster containing coefficients of variation for each Z
        column with respect to elevation

        :return: cv_elevation_raster
        :rtype: np.array
        """
        x_len = len(self.grid)
        y_len = len(self.grid[0])

        raster = np.zeros([x_len, y_len])
        for x in range(x_len):
            for y in range(y_len):
                z_col_array = self.get_z_column(x, y)
                if (z_col_array is None) or (not z_col_array.any()):
                    col_cv_elev = None
                else:
                    col_std = z_col_array[:, 2].std()
                    col_mean = z_col_array[:, 2].mean()
                    col_cv_elev = col_std / col_mean
                raster[x][y] = col_cv_elev

        cv_elevation_raster = np.array(raster)
        return cv_elevation_raster

    def get_cv_height_raster(self):
        """
        Returns XY raster containing coefficients of variation for each Z
        column with respect to height

        :return: cv_height_raster
        :rtype: np.array
        """
        x_len = len(self.grid)
        y_len = len(self.grid[0])

        raster = np.zeros([x_len, y_len])
        for x in range(x_len):
            for y in range(y_len):
                z_col_array = self.get_z_column(x, y)
                if (z_col_array is None) or (not z_col_array.any()):
                    col_cv_height = None
                else:
                    col_std = z_col_array[:, 2].std()
                    col_mean = z_col_array[:, 2].mean()
                    col_cv_height = col_std / col_mean
                raster[x][y] = col_cv_height

        cv_height_raster = np.array(raster)
        return cv_height_raster

    def get_Q95_elevation_raster(self, percentile=95):
        """
        Returns XY raster containing the Q95 percentile z-value for each Z
        column with respect to elevation

        :return: q95_elevation_raster
        :rtype: np.array
        """
        x_len = len(self.grid)
        y_len = len(self.grid[0])

        raster = np.zeros([x_len, y_len])
        for x in range(x_len):
            for y in range(y_len):
                z_col_array = self.get_z_column(x, y)
                if (z_col_array is None) or (not z_col_array.any()):
                    q95_value = None
                else:
                    q95_value = stats.scoreatpercentile(z_col_array[:, 2], percentile)
                raster[x][y] = q95_value

        q95_elevation_raster = np.array(raster)
        return q95_elevation_raster

        # stats.scoreatpercentile(heights,95)
        pass

    def get_color_raster(self):
        """
        Returns XY raster containing the RGB value for the highest point in
        each Z column

        :return: color_raster
        :rtype: np.array

        | **Example**
        |
        """
        x_len = len(self.grid)
        y_len = len(self.grid[0])

        raster = np.zeros([x_len, y_len, 3])
        for x in range(x_len):
            for y in range(y_len):
                z_col_array = self.get_z_column(x, y)
                if (z_col_array is None) or (not z_col_array.any()):
                    rgb = None
                else:
                    max_index = np.argmax(z_col_array[:, 2])
                    rgb = z_col_array[max_index, 3:6]
                raster[x][y] = rgb

        color_raster = np.array(raster, dtype=np.uint8)
        return color_raster

    def get_height_range_raster(self):
        """
        Returns XY raster containing the difference between the highest point
        and the lowest point in each Z column

        :return: height_range_raster
        :rtype: np.array
        """
        x_len = len(self.grid)
        y_len = len(self.grid[0])

        raster = np.zeros([x_len, y_len])
        for x in range(x_len):
            for y in range(y_len):
                z_col_array = self.get_z_column(x, y)
                if (z_col_array is None) or (not z_col_array.any()):
                    height_range = None
                else:
                    col_max = z_col_array[:, 2].max()
                    col_min = z_col_array[:, 2].min()
                    height_range = (col_max - col_min)
                raster[x][y] = height_range

        height_range_raster = np.array(raster)
        return height_range_raster

    def get_log_density_raster(self):
        """
        (Unimplemented)
        (Future implementation: add layer selection)
        Returns XY raster of containing logarithmic point cloud density for
        each Z column

        point_density * log(point_density)

        :return: log_density_raster
        :rtype: np.array
        """
        x_len = len(self.grid)
        y_len = len(self.grid[0])

        raster = np.zeros([x_len, y_len])
        for x in range(x_len):
            for y in range(y_len):
                z_col_array = self.get_z_column(x, y)
                if (z_col_array is None) or (not z_col_array.any()):
                    col_log_dens = None
                else:
                    # EQUATION HERE
                    #col_log_dens = z_col_array[:, 2]).size
                    pass
                raster[x][y] = col_log_dens

        log_density_raster = np.array(raster)
        return log_density_raster

    def get_max_elevation_raster(self):
        """
        (Note: Distinction needed for height and elevation)
        Returns XY raster containing the maximum z-value for each
        Z column in terms of elevation

        :return: max_elevation_raster
        :rtype: np.array
        """
        x_len = len(self.grid)
        y_len = len(self.grid[0])

        raster = np.zeros([x_len, y_len])
        for x in range(x_len):
            for y in range(y_len):
                z_col_array = self.get_z_column(x, y)
                if (z_col_array is None) or (not z_col_array.any()):
                    col_max_elev = None
                else:
                    col_max_elev = np.max(z_col_array[:, 2])
                raster[x][y] = col_max_elev

        max_elevation_raster = np.array(raster)
        return max_elevation_raster

    def get_max_height_raster(self):
        """
        (Note: Distinction needed for height and elevation)
        Returns XY raster containing the maximum z-value for each
        Z column in terms of height

        :return: max_height_raster
        :rtype: np.array
        """
        x_len = len(self.grid)
        y_len = len(self.grid[0])

        raster = np.zeros([x_len, y_len])
        for x in range(x_len):
            for y in range(y_len):
                z_col_array = self.get_z_column(x, y)
                if (z_col_array is None) or (not z_col_array.any()):
                    col_max_height = None
                else:
                    col_max_height = np.max(z_col_array[:, 2])
                raster[x][y] = col_max_height

        max_height_raster = np.array(raster)
        return max_height_raster

    def get_mean_elevation_raster(self):
        """
        (Note: Distinction needed for height and elevation)
        Returns XY raster containing the mean z-value for each
        Z column in terms of elevation

        :return: mean_elevation_raster
        :rtype: np.array
        """
        x_len = len(self.grid)
        y_len = len(self.grid[0])

        raster = np.zeros([x_len, y_len])
        for x in range(x_len):
            for y in range(y_len):
                z_col_array = self.get_z_column(x, y)
                if (z_col_array is None) or (not z_col_array.any()):
                    col_mean_elev = None
                else:
                    col_mean_elev = np.mean(z_col_array[:, 2])
                raster[x][y] = col_mean_elev

        mean_elevation_raster = np.array(raster)
        return mean_elevation_raster

    def get_mean_height_raster(self):
        """
        (Note: Distinction needed for height and elevation)
        Returns XY raster containing the mean z-value for each
        Z column in terms of height

        :return: mean_height_raster
        :rtype: np.array
        """
        x_len = len(self.grid)
        y_len = len(self.grid[0])

        raster = np.zeros([x_len, y_len])
        for x in range(x_len):
            for y in range(y_len):
                z_col_array = self.get_z_column(x, y)
                if (z_col_array is None) or (not z_col_array.any()):
                    col_mean_height = None
                else:
                    col_mean_height = np.mean(z_col_array[:, 2])
                raster[x][y] = col_mean_height

        mean_height_raster = np.array(raster)
        return mean_height_raster

    def get_median_elevation_raster(self):
        """
        (Note: Distinction needed for height and elevation)
        Returns XY raster containing the median z-value for each
        Z column in terms of elevation

        :return: median_elevation_raster
        :rtype: np.array
        """
        x_len = len(self.grid)
        y_len = len(self.grid[0])

        raster = np.zeros([x_len, y_len])
        for x in range(x_len):
            for y in range(y_len):
                z_col_array = self.get_z_column(x, y)
                if (z_col_array is None) or (not z_col_array.any()):
                    col_median_elev = None
                else:
                    col_median_elev = np.median(z_col_array[:, 2])
                raster[x][y] = col_median_elev

        median_elevation_raster = np.array(raster)
        return median_elevation_raster

    def get_median_height_raster(self):
        """
        (Note: Distinction needed for height and elevation)
        Returns XY raster containing the median z-value for each
        Z column in terms of height

        :return: median_height_raster
        :rtype: np.array
        """
        x_len = len(self.grid)
        y_len = len(self.grid[0])

        raster = np.zeros([x_len, y_len])
        for x in range(x_len):
            for y in range(y_len):
                z_col_array = self.get_z_column(x, y)
                if (z_col_array is None) or (not z_col_array.any()):
                    col_median_height = None
                else:
                    col_median_height = np.median(z_col_array[:, 2])
                raster[x][y] = col_median_height

        median_height_raster = np.array(raster)
        return median_height_raster

    def get_point_density_raster(self):
        """
        (Future implementation: add layer selection)
        Returns XY raster containing the point density for each
        Z column

        :return: point_density_raster
        :rtype: np.array
        """
        x_len = len(self.grid)
        y_len = len(self.grid[0])

        raster = np.zeros([x_len, y_len])
        for x in range(x_len):
            for y in range(y_len):
                z_col_array = self.get_z_column(x, y)
                if (z_col_array is None) or (not z_col_array.any()):
                    column_points = 0
                else:
                    column_points = z_col_array[:, 2].size
                raster[x][y] = column_points

        point_density_raster = np.array(raster)
        return point_density_raster

    def get_std_raster(self):
        """
        (Future implementation: add layer selection)

        Returns XY raster containing the standard deviation for each
        Z column in terms of elevation

        :return: std_raster
        :rtype: np.array
        """
        x_len = len(self.grid)
        y_len = len(self.grid[0])

        raster = np.zeros([x_len, y_len])
        for x in range(x_len):
            for y in range(y_len):
                z_col_array = self.get_z_column(x, y)
                if (z_col_array is None) or (not z_col_array.any()):
                    col_std = None
                else:
                    col_std = z_col_array[:, 2].std()
                raster[x][y] = col_std

        std_raster = np.array(raster)
        return std_raster

#Compare Functions
    def compare_to_cloud(self):  # Needs clarity
        pass

    def mapOverlap(self):  # Needs clarity
        pass

    def compare_to_raster(self, r1, r2):  # Needs clarity
        pass

    def cross_correlate_with_raster(self, r1, r2):  # Needs clarity
        pass

#Plot Functions
    def plot_raster_heatmap(self, raster, title=None, png_file=None):
        """
        Generates 2D heatmap of given 2D raster

        :param np.array raster:
        :param string title: (Optional title)
        :param file png_file: (Optional) outputs image to file as png
        """
        pl.figure()
        masked_raster = np.ma.array(raster, mask=np.isnan(raster))

        if title:
            pl.title(title)

        pl.pcolor(masked_raster)
        pl.colorbar()

        if png_file:
            pl.savefig(png_file)
        else:
            pl.show()

        pl.close()

        return

    def plot_raster_colors(self, raster, title=None, png_file=None):
        """
        Plots color raster

        :param np.array raster: Two-dimensional grid with each cell containing
            three values (RGB)
        :param string title: (Optional title)
        :param file png_file: (Optional) outputs image to file as pn
        """
        pl.figure()
        masked_raster = (np.ma.array(raster, mask=np.isnan(raster)) / 255.0)

        pl.imshow(masked_raster)

        if png_file:
            pl.savefig(png_file)
        else:
            pl.show()

        pl.close()
        return

    def plot_meshgrid(self, raster):
        """
        (Unimplemented)
        Generates 3D mesh of given raster

        :param np.array raster:

        :return: image
        :rtype: png?
        """

        return
