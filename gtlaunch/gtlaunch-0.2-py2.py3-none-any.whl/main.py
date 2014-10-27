#!/usr/bin/env python

import argparse
import sys

from gtlaunch import __version__
from launcher import Launcher, LauncherError


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--config', metavar='FILE', help="path to configuration file",
        default="~/gtlaunch.json",
    )
    parser.add_argument(
        '-v', '--verbose', help="verbose output",
        action='store_true',
    )
    parser.add_argument(
        '-V', '--version', action='version',
        version='%%(prog)s %s' % __version__,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-l', '--list', help="list all projects", action='store_true',
    )
    group.add_argument(
        dest='project', metavar='PROJECT', help="project label", nargs='?',
    )
    args = parser.parse_args()
    try:
        launcher = Launcher(args)
        launcher.run()
    except LauncherError as e:
        print("Launcher error: {}".format(e))
        sys.exit(1)


if __name__ == "__main__":
    run()
