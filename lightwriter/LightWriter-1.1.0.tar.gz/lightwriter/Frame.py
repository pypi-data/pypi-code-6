import math
import random
import webcolors


class Frame(object):

    def __init__(self):
        self.data = []
        for i in range(10):
            self.data.append([0, 0, 0, 0])

    def set_color_by_name(self, name, node=None):
        rgb = webcolors.name_to_rgb(name)
        self.set_color_by_rgb(*rgb, node=node)

    def set_color_by_rgb(self, r, g, b, node=None):
        nodes = [node] if node is not None else range(10)
        for i in nodes:
            self.data[i] = [0, r, b, g]

    def set_brightness(self, percent, allow_zero=False, node=None):
        factor = percent / 100.0
        nodes = [node] if node is not None else range(10)
        for i in nodes:
            for j in range(1, 4):
                self.data[i][j] = int(factor * self.data[i][j])
                if not allow_zero and self.data[i][j] == 0:
                    self.data[i][j] += 1

    def gradiant(self):
        for i in range(1, 11):
            self.set_brightness(i * 10, node=i-1)

    def shift(self, n):
        self.data = self.data[-n:] + self.data[:-n]

    def random(self, node=None):
        nodes = [node] if node else range(10)
        for i in nodes:
            for j in range(1, 4):
                self.data[i][j] = random.randint(0, 254)

    def height(self, height=10):
        for i in range(10, height-1, -1):
            self.set_color_by_name('black', node=i)

    def set_node_colors_by_name(self, nodes):
        nodes = self._distribute_nodes(nodes)
        for i in range(10):
            self.set_color_by_name(nodes[i], node=i)

    def set_node_colors_by_rgb(self, nodes):
        nodes = self._distribute_nodes(nodes)
        for i in range(10):
            self.set_color_by_rgb(nodes[i][0], nodes[i][1], nodes[i][2], node=i)

    def _distribute_nodes(self, nodes):
        groups = []
        for i in range(len(nodes)):
            groups.append([])
            for j in range(int(math.floor(10.0 / len(nodes)))):
                groups[i].append(nodes[i])
        num_additional = 10 - len(groups[0]) * len(groups)
        multiplier = 1
        middle = int(math.floor(len(groups) / 2.0))
        for i in range(num_additional):
            groups[middle].append(groups[middle][0])
            middle += i * multiplier
            multiplier *= -1
        return [item for sublist in groups for item in sublist]
