#!/usr/bin/env python2.7
# Copyright: This module has been placed under the public license

"""
Because you have better things to do.
"""

import inspect
import logging
import logging.config
import logging.handlers
from logging import NOTSET, INFO, DEBUG, WARNING, ERROR, CRITICAL
from simplelog.defaults import *
import os
from os.path import join

__version__ = "0.2.3"

class SimpleLog(logging.Logger):
    """
    Simplelog, because you have better things to do then worry about logging.
    """
    def __init__(self, name=SIMPLELOG_NAME, level=logging.INFO,
            path=None,  quiet=False):
        """
        @param:
        name - name of log, default is simplelog
        level - log level
        path - filepath, defaults to <cwd>/simplelog.log
        path - default is current directory, 'tmp' puts log in /tmp folder
        quiet - print message to standard out?
        @return:
        simple log logger object
        """
        super(SimpleLog, self).__init__(name, level)

        if not path:
            path = SIMPLELOG_DEFAULT_PATH

        #State
        self.path = path
        self.quiet = quiet

        #Handlers
        if not quiet:
            self.sh = logging.StreamHandler()
            self.sh.setFormatter(SIMPLE_FORMATTER)
            self.addHandler(self.sh)

        fh = logging.FileHandler(filename=path)
        fh.setFormatter(SIMPLE_FORMATTER)
        self.addHandler(fh)
        self.setLevel(level)


    def setLevel(self, level):
        """
        Set level for simplelog and its handlers

        :param level: debug level to set
        """
        super(SimpleLog, self).setLevel(level)
        for hndl in self.handlers:
            hndl.setLevel(level)

    def setFormatter(self, fmt=None, datefmt=None):
        """
        Sets format in each handler
        :params format: either a Formatter object or format string
        """
        formatter = logging.Formatter(fmt, datefmt)
        for hndl in self.handlers:
            hndl.setFormatter(formatter)

    #TODO: decide whether to keep or not
    def disable(self):
        """
        Disable simplelog by getting rid of all handlers
        """
        self.handlers = [] #could this result in a memory leak?
        assert(self.handlers == [])

    def enable(self):
        """
        Enable simplelog
        """
        self.__init__(path = self.path, quiet = self.quiet,
                    level = self.level)

    def log(self, level, msg, *args, **kwargs):
        super(SimpleLog, self).log(level, msg, *args, **kwargs)
        #self.sl_debug.log(level, msg, *args, **kwargs)

    def dump(self, var_name):
        """
        Prints the content of the string along with the string name
        @param:
        var_name - a string constant
        @return:
        none
        """
        #TODO: this doesn't work [critical, bug]
        try:
            value = locals()[var_name]
        except KeyError:
            value = globals()[var_name]
        self.log(self.level, self.var_name + ":" + str(value))

    @property
    def config():
        return self.config

### Convenience
SIMPLELOG_DEFAULT = None

def initialize():
    """ initialize default simplelog """
    global SIMPLELOG_DEFAULT
    if not SIMPLELOG_DEFAULT:
        #FIXME: don't hardcode
        SIMPLELOG_DEFAULT = SimpleLog(path="/tmp/simplelog.log", level = logging.INFO)

#TODO: support *args
def log(msg, level = None):
    """
    Log the output. Nothing more, nothing less
    """
    initialize()
    if not level: level = SIMPLELOG_DEFAULT.level
    SIMPLELOG_DEFAULT.log(level, msg)

def debug(msg):
    level = logging.DEBUG
    log(msg, level)

def info(msg):
    level = logging.INFO
    log(msg, level)

def error(msg):
    level = logging.ERROR
    log(msg, level)

def warning(msg):
    level = logging.WARNING
    log(msg, level)

def critical(msg):
    level = logging.CRITICAL
    log(msg, level)

