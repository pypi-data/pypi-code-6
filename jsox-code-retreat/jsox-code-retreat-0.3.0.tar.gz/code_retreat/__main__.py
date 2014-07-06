#!/usr/bin/env python

import argparse
import imp
import logging
import os
import sys
import time

from .server import get_socket, NoData, send
from .testing import run_tests


log = logging.getLogger('code-retreat')


def import_user_code(path):
    """Import user code from argument"""
    try:
        return imp.load_source('user_code', path)
    except IOError:
        sys.stderr.write('Could not find file "{}".\n'.format(path))
        sys.exit(1)


def main(path):
    """
    open socket
    watch file
    on modified
        run tests
        check socket is open
            push output to server
    """
    sock = get_socket()

    before = os.path.getmtime(path)
    while True:
        time.sleep(1)
        after = os.path.getmtime(path)
        if after > before:
            log.debug('User code modified.')

            # import user code
            user_code = import_user_code(path)

            # run tests on the code
            # passed, ran, failures = run_tests(path)
            passed = run_tests(path)

            # TODO: push results to server
            # send_tests()

            if passed:
                try:
                    send(sock, user_code)
                except NoData:
                    pass

        # reset before so we can check in the next loop
        before = after


def run():
    """
    Wrapper for the main function

    Wraps main with a keyboard interrupt catch so running the module directly
    and from the console_scripts can use the same functionality without having
    extra indentation in main.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('path', metavar='PATH')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true')
    args = parser.parse_args()

    logging.basicConfig(
        format='%(asctime)-15s %(levelname)-8s %(name)-11s %(message)s',
        level=logging.DEBUG if args.debug else logging.CRITICAL,
    )

    try:
        main(args.path)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    run()
