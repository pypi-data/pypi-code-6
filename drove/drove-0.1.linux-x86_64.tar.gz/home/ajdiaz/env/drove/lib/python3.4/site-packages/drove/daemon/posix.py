#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""Generic linux daemon base class for python 3.x.


..note::
    Gently taken from http://www.jejik.com/files/examples/daemon3x.py
"""

import sys
import os
import signal


from . import Daemon


class PosixDaemon(Daemon):

    def __init__(self, handler, exit_handler=None):
        """Implement a daemon for posix systems using generic posix
        daemon class.

        :type handler: a callable object
        :param handler: a callable object to run in background.
        """
        self.handler = handler
        self.pid = 0

        if exit_handler:
            self.set_exit_handler(exit_handler)

        Daemon.__init__(self)

    def set_exit_handler(self, func):
        signal.signal(signal.SIGTERM, func)

    def foreground(self):
        self.handler()

    def start(self):
        self.pid = os.fork()
        if self.pid:
            # parent
            return self.pid
        else:
            # child
            sys.stdin = open(os.devnull, 'r')
            sys.stdout = open(os.devnull, 'a+')
            sys.stderr = open(os.devnull, 'a+')

            self.handler()

    def stop(self):
        if self.pid:
            os.kill(self.pid, 2)
            self.pid = 0

    def restart(self):
        self.stop()
        return self.start()
