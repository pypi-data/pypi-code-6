import os
import time
import shutil
import xml.etree.ElementTree as ET
from selenium import webdriver
from gmapsbounds import utils
from gmapsbounds import reader
from gmapsbounds import constants
from gmapsbounds import llpx

class Location:
    def __init__(self, driver, name, save_dir):
        self.driver = driver
        self.name = name
        self.save_dir = save_dir
        self.center = ''
        self.zoom = ''
        self.polygons = []

    def download_center_map(self):
        self.load_map()
        self.center, self.zoom = utils.parse_url(self.driver.current_url)
        center_list = [float(coord) for coord in self.center.split(', ')]
        if self.center in constants.ZOOM_OUT:
            self.zoom_out()
        self.offset = llpx.lat_lng_to_pixels(center_list[0], center_list[1], self.zoom)
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

    def take_map_screenshot(self, filename):
        # this closes the ad panel
        self.driver.find_element_by_class_name('widget-scale').click()
        time.sleep(1)
        # usually one second is enough to close the panel. Sometimes on
        # slower internet connections it isn't, and we just aren't able
        # to use that portion of the screenshot
        self.driver.save_screenshot(os.path.join(self.save_dir, filename))
        # shutil.copyfile(os.path.join(self.save_dir, filename), filename)

    def calculate_coordinates(self):
        rgb_im = utils.load_image(os.path.join(self.save_dir, 'boundaries.png'))
        nodes = reader.get_nodes(rgb_im)
        self.polygons = reader.get_polygons(nodes, rgb_im)
        self.polygons = reader.prune_extra_nodes(self.polygons)
        self.polygons = reader.prune_overlapping_nodes(self.polygons)
        self.pixcenter = [rgb_im.size[0] // 2, rgb_im.size[1] // 2]
        self.attach_nodes()

    def attach_nodes(self):
        for poly in self.polygons:
            for node in poly.nodes:
                node.location = self
            if poly.inner is not None:
                for node in poly.inner.nodes:
                    node.location = self