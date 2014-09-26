# -*- coding: utf-8 -*-


class Point(object):
    def distanceX(self, other):
        if self.x >= other.x:
            return self.x - other.x
        else:
            return other.x - self.x

    def distanceY(self, other):
        if self.y >= other.y:
            return self.y - other.y
        else:
            return other.y - self.y

    def distance(self, other):
        pass

    def __init__(self):
        self.x = 0
        self.y = 0


class Bounds(object):
    def getWidth(self):
        return self.end.distanceX(self.start)

    def getHeight(self):
        return self.end.distanceY(self.start)

    def setWidth(self, width):
        self.end.x = width

    def setHeight(self, height):
        self.end.y = height

    def calcCenter(self):
        self.center.x = self.getWidth() / 2
        self.center.y = self.getHeight() / 2

    def getCenter(self):
        return self.center

    def __init__(self):
        self.start = Point()
        self.end = Point()
        self.center = Point()
