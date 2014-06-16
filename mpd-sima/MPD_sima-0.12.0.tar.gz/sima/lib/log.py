# -*- coding: utf-8 -*-
# Copyright (c) 2009, 2010, 2013, 2014 Jack Kaliko <kaliko@azylum.org>
#
#  This file is part of sima
#
#  sima is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  sima is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with sima.  If not, see <http://www.gnu.org/licenses/>.
#
#

"""
Logging facility for sima.
"""

# standard library import
import logging
import sys


LOG_FORMATS = {
        logging.DEBUG: '{asctime} {filename: >11}:{lineno: <3} {levelname: <7}: {message}',
        logging.INFO:  '{asctime} {levelname: <7}: {message}',
        #logging.DEBUG: '{asctime} {filename}:{lineno}({funcName}) '
                                 #'{levelname}: {message}',
        }
DATE_FMT = "%Y-%m-%d %H:%M:%S"


class LevelFilter(logging.Filter):# Logging facility
    """
    Enable logging between two log level by filtering everything < level.
    """

    def __init__(self, filt_level):
        logging.Filter.__init__(self)
        self.level = filt_level

    def filter(self, record):
        """Defines loglevel"""
        return record.levelno <= self.level


class SimaLogger:

    def __init__(self, level='info', name='sima'):
        self.fileh = self.couth = self.cerrh = None
        user_log_level = getattr(logging, level.upper())
        if user_log_level > logging.DEBUG:
            log_format = LOG_FORMATS.get(logging.INFO)
        else:
            log_format = LOG_FORMATS.get(logging.DEBUG)
        self.logg = logging.getLogger(name)
        self.handlers = []
        self.formatter = logging.Formatter(log_format, DATE_FMT, '{')
        self.logg.setLevel(user_log_level)

    def get_logger(self):
        return self.logg

    def set_logfile(self, logfile):
        if self.logg.hasHandlers():
            return
        # create file handler
        self.fileh = logging.FileHandler(logfile)
        #fileh.setLevel(user_log_level)
        self.fileh.setFormatter(self.formatter)
        self.logg.addHandler(self.fileh)

    def set_console(self):
        if self.logg.hasHandlers():
            if self.fileh:
                self.logg.warning('Cannot leave file for console logging')
            return
        # create console handler with a specified log level (STDOUT)
        couth = logging.StreamHandler(sys.stdout)
        couth.addFilter(LevelFilter(logging.WARNING))
        # create console handler with warning log level (STDERR)
        self.cerrh = logging.StreamHandler(sys.stderr)

        #cerrh.setLevel(logging.WARNING)
        self.cerrh.setLevel(logging.ERROR)

        # add formatter to the handlers
        self.cerrh.setFormatter(self.formatter)
        self.couth.setFormatter(self.formatter)

        # add the handlers to SIMA_LOGGER
        self.logg.addHandler(self.couth)
        self.logg.addHandler(self.cerrh)


def set_logger(level='info', name='sima'):
    """
    Set the logger and log level
    logger:
        level: in debug, info, warning,…

    """
    user_log_level = getattr(logging, level.upper())
    if user_log_level > logging.DEBUG:
        log_format = LOG_FORMATS.get(logging.INFO)
    else:
        log_format = LOG_FORMATS.get(logging.DEBUG)
    logg = logging.getLogger(name)
    formatter = logging.Formatter(log_format, DATE_FMT, '{')
    logg.setLevel(user_log_level)

def set_logfile(logfile):
    # create file handler
    fileh = logging.FileHandler(logfile)
    #fileh.setLevel(user_log_level)
    fileh.setFormatter(formatter)
    if not logging.getLogger('sima').hasHandlers():
        logg.addHandler(fileh)

def set_console():
    if not logging.getLogger('sima').hasHandlers():
        # create console handler with a specified log level (STDOUT)
        couth = logging.StreamHandler(sys.stdout)
        couth.addFilter(LevelFilter(logging.WARNING))
        # create console handler with warning log level (STDERR)
        cerrh = logging.StreamHandler(sys.stderr)
    #cerrh.setLevel(logging.WARNING)
    cerrh.setLevel(logging.ERROR)

    # add formatter to the handlers
    cerrh.setFormatter(formatter)
    couth.setFormatter(formatter)

    # add the handlers to SIMA_LOGGER
    logg.addHandler(couth)
    logg.addHandler(cerrh)

# VIM MODLINE
# vim: ai ts=4 sw=4 sts=4 expandtab
