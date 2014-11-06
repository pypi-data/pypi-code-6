
import logging


_logger = None


def get_logger():
    global _logger
    if _logger is None:
        _logger = logging.getLogger('twsfolders')
        return _logger
    else:
        return _logger


def log_debug(message, context=None):
    if context:
        msg = '%s - %s' % (context, message)
    else:
        msg = message

    get_logger().debug(msg)