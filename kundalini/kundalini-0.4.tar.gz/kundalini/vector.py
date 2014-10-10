import math
from numbers import Number
from numpy import array
from collections import namedtuple

__all__ = ['Vector']

ndarray = type(array([]))


#-----------------------------------------------------------------------
class VectorMeta(type):

    def __call__(cls, values):
        if isinstance(values, (list, tuple)):
            self = type.__call__(cls, len(values), float)
            for i, v in enumerate(values):
                self[i] = v

        else:
            self = type.__call__(cls, values)

        return self


#-----------------------------------------------------------------------
class Vector(ndarray, metaclass=VectorMeta):

    @property
    def x(self):
        return self[0]


    #---------------------------------------------------------------
    @property
    def angle_xy(self):
        return self.angles[0]


    #---------------------------------------------------------------
    @property
    def y(self):
        return self[1]


    #---------------------------------------------------------------
    @property
    def angle_xz(self):
        return self.angles[1]


    #---------------------------------------------------------------
    @property
    def z(self):
        return self[2]


    #---------------------------------------------------------------
    @property
    def angle_xw(self):
        return self.angles[2]


    #---------------------------------------------------------------
    @property
    def w(self):
        return self[3]


    #---------------------------------------------------------------
    @property
    def magnitude(self) -> float:
        mag = self[0]
        for v in self[1:]:
            mag = math.sqrt(pow(mag, 2) + pow(v, 2))
        return mag


    #---------------------------------------------------------------
    @property
    def angles(self) -> tuple:
        angles = [
            math.asin(v / math.sqrt(pow(self.x, 2) + pow(v, 2)))
            for v in self[1:]
        ]
        return tuple(map(math.degrees, angles))


    #---------------------------------------------------------------
    @classmethod
    def from_angles(cls, angles:tuple, *, magnitude:float=1.) -> namedtuple:
        angles = tuple(map(math.radians, angles))
        x = math.cos(angles[0])
        y = math.sin(angles[0])
        resources = [x, y]

        for angle in angles[1:]:
            ax = math.cos(angle)
            resources.append(math.sin(angle) * x / ax)

        vector = cls(resources)
        mag = vector.magnitude
        return vector * magnitude / mag
