__all__ = ["main"]
import sys
import getopt
from mydupfilekiller.core import *


def usage():
    print("usage: %s [-h|-l] [--help] ..." % sys.argv[0])
    print("Options and arguments:")
    print("-l     : only list duplicate files.")
    print("arg ...: paths to find duplicate files.")


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "lh", ["help"])
        delete = True
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage()
                sys.exit()
            elif opt == "-l":
                delete = False
            else:
                assert False, "Unrecognized option"
        if len(args) == 0:
            print("Please specify at least one path.")
            sys.exit()
        if delete:
            find_and_delete(args, output=True)
        else:
            find(args, output=True)

    except getopt.GetoptError:
        usage()
