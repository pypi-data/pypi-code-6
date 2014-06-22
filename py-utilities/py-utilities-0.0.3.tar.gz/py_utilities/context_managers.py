#!/usr/bin/env python
# -*- coding: utf-8 -*-

from contextlib import contextmanager
import os


@contextmanager
def cd(path=None):
    prev_cwd = os.getcwd()
    if path is not None:
        os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)

# vim: filetype=python
