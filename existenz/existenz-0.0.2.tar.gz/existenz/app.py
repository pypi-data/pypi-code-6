#!/usr/bin/env python
"""The initial execution runner of **Existenz**.

"""
import sys

from cognate.component_core import ComponentCore

from existenz.world import World


class App(ComponentCore):
    """The core application class."""

    def __init__(self, rotate=3, size=10, **kwargs):
        """

        :param rotate:
        :type rotate: int
        :param size:
        :type size: int
        """
        self.rotate = rotate
        self.size = size

        self.world = None

        ComponentCore.__init__(self, **kwargs)

    def cognate_options(self, arg_parser):
        arg_parser.add_argument('-r', '--rotate',
                                type=int,
                                default=self.rotate,
                                help='Number of days to run.')
        arg_parser.add_argument('-s', '--size',
                                type=int,
                                default=self.size,
                                help='Size of world.')

    def cognate_configure(self, args):
        # create the world
        self.world = World(self.size)

    def run(self):
        """Executes the configured world scenario."""
        self.world.rotate(self.rotate)


if __name__ == '__main__':
    app = App(argv=sys.argv)  # pylint: disable=invalid-name
    app.run()
