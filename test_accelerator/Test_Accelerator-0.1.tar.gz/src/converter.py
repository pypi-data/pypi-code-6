__author__ = 'Tanner Baldus'
from settings import INSTALLED_FRAMEWORKS
from  settings import  get_framework, get_component

import argparse
import os.path

parser = argparse.ArgumentParser()
def check_negative(value):
    ivalue = int(value)
    if ivalue < 0:
         raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue

required = parser.add_argument_group("Required args")
optional = parser.add_argument_group("Optional args")

required.add_argument("--framework", dest="framework", required=True,
                    help="Which framework to parse.")

required.add_argument("--testrunner", dest="test_runner", required=True,
                    help="Path to the testrunner")

required.add_argument("--files", "-f", action="store", dest="files", required=True,
                    help="A comma separated list of files and directories to search.")

required.add_argument("--test_target", "-t", action="store", dest="test_target", required=True,
                     help='The compiled test file. e.g. tests.dll')


optional.add_argument("--pattern", "-p", action="store", dest="pattern",
                    help="glob pattern for files to search", default='*')

optional.add_argument("--recursive", "-r", action="store_true", dest="recursive",
                        help="Whether to recursively search directory", default=False)


optional.add_argument("--makefile" "-m", action="store", dest="makefile_path",
                  help="Path to write makefile to", default=os.path.join(os.getcwd(), 'Makefile'))

optional.add_argument("--agent", "-a", action="store", required=True, dest="agents", type=check_negative,
                    default=1, help="How many agents are you using")





def make_run_command(framework, suite, test_target):
    """
    Creates the command for the framework to run a subset of tests.
    :param framework: The Framework to get the command from
    :param suite: the test suite to run usually $1 in makefile
    :param test_target: path to compiled test file target. ex: tests.dll
    :return: command string
    """
    command = get_component(framework, 'command')
    return command.format(suite=suite, test_file=test_target)


def make_command_line_args(framework, file_str, recursive, glob_pattern, agents):
    """
    Creates command line arguments to be given to
    the parser in the makefile.
    :param arguments: arguments from argparse
    :return: string of command line arguments for python call in makefile
    """
    command_line = "--framework {} -f {} -p {} -a {}"
    if recursive:
        command_line += " -r"
    return command_line.format(framework, file_str, glob_pattern, agents)


def makefile_generator(arguments):
    """
    Generates a string of the filled in Makefile template.

    :param arguments: the arguments object created by argparse
    :return: a filled in Makefile template string
    """
    run_test_command = make_run_command(arguments.framework, '$1', arguments.test_target)
    cmd_line = make_command_line_args(arguments.framework, arguments.files,
                                      arguments.recursive, arguments.pattern, arguments.agents)

    entry_point = 'ecparse'
    list_cmd = '{} {}'.format(entry_point, cmd_line)
    makefile_string = get_component(arguments.framework, 'makefile')
    return makefile_string.format(testrunner=arguments.test_runner, list_cmd=list_cmd, run_cmd=run_test_command)


def main():
    arguments = parser.parse_args()
    print arguments
    makefile_string = makefile_generator(arguments)
    with open(arguments.makefile_path, 'w') as makefile:
        makefile.write(makefile_string)
    print makefile_string

if __name__ == '__main__':
    main()