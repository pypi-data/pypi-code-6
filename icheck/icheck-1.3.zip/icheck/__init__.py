#!/usr/bin/env python3.4
from __future__ import print_function

from butter.inotify import Inotify, IN_MODIFY
from argparse import ArgumentParser
from blessed import Terminal
from fnmatch import fnmatch
from subprocess import call
import logging
import sys
import os

__author__ = "Da_Blitz"
__email__ = "code@blitz.works"
__url__ = "http://blitz.works/icheck"
__license__ = "BSD3"
__version__ = "1.3"

log = logging.getLogger()

devnull = open(os.devnull, 'r')


def main():
    args = ArgumentParser()
    args.add_argument('-b', '--bell', default=False, action='store_true',
        help="Flash the terminal or send a bell signal when there is an issue (default: disabled)")
    args.add_argument('-m', '--message', nargs=1, metavar="CMD",
        help="Invoke a messaging command on syntax errors (default: disabled)")
    args.add_argument('-s', '--hashbang', nargs='?', const="python", metavar="STRING",
        help="Match files that contain the specified arg in the hashbang line (first line) (default: %(default)s)")
    args.add_argument('-g', '--glob', action="append",
        help="Only match files that match the supplied file glob")
    args.add_argument('-f', '--format', choices=('oneline', 'short', 'long'), default='oneline',
        help="Change how much information is displayed on error (default: %(default)s)")
    args.add_argument('-c', '--no-color', default=False, action='store_true',
        help="Disable the use of color")
    args.add_argument('-v', '--verbose', action='count', default=0,
        help="Specify one or more times to log verbosely")
    args.add_argument('dir', nargs="+",
        help="Directories or files to watch for changes")
    
    options = args.parse_args()
    
    formated_print = {'oneline': print_oneline,
                      'short': print_short,
                      'long': print_long,
                     }.get(options.format, 'oneline')

    log_level = {0: logging.ERROR,
                 1: logging.WARN,
                 2: logging.INFO,
                 3: logging.DEBUG,
                }.get(options.verbose, logging.DEBUG)
    handler = logging.StreamHandler()
    log.setLevel(log_level)
    log.addHandler(handler)
    log.debug('Logging Initalized')
    
    notify = Inotify()
    watches = {}
    for dir in options.dir:
        if not os.path.exists(dir):
            print("'{}' does not exist".format(dir), file=sys.stderr)
            sys.exit(0)
        else:
            log.info("Adding watch for: %s", dir)
            wd = notify.watch(dir, IN_MODIFY)
            watches[wd] = dir.encode()
    
    if options.no_color:
        logging.info('Disabling color')
        term = Terminal(stream=devnull)
    else:
        term = Terminal()

    for event in notify:
        dir = watches[event.wd]
        filepath = os.path.join(dir, event.filename)
        log.info("Recived event for: %s", filepath)
        

        if options.glob:
            if not any(fnmatch(filepath, match.encode()) for match in options.glob):
                log.debug("Recived event but not proceeding due to glob failure")
                continue
        
        if options.hashbang:
            try:
                with open(filepath, 'r') as f:
                    line = f.readline()
                    if options.hashbang not in line:
                        log.debug('Recived event but not proceeding due to hashbang failure')
                        continue
            except FileNotFoundError:
                # some VCS's delete and recreate the file it seems, meaning we can race
                # i fully expect to have to add more exception coverage here and elsewhere
                break
        
        try:
            err = check_file(filepath)
        except Exception as err:
            # null out the error and skip it
            logging.exception("An Unknown error occured, please consider submitting a bug report")
            err = None
        if err:
            if options.bell:
                log.debug("Ringing the bell")
                print(term.flash, end="")
            if options.message and term.is_a_tty:
                log.debug("Sending a message")
                line = err.text.strip()
                msg = "{e.filename}: line {e.lineno}, char {e.offset}: {line}".format(e=err, line=line)
                ret = call(options.message + [msg], shell=True)
                log.debug("Command returned with exit code %d: %s", ret, options.message + [msg])
            log.debug("Displaying error message")
            formated_print(err, term)


def print_oneline(err, term):
    line = err.text.rstrip()
    print("{t.green}{e.filename}{t.normal}: line {t.bold}{e.lineno}{t.normal}, char {t.bold}{e.offset}{t.normal}: {line}".format(e=err, line=line, t=term))


def print_short(err, term):
    line = err.text.rstrip()
    print("{t.green}{e.filename}{t.normal}: line {t.bold}{e.lineno}{t.normal}, char {t.bold}{e.offset}{t.normal}:".format(e=err, line=line, t=term))
    print(term.bold_red + line + term.normal)
    spacer = "-" * (err.offset - 1)
    print("{t.green}{}{t.white_bold}^{t.normal}".format(spacer, t=term))


def print_long(err, term):
    print("{t.green}{e.filename}{t.normal}: line {t.bold}{e.lineno}{t.normal}, char {t.bold}{e.offset}{t.normal}:".format(e=err, t=term))

    context = 5 # lines
    with open(err.filename, 'r') as f:
        preamble_buffer = []
        for line_num, line in enumerate(f, start=1):
            line = line.rstrip()
            preamble_buffer.append((line_num, line))
            # we add an extra line as it will contain the error line
            # as well
            preamble_buffer = preamble_buffer[-(context + 1):]
            if line_num == err.lineno:
                err_line_num = line_num
                break
        else:
            raise IOError("file appears to have truncated scince last read")
        
        postamble_buffer = []
        for offset, line in zip(range(context), f):
            line = line.rstrip()
            postamble_buffer.append((err_line_num + 1 + offset, line))

    line_num_len = max(max(preamble_buffer,  key=lambda x: len(str(x[0])))[0],
                       len(str(err.lineno)),
                       max(postamble_buffer, key=lambda x: len(str(x[0])))[0],
                      )
    line_num_len = len(str(line_num_len))

    for line_num, line in preamble_buffer[:-1]:
        print("{t.blue}{1:>{0}}{t.normal}: {t.green}{2}{t.normal}".format(line_num_len, line_num, line, t=term))
    
    # error line
    line_num, line = preamble_buffer[-1]
    print("{t.blue}{1:>{0}}{t.normal}: {t.red}{2}{t.normal}".format(line_num_len, line_num, line, t=term))
        
    spacer = "-" * (err.offset - 1)
    print("{t.blue}{1:{0}}{t.normal}  {t.green}{spacer}{t.bold_white}^{t.normal}".format(line_num_len, '', spacer=spacer, t=term))
    
    for line_num, line in postamble_buffer:
        print("{t.blue}{1:>{0}}{t.normal}: {t.bold_black}{2}{t.normal}".format(line_num_len, line_num, line, t=term))


def check_file(path):
    with open(path, 'r') as f:
        try:
            compile(f.read(), f.name, 'exec')
        except SyntaxError as err:
            syntax_error = err
        else:
            syntax_error = None

    return syntax_error

def entry_point():
    try:
        main()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    entry_point()
