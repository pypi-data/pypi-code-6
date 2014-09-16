#!/usr/bin/env python
# coding:utf-8
"""lrdgdal utilities for ogc and rdf

This module contains mostly utilities for transforming values between ogc and
rdf.
"""

__author__ = "Thomas Scharrenbach (thomas@scharrenbach.net)"
__copyright__ = "Copyright (C) 2014 Thomas Scharrenbach"
__license__ = "Apache License v2"
__version__ = "0.0.4"

import logging

import re

try:
    from osgeo import ogr, osr
except ImportError:
    try:
        import gdal
        import ogr
        import osr
    except Exception as e:
        logging.error('Could not load gdal package!')
        raise e

from lxml import etree

WGS84_IRI = 'http://www.opengis.net/def/crs/OGC/1.3/CRS84'
WGS84_URN = 'urn:ogc:def:crs:OGC:1.3:CRS84'
WKT_RE = r'(<.*>)[ ]+(.*)'


def parse_wktliteral(wkt_literal):
    """Parses a WKT RDF Literal value.

    WKT RDFS Literals have string values of "<IRI> WKT".
    IRI must identify a valid spatial reference system that GDAL can parse.

    :param wkt_literal: the Literal to parse.
    :return:
    """

    pattern = re.compile(WKT_RE)
    match = pattern.match(wkt_literal)
    if match is None:
        raise Exception('Not a valid WKT literal: {}'.format(wkt_literal))

    spatial_ref = osr.SpatialReference()
    spatial_ref.ImportFromWkt(osr.GetUserInputAsWKT(WGS84_IRI))

    return spatial_ref, ogr.CreateGeometryFromWkt(match.group(2))


def encode_as_wktliteral(spatial_ref, geometry):
    """Encode a geometry as an WKS RDF Literal.

    :param spatial_ref: the spatial reference system
    :param geometry:
    :return: the string value of the RDF Literal.
    """
    spatial_ref_iri = extract_iri_from_srs(spatial_ref)
    return '<{}> {}'.format(spatial_ref_iri, str(geometry))


def extract_iri_from_srs(spatial_ref):
    """Extract the IRI of a spatial reference system.

    :param spatial_ref: a spatial reference system
    :return: IRI of the spatial reference system
    """
    # Add proper namespace to GML representation of spatial reference system.
    tree = etree.fromstring(
        spatial_ref.ExportToXML().replace(
            ">",
            " xmlns:gml=\"http://www.opengis.net/gml/\""
            + " xmlns:xlink=\"http://www.w3.org/1999/xlink\""
            + " xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\">",
            1)
    )

    # Retrieve IRI via xpath query.
    result = tree.xpath(
        '/gml:GeographicCRS/gml:srsID/gml:name',
        namespaces={'gml': 'http://www.opengis.net/gml/'})
    return '{}{}'.format(
        result[0].get('{http://www.opengis.net/gml/}codeSpace'),
        result[0].text)