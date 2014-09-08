import os
import time
import collections
import tempfile
import math
from selenium import webdriver
from gmapsbounds import utils
from gmapsbounds import reader
from gmapsbounds import constants

class Location:
    def __init__(self, driver, name):
        self.driver = driver
        self.name = name
        self.save_dir = tempfile.mkdtemp()
        self.center = ''
        self.zoom = ''
        self.boundaries = []

    def download_center_map(self):
        self.load_map()
        self.center, self.zoom = utils.parse_url(self.driver.current_url)
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
        container = self.driver.find_element_by_id('app-container')
        container.click()
        time.sleep(5)
        self.driver.save_screenshot(os.path.join(self.save_dir, filename))

    def calculate_coordinates(self):
        boundaries_filename = os.path.join(self.save_dir, 'boundaries.png')
        rgb_im = reader.load_image(boundaries_filename)
        nodes = reader.get_nodes(rgb_im)
        self.boundaries = reader.order_nodes(nodes, rgb_im)
        self.boundaries = utils.prune_nodes(self.boundaries)
        self.boundaries = utils.remove_overlapping_polygons(self.boundaries)
        location_map = reader.Map(self.center, rgb_im.size[0], rgb_im.size[1], self.zoom)
        location_map.attach_nodes(self.boundaries)
        with open('cityarray.js', 'w') as f:
            f.write('var COORDINATES = [\n')
            for node_collection in self.boundaries:
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
        for node_collection in self.boundaries:
            boundaries.append([node.get_lat_lng() for node in node_collection])
        return collections.OrderedDict([
            ['name', self.name],
            ['center', center_list],
            ['boundaries', boundaries]
        ])
