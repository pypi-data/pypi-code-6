#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .ini import IniProviderBackend
import os


def get_provider(path):
    file_name, file_ext = os.path.splitext(path)
    return {
        '.ini': IniProviderBackend
    }.get(file_ext.lower())(path)

# vim: filetype=python
