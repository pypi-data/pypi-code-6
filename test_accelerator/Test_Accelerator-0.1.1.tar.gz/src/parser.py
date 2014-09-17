from parse_tools import print_test_names
from argparse import ArgumentParser
from settings import get_component
import os

argparser = ArgumentParser()

argparser.add_argument("--framework", dest="framework", required=True,
                    help="Which framework to parse.")


argparser.add_argument("--files", "-f", action="store", dest="files", default=os.getcwd(),
                    help="A directory or comma separated list of files to search")

argparser.add_argument("--pattern", "-p", action="store", dest="pattern",
                    help="glob pattern for files to search", default='*')

argparser.add_argument("--recursive", "-r", action="store_true", dest="recursive",
                        help="Whether to recursively search directory", default=False)

argparser.add_argument("--agent", "-a", action="store", required=True, dest="agents", type=int,
                    help="How many agents are you using")




def testfile_parse(arguments):
    """
    Using the argparse arguments calls print_test_names
    :param arguments: argparse arguments
    :return: None
    """
    framework = arguments.framework
    nodes = get_component(framework, 'nodes')
    strip = get_component(framework,'strip')
    print_test_names(arguments.agents, arguments.files, arguments.recursive, arguments.pattern, nodes, strip)


def main():
    arguments = argparser.parse_args()
    testfile_parse(arguments)

if __name__ == '__main__':
    main()
