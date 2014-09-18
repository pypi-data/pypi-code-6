#!/usr/bin/env python
# coding:utf-8

"""lrdgadl GDAL RDF constants"""

__author__ = 'Thomas Scharrenbach (thomas@scharrenbach.net)'
__copyright__ = 'Copyright (C) 2014 Thomas Scharrenbach'
__license__ = 'Apache License v2'
__version__ = '0.0.6'

try:
    from osgeo import gdal
except ImportError:
    import gdal


from rdflib import URIRef

#The base namespace for gdal rdf graphs.
NS = 'http://scharrenbach.net/gdal#'

#The base namespace for gdal drivers.
NS_DRIVERS = 'http://scharrenbach.net/gdal/drivers#'

#URI for band types.
band = URIRef(NS + 'Band')

rasterXSize = URIRef(NS + 'rasterXSize')

rasterYSize = URIRef(NS + 'rasterYSize')

blockXSize = URIRef(NS + 'blockXSize')

blockYSize = URIRef(NS + 'blockYSize')

bandNoDataValue = URIRef(NS + 'bandNoDataValue')

bandMin = URIRef(NS + 'bandMin')

bandMax = URIRef(NS + 'bandMax')

bandStatsMin = URIRef(NS + 'bandStatsMin')

bandStatsMax = URIRef(NS + 'bandStatsMax')

bandStatsMean = URIRef(NS + 'bandStatsMean')

bandStatsStdDev = URIRef(NS + 'bandStatsStdDev')

bandScale = URIRef(NS + 'bandScale')

band_unit_type = URIRef(NS + 'band_unit_type')

mask_band = URIRef(NS + 'mask_band')

mask_flags = URIRef(NS + 'mask_flags')

color_interpretation = URIRef(NS + 'color_interpretation')

dataType = URIRef(NS + 'dataType')

raster = URIRef(NS + 'Raster')

projection = URIRef(NS + 'projection')

driver = URIRef(NS + 'Driver')

geo_transform = URIRef(NS + 'geo_transform')

gcp = URIRef(NS + 'Gcp')

meta_dict = URIRef(NS + 'meta_dict')

meta_key = URIRef(NS + 'meta_key')

meta_value = URIRef(NS + 'meta_value')

short_name = URIRef(NS + 'short_name')

long_name = URIRef(NS + 'long_name')

description = URIRef(NS + 'description')

band_value = URIRef(NS + 'bandValue')

clip = URIRef(NS + 'clip')

clip_value = URIRef(NS + 'clipValue')

mask_geometry = URIRef(NS + 'maskGeometry')

pixel_value = URIRef(NS + 'pixelValue')

pixel_coordinates = URIRef(NS + 'pixelCoordinates')


GCI_AlphaBand = URIRef(NS + 'GCI_AlphaBand')
GCI_BlackBand = URIRef(NS + 'GCI_BlackBand')
GCI_BlueBand = URIRef(NS + 'GCI_BlueBand')
GCI_CyanBand = URIRef(NS + 'GCI_CyanBand')
GCI_GrayIndex = URIRef(NS + 'GCI_GrayIndex')
GCI_GreenBand = URIRef(NS + 'GCI_GreenBand')
GCI_HueBand = URIRef(NS + 'GCI_HueBand')
GCI_LightnessBand = URIRef(NS + 'GCI_LightnessBand')
GCI_MagentaBand = URIRef(NS + 'GCI_MagentaBand')
GCI_PaletteIndex = URIRef(NS + 'GCI_PaletteIndex')
GCI_RedBand = URIRef(NS + 'GCI_RedBand')
GCI_SaturationBand = URIRef(NS + 'GCI_SaturationBand')
GCI_Undefined = URIRef(NS + 'GCI_Undefined')
GCI_YCbCr_CbBand = URIRef(NS + 'GCI_YCbCr_CbBand')
GCI_YCbCr_CrBand = URIRef(NS + 'GCI_YCbCr_CrBand')
GCI_YCbCr_YBand = URIRef(NS + 'GCI_YCbCr_YBand')
GCI_YellowBand = URIRef(NS + 'GCI_YellowBand')


def create_gci(gci):
    if gci == gdal.GCI_AlphaBand:
        return GCI_AlphaBand
    elif gci == gdal.GCI_BlackBand:
        return GCI_BlackBand
    elif gci == gdal.GCI_BlueBand:
        return GCI_BlueBand
    elif gci == gdal.GCI_CyanBand:
        return GCI_CyanBand
    elif gci == gdal.GCI_GrayIndex:
        return GCI_GrayIndex
    elif gci == gdal.GCI_GreenBand:
        return GCI_GreenBand
    elif gci == gdal.GCI_HueBand:
        return GCI_HueBand
    elif gci == gdal.GCI_LightnessBand:
        return GCI_LightnessBand
    elif gci == gdal.GCI_MagentaBand:
        return GCI_MagentaBand
    elif gci == gdal.GCI_PaletteIndex:
        return GCI_PaletteIndex
    elif gci == gdal.GCI_RedBand:
        return GCI_RedBand
    elif gci == gdal.GCI_SaturationBand:
        return GCI_SaturationBand
    elif gci == gdal.GCI_Undefined:
        return GCI_Undefined
    elif gci == gdal.GCI_YCbCr_CbBand:
        return GCI_YCbCr_CbBand
    elif gci == gdal.GCI_YCbCr_CrBand:
        return GCI_YCbCr_CrBand
    elif gci == gdal.GCI_YCbCr_YBand:
        return GCI_YCbCr_YBand
    elif gci == gdal.GCI_YellowBand:
        return GCI_YellowBand
    else:
        return GCI_Undefined
        
GDT_Byte = URIRef(NS + 'GDT_Byte')
GDT_CFloat32 = URIRef(NS + 'GDT_CFloat32')
GDT_CFloat64 = URIRef(NS + 'GDT_CFloat64')
GDT_CInt16 = URIRef(NS + 'GDT_CInt16')
GDT_CInt32 = URIRef(NS + 'GDT_CInt32')
GDT_Float32 = URIRef(NS + 'GDT_Float32')
GDT_Float64 = URIRef(NS + 'GDT_Float64')
GDT_Int16 = URIRef(NS + 'GDT_Int16')
GDT_TypeCount = URIRef(NS + 'GDT_TypeCount')
GDT_UInt16 = URIRef(NS + 'GDT_UInt16')
GDT_UInt32 = URIRef(NS + 'GDT_UInt32')
GDT_Unknown = URIRef(NS + 'GDT_Unknown')


def create_gdt(gdt):
    if gdt == gdal.GDT_Byte:
        return GDT_Byte
    elif gdt == gdal.GDT_CFloat32:
        return GDT_CFloat32
    elif gdt == gdal.GDT_CFloat64:
        return GDT_CFloat64
    elif gdt == gdal.GDT_CInt16:
        return GDT_CInt16
    elif gdt == gdal.GDT_CInt32:
        return GDT_CInt32
    elif gdt == gdal.GDT_Float32:
        return GDT_Float32
    elif gdt == gdal.GDT_Float64:
        return GDT_Float64
    elif gdt == gdal.GDT_Int16:
        return GDT_Int16
    elif gdt == gdal.GDT_TypeCount:
        return GDT_TypeCount
    elif gdt == gdal.GDT_UInt16:
        return GDT_UInt16
    elif gdt == gdal.GDT_UInt32:
        return GDT_UInt32
    elif gdt == gdal.GDT_Unknown:
        return GDT_Unknown
    else:
        return GDT_Unknown