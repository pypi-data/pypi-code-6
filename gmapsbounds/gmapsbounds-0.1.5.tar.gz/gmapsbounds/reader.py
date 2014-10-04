from gmapsbounds import utils
from gmapsbounds import constants
from gmapsbounds import llpx
from gmapsbounds import polygon

def get_nodes(rgb_image):
    nodes = []
    width, height = rgb_image.size
    do_not_check = set()
    menu_borders = utils.get_menu_borders(rgb_image)
    for x in range(width):
        for y in range(height):
            if ((y in range(menu_borders[0][0], menu_borders[0][1] + 1) and
                x in range (menu_borders[1][0], menu_borders[1][1] + 1)) or
                (x, y) in do_not_check):
                continue
            r, g, b = rgb_image.getpixel((x, y))
            if [r, g, b] == constants.INVALID[2]:
                exclude_surrounding_nodes(x, y, do_not_check, rgb_image)
            if valid_color(r, g, b) and no_invalid_adjacent(x, y, rgb_image):
                nodes.append(Node(x, y))
    if not nodes:
        raise RuntimeError('Could not detect a boundary around this location')
    nodes[0].visited = True
    return nodes

def prune_extra_nodes(polygons):
    pruned_polygons = []
    for poly in polygons:
        if len(poly.nodes) < constants.MINIMUM_PRUNING_SIZE:
            assert len(poly.nodes) > 2
            pruned_polygons.append(poly)
            continue
        pruned = polygon.Polygon(poly.nodes[:2])
        for node in poly.nodes[2:]:
            if (utils.get_slope(pruned.nodes[-2], pruned.nodes[-1]) == utils.get_slope(pruned.nodes[-2], node) or
                utils.get_distance(pruned.nodes[-1], node)) <= 2:
                pruned.nodes.pop()
            pruned.nodes.append(node)
        if len(pruned.nodes) > 2:
            pruned_polygons.append(pruned)
    return pruned_polygons

def exclude_surrounding_nodes(x, y, nodes_to_exclude, rgb_im, depth=5):
    for i in range(-depth, depth + 1):
        for j in range(-depth, depth + 1):
            r, g, b = rgb_im.getpixel((x+i, y+j))
            if [r, g, b] != constants.INVALID[2] or (i == 0 and j == 0):
                try:
                    nodes_to_exclude.add((x+i, y+j))
                except:
                    pass

def valid_color(r, g, b):
    if ([r, g, b] in constants.VALID or
        (r in constants.ALLOWABLE_RED and g in constants.ALLOWABLE_GREEN and
        b in constants.ALLOWABLE_BLUE and abs(g - b) < constants.MAX_BLUE_GREEN_DIFFERENCE)):
        return True
    return False

def no_invalid_adjacent(x, y, image):
    for i in range(-2, 3):
        for j in range(-2, 3):
            try:
                r, g, b = image.getpixel((x + i, y + j))
                if [r, g, b] in constants.INVALID or (r in constants.ALLOWABLE_RED and 100 > g == b):
                    return False
            except IndexError:
                return False
    return True

def get_polygons(nodes, rgb_im):
    polygons = []
    unvisited = [node for node in nodes if node.visited is False]
    while unvisited:
        poly = polygon.Polygon()
        current = unvisited[0]
        current.visited = True
        closest, distance = get_closest_unvisited_node(current, nodes, rgb_im)
        if distance is not None and distance > constants.MAX_NODE_DIFFERENCE:
            unvisited = unvisited[1:]
            continue
        while closest is not None:
            poly.nodes.append(current)
            current = closest
            current.visited = True
            closest, distance = get_closest_unvisited_node(current, nodes, rgb_im)
            if closest is None:
                break
            i = -1
            while distance > constants.MAX_NODE_DIFFERENCE:
                if (current is poly.nodes[0] or i < -constants.MAX_NODE_BACKTRACK
                    or (utils.get_distance(poly.nodes[0], current) < constants.MAX_NODE_DIFFERENCE and
                    len(poly.nodes) >= len(nodes) / 2)):
                    closest = None
                    break
                current = poly.nodes[i]
                closest, distance = get_closest_unvisited_node(current, unvisited, rgb_im)
                i -= 1
        if len(poly.nodes) > 2:
            polygons.append(poly)
        unvisited = [node for node in nodes if node.visited is False]
    return polygons

def prune_overlapping_nodes(polygons):
    assert polygons
    polygons = utils.sort_by_polygon_length(polygons)
    polygons.reverse()
    exterior_polygons = [polygons[0]]
    for test_polygon in polygons[1:]:
        starting_count = len(test_polygon.nodes)
        for exterior_polygon in exterior_polygons:
            exterior_nodes = test_polygon.get_exterior_nodes(exterior_polygon)
            if not exterior_nodes:
                if len(test_polygon.nodes) == starting_count:
                    exterior_polygon.inner = test_polygon
            elif (exterior_polygon is exterior_polygons[-1] and
                len(exterior_nodes) > 2 and
                utils.get_distance(exterior_nodes[0], exterior_nodes[-1]) <=
                constants.MAX_NODE_DIFFERENCE):
                test_polygon.nodes = exterior_nodes
                exterior_polygons.append(test_polygon)
                break
    return exterior_polygons

def get_closest_unvisited_node(current, nodes, rgb_im):
    closest_node = None
    shortest_distance = None
    pos = nodes.index(current)
    i = 1
    go_up = True
    go_down = True
    while (0 <= pos - i or len(nodes) > pos + i) and (go_up or go_down):
        for sign in [-1, 1]:
            if sign == -1 and not go_down or sign == 1 and not go_up:
                continue
            index = pos + i*sign
            if not 0 <= index < len(nodes):
                continue
            node = nodes[index]
            if closest_node is not None:
                if sign == -1 and shortest_distance < current.x - node.x:
                    go_down = False
                elif sign == 1 and shortest_distance < node.x - current.x:
                    go_up = False
            if node.visited:
                continue
            distance = utils.get_distance(nodes[pos], node)
            distance *= utils.get_water_multiplier(current, node, rgb_im)
            if shortest_distance is None or distance < shortest_distance:
                closest_node = node
                shortest_distance = distance
        i += 1
    return closest_node, shortest_distance

def add_skipped_nodes(x, y, do_not_check):
    do_not_check.add((x+1, y-1))
    do_not_check.add((x+1, y))
    do_not_check.add((x+1, y+1))
    do_not_check.add((x, y+1))

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.location = None
        self.visited = False

    def get_lat_lng(self):
        return llpx.pixels_to_lat_lng(self.location.offset[0] - self.location.pixcenter[0] + self.x,
            self.location.offset[1] - self.location.pixcenter[1] + self.y, self.location.zoom)

    def __str__(self):
        return '<Node at {}, {}>'.format(self.x, self.y)

    def __repr__(self):
        return self.__str__()