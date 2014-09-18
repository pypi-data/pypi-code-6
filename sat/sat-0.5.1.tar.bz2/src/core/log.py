#!/usr/bin/python
# -*- coding: utf-8 -*-

# SàT: a XMPP client
# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014 Jérôme Poisson (goffi@goffi.org)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""High level logging functions"""
# XXX: this module use standard logging module when possible, but as SàT can work in different cases where logging is not the best choice (twisted, pyjamas, etc), it is necessary to have a dedicated module. Additional feature like environment variables and colors are also managed.

from sat.core.constants import Const as C
from sat.core import exceptions

backend = None
_loggers = {}
handlers = {}


class Filtered(Exception):
    pass


class Logger(object):
    """High level logging class"""
    fmt = None # format option as given by user (e.g. SAT_LOG_LOGGER)
    filter_name = None # filter to call
    post_treat = None

    def __init__(self, name):
        if isinstance(name, Logger):
            self.copy(name)
        else:
            self._name = name

    def copy(self, other):
        """Copy values from other Logger"""
        self.fmt = other.fmt
        self.Filter_name = other.fmt
        self.post_treat = other.post_treat
        self._name = other._name

    def out(self, message, level=None):
        """Actually log the message

        @param message: formatted message
        """
        print message

    def log(self, level, message):
        """Print message

        @param level: one of C.LOG_LEVELS
        @param message: message to format and print
        """
        try:
            formatted = self.format(level, message)
            if self.post_treat is None:
                self.out(formatted, level)
            else:
                self.out(self.post_treat(level, formatted), level)
        except Filtered:
            pass

    def format(self, level, message):
        """Format message according to Logger.fmt

        @param level: one of C.LOG_LEVELS
        @param message: message to format
        @return: formatted message

        @raise: Filtered when the message must not be logged
        """
        if self.fmt is None and self.filter_name is None:
            return message
        record = {'name': self._name,
                  'message': message,
                  'levelname': level,
                 }
        try:
            if not self.filter_name.dictFilter(record):
                raise Filtered
        except (AttributeError, TypeError): # XXX: TypeError is here because of a pyjamas bug which need to be fixed (TypeError is raised instead of AttributeError)
            if self.filter_name is not None:
                raise ValueError("Bad filter: filters must have a .filter method")
        try:
            return self.fmt % record
        except TypeError:
            return message
        except KeyError as e:
            if e.args[0] == 'profile':
                # XXX: %(profile)s use some magic with introspection, for debugging purpose only *DO NOT* use in production
                record['profile'] = configure_cls[backend].getProfile()
                return self.fmt % record
            else:
                raise e

    def debug(self, msg):
        self.log(C.LOG_LVL_DEBUG, msg)

    def info(self, msg):
        self.log(C.LOG_LVL_INFO, msg)

    def warning(self, msg):
        self.log(C.LOG_LVL_WARNING, msg)

    def error(self, msg):
        self.log(C.LOG_LVL_ERROR, msg)

    def critical(self, msg):
        self.log(C.LOG_LVL_CRITICAL, msg)


class FilterName(object):
    """Filter on logger name according to a regex"""

    def __init__(self, name_re):
        """Initialise name filter

        @param name_re: regular expression used to filter names (using search and not match)
        """
        assert name_re
        import re
        self.name_re = re.compile(name_re)

    def filter(self, record):
        if self.name_re.search(record.name) is not None:
            return 1
        return 0

    def dictFilter(self, dict_record):
        """Filter using a dictionary record

        @param dict_record: dictionary with at list a key "name" with logger name
        @return: True if message should be logged
        """
        class LogRecord(object):
            pass
        log_record = LogRecord()
        log_record.name = dict_record['name']
        return self.filter(log_record) == 1


class ConfigureBase(object):
    LOGGER_CLASS = Logger

    def __init__(self, level=None, fmt=None, output=None, logger=None, colors=False, force_colors=False, backend_data=None):
        """Configure a backend

        @param level: one of C.LOG_LEVELS
        @param fmt: format string, pretty much as in std logging. Accept the following keywords (maybe more depending on backend):
            - "message"
            - "levelname"
            - "name" (logger name)
        @param logger: if set, use it as a regular expression to filter on logger name.
            Use search to match expression, so ^ or $ can be necessary.
        @param colors: if True use ANSI colors to show log levels
        @param force_colors: if True ANSI colors are used even if stdout is not a tty
        """
        self.backend_data = backend_data
        self.preTreatment()
        self.configureLevel(level)
        self.configureFormat(fmt)
        self.configureOutput(output)
        self.configureLogger(logger)
        self.configureColors(colors, force_colors)
        self.postTreatment()
        self.updateCurrentLogger()

    def updateCurrentLogger(self):
        """update existing logger to the class needed for this backend"""
        if self.LOGGER_CLASS is None:
            return
        for name, logger in _loggers.items():
            _loggers[name] = self.LOGGER_CLASS(logger)

    def preTreatment(self):
        pass

    def configureLevel(self, level):
        if level is not None:
            # we deactivate methods below level
            level_idx = C.LOG_LEVELS.index(level)
            def dev_null(self, msg):
                pass
            for _level in C.LOG_LEVELS[:level_idx]:
                setattr(Logger, _level.lower(), dev_null)

    def configureFormat(self, fmt):
        if fmt is not None:
            if fmt != '%(message)s': # %(message)s is the same as None
                Logger.fmt = fmt

    def configureOutput(self, output):
        if output is not None:
            if output != C.LOG_OPT_OUTPUT_SEP + C.LOG_OPT_OUTPUT_DEFAULT:
                # TODO: manage other outputs
                raise NotImplementedError("Basic backend only manage default output yet")

    def configureLogger(self, logger):
        if logger:
            Logger.filter_name = FilterName(logger)

    def configureColors(self, colors, force_colors):
        pass

    def postTreatment(self):
        pass

    def manageOutputs(self, outputs_raw):
        """ Parse output option in a backend agnostic way, and fill handlers consequently

        @param outputs_raw: output option as enterred in environment variable or in configuration
        """
        if not outputs_raw:
            return
        outputs = outputs_raw.split(C.LOG_OPT_OUTPUT_SEP)
        global handlers
        if len(outputs) == 1:
            handlers[C.LOG_OPT_OUTPUT_FILE] = [outputs.pop()]

        for output in outputs:
            if not output:
                continue
            if output[-1] == ')':
                # we have options
                opt_begin = output.rfind('(')
                options = output[opt_begin+1:-1]
                output = output[:opt_begin]
            else:
                options = None

            if output not in (C.LOG_OPT_OUTPUT_DEFAULT, C.LOG_OPT_OUTPUT_FILE, C.LOG_OPT_OUTPUT_MEMORY):
                raise ValueError(u"Invalid output [%s]" % output)

            if output == C.LOG_OPT_OUTPUT_DEFAULT:
                # no option for defaut handler
                handlers[output] = None
            elif output == C.LOG_OPT_OUTPUT_FILE:
                if not options:
                    ValueError("%(handler)s output need a path as option" % {'handler': output})
                handlers.setdefault(output, []).append(options)
                options = None # option are parsed, we can empty them
            elif output == C.LOG_OPT_OUTPUT_MEMORY:
                # we have memory handler, option can be the len limit or None
                try:
                    limit = int(options)
                    options = None # option are parsed, we can empty them
                except (TypeError, ValueError):
                    limit = C.LOG_OPT_OUTPUT_MEMORY_LIMIT
                handlers[output] = limit

            if options: # we should not have unparsed options
                raise ValueError(u"options [%(options)s] are not supported for %(handler)s output" % {'options': options, 'handler': output})

    @staticmethod
    def memoryGet(size=None):
        """Return buffered logs

        @param size: number of logs to return
        """
        raise NotImplementedError

    @staticmethod
    def ansiColors(level, message):
        """Colorise message depending on level for terminals

        @param level: one of C.LOG_LEVELS
        @param message: formatted message to log
        @return: message with ANSI escape codes for coloration
        """
        if level == C.LOG_LVL_DEBUG:
            out = (C.ANSI_FG_CYAN, message, C.ANSI_RESET)
        elif level == C.LOG_LVL_WARNING:
            out = (C.ANSI_FG_YELLOW, message, C.ANSI_RESET)
        elif level == C.LOG_LVL_ERROR:
            out = (C.ANSI_FG_RED,
                   C.ANSI_BLINK,
                   r'/!\ ',
                   C.ANSI_BLINK_OFF,
                   message,
                   C.ANSI_RESET)
        elif level == C.LOG_LVL_CRITICAL:
            out = (C.ANSI_BOLD,
                   C.ANSI_FG_RED,
                   'Guru Meditation ',
                   C.ANSI_NORMAL_WEIGHT,
                   message,
                   C.ANSI_RESET)
        else:
            out = message
        return ''.join(out)

    @staticmethod
    def getProfile():
        """Try to find profile value using introspection"""
        raise NotImplementedError


class ConfigureCustom(ConfigureBase):
    LOGGER_CLASS = None

    def __init__(self, logger_class, *args, **kwargs):
        ConfigureCustom.LOGGER_CLASS = logger_class


configure_cls = { None: ConfigureBase,
                   C.LOG_BACKEND_CUSTOM: ConfigureCustom
                 }  # XXX: (key: backend, value: Configure subclass) must be filled when new backend are added


def configure(backend_, **options):
    """Configure logging behaviour
    @param backend: can be:
        C.LOG_BACKEND_BASIC: use a basic print based logging
        C.LOG_BACKEND_CUSTOM: use a given Logger subclass
    """
    global backend
    if backend is not None:
        raise exceptions.InternalError("Logging can only be configured once")
    backend = backend_

    try:
        configure_class = configure_cls[backend]
    except KeyError:
        raise ValueError("unknown backend [%s]" % backend)
    if backend == C.LOG_BACKEND_CUSTOM:
        logger_class = options.pop('logger_class')
        configure_class(logger_class, **options)
    else:
        configure_class(**options)

def memoryGet(size=None):
    if not C.LOG_OPT_OUTPUT_MEMORY in handlers:
        raise ValueError('memory output is not used')
    return configure_cls[backend].memoryGet(size)

def getLogger(name=C.LOG_BASE_LOGGER):
    try:
        logger_class = configure_cls[backend].LOGGER_CLASS
    except KeyError:
        raise ValueError("This method should not be called with backend [%s]" % backend)
    return _loggers.setdefault(name, logger_class(name))

_root_logger = getLogger()

def debug(msg):
    _root_logger.debug(msg)

def info(msg):
    _root_logger.info(msg)

def warning(msg):
    _root_logger.warning(msg)

def error(msg):
    _root_logger.error(msg)

def critical(msg):
    _root_logger.critical(msg)
