import math


class Color:
    r = 0
    g = 0
    b = 0
    a = 0

    def __init__(self, r, g, b, a=255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def normalize(self):
        self.r = math.ceil(self.r)
        self.g = math.ceil(self.g)
        self.b = math.ceil(self.b)
        self.a = math.ceil(self.a)

    @property
    def to_tuple(self):
        r = (self.r, self.g, self.b, self.a,)
        return r

    def __repr__(self):
        return '<%s: %d, %d, %d, %d>' % (self.__class__.__name__, self.r, self.g, self.b, self.a)

    def __str__(self):
        return '<%d, %d, %d, %d>' % (self.r, self.g, self.b, self.a)