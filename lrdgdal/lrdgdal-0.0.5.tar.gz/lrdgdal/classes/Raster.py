#!/usr/bin/env python
# coding:utf-8

"""lrdgdal Raster class"""

__author__ = "Thomas Scharrenbach (thomas@scharrenbach.net)"
__copyright__ = "Copyright (C) 2014 Thomas Scharrenbach"
__license__ = "Apache License v2"
__version__ = "0.0.6"

from rdflib import URIRef

from osgeo import osr

from lrdgdal import gdalutils
from lrdgdal import gdalrdf

from lrdgdal import BandRDFGraph

import numpy

from numpy.linalg import inv


class Raster(object):
    """An object that holds various data for a gdal dataset.

    This class is essentially a wrapper for a gdal raster object with
    extended utility functions.
    """

    def __init__(self, dataset, raster_iri):
        """Initializes all values for meta-data and geo-processing.

        :param dataset: a gdal dataset.

        Stores the affine geo-transformation and its inverse for later
        processing.
        """

        self.__dataset = dataset

        self.__iri = URIRef(raster_iri)

        self.__geo_trans = self.dataset.GetGeoTransform()

        self.__affine_trans = numpy.array([
            [self.__geo_trans[1], self.__geo_trans[2], self.__geo_trans[0]],
            [self.__geo_trans[4], self.__geo_trans[5], self.__geo_trans[3]],
            [0, 0, 1]
        ])

        self.__affine_trans_inv = inv(self.__affine_trans)

        self.__spatial_ref = osr.SpatialReference(self.dataset.GetProjection())

        self.__raster_dimensions = numpy.array([
            [self.dataset.RasterXSize],
            [self.dataset.RasterYSize],
            [1]
        ])

        self.__bands = dict()

        # TODO
        #geo_trans = self.dataset.GetGeoTransform()

        for band_no in range(self.dataset.RasterCount):
            band_no += 1

            try:
                src_band = self.dataset.GetRasterBand(band_no)
            except RuntimeError:
                raise Exception('No band {} found'.format(band_no))

            self.add_band(BandRDFGraph(
                band=src_band,
                raster=self,
                iri=gdalrdf.create_band_iri(raster_iri=self.iri, band_no=band_no)))

    def __exit__(self, type, value, traceback):
        """Cleans up, in particular deletes the reference to the raster dataset.

        :param type:
        :param value:
        :param traceback:
        """
        self.__dataset = None

    def add_band(self, b):
        self.__bands[b.iri] = b

    def geopoint_to_raster_coordinates(self, point, spatial_ref_point=gdalutils.WGS84):
        """geopoint_to_raster_coordinates(point, spatial_ref_point=gdalutils.WGS84)

        Transforms a geo-referenced point to real-valued raster coordinates.

        :param point: the geo-reference point to transform
        :param spatial_ref_point: the spatial reference system of the point (default WGS84)
        :return: point transformed to raster coordinates
        """
        point_geo_coordinates = gdalutils.project_coordinates(
            point=point,
            spatial_ref_target=self.__spatial_ref,
            spatial_ref_src=spatial_ref_point)
        return gdalutils.project_geo_to_raster(
            [point_geo_coordinates],
            self.__affine_trans_inv)

    def rasterbb_to_geo(self, spatial_ref_target=None):
        """Turns the raster's bounding box into a set of geo-referenced points.

        :param spatial_ref_target: the spatial reference system of the point (default None)
        :return: a list of points (2D arrays) representing the raster's bounding box.
        """
        result = gdalutils.project_raster_to_geo(
            points=self.bbox,
            affine_trans=self.__affine_trans)

        if spatial_ref_target is not None:
            result = [
                gdalutils.project_coordinates(
                    point=c,
                    spatial_ref_src=self.__spatial_ref,
                    spatial_ref_target=spatial_ref_target)
                for c in result]

        return result

    def point_in_raster(self, point):
        """Checks whether a point (in raster coords) lies within the raster.

        Important: please make sure that you transformed the point into
        raster coordinates before applying this method!

        :param point: the point to check
        :return: True if point in raster, False else.
        """
        import logging
        logging.warning('Raster point in raster...')
        return gdalutils.point_in_raster(
            point, self.__affine_trans_inv, self.__raster_dimensions)

    @property
    def dataset(self):
        """The raster's gdal raster dataset."""
        return self.__dataset

    @property
    def spatial_ref(self):
        """The raster's gdal spatial reference."""
        return self.__spatial_ref

    @property
    def affine_trans(self):
        """The raster's gdal affine transformation matrix."""
        return self.__affine_trans

    @property
    def affine_trans_inv(self):
        """The raster's gdal inverse affine transformation matrix."""
        return self.__affine_trans_inv

    @property
    def raster_dimensions(self):
        """The raster's dimensions [x, y]."""
        return self.__raster_dimensions

    @property
    def iri(self):
        """The raster's IRI under which it is available in an lrdgdal.RasterGraph."""
        return self.__iri

    @property
    def bands(self):
        """Map of pairs <band_iri, band> of the raster's bands."""
        return self.__bands

    @property
    def bbox(self):
        """
        :return: bounding box as a list of points in raster coordinates
        """
        return [
            [1, 1],
            [1, self.dataset.RasterYSize],
            [self.dataset.RasterXSize, self.dataset.RasterYSize],
            [self.dataset.RasterXSize, 1]]