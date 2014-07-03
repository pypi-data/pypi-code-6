import argparse
import sys

from . import __version__
from .core import *


__all__ = ["main"]



def usage():
    print("usage: %s [-h|-l] [--help] ..." % sys.argv[0])
    print("Options and arguments:")
    print("-l     : only list duplicate files.")
    print("arg ...: paths to find duplicate files.")


def main():
    """
    Simple console version for the module.
    :return: None
    """
    parser = argparse.ArgumentParser(description="My Duplicate File Killer.")
    parser.add_argument("-l", '--list', default=False,
                       action="store_true", help='List duplicate files only.')
    parser.add_argument('--version', action='version', version='My Duplicate File Killer v%s' % __version__)
    parser.add_argument('paths', nargs='+')
    ns = parser.parse_args()
    if not ns.list:
        find_and_delete(ns.paths, output=True)
    else:
        find(ns.paths, output=True)

if __name__ == "__main__":
    main()
