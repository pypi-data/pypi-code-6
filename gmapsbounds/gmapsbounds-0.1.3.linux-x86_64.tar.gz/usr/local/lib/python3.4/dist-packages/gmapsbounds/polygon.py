from gmapsbounds import utils

class Polygon:
    def __init__(self, nodes=None):
        if nodes is None:
            nodes = []
        self.nodes = nodes
        self.inner = None

    def contains(self, point):
        assert len(self.nodes) > 2
        crossings = 0
        i = -len(self.nodes) + 1
        for node in self.nodes:
            if utils.ray_crosses_edge(point, node, self.nodes[i]):
                crossings += 1
            i += 1
        return crossings % 2 == 1

    def get_exterior_nodes(self, poly):
        assert len(self.nodes) > 2
        exterior_nodes = []
        replace_list = []
        for node in self.nodes:
            if not poly.contains(node):
                replace_list.append(node)
            else:
                if len(replace_list) > len(exterior_nodes):
                    exterior_nodes = replace_list
                replace_list = []
        if len(replace_list) > len(exterior_nodes):
            exterior_nodes = replace_list
        return exterior_nodes