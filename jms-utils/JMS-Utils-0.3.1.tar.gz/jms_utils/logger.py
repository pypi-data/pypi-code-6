import logging
import warnings


def log_format_string():
    warnings.warn('Use the jms_utils.logging module. This will be '
                  'removed in v0.6', DeprecationWarning)
    return logging.Formatter('[%(levelname)s] %(name)s '
                             '%(lineno)d: %(message)s')
