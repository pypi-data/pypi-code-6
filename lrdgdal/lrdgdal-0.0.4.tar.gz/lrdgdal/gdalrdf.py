#!/usr/bin/env python
# coding:utf-8

"""lrdgdal gdalrdf module"""

import logging

from . import gdalutils

__author__ = "Thomas Scharrenbach (thomas@scharrenbach.net)"
__copyright__ = "Copyright (C) 2014 Thomas Scharrenbach"
__license__ = "Apache License v2"
__version__ = "0.0.4"

import tempfile

from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, XSD

import lxml.etree as etree

try:
    from urllib.request import urlretrieve
except:
    from urllib import urlretrieve

try:
    from osgeo import gdal
    from osgeo import osr
except ImportError:
    try:
        import gdal
    except Exception as e:
        logging.error('Could not load gdal package!')
        raise e


from .namespace import GDAL

_gdal2xsd = {'Byte': XSD.byte}


def gdaldatatype_to_xsd(gdal_datatype):
    """Translates gdal type names to XSD types.

    :param gdal_datatype:
    :return:
    """
    if gdal_datatype in _gdal2xsd.keys():
        return _gdal2xsd.get(gdal_datatype)
    else:
        return None


def create_raster_from_file(filename):
    """Open a gdal dataset from a file.

    :param filename: name of the raster file to open
    :return: gdal dataset
    """
    dataset = gdal.Open(filename)
    return dataset


def create_raster_from_iri(iri):
    """Open a gdal dataset from an IRI.

    :param iri: IRI to use for downloading the raster file
    :return: gdal dataset
    """
    tmp_file = tempfile.NamedTemporaryFile(delete=True)
    urlretrieve(iri, tmp_file.name)
    return create_raster_from_file(filename=tmp_file.name)


def create_raster_from_stream(stream):
    """Open a gdal dataset from input stream stream.

    :param stream: stream stream
    :return: gdal dataset

    The stream is first written to a tempfile that is deleted on exit. Then we try to open this tempfile using the gdal
    library.
    """
    tmp_file = tempfile.NamedTemporaryFile(delete=True)
    tmp_file.write(stream.read())
    return create_raster_from_file(filename=tmp_file.name)


def create_raster_from_data(data):
    """Open a gdal dataset from input data.

    :param data: input data
    :return: gdal dataset

    The data is first written to a tempfile that is deleted on exit. Then we try to open this tempfile using the gdal
    library.
    """
    tmp_file = tempfile.NamedTemporaryFile(delete=True)
    tmp_file.write(data=data)
    return create_raster_from_file(filename=tmp_file.name)


def create_triples_for_raster(raster):
    """Generate RDF triples for a raster.

    :param raster: lrdgdal.Raster
    :return: list of RDF triples
    """
    g_raster_iri = raster.iri
    g_dataset = raster.dataset
    triples = list()
    triples.append((g_raster_iri, RDF.type, GDAL.raster))

    # Add dimensions of raster
    triples.append((g_raster_iri, GDAL.rasterXSize, Literal(g_dataset.RasterXSize, datatype=XSD.integer)))
    triples.append((g_raster_iri, GDAL.rasterYSize, Literal(g_dataset.RasterYSize, datatype=XSD.integer)))

    # Add description string of raster
    triples.append((g_raster_iri, GDAL.description, Literal(g_dataset.GetDescription(), datatype=XSD.string)))

    _describe_spatial_ref(raster)

    # add gcps if any
    # TODO

    return triples


def create_band_iri(raster_iri, band_no):
    """Generic method for generating the correct IRI for a raster's band.

    :param raster_iri: iri of raster.
    :param band_no: number of the band.
    :return: IRI relative to the raster's IRI.
    """
    return URIRef('{}band{}/'.format(raster_iri, band_no))


def create_triples_for_band(band, raster):
    """Generate RDF triples for a band.

    :param band: lrdgdal.Band
    :param raster: lrdgdal.Raster
    :return: list of RDF triples
    """
    band_iri = band.iri
    raster_iri = raster.iri
    src_band = band.band

    triples = list()
    triples.append((band_iri, RDF.type, GDAL.band))
    triples.append((band_iri, GDAL.band, raster_iri))

    bs = src_band.GetBlockSize()
    triples.append((band_iri, GDAL.blockXSize, Literal(bs[0], datatype=XSD.integer)))
    triples.append((band_iri, GDAL.blockYSize, Literal(bs[1], datatype=XSD.integer)))

    category_names = src_band.GetCategoryNames()
    if category_names is not None:
        pass

    colour_interpretation = src_band.GetColorInterpretation()
    if colour_interpretation is not None:
        triples.append((band_iri, GDAL.color_interpretation, Literal(GDAL.create_gci(colour_interpretation))))

    triples.append((band_iri, GDAL.color_interpretation, Literal(GDAL.create_gdt(src_band.DataType))))

    mask_band_no = src_band.GetMaskBand().GetBand()
    if mask_band_no is not None:
        triples.append((band_iri, GDAL.mask_band, create_band_iri(raster_iri=raster.iri, band_no=mask_band_no)))

    # rat = src_band.GetDefaultRAT()
    # rat = gdal.RasterAttributeTable()

    mask_flags = src_band.GetMaskFlags()
    if mask_flags is not None:
        triples.append((band_iri, GDAL.mask_flags, Literal(mask_flags, datatype=XSD.integer)))
    src_band.GetHistogram(
        min=-0.5,
        max=255.5,
        buckets=256,
        include_out_of_range=0,
        approx_ok=1,
        callback=None,
        callback_data=None)
    src_band.HasArbitraryOverviews()
    src_band.GetCategoryNames()

    nodata_value = src_band.GetNoDataValue()
    if nodata_value is not None:
        triples.append((band_iri, GDAL.bandNoDataValue, Literal(nodata_value)))

    minimum = src_band.GetMinimum()
    if minimum is not None:
        triples.append((band_iri, GDAL.bandMin, Literal(minimum)))

    maximum = src_band.GetMaximum()
    if maximum is not None:
        triples.append((band_iri, GDAL.bandMax, Literal(maximum)))

    scale = src_band.GetScale()
    if scale is not None:
        triples.append((band_iri, GDAL.bandScale, Literal(scale)))

    unit_type = src_band.GetUnitType()
    if unit_type is not None and unit_type != '':
        triples.append((band_iri, GDAL.band_unit_type, Literal(unit_type)))

    ctable = src_band.GetColorTable()
    if ctable is None:
        logging.info('No ColorTable found')

    else:
        logging.debug("[ COLOR TABLE COUNT ] = {}".format(ctable.GetCount()))
        for i in range(0, ctable.GetCount()):
            entry = ctable.GetColorEntry(i)
            if not entry:
                continue
            logging.debug("[ COLOR ENTRY RGB ] = {}".format(ctable.GetColorEntryAsRGB(i, entry)))

    stats = src_band.GetStatistics(True, True)
    if stats is not None:
        triples.append((band_iri, GDAL.bandStatsMin, Literal(stats[0])))
        triples.append((band_iri, GDAL.bandStatsMax, Literal(stats[1])))
        triples.append((band_iri, GDAL.bandStatsMean, Literal(stats[2])))
        triples.append((band_iri, GDAL.bandStatsStdDev, Literal(stats[3])))
    return triples


def get_pixel_value(
        dataset,
        band_no,
        spatial_ref_raster,
        point,
        affine_trans_inv,
        raster_dimensions,
        spatial_ref_point=gdalutils.WGS84):
    """get_pixel_value(dataset, band_no, spatial_ref_raster, point, affine_trans_inv, raster_dimensions,
    spatial_ref_point=gdalutils.WGS84)

    Get pixel value of a point for a band of a raster.

    :param dataset: gdal raster dataset
    :param band_no: number of the dataset's band to query
    :param spatial_ref_raster: the srs of the raster dataset
    :param point: point as array
    :param affine_trans_inv: inverse matrix of affine transformation
    :param raster_dimensions: [x, y]
    :param spatial_ref_point: the srs of the point (default WGS84)
    :return: the pixel value as rdf literal
    """
    band = dataset.GetRasterBand(band_no)
    point_geo_coordinates = gdalutils.project_coordinates(
        point=point,
        spatial_ref_target=spatial_ref_raster,
        spatial_ref_src=spatial_ref_point)

    point_raster_coordinates = gdalutils.project_geo_to_raster(
        points=[point_geo_coordinates],
        affine_trans_inv=affine_trans_inv)[0]

    if gdalutils.point_in_raster(
            point=point_geo_coordinates, affine_trans_inv=affine_trans_inv,
            raster_dimensions=raster_dimensions):
        # Let's not forget to subtract one to match zero-based indices.
        raster_pixel_value = \
            band.ReadAsArray(
                int(round(point_raster_coordinates[0]-1)),
                int(round(point_raster_coordinates[1]-1)), 1, 1)

        if raster_pixel_value is not None:
            xsd_type = \
                gdaldatatype_to_xsd(gdal.GetDataTypeName(band.DataType))
            if xsd_type is None:
                xsd_type = XSD.string

            return Literal(raster_pixel_value[0][0], datatype=xsd_type)
        else:
            return None
    else:
        logging.warning('POINT NOT IN RASTER! {}'.format(point_raster_coordinates))
        return None


def _describe_spatial_ref(raster):
    triples = []
    dataset = raster.dataset
    raster_iri = raster.iri

    projection = dataset.GetProjection()
    spatial_ref = osr.SpatialReference(projection)

    dom = etree.fromstring(spatial_ref.ExportToXML().replace(
        ">", " xmlns:gml=\"http://www.opengis.net/gml/\""
             " xmlns:xlink=\"http://www.w3.org/1999/xlink\" "
             "xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\">", 1))


    logging.debug(etree.tostring(dom))

    from pkg_resources import resource_string
    xml2rdf = resource_string(__name__, 'xml2rdf.xsl')
    xslt = etree.fromstring(xml2rdf)

    transform = etree.XSLT(xslt)
    newdom = transform(dom)

    sr = Graph().parse(data=newdom)

    for s in sr.subjects(RDF.type, URIRef('http://www.opengis.net/gml/ProjectedCRS')):
        triples.append((raster_iri, GDAL.projection, s))
    return triples
