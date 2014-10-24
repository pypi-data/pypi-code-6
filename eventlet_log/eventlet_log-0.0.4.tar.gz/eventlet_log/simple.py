# -*- coding: utf-8 -*-

import eventlet
from eventlet.green import thread, threading

import logging
# from OpenStack Swift
logging.thread = eventlet.green.thread
logging.threading = eventlet.green.threading
logging._lock = logging.threading.RLock()


def create_generic_logger(name, handler, format, level):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler.setLevel(level)
    formatter = logging.Formatter(format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    log = logger.info
    log_exc = logger.exception

    return (log, log_exc, logger)


def create_logger(name, format='%(message)s', level=logging.DEBUG):
    '''
    Create eventlet compatible logger with given *name*, *format* and
    *level*.
    If format is not given, logger will print only message.
    Default log level -- DEBUG.
    Returns (log, log_exc, logger), where:
      log is wrapper around *logger.info*
      log_exc is wrapper around *logger.excption*
      logger -- is logger itself
    '''
    return create_generic_logger(name, logging.StreamHandler(),
                                 format, level)


__KEEP_FILEHANDLERS = False

def switch_keeping_filehandlers(boolval):
    global __KEEP_FILEHANDLERS
    __KEEP_FILEHANDLERS = bool(boolval)

__filehandlers = {}

def create_file_logger(name, filename,
                       format='%(message)s', level=logging.DEBUG):
    handler = logging.FileHandler(filename)
    if __KEEP_FILEHANDLERS:
        __filehandlers[(name, filename)] = handler
    return create_generic_logger(name, handler,
                                 format, level)

def stop_file_logger(name, filename):
    if (name, filename) in __filehandlers:
        logger = logging.getLogger(name)
        handler = __filehandlers[(name, filename)]
        handler.close()
        logger.removeHandler(handler)
        del __filehandlers[(name, filename)]
    else:
        raise Exception('No such handler registered: %s , %s' \
                         % (name, filename))
