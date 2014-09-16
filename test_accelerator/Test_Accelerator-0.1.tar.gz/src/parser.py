from parse_tools import print_test_names
from argparse import ArgumentParser
from settings import get_nodes, get_strip
import os

parser = ArgumentParser()

parser.add_argument("--framework", dest="framework", required=True,
                    help="Which framework to parse.")


parser.add_argument("--files", "-f", action="store", dest="files", default=os.getcwd(),
                    help="A directory or comma separated list of files to search")

parser.add_argument("--pattern", "-p", action="store", dest="pattern",
                    help="glob pattern for files to search", default='*')

parser.add_argument("--recursive", "-r", action="store_true", dest="recursive",
                        help="Whether to recursively search directory", default=False)

parser.add_argument("--agent", "-a", action="store", required=True, dest="agents", type=int,
                    help="How many agents are you using")




def testfile_parse(arguments):
    """
    Using the argparse arguments calls print_test_names
    :param arguments: argparse arguments
    :return: None
    """
    nodes = get_nodes(arguments)
    strip = get_strip(arguments)
    print_test_names(arguments.agents, arguments.files, arguments.recursive, arguments.pattern, nodes, strip)


def main():
    arguments = parser.parse_args()
    testfile_parse(arguments)

if __name__ == '__main__':
    main()
