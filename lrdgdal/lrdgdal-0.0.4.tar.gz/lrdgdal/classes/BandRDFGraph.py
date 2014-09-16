#!/usr/bin/env python
# coding:utf-8

"""lrdgdal Band class"""

__author__ = "Thomas Scharrenbach (thomas@scharrenbach.net)"
__copyright__ = "Copyright (C) 2014 Thomas Scharrenbach"
__license__ = "Apache License v2"
__version__ = "0.0.4"

from rdflib import Graph


class BandRDFGraph(Graph):
    """Holds a gdal band.

    This class is essentially a wrapper for a gdal band object with
    extended utility functions.
    """

    def __init__(self, band, raster, iri):
        """Create a new band holding a reference to a band.

        :param band: the actual gdal band object.
        :param iri: the iri under which this band is referenced.
        """
        super(BandRDFGraph, self).__init__(identifier=iri)
        self.__raster = raster
        self.__band = band
        self.__iri = iri

    @property
    def iri(self):
        """The band's IRI relative to it's raster's IRI."""
        return self.__iri

    @property
    def band(self):
        """The gdal band object."""
        return self.__band

    @property
    def raster(self):
        """The lrdgdal.Raster object this band belongs to."""
        return self.__raster