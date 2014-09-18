#!/usr/bin/env python
# coding:utf-8

"""lrdgdal sparql module"""

from lrdgdal.classes import RasterRDFDataset

__author__ = "Thomas Scharrenbach (thomas@scharrenbach.net)"
__copyright__ = "Copyright (C) 2014 Thomas Scharrenbach"
__license__ = "Apache License v2"
__version__ = "0.0.6"

import logging

import binascii

from rdflib import BNode, Variable, Literal, URIRef

from rdflib.namespace import XSD

from lrdgdal.namespace import GDAL

from lrdgdal import BandRDFGraph, gdalrdf, gdalutils, ogcutils


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
            # Skip evaluation since the graph does not represent a raster band.
            raise NotImplementedError()

    else:
        # Skip evaluation since we only handle BGP matching.
        raise NotImplementedError()


def lrdgal_bgp_clip(ctx, part):
    """Clip a raster with a polygon geometry.

    :param ctx: input solution mappings and the graph
    :param part: the basic graph pattern
    :return: a set of solution mappings
    """
    if part.name == 'BGP':
        logging.debug('Evaluating BGP for "lrdgal_bgp_clip"')

        if type(ctx.graph) is BandRDFGraph:
            logging.debug('Found graph of type "BandRDFGraph"')
            band = ctx.graph
            value_mask_geometry = None
            non_gdal_triples = list()

            we_are_responsible = True
            var_band = None
            value_clip_value = None
            value_clip = None
            var_clip = None
            value_mask_geometry = None

            seen_clip_value = False
            seen_clip = False
            seen_mask_geometry = False

            # The BGP must have the following structure:
            #
            # (?VAR_X or IRI_X) lrdgdal:clipValue (?VAR_Y or IRI_Y or BNODE_Y) .
            # (?VAR_Y or IRI_Y or BNODE_Y) lrdgdal:clip (?VAR_Z or IRI_Z or BNODE_Z) .
            # (?VAR_Y or IRI_Y or BNODE_Y) lrdgdal:maskGeometry WKT_LITERAL .
            #
            for t in part.triples:
                if t[1] == GDAL.clip_value:
                    if seen_clip_value:
                        raise RuntimeError(
                            'Not more than one property with IRI "{}" allowed!'.format(GDAL.clip))
                    seen_clip_value = True
                    if type(t[0]) is Variable:
                        if ctx[t[0]] is not None:
                            if ctx[t[0]] != URIRef(band.iri):
                                we_are_responsible = False
                        else:
                            var_band = t[0]

                    # Check join condition
                    if value_clip_value is None:
                        # Save for checking join condition
                        value_clip_value = t[2]
                    else:
                        # if join condition not fulfilled, we are not responsible
                        if value_clip_value != t[2]:
                            we_are_responsible = False
                            logging.warning('No join for bgp possible, no results!')

                elif t[1] == GDAL.clip:
                    if seen_clip:
                        raise RuntimeError(
                            'Not more than one property with IRI "{}" allowed!'.format(GDAL.clip_value))
                    seen_clip = True

                    if type(t[2]) is Variable:
                        var_clip = t[2]
                    elif type(t[2]) is Literal:
                        value_clip = t[2]
                    else:
                        we_are_responsible = False
                        logging.warning('Clip must be variable or Literal, no results!')

                    # Check join condition
                    if value_clip_value is None:
                        # Save for checking join condition
                        value_clip_value = t[0]
                    else:
                        # if join condition not fulfilled, we are not responsible
                        if value_clip_value != t[0]:
                            we_are_responsible = False
                            logging.warning('No join for bgp possible, no results!')

                elif t[1] == GDAL.mask_geometry:
                    if seen_mask_geometry:
                        raise RuntimeError(
                            'Not more than one property with IRI "{}" allowed!'.format(GDAL.mask_geometry))
                    seen_mask_geometry = True

                    # Check join condition
                    if value_clip_value is None:
                        # Save for checking join condition
                        value_clip_value = t[0]
                    else:
                        # if join condition not fulfilled, we are not responsible
                        if value_clip_value != t[0]:
                            we_are_responsible = False
                            logging.warning('No join for bgp possible, no results!')

                    if type(t[2]) is Literal:
                        srs, value_mask_geometry = ogcutils.parse_wktliteral(t[2])
                        pass
                    else:
                        we_are_responsible = False
                        logging.warning('Mask geometry must be WKTLiteral, no results!')

                # Triples not handled by this BGP!
                else:
                    non_gdal_triples.append(t)

            if we_are_responsible and seen_clip_value and seen_clip and seen_mask_geometry:
                clip_data = gdalutils.clip_dataset(
                    dataset=band.raster.dataset , mask_geometry=value_mask_geometry,
                    bands=[band.band.GetBand()], nodata_value=-1, fill_value=0)
                bin_values = gdalrdf.geotiff2base64(dataset=clip_data)
                value_clip = Literal(binascii.hexlify(bin_values), datatype=XSD.hexBinary)
                if var_band is not None:
                    c = ctx.push()
                    c[var_band] = URIRef(band.iri)
                else:
                    c  = ctx
                if var_clip is not None:
                    c[var_clip] = value_clip
                if type(value_clip_value) is Variable:
                    c[value_clip_value] = BNode()
                from rdflib.plugins.sparql.evaluate import evalBGP
                return evalBGP(c, non_gdal_triples)

            else:
                logging.warning('No join for bgp possible, no results!')
                # Skip evaluation since the bgp is not eligible.
                raise NotImplementedError()

        else:
            # Skip evaluation since the graph does not represent a raster band.
            raise NotImplementedError()

    else:
        # Skip evaluation since we only handle BGP matching.
        raise NotImplementedError()


# Create a registry for the bgp extensions defines in this module.
_registry = dict()
_registry[GDAL.band_value] = lrdgal_bgp_band_value
_registry[GDAL.clip] = lrdgal_bgp_clip


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
