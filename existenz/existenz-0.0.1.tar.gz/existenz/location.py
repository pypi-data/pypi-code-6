"""A location is the representation of a given point on a glove."""
import json


class Location(object):
    """A representation of a given point on a globe."""

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._plant = 0

    @property
    def x(self):
        """The abscissa of the locations coordinate.

        :rtype: int
        """
        return self._x

    @property
    def y(self):
        """The ordinate of the location coordinate

        :rtype: int"""
        return self._y

    @property
    def coordinate(self):
        """The coordinate of a given location.

        :rtype: tuple (int, int)"""
        return self.x, self.y

    @property
    def plant(self):
        """Set 1 if there is plant life, else set to 0."""
        return self._plant

    @plant.setter
    def plant(self, plant):
        """Set if a given location has a plant."""
        self._plant = plant

    def __repr__(self):
        return json.dumps({'x': self.x, 'y': self.y, 'plant': self.plant})

    def __str__(self):
        return self.__repr__()
