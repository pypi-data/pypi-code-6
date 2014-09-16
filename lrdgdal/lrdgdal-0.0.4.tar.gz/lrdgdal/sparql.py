#!/usr/bin/env python
# coding:utf-8

"""lrdgdal sparql module"""

from lrdgdal.classes import RasterRDFDataset

__author__ = "Thomas Scharrenbach (thomas@scharrenbach.net)"
__copyright__ = "Copyright (C) 2014 Thomas Scharrenbach"
__license__ = "Apache License v2"
__version__ = "0.0.4"

import logging

from rdflib import BNode, Variable, Literal

from .namespace import GDAL

from . import BandRDFGraph, gdalrdf, ogcutils


def lrdgal_bgp_band_value(ctx, part):
    """Evaluate raster graph for pixel value of a band.

    :param ctx: input solution mappings and the graph
    :param part: the basic graph pattern
    :return: a set of solution mappings
    """
    if part.name == 'BGP':
        logging.debug('Evaluating BGP for "lrdgal_bgp_band_value"')
        if type(ctx.graph) is BandRDFGraph:
            logging.debug('Found graph of type "BandRDFGraph"')
            g = ctx.graph
            point = None
            spatial_ref_point = None

            non_gdal_triples = []
            band_iris = []

            # Iterator through the triple pattern and check whether it
            # contains all information necessary to perform a pixel lookup.
            for t in part.triples:
                if t[1] == GDAL.band_value:
                    band_value_var = t[2]
                    if type(t[0]) is Variable:
                        band_iris = [g.iri]
                    else:
                        band_iris.append(t[0])

                elif t[1] == GDAL.pixel_coordinates and type(t[2]) is Literal:
                    spatial_ref_point, point = ogcutils.parse_wktliteral(t[2])

                elif t[1] == GDAL.pixel_value and type(t[2]) is Variable:
                    pixel_value_var = t[2]

                else:
                    non_gdal_triples.append(t)

            if point is not None and spatial_ref_point is not None:
                c = None
                for band_iri in band_iris:
                    band = g
                    raster = band.raster
                    c = ctx.push()
                    c[band_value_var] = BNode()
                    c[pixel_value_var] = \
                        gdalrdf.get_pixel_value(
                            dataset=raster.dataset,
                            band_no=1,
                            spatial_ref_raster=raster.spatial_ref,
                            point=[point.GetX(), point.GetY()],
                            affine_trans_inv=raster.affine_trans_inv,
                            raster_dimensions=raster.raster_dimensions,
                            spatial_ref_point=spatial_ref_point
                        )
                # Delegate to normal BGP evaluation with remaining non_gdal
                # patterns.
                # NOTE: this import cannot be done outside this method!
                from rdflib.plugins.sparql.evaluate import evalBGP
                if c is not None:
                    return evalBGP(c, non_gdal_triples)
                else:
                    return ctx.solution()

            else:
                # Skip evaluation since the BGP does not hold all required
                # information.
                raise NotImplementedError()

        else:
            # Skip evaluation since the graph does not represent a raster.
            raise NotImplementedError()

    else:
        # Skip evaluation since we only handle BGP matching.
        raise NotImplementedError()


_registry = dict()
_registry[GDAL.band_value] = lrdgal_bgp_band_value


def activate(modules='all'):
    """Activate the specified bgp extensions

    :param modules: IRIs of extensions to activate (default: all)
    :return:
    """
    from rdflib.plugins.sparql import CUSTOM_EVALS
    if modules == 'all':
        for key, value in _registry.items():
            CUSTOM_EVALS[key] = value
    else:
        for key in modules:
            if key in _registry:
                CUSTOM_EVALS[key] = _registry.get(key)
