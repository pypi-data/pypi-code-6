#!/usr/bin/env python
# coding:utf-8
"""lrdgdal RasterGraph class"""

__author__ = "Thomas Scharrenbach (thomas@scharrenbach.net)"
__copyright__ = "Copyright (C) 2014 Thomas Scharrenbach"
__license__ = "Apache License v2"
__version__ = "0.0.3"

from rdflib import Graph, Dataset

from .. import gdalrdf

from .Raster import Raster


class RasterRDFDataset(Dataset):
    """An RDF dataset that holds multiple graphs storing meta-data and pixel-data."""

    def __init__(self, store='default'):
        """Stores RDF graphs along with raster data.

        :store see rdflib documentation

        Sets default_union to False, since it is not desirable to have pixel values accessable from the default graph.
        """
        super(RasterRDFDataset, self).__init__(store=store, default_union=False)

        self.__raster_map = dict()
        self.__band_map = dict()

        d = Dataset()
        d.add_graph(Graph())

        try:
            g = Graph()
            self.add_graph(g)
        except:
            import sys
            sys.exit(0)

    def add_raster(self, raster):
        """Adds a lrdgdal.Raster.

        If the raster was already added to this dataset, an Exception will be raised.

        :param raster: the lrdgdal.Raster to add.
        """
        if not raster.iri in self.__raster_map:
            for t in gdalrdf.create_triples_for_raster(raster=raster):
                self.add(t)

            for band_iri, band in raster.bands.items():
                self.add_graph(band)
                for t in gdalrdf.create_triples_for_band(band=band, raster=raster):
                    self.add(t)
            self.__raster_map[raster.iri] = raster

        else:
            raise Exception('Raster <{}> already in raster graph!'.format(raster.iri))

    def parse(self, source=None, publicID=None, format='gdal', location=None, file=None, data=None, **args):
        """Read a raster or a regular RDF graph from a file, an IRI or an input stream and add it to the dataset.

        If the format does not match 'gdal', then parsing is delegated to the super class.

        The order in which the parameters are evaluated is:

        * source
        * file
        * location
        * data

        If all of the above are None, then an exception will be raised.

        If any of the above is not None, then the respective creation method will be tried. In case creation raises
        an Exception, this Exception will be forwarded.

        :param source: stream from which to load gdal dataset or RDF graph.
        :param publicID: IRI under which the loaded graph shall be available.
        :param format: use 'gdal' for gdal datasets; for other see the rdflib documentation.
        :param location: IRI from which to load gdal dataset or RDF graph.
        :param file: file from which to load gdal dataset or RDF graph.
        :param data: data from which to load gdal dataset or RDF graph.
        :param args: optional args for loading RDF graphs.
        :return: the parsed graph.
        """
        if format != 'gdal':
            super(RasterRDFDataset, self).parse(
                source=source, publicID=publicID, format=format, location=location, data=data, args=args)
        else:
            if publicID is None:
                raise Exception('Raster must have an IRI!')

            if source is not None:
                try:
                    self.add_raster(
                        Raster(dataset=gdalrdf.create_raster_from_stream(stream=source), raster_iri=publicID))
                except Exception as e:
                    raise e

            elif file is not None:
                try:
                    self.add_raster(Raster(dataset=gdalrdf.create_raster_from_file(filename=file), raster_iri=publicID))
                except Exception as e:
                    raise e

            elif location is not None:
                try:
                    self.add_raster(Raster(dataset=gdalrdf.create_raster_from_iri(iri=location), raster_iri=publicID))
                except Exception as e:
                    raise e

            elif data is not None:
                try:
                    self.add_raster(Raster(dataset=gdalrdf.create_raster_from_data(data=data), raster_iri=publicID))
                except Exception as e:
                    raise e

            else:
                raise Exception('Neither file, nor IRI nor input stream defined! Cannot create raster!')

    def get_raster_map(self):
        return self.__raster_map

    def get_band_map(self):
        return self.__band_map

    def get_raster(self, raster_iri):
        return self.__raster_map[raster_iri]

    def get_band(self, band_iri):
        return self.__band_map[band_iri]