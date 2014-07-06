# -*- coding: utf-8 -*-

import logging

import pbr.version


__version__ = pbr.version.VersionInfo(
    'splitter').version_string()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('splitter')
logger.addHandler(logging.NullHandler())
