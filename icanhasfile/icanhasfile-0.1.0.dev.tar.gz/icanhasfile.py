#!/usr/bin/env python

"""
NAME:
     icanhasfile -- COMPUTR, U HAS FILE. I CAN HAS IT?

USAGE:
     icanhasfile [options] <path> <filepattern>
     icanhasfile --help
     icanhasfile --version

DESCRIPTION:
     icanhasfile helps you locate and operate on files using command-line
     glob searches.

OPTIONS:
     --help, -h, -?
         Show this screen.

     --version
         Show the version.

     --command <command>, -c <command>
         Command to use on the file.
         Defaults to $ICANHASFILE_COMMAND, $EDITOR, or 'cat' (in order
         of precedence)

     --ignore-case, -i
         Perform case-insensitive matching. Defaults to case-sensitive.

     --exclude-dirs <exclude_dirs>
         Directory names to ignore in file searches.
         Defaults to $ICANHASFILE_EXCLUDE_DIRS.

EXAMPLES
      icanhasfile . '*.py'
         Open a file with a '.py' suffix under current directory

      icanhasfile --command cat ~/checkout/projects/service 'pom.xml'
         cat a file named 'pom.xml' in ~/checkout/projects/service

"""
import fnmatch
import os
import re
import subprocess
import sys

import docopt


__version__ = '0.1.0.dev'


def process(base_path, filepattern, command, ignore_case, exclude_dirs):
    """Execute the search and has the file."""
    matches = get_matches(base_path, filepattern, ignore_case, exclude_dirs)
    if len(matches) == 0:
        print('No match')
    elif len(matches) == 1:
        has_the_file(command, matches[0])
    else:
        print('Multiple matches')
        for (index, match) in enumerate(matches):
            match_string = os.path.relpath(match, base_path)
            print('[%d] %s' % (index, match_string))
        index = get_match_index(len(matches))
        has_the_file(command, matches[index])


def get_matches(base_path, filepattern, ignore_case, exclude_dirs):
    """Return a list of file Strings that match the criteria."""
    matches = []
    for (path, dirs, files) in os.walk(base_path):
        for dir in dirs:
            if dir in exclude_dirs:
                dirs.remove(dir)
        for file in files:
            if is_match(file, filepattern, ignore_case):
                matches.append(os.path.join(path, file))
    return matches


def is_match(file, filepattern, ignore_case):
    """Return True if the file is a match; False otherwise."""
    pattern_string = fnmatch.translate(filepattern)
    if ignore_case:
        pattern = re.compile(pattern_string, re.IGNORECASE)
    else:
        pattern = re.compile(pattern_string)
    return pattern.match(file)


def get_match_index(num_matches):
    """Return the zero-based match index from the user input."""
    error_message = 'Entry must be an int between 0 and %d' % (num_matches-1)
    while True:
        input = raw_input('Choose a number (q to quit): ').strip()
        if input == 'q':
            print('KTHXBYE.')
            sys.exit(0)
        try:
            index = int(input)
            if 0 <= index < num_matches:
                return index
            else:
                print(error_message)
        except ValueError:
            print(error_message)


def has_the_file(command, file):
    """Run the command on the file, waiting for command to complete."""
    subprocess.call([command, file])


def get_value(option_value, environment_vars=None, default=None):
    """Return a String value for a given option.

    The order of precedence is: the option value, an environment value,
    a default String.

    """
    if option_value is not None:
        return option_value
    if environment_vars:
        for environment_var in environment_vars:
            if os.getenv(environment_var):
                return os.getenv(environment_var)
    return default


def get_value_list(option_value, environment_vars=None, default=None):
    """Return a list of Strings for a given option.

    The order of precedence is: the option value, an environment value,
    a default List. The String value is assumed to be comma-delimited.

    """
    option = get_value(option_value, environment_vars, default)
    if option:
        return option.split(',')
    return default


def main():
    """Parse the arguments and execute the main flow."""
    args = docopt.docopt(__doc__, version='icanhasfile ' + __version__)
    process(
        args['<path>'],
        args['<filepattern>'],
        get_value(
            args['--command'], ['ICANHASFILE_COMMAND', 'EDITOR'], 'cat'),
        get_value(
            args['--ignore-case']),
        get_value_list(
            args['--exclude-dirs'], ['ICANHASFILE_EXCLUDE_DIRS'], [])
    )


if __name__ == '__main__':
    main()
