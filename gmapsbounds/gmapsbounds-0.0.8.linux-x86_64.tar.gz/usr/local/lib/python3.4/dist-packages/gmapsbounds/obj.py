import os
import time
from selenium import webdriver
from gmapsbounds import utils
from gmapsbounds import reader
from gmapsbounds import constants

class City:
    def __init__(self, driver, name, fast_mode=False):
        self.driver = driver
        self.name = name
        self.save_dir = os.path.join('cities', name)
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        self.fast_mode = fast_mode
        self.center = ''
        self.zoom = ''

    def download_center_map(self):
        self.load_city_map()
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

    def load_city_map(self):
        self.driver.get('https://www.google.com/maps/')
        submit_box = utils.wait_until(self.driver.find_element_by_id, 'searchboxinput')
        submit_box.clear()
        submit_box.send_keys(self.name)
        utils.wait_until(self.driver.find_element_by_class_name, 'searchbutton').click()
        while ['https:', '', 'www.google.com', 'maps', 'place'] != self.driver.current_url.split('/')[:5]:
            pass

    def load_map_detailed(self, lat_lng, zoom):
        self.driver.get('https://www.google.com/maps/place/{}/@{},{}z'.format(
        self.name.replace(' ', '+'), lat_lng.replace(' ', ''), zoom))

    def set_corner_information(self):
        self.driver.get('file://{}/../js/index.html'.format(os.path.realpath(__file__)))
        time.sleep(10)
        # ele = utils.wait_until(self.driver.find_element_by_id, 'cityinfo')
        # ele.clear()
        # ele.send_keys('{}, {}'.format(self.center, self.zoom))
        # self.driver.find_element_by_id('submitbutton').click()
        # while not ele.get_attribute('value'):
        #     pass
        # self.boundaries = [float(bound) for bound in ele.get_attribute('value').replace('(', '').replace(')', '').split(', ')]


    def take_map_screenshot(self, filename):
        container = self.driver.find_element_by_id('app-container')
        container.click()
        time.sleep(5)
        self.driver.save_screenshot(os.path.join(self.save_dir, filename))


    def calculate_coordinates(self):
        boundaries_filename = os.path.join(self.save_dir, 'boundaries.png')
        rgb_im = reader.load_image(boundaries_filename)
        nodes = reader.get_nodes(rgb_im, self.fast_mode)
        ordered_nodes = reader.order_nodes(nodes, rgb_im)
        ordered_nodes = utils.prune_nodes(ordered_nodes)
        ordered_nodes = utils.remove_overlapping_polygons(ordered_nodes)
        city_map = reader.Map(self.center, self.boundaries, rgb_im.size[0], rgb_im.size[1])
        city_map.attach_nodes(ordered_nodes)
        reader.write_coordinates(self.save_dir, city_map.nodes)
        with open(os.path.join('js', 'cityarray.js'), 'w') as f:
            f.write('var COORDINATES = [\n')
            for node_collection in ordered_nodes:
                f.write('[\n')
                for node in node_collection:
                    f.write('new google.maps.LatLng({}, {}),\n'.format(node.lat, node.lng))
                f.write('],\n')    
            f.write('];\n')
            f.write('\n')
            f.write('var INFO = "{}, {}";'.format(self.center, self.zoom))