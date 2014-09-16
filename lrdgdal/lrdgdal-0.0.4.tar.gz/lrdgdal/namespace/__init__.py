#!/usr/bin/env python
# coding:utf-8

"""lrdgdal namespace package"""

__author__ = "Thomas Scharrenbach (thomas@scharrenbach.net)"
__copyright__ = "Copyright (C) 2014 Thomas Scharrenbach"
__license__ = "Apache License v2"
__version__ = "0.0.4"

from . import GDAL

from . import GEOSPARQL

__all__ = ['GDAL', 'GEOSPARQL']