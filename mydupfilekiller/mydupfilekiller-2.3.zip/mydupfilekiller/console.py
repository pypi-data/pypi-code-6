__all__ = ["main"]
from optparse import OptionParser
import sys

from mydupfilekiller.core import *
from mydupfilekiller import __version__


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
    parser = OptionParser(version=__version__)
    parser.add_option("-l", '--list',
                       action="store_true", dest="list",
                       default=False, help='List duplicate files only.')
    opts, args = parser.parse_args()
    if len(args) == 0:
        print("Please specify at least one path.")
        sys.exit()
    if not opts.list:
        find_and_delete(args, output=True)
    else:
        find(args, output=True)

if __name__ == "__main__":
    main()
