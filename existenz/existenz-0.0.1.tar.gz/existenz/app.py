#!/usr/bin/env python
"""The initial execution runner of **Existenz**.

"""
import argparse

from world import World


class App(object):
    """The core application class."""

    def __init__(self, rotate=3, size=10):
        """

        :param rotate:
        :type rotate: int
        :param size:
        :type size: int
        """
        self.rotate = rotate

        # create the world
        self.world = World(size)

    def run(self):
        """Executes the configured world scenario."""
        self.world.rotate(self.rotate)


if __name__ == '__main__':
    # Get the args.
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--rotate',
                        type=int,
                        default=3,
                        help='Number of days to run.')
    parser.add_argument('-s', '--size',
                        type=int,
                        default=10,
                        help='Size of world.')
    args = parser.parse_args()

    # run the app
    app = App(rotate=args.rotate, size=args.size)
    app.run()
