import os
import time
import collections
import tempfile
import math
import xml.etree.ElementTree as ET
from selenium import webdriver
from gmapsbounds import utils
from gmapsbounds import reader
from gmapsbounds import constants
from gmapsbounds import llpx

class Location:
    def __init__(self, driver, name):
        self.driver = driver
        self.name = name
        self.save_dir = tempfile.mkdtemp()
        self.center = ''
        self.zoom = ''
        self.nodes = []

    def download_center_map(self):
        self.load_map()
        self.center, self.zoom = utils.parse_url(self.driver.current_url)
        center_list = [float(coord) for coord in self.center.split(', ')]
        self.offset = llpx.lat_lng_to_pixels(center_list[0], center_list[1], self.zoom)
        if self.center in constants.ZOOM_OUT:
            self.zoom_out()
        self.take_map_screenshot('boundaries.png')

    def zoom_out(self):
        self.zoom = str(int(self.zoom) - 1)
        current_url = self.driver.current_url
        self.driver.get('https://www.google.com/maps/place/{}/@{},{}z/'.format(
        self.name.replace(' ', '+'), self.center.replace(' ', ''), self.zoom))
        while current_url == self.driver.current_url:
            pass

    def load_map(self):
        self.driver.get('https://www.google.com/maps/place/{}'.format(self.name.replace(' ', '+')))
        while (['https:', '', 'www.google.com', 'maps', 'place'] !=
            self.driver.current_url.split('/')[:5] or '@' not in self.driver.current_url):
            pass

    def load_map_detailed(self, lat_lng, zoom):
        self.driver.get('https://www.google.com/maps/place/{}/@{},{}z'.format(
        self.name.replace(' ', '+'), lat_lng.replace(' ', ''), zoom))

    def take_map_screenshot(self, filename):
        container = self.driver.find_element_by_class_name('widget-scale')
        # clicking this closes the ad panel
        container.click()
        time.sleep(5)
        self.driver.save_screenshot(os.path.join(self.save_dir, filename))
        self.driver.save_screenshot(filename)

    def calculate_coordinates(self):
        boundaries_filename = os.path.join(self.save_dir, 'boundaries.png')
        rgb_im = utils.load_image(boundaries_filename)
        nodes = reader.get_nodes(rgb_im)
        self.nodes = reader.order_nodes(nodes, rgb_im)
        self.nodes = utils.prune_nodes(self.nodes)
        self.nodes = utils.remove_overlapping_polygons(self.nodes)
        self.pixcenter = [rgb_im.size[0] // 2, rgb_im.size[1] // 2]
        for node_collection in self.nodes:
            for node in node_collection:
                node.location = self
        with open('cityarray.js', 'w') as f:
            f.write('var COORDINATES = [\n')
            for node_collection in self.nodes:
                f.write('[\n')
                for node in node_collection:
                    lat, lng = node.get_lat_lng()
                    f.write('new google.maps.LatLng({}, {}),\n'.format(lat, lng))
                f.write('],\n')    
            f.write('];\n')
            f.write('\n')
            f.write('var INFO = "{}, {}";'.format(self.center, self.zoom))

    def as_dict(self):
        boundaries = []
        center_list = [float(coord) for coord in self.center.split(', ')]
        for node_collection in self.nodes:
            boundaries.append([node.get_lat_lng() for node in node_collection])
        return collections.OrderedDict([
            ['name', self.name],
            ['center', center_list],
            ['boundaries', boundaries]
        ])

    def write_to_kml(self, filename):
        root = ET.Element('kml')
        root.set('xmlns', 'http://www.opengis.net/kml/2.2')
        placemark = ET.SubElement(root, 'Placemark')
        placemark.append(utils.makeelement('name', self.name))
        for node_collection in self.nodes:
            polygon = ET.SubElement(placemark, 'Polygon')
            polygon.append(utils.makeelement('extrude', '1'))
            polygon.append(utils.makeelement('altitudeMode', 'relativeToGround'))
            boundary = ET.SubElement(polygon, 'outerBoundaryIs')
            linear_ring = ET.SubElement(boundary, 'LinearRing')
            coordinates = ET.SubElement(linear_ring, 'coordinates')
            text_list = []
            for node in node_collection:
                coords_as_strings = [str(coord) for coord in node.get_lat_lng()]
                text_list.append(','.join(reversed(coords_as_strings)))
            coordinates.text = '\n'.join(text_list)
        with open(filename, 'w') as f:
            f.write(ET.tostring(root).decode('utf8'))
