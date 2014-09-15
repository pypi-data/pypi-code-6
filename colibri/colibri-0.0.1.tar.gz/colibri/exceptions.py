# -*- coding: utf-8 -*-
"""
colibri.exceptions
~~~~~~~~~~~~~~~~~~

This module contains colibri-specific exceptions.

"""
from __future__ import absolute_import


class ColibriException(Exception):
    """Base class for all exceptions."""


class UnexpectedFrame(ColibriException):
    """Raised when unexpected frame is received"""


class QueueEmpty(ColibriException):
    """Raised when trying to BasicGet from empty queue"""
