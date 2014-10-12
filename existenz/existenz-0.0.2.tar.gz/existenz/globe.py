"""A globe is used to represent a given state of the world."""
from existenz.location import Location
from existenz.util_decorator import memoize


class Globe(object):
    """A Globe is used to represent a given state of the world."""

    def __init__(self, size=5):
        self._size = size
        self._total_locations = size * size

        self._locations = []
        for x_coord in range(0, self._size):
            for y_coord in range(0, self._size):
                location = Location(x_coord, y_coord)
                self._locations.append(location)

    @property
    def locations(self):
        """A list of the locations in a given globe."""
        return self._locations

    @property
    def size(self):
        """The size of a side of the globe."""
        return self._size

    def get_location(self, x_coord, y_coord):
        """Retrieve a given location from given coordinates.

        :param x_coord: The abscissa of the coordinate.
        :type x_coord: int
        :param y_coord: The ordinate of the coordinate.
        :type y_coord: int
        :return: The location for the given coordinates.
        :rtype: existenz.location.Location
        """
        index = (x_coord * self._size) + y_coord
        x_out_of_bound = x_coord < 0 or x_coord >= self._size
        y_out_of_bound = y_coord < 0 or y_coord >= self._size
        if index > self._total_locations or x_out_of_bound or y_out_of_bound:
            raise IndexError('No coordinate (%s, %s)' % (x_coord, y_coord))
        return self._locations[index]

    @memoize
    def get_neighbors(self, x_coord, y_coord):
        """Retrieve the locations adjacent to the given coordinates.

        :param x_coord: The abscissa of the coordinates.
        :type x_coord: int
        :param y_coord: The ordinate of the coordinates.
        :type y_coord: int
        :return: A list of neighbors locations.
        :rtype: list(existenz.location.Location)
        """
        return list(self.locations[index] for index in
                    self._neighbors(x_coord, y_coord))

    def _neighbors(self, x_coord, y_coord):
        """Calculates the neighbors to a given coordinate.

        :param x_coord: The abscissa of the target coordinate.
        :type x_coord: int
        :param y_coord: The ordinate of the target coordinate.
        :type y_coord: int
        :return: list
        """
        indexes = list()
        for x_inc in [-1, 0, 1]:
            for y_inc in [-1, 0, 1]:
                if x_inc == 0 and y_inc == 0:
                    # Skip the central location.
                    continue
                x_ordinate = (x_coord + x_inc) % self.size
                y_ordiante = (y_coord + y_inc) % self.size
                index = (self.size * x_ordinate) + y_ordiante
                indexes.append(index)
        return indexes
