#!/usr/bin/env python
# -*- coding: utf-8 -*-


class TimeOutException(Exception):
    """Raised when the task is not performed in given time."""
    pass