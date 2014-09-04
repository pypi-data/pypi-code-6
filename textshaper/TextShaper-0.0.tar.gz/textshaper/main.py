#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
package to shape text blocks
"""

import argparse
import os
import subprocess
import sys
import time
from .commands import Commands
from .indent import deindent, indent
from .onelineit import onelineit
from .tablify import make_csv
from .whitespace import underscore
from which import which

HR = '--'

def info(content):
    """gathers info about the content and returns a dict"""

    lines = content.splitlines()
    return {'lines': len(lines),
            'chars': len(content),
            'columns': max([len(line) for line in lines])}


def display(content, keys=('lines', 'chars', 'columns'), hr=HR):
    """displays the content"""
    print (content)
    if keys:
        _info = info(content)
        print (hr)
    print ('; '.join(['{}: {}'.format(key, _info[key])
                      for key in keys]))

def add_commands():
    # TODO: do this dynamically
    commands = Commands()
    commands.add(indent, 'i')
    commands.add(deindent, 'd')
    commands.add(onelineit, 'o')
    commands.add(underscore, 'u')
    commands.add(make_csv, 'c')
    return commands


def add_options(parser):
    """add options to the parser instance"""

    parser.add_argument('-f', '--file',  dest='input',
                        type=argparse.FileType('r'), default=sys.stdin,
                        help="file to read from [DEFAULT: stdin]")
    parser.add_argument('-n', '--no-strip', dest='strip',
                        action='store_false', default=True,
                        help="do not strip whitespace before processing")

    if which('xclip'): # TODO: support e.g. xsel or python native
        parser.add_argument('-c', '-o', '--clip', '--copy', dest='copy_to_clipboard',
                            action='store_true', default=False,
                            help="copy to clipboard")
        parser.add_argument('-i', dest='input_from_clipboard',
                            action='store_true', default=False,
                            help="copy from clipboard")


def main(args=sys.argv[1:]):
    """CLI"""

    # TODO: read ~/.textshaper

    # parse command line options
    parser = argparse.ArgumentParser(description=__doc__)
    add_options(parser)
    options = parser.parse_args(args)

    # read input
    if getattr(options, 'input_from_clipboard', False):
        content = subprocess.check_output(['xclip', '-o'])
    else:
        content = options.input.read()

    # get formatting commands
    commands = add_commands()

    # pre-process output
    if options.strip:
        content = content.strip()

    # main display loop
    # TODO: read input + commands
    try:
        while True:
            # print formatted content
            display(content)
            print (commands.display())
            choice = raw_input('? ')
            new_content = commands(choice, content)
            if new_content is None:
                print ("Choice '{}' not recognized".format(choice))
                continue
            content = new_content

            if options.copy_to_clipboard:
                # copy content to X clipboard
                process = subprocess.Popen(['xclip', '-i'], stdin=subprocess.PIPE)
                _, _ = process.communicate(content)
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == '__main__':
  main()

