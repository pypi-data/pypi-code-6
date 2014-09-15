# -*- coding: utf-8 -*-
"""
colibri.log
~~~~~~~~~~~

Logging utilities.

"""
from __future__ import absolute_import

import logging

__all__ = ['get_logger']


class NullHandler(logging.Handler):

    def emit(self, record):
        pass


def get_logger(logger):
    if isinstance(logger, str):
        logger = logging.getLogger(logger)
    if not logger.handlers:
        logger.addHandler(NullHandler())
    return logger
