#!/usr/bin/env python
# coding:utf-8

"""lrdgadl GEOSPARQL RDF constants"""

__author__ = "Thomas Scharrenbach (thomas@scharrenbach.net)"
__copyright__ = "Copyright (C) 2014 Thomas Scharrenbach"
__license__ = "Apache License v2"
__version__ = "0.0.6"

from rdflib import URIRef

NS = 'http://www.opengis.net/geosparql#'

PREFERRED_PREFIX = 'ogc'

WKT_LITERAL = URIRef(NS + 'wktLiteral')