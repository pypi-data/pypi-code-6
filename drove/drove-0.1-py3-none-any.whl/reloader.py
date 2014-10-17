#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
"""

from .timer import Timer
from .log import getLogger


class Reloader(object):
    def __init__(self, elements, interval=20):
        self.elements = elements
        self.interval = interval
        self.log = getLogger()

    def reload(self):
        for element in self.elements:
            fun = getattr(element, "reload", None)
            if fun and hasattr(fun, "__call__"):  # poor man iscallable
                self.log.debug("Reloading object: %s" %
                               (element.__class__.__name__,))
                fun()

    def start(self):
        Timer(self.interval, self.reload).run()
