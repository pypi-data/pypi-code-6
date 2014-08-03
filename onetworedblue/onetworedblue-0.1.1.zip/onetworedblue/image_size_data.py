__author__ = 'Eric'
import math
from PIL import Image

default_look_angle_x = 42.3211 * math.pi / 180.
default_look_angle_y = 34.26 * math.pi / 180.

class ImageSizeData(object):
    def __init__(self, image_file_path, altitude):
        with open(image_file_path, 'rb') as im_file:
            im = Image.open(im_file)
            self.image_size_x, self.image_size_y = im.size

        self.altitude = altitude

        self.look_angle_x = default_look_angle_x
        self.look_angle_y = default_look_angle_y

    @property
    def view_width_meters(self):
        return 2. * self.altitude * math.atan(self.look_angle_x/2.)

    @property
    def view_height_meters(self):
        return 2. * self.altitude * math.atan(self.look_angle_y/2.)

    @property
    def area_sq_meters(self):
        return self.view_width_meters * self.view_width_meters

    @property
    def ratio_meters_to_pixels_x(self):
        return self.view_width_meters / self.image_size_x

    @property
    def ratio_meters_to_pixels_y(self):
        return self.view_height_meters / self.image_size_y

    def pixels_to_meters_x(self, num_pixels):
        return num_pixels * self.ratio_meters_to_pixels_x

    def pixels_to_meters_y(self, num_pixels):
        return num_pixels * self.ratio_meters_to_pixels_y

    def pixels_to_meters(self, point):
        return (self.pixels_to_meters_x(point[0]), self.pixels_to_meters_y(point[1]))

    def get_distance_meters(self, first_point, second_point):
        distance_x = abs(first_point[0] - second_point[0])
        distance_y = abs(first_point[1] - second_point[1])

        meters_x = self.pixels_to_meters_x(distance_x)
        meters_y = self.pixels_to_meters_y(distance_y)

        return math.sqrt(meters_x**2. + meters_y**2.)

    def get_distance_cm(self, first_point, second_point):
        return self.get_distance_meters(first_point, second_point) * 100.

    def get_area_sq_meters(self, polygon_points):
        # First, convert the points to meter space
        points_m = [self.pixels_to_meters(point) for point in polygon_points]

        # Now, get the area
        return polygon_area(points_m)

    def get_area_sq_cm(self, polygon_points):
        return self.get_area_sq_meters(polygon_points) * (100.**2)


def polygon_area(corners):
    corners = polygon_sort(corners)
    n = len(corners) # of corners
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]
    area = abs(area) / 2.0
    return area

def polygon_sort(corners):
    # calculate centroid of the polygon
    n = len(corners) # of corners
    cx = float(sum(x for x, y in corners)) / n
    cy = float(sum(y for x, y in corners)) / n
    # create a new list of corners which includes angles
    cornersWithAngles = []
    for x, y in corners:
        an = (math.atan2(y - cy, x - cx) + 2.0 * math.pi) % (2.0 * math.pi)
        cornersWithAngles.append((x, y, an))
    # sort it using the angles
    cornersWithAngles.sort(key = lambda tup: tup[2])
    # return the sorted corners w/ angles removed
    return map(lambda (x, y, an): (x, y), cornersWithAngles)



