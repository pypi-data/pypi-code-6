import os
import re
import time
from PIL import Image
import xml.etree.ElementTree as ET
from selenium import webdriver
from gmapsbounds import constants

def load_image(filename):
    im = Image.open(filename)
    im.load()
    return im.convert('RGB')

def parse_url(url):
    spl = url.split('/')
    assert ['https:', '', 'www.google.com', 'maps', 'place'] == spl[:5]
    lat_lng = re.search(r'@([-0-9.]+,[-0-9.]+)', spl[6]).group(1)
    lat_lng = lat_lng.replace(',', ', ')
    zoom = re.search(r'(\d{1,2})z$', spl[6]).group(1)
    return lat_lng, zoom

def launch_driver(url=''):
    driver = webdriver.Firefox()
    driver.maximize_window()
    if url:
        driver.get(url)
    return driver

def ray_crosses_edge(point, v1, v2):
    '''
    Test whether a point lies within a polygon, excluding vertices and edges
    '''
    # All three args are nodes with x and y properties
    # Ray goes north for this function
    if (point.x > max(v1.x, v2.x) or point.x < min(v1.x, v2.x) or
        point.y < min(v1.y, v2.y) or (v1.x == point.x and v1.x <= v2.x)):
        return False
    return not (point.y <= v2.y - (v2.x - point.x) * get_slope(v1, v2))

def get_water_multiplier(node1, node2, rgb_image):
    '''
    Return approximate water multiplication factor between two nodes
    '''
    x = node1.x
    y = node1.y
    count = 0
    iterations = 10
    for i in range(iterations):
        x += (node2.x - node1.x) / iterations
        y += (node2.y - node1.y) / iterations
        r, g, b = rgb_image.getpixel((x, y))
        if is_water(r, g, b):
            count += 1
    return 1 + count * .5

def is_water(r, g, b):
    if r in constants.WATER_RED and g in constants.WATER_GREEN and b in constants.WATER_BLUE:
        return True
    return False

def get_slope(node1, node2):
    try:
        return (node2.y-node1.y) / (node2.x - node1.x)
    except:
        return None

def get_distance(node1, node2):
    return((node1.x - node2.x)**2 + (node1.y - node2.y)**2)**.5

def get_midpoint(node1, node2):
    return (node1.x + (node2.x - node1.x) / 2, node1.y + (node2.y - node1.y) / 2)

def makeelement(tag, text=None, attributes=None, tail=None):
    if attributes is None:
        attributes = {}
    newelement = ET.Element(tag)
    for k, v in attributes.items():
        newelement.set(k, v)
    if text is not None: newelement.text = text
    if tail is not None: newelement.tail = tail
    return newelement


def sort_by_polygon_length(polygons):
    less = []
    equal = []
    greater = []
    if len(polygons) > 1:
        pivot = polygons[0]
        for poly in polygons:
            if len(poly.nodes) < len(pivot.nodes):
                less.append(poly)
            if len(poly.nodes) == len(pivot.nodes):
                equal.append(poly)
            if len(poly.nodes) > len(pivot.nodes):
                greater.append(poly)
        return sort_by_polygon_length(less) + equal + sort_by_polygon_length(greater)
    return polygons

def get_menu_borders(rgb_image):
    for x in range(30, 430):
        r, g, b = rgb_image.getpixel((x, 370))
        if [r, g, b] != [255, 255, 255]:
            return constants.MENU_BORDERS
    return constants.MENU_BORDERS_WITH_ADS

def add_coordinates_to_boundary(boundary, nodes):
    linear_ring = ET.SubElement(boundary, 'LinearRing')
    coordinates = ET.SubElement(linear_ring, 'coordinates')
    text_list = []
    for node in nodes:
        coords_as_strings = [str(coord) for coord in node.get_lat_lng()]
        text_list.append(','.join(reversed(coords_as_strings)))
    coordinates.text = '\n'.join(text_list)

def add_polygons_to_placemark(placemark, polygons):
     for poly in polygons:
        polygon = ET.SubElement(placemark, 'Polygon')
        polygon.append(makeelement('extrude', '1'))
        polygon.append(makeelement('altitudeMode', 'relativeToGround'))
        boundary = ET.SubElement(polygon, 'outerBoundaryIs')
        add_coordinates_to_boundary(boundary, poly.nodes)
        if poly.inner is not None:
            boundary = ET.SubElement(polygon, 'innerBoundaryIs')
            add_coordinates_to_boundary(boundary, poly.inner.nodes)

def add_placemark(root, location):
    placemark = ET.SubElement(root, 'Placemark')
    placemark.append(makeelement('name', location.name))
    add_polygons_to_placemark(placemark, location.polygons)

def write_to_kml(location_list, filename):
    if filename.endswith('.kml'):
        root = makeelement('kml', attributes={'xmlns': 'http://www.opengis.net/kml/2.2'})
        for location in location_list:
            add_placemark(root, location)
        with open(filename, 'w') as f:
            f.write(ET.tostring(root).decode('utf8'))
    else:
        for location in location_list:
            root = makeelement('kml', attributes={'xmlns': 'http://www.opengis.net/kml/2.2'})
            add_placemark(root, location)
            with open('{}.kml'.format(os.path.join(filename, location.name)), 'w') as f:
                f.write(ET.tostring(root).decode('utf8'))
