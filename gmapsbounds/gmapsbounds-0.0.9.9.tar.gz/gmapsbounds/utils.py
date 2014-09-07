import os
import re
import time
from selenium import webdriver
from gmapsbounds import constants

def get_city_list(filename):
    cities = []
    with open(filename) as f:
        for line in f:
            try:
                city_split = line.split(',')
                if city_split[0][-1] == ' ': city_split[0] = city_split[0][:-1]
                cities.append('{}, {}'.format(city_split[0], city_split[1]))
            except IndexError:
                pass
    return cities

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

def wait_until(func, arg, interval=1):
    while True:
        try:
            return func(arg)
        except:
            time.sleep(interval)

def poly_overlap(poly1, poly2):
    i = -len(poly1) + 1
    for point in poly1:
        mx, my = get_midpoint(point, poly1[i])
        # midpoint = reader.Node(mx, my)
        if contains(point, poly2): # or contains(midpoint, poly2)
            return True
    return False

def contains(point, polygon):
    assert len(polygon) > 2
    crossings = 0
    i = -len(polygon) + 1
    matched_y = set()
    for node in polygon:
        if ray_crosses_edge(point, node, polygon[i]):
            if not point.y in matched_y:
                matched_y.add(point.y)
                crossings += 1
        i += 1
    return crossings % 2 == 1

def ray_crosses_edge(point, v1, v2):
    # All three args are nodes with x and y properties
    # Ray goes north for this function
    if point.x > max(v1.x, v2.x):
        return False
    if point.x < min(v1.x, v2.x):
        return False
    if point.y < min(v1.y, v2.y):
        return False
    if v1.x == v2.x:
        return False
    slope = (v2.y-v1.y) / (v2.x - v1.x)
    if point.y <= v2.y - (v2.x - point.x) * slope:
        return False
    return True

def remove_overlapping_polygons(polygons):
    assert polygons
    polygons.sort(key=len, reverse=True)
    okay_polygons = [polygons[0]]
    for test_polygon in polygons:
        overlap = False
        if test_polygon in okay_polygons:
            continue
        for okay_polygon in okay_polygons:
            if poly_overlap(test_polygon, okay_polygon):
                overlap = True
                break
        if not overlap:
            okay_polygons.append(test_polygon)
    return okay_polygons

def max_length_list(alist):
    max_list = None
    for sublist in alist:
        if max_list is None or len(sublist) > len(max_list):
            max_list = sublist
    return max_list

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

def prune_nodes(nodes):
    pruned_nodes = []
    for node_collection in nodes:
        assert len(node_collection) > 2
        pruned_collection = node_collection[:2]
        for node in node_collection[2:]:
            if (get_slope(pruned_collection[-2], pruned_collection[-1]) == get_slope(pruned_collection[-2], node) or
                get_distance(pruned_collection[-1], node)) <= 2:
                pruned_collection.pop()
            pruned_collection.append(node)
        if len(pruned_collection) > 2:
            pruned_nodes.append(pruned_collection)
    return pruned_nodes

def get_slope(node1, node2):
    try:
        return (node2.y-node1.y) / (node2.x - node1.x)
    except:
        return None

def get_distance(node1, node2):
    return((node1.x - node2.x)**2 + (node1.y - node2.y)**2)**.5

def get_midpoint(node1, node2):
    return (node1.x + (node2.x - node1.x) / 2, node1.y + (node2.y - node1.y) / 2)