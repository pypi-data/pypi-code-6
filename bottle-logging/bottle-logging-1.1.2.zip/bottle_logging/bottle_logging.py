# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'
import logging


class LoggingPlugin(object):
    """
    Allows to write log for bottle applications
    """
    name = 'logging_plugin'
    api = 2

    def __init__(self):
        #todo: add stream and format parameters
        self.app = None
        self.logger = None

    def setup(self, app):
        self.app = app
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(module)s:%(asctime)s:[%(levelname)s] %(message)s')
        formatter.datefmt = '%d/%m/%y %H:%M'
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.logger = logger
        self.app.log = self.log

    def log(self, msg, level=None):
        import traceback
        #d = traceback.print_stack(limit=2)
        #traceback.print_last()
        levels = {
            'critical': 50,
            'error': 40,
            'warning': 30,
            'info': 20,
            'debug': 10,
        }
        cur_level = levels.get(level, 40)
        self.logger.log(cur_level, msg)

    def apply(self, callback, route):
        return callback
