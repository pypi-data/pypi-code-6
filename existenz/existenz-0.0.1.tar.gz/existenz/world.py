"""A representation of the World."""
import random
from sys import stdout

from globe import Globe


class World(object):
    """Representation of the world for denizens to live and die."""

    def __init__(self, size=10):
        self._size = size
        self._day = 0

        # create the two globes for current and future world states
        self._current_globe = Globe(self._size)
        self._future_globe = Globe(self._size)

        # seed the current world
        random.seed(1)  # todo: raul - replace this will random configuration
        for location in self.globe.locations:
            location.plant = random.randint(0, 1)

        self.dump_world()

    @property
    def globe(self):
        """A representation of the current state of the world."""
        return self._current_globe

    @property
    def future_world(self):
        """A representation of the future world being constructed."""
        return self._future_globe

    @property
    def size(self):
        """The size of the world length.

        The total number of locations is equivalent to size * size.
        """
        return self._size

    def rotate(self, days=1):
        """Cycle through a given number of days in the world.

        :param days: The number of days the world should life-cycle it denizens.
        :type days: int
        """
        for cycle in range(0, days):
            self._day += 1

            self.process_plants()

            # rotate the globes after processing
            temp_globe = self._current_globe
            self._current_globe = self._future_globe
            self._future_globe = temp_globe

            self.dump_world()

    def process_plants(self):
        """Method that will life-cycle plants in the world."""
        for loc in self.globe.locations:
            future_loc = self.future_world.get_location(loc.x, loc.y)
            future_loc.plant = self.grow(loc)

    def grow(self, location):
        """Method to determine if a plant should grow in a given location.

        :param location: A candidate location for plant life.
        :type location: existenz.location.Location
        :return: A 1 is returned if the location should have a plant, else a
            0 is returned if no plant should exist on the given location.
        :rtype: int
        """
        neighbors = self.globe.get_neighbors(location.x, location.y)
        life_count = 0
        for n in neighbors:
            life_count = life_count + 1 if n.plant else life_count

        if location.plant:
            if life_count < 2 or life_count > 4:
                return 0
            else:
                return 1
        else:
            if life_count == 3:
                return 1
            else:
                return 0

    def dump_world(self):
        """Method that will dump the state of the current world to stdio."""
        stdout.write('-- day: ' + str(self._day) + '\n')
        for x in range(0, self.size):
            for y in range(0, self.size):
                index = (self.size * x) + y
                loc = self._current_globe.locations[index]
                stdout.write(str(loc))
            stdout.write('\n')
