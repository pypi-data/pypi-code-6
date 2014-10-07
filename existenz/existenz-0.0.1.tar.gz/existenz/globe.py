"""A globe is used to represent a given state of the world."""
from location import Location
from util_decorator import memoize


class Globe(object):
    """A Globe is used to represent a given state of the world."""

    def __init__(self, size=5):
        self._size = size
        self._total_locations = size * size

        self._locations = []
        for x in range(0, self._size):
            for y in range(0, self._size):
                location = Location(x, y)
                self._locations.append(location)

    @property
    def locations(self):
        """A list of the locations in a given globe."""
        return self._locations

    @property
    def size(self):
        """The size of a side of the globe."""
        return self._size

    def get_location(self, x, y):
        """Retrieve a given location from given coordinates.

        :param x: The abscissa of the coordinate.
        :type x: int
        :param y: The ordinate of the coordinate.
        :type y: int
        :return: The location for the given coordinates.
        :rtype: existenz.location.Location
        """
        index = (x * self._size) + y
        x_out_of_bound = x < 0 or x >= self._size
        y_out_of_bound = y < 0 or y >= self._size
        if index > self._total_locations or x_out_of_bound or y_out_of_bound:
            raise IndexError('No coordinate (%s, %s)' % (x, y))
        return self._locations[index]

    @memoize
    def get_neighbors(self, x, y):
        """Retrieve the locations adjacent to the given coordinates.

        :param x: The abscissa of the coordinates.
        :type x: int
        :param y: The ordinate of the coordinates.
        :type y: int
        :return: A list of neighbors locations.
        :rtype: list(existenz.location.Location)
        """
        return list(self.locations[index] for index in self._neighbors(x, y))

    def _neighbors(self, x, y):
        indexes = list()
        for a in [-1, 0, 1]:
            for b in [-1, 0, 1]:
                if a == 0 and b == 0:
                    # Skip the central location.
                    continue
                x_ordinate = (x + a) % self.size
                y_ordiante = (y + b) % self.size
                index = (self.size * x_ordinate) + y_ordiante
                indexes.append(index)
        return indexes
