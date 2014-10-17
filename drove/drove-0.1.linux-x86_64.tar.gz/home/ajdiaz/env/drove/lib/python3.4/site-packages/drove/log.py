#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

"""The log module provides a helper for logging.
"""

import sys
import logging
from logging import NullHandler
from logging import StreamHandler
from logging.handlers import SysLogHandler
from logging.handlers import RotatingFileHandler


LOG_FORMAT = "[%(asctime)s]   %(levelname)-5s   %(message)s"

logging.basicConfig(format=LOG_FORMAT,
                    level=logging.INFO,
                    stream=sys.stderr)

DEBUG = logging.DEBUG
INFO = logging.INFO
WARN = logging.WARN
ERROR = logging.ERROR
FATAL = logging.FATAL

LOGLEVELS = {
    "debug": DEBUG,
    "info": INFO,
    "warn": WARN,
    "warning": WARN,
    "error": ERROR,
    "fatal": FATAL
}


def getDefaultLogger():
    """Get a default console logger"""
    return logging.getLogger("drove.default")


class AppLogger(logging.getLoggerClass()):
    """Create a modular logger for an application. Usually you don't want
    to use this class directly, but use getLogger method instead.
    """
    def __init__(self,
                 syslog=False,
                 console=False,
                 logfile=False,
                 logfile_size=0,
                 logfile_keep=0,
                 loglevel="info"):
        super(AppLogger, self).__init__("drove", LOGLEVELS.get(loglevel,
                                                               logging.INFO))

        if syslog:
            if syslog is True:
                syslog = self.get_syslog_socket()

            handler = SysLogHandler(address=syslog)
            handler.encodePriority("daemon", "alert")
            handler.setFormatter(logging.Formatter(fmt=LOG_FORMAT))
            self.addHandler(handler)

        if logfile:
            handler = RotatingFileHandler(logfile,
                                          maxBytes=logfile_size,
                                          backupCount=logfile_keep)
            handler.setFormatter(logging.Formatter(fmt=LOG_FORMAT))
            self.addHandler(handler)

        if console:
            handler = StreamHandler(sys.stderr)
            handler.setFormatter(logging.Formatter(fmt=LOG_FORMAT))
            self.addHandler(handler)

        self.addHandler(NullHandler())

    def get_syslog_socket(self):
        platform = sys.platform
        if platform == "darwin":
            return "/var/run/syslog"
        elif platform.startswith("freebsd"):
            return "/var/run/log"
        else:
            return "/dev/log"

_logger = None


def getLogger(*args, **kwargs):
    """Singleton to get an unique log object across any
    caller class or thread."""
    global _logger
    if _logger is None:
        _logger = AppLogger(*args, **kwargs)
    return _logger
