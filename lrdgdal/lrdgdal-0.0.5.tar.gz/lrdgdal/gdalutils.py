#!/usr/bin/env python
# coding:utf-8
"""lrdgdal utilities for gdal

This module contains mostly utilities for projecting points between different reference systems.
"""

__author__ = "Thomas Scharrenbach (thomas@scharrenbach.net)"
__copyright__ = "Copyright (C) 2014 Thomas Scharrenbach"
__license__ = "Apache License v2"
__version__ = "0.0.6"

import logging

import tempfile

import numpy

try:
    from osgeo import osr
    from osgeo import ogr
    from osgeo import gdal
except ImportError:
    import osr
    import ogr
    import gdal

WGS84 = osr.SpatialReference()
WGS84.SetWellKnownGeogCS("WGS84")


def project_coordinates(point, spatial_ref_target, spatial_ref_src=WGS84):
    """Transforms a geo-referenced point to real-valued target referenced system coordinates.

    :param point: the geo-reference point to transform
    :param spatial_ref_target: the spatial reference system of the target
    :param spatial_ref_src: the spatial reference system of the point (default WGS84)
    :return: point transformed to target coordinates
    """
    coordinate_trans = \
        osr.CoordinateTransformation(spatial_ref_src, spatial_ref_target)
    projected_point = \
        coordinate_trans.TransformPoint(point[0], point[1])

    # omit z-variable, since it has no meaning!
    return [projected_point[0], projected_point[1]]


def project_raster_to_geo(points, affine_trans):
    """Turns points in raster coordinates into a set of geo-referenced points.

    :param points: the points to transform
    :param affine_trans: the affine geo-transformation of the raster
    :return: array of points
    """
    x = numpy.array([[c[0] for c in points], [c[1] for c in points], [1 for c in points]])

    # TODO handle homogeneous coordinates zero values.
    return [[c[0]/c[2], c[1]/c[2]] for c in numpy.dot(affine_trans, x).T]


def project_geo_to_raster(points, affine_trans_inv):
    """Computes raster coordinates of a geo-referenced point.

    :param points: the points to project
    :param affine_trans_inv: the inverse of the raster's affine geo-transformation
    :return: True if point in raster, False else.

    Important: please make sure that the point is geo-referenced according to the
    raster's spatial reference system!
    """
    x = numpy.array([[c[0] for c in points], [c[1] for c in points], [1 for c in points]])

    # TODO handle homogeneous coordinates zero values.
    return [[c[0]/c[2], c[1]/c[2]] for c in numpy.dot(affine_trans_inv, x).T]


def point_in_raster(point, affine_trans_inv, raster_dimensions):
    """Checks whether a point (in raster coords) lies within the raster.

    :param point: the point to check
    :param affine_trans_inv: the inverse of the raster's affine geo-transformation
    :param raster_dimensions: [xsize, ysize, 1] as numpy array
    :return: True if point in raster, False else.

    Important: please make sure that you transformed the point into
    raster coordinates before applying this method!
    """
    r_c = project_geo_to_raster(
        points=[point],
        affine_trans_inv=affine_trans_inv)[0]
    in_raster = numpy.subtract(raster_dimensions, numpy.array([[r_c[0]], [r_c[1]], [1]]))

    # Return single truth value instead of numpy array.
    if round(in_raster[0][0]) >= 0 and round(in_raster[1][0]) >= 0:
        return True
    else:
        logging.warning('POINT NOT IN RASTER!')
        return False


def create_raster_base(
        driver="GTiff", raster_x_size=512, raster_y_size=256,
        geo_transform=[0, 1, 0, 0, 0, 1], srs=WGS84):
    """Base method for creating a raster.

    :param driver: driver of raster (default "GTiff")
    :param raster_x_size: x-size of raster (default 512)
    :param raster_y_size: y-size of raster (default 256)
    :param geo_transform: affine transformation (default [0,1,0,0,0,1])
    :param srs: spatial reference system (default WGS84)
    :return: raster without data.
    """
    driver = gdal.GetDriverByName(driver)
    if driver is None:
        raise Exception('Driver could not be instantiated: {}'.format(driver))

    dataset_file = tempfile.NamedTemporaryFile(delete=True)
    dataset = driver.Create(
        utf8_path=dataset_file.name, xsize=raster_x_size, ysize=raster_y_size,
        bands=1, eType=gdal.GDT_Byte)

    dataset.SetGeoTransform(geo_transform)
    dataset.SetProjection(srs.ExportToWkt())

    return dataset


def create_dataset_random(
        driver="MEM",
        raster_x_size=512,
        raster_y_size=512,
        geo_transform=[0, 1, 0, 0, 0, 1],
        srs=WGS84):
    """Create a gdal raster dataset of random numbers.

        :return: raster filled with random numbers
    """
    dataset = create_raster_base(
        driver=driver, raster_x_size=raster_x_size, raster_y_size=raster_y_size,
        geo_transform=geo_transform, srs=srs)

    raster = numpy.random.random_integers(0, 100, (dataset.RasterXSize, dataset.RasterYSize))
    dataset.GetRasterBand(1).WriteArray(raster)

    return dataset


def create_dataset_zeros(
        driver="GTiff", raster_x_size=512, raster_y_size=512, geo_transform=[0, 1, 0, 0, 0, 1], srs=WGS84):
    """Create a gdal raster dataset of zeros.

    :return: raster filled with zeros
    """
    dataset = create_raster_base(
        driver=driver, raster_x_size=raster_x_size, raster_y_size=raster_y_size,
        geo_transform=geo_transform, srs=srs)

    raster = numpy.zeros((dataset.RasterYSize, dataset.RasterXSize), dtype=numpy.uint8)
    dataset.GetRasterBand(1).WriteArray(raster)

    return dataset


def points2polygon(points):
    """Create a polygon from a list of points.

    :param points: list of 2D points
    :return: ogr polygon
    """
    # Create ring from list of points.
    ring = ogr.Geometry(ogr.wkbLinearRing)
    first = None
    for p in points:
        if first is None:
            first = p
        logging.debug('Adding point to geometry: {}'.format(p))
        ring.AddPoint_2D(p[0], p[1])
    ring.AddPoint_2D(first[0], first[1])

    # Create polygon
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)
    return poly


def affine_transformation(dataset):
    """Creates a numpy matrix holding the affine transformation in homogeneous coordinates.

    :param dataset: the gdal dataset
    :return: 3x3 numpy array with affine transformation
    """
    geo_trans = dataset.GetGeoTransform()
    return numpy.array([
        [geo_trans[1], geo_trans[2], geo_trans[0]],
        [geo_trans[4], geo_trans[5], geo_trans[3]],
        [0, 0, 1]
    ])


def affine_transformation_inv(dataset):
    """Creates a numpy matrix holding the inverse affine transformation in homogeneous coordinates.

    :param dataset: the gdal dataset
    :return: 3x3 numpy array with inverse affine transformation
    """
    return numpy.linalg.inv(affine_transformation(dataset=dataset))


def geometry_geo2raster(geometry, affine_trans_inv):
    """Projects a geometry into a raster.

    Note that the original object will be changed. In case this is not desired, please specify a clone as an argument
    to this method, for example, using Geometry.Clone().

    :param geometry: the geometry to transform
    :param affine_trans_inv: the inverse of the raster's affine transformation.
    :return: the modified geometry.
    """
    # Recursively process all sub-geometries
    for g in range(0, geometry.GetGeometryCount()):
        geometry_geo2raster(geometry.GetGeometryRef(g), affine_trans_inv)

    # Project each point into the raster's coordinate system.
    for p in range(0, geometry.GetPointCount()):
        point = geometry.GetPoint_2D(p)
        point = project_geo_to_raster([point], affine_trans_inv)[0]
        geometry.SetPoint_2D(point=p, x=point[0], y=point[1])

    return geometry


def bbox_for_geometry_inside_dataset(dataset, mask_geometry):
    """

    :param dataset:
    :param mask_geometry:
    :return:
    """

    # Create a copy of the mask mask_geometry and project it to the raster's SRS.
    geometry_raster = mask_geometry.Clone()
    geometry_raster.TransformTo(osr.SpatialReference(dataset.GetProjection()))

    # Project the mask geometry into raster coordinates.
    geometry_geo2raster(geometry_raster, affine_transformation_inv(dataset))

    # Convert the raster's bounding box to a mask_geometry in order to intersect it with the mask mask_geometry.
    bbox = points2polygon(
        [[0, 0],
        [0, dataset.RasterYSize],
        [dataset.RasterXSize, dataset.RasterYSize],
        [dataset.RasterXSize, 0]])

    # Get the bounding box of the intersection of the mask geometry with the raster's bounding box.
    # This will give us the bounding box for the clipping region, which we have to specifiy by
    # offset and size for gdal's methods for reading raster data.
    env = geometry_raster.Intersection(bbox).GetEnvelope()
    xoff = round(env[0])
    yoff = round(env[2])
    win_xsize = round(env[1])
    win_ysize = round(env[3])

    logging.debug('GEO_RASTER: {}'.format(geometry_raster))
    logging.debug('ENVELOPE_GEO_RASTER: {}'.format(env))

    # Due to rounding errors we have to check whether the computed values fir the raster's dimensions.
    # In case they do not fit we have to correct these.
    if xoff + win_xsize > dataset.RasterXSize:
        logging.debug('Correcting win_xsize from "{}" to "{}"'.format(
            win_xsize, dataset.RasterXSize - xoff))
        win_xsize = dataset.RasterXSize - xoff
    if yoff + win_ysize > dataset.RasterYSize:
        logging.debug('Correcting win_ysize from "{}" to "{}"'.format(
            win_ysize, dataset.RasterYSize - yoff))
        win_ysize = dataset.RasterYSize - yoff

    logging.debug('xSize: {}, ySize: {}'.format(dataset.RasterXSize, dataset.RasterYSize))
    logging.debug('xoff: {}, yoff:{}, win_x:{}, win_y:{}'.format(xoff, yoff, win_xsize, win_ysize))

    return xoff, yoff, win_xsize, win_ysize


def create_mask_dataset(dataset, mask_geometry, nodata_value=-1, gdal_driver_name='MEM', ogr_driver_name='Memory'):
    """Create a mask raster dataset from a mask geometry.

    :param dataset:
    :param mask_geometry:
    :param nodata_value:
    :param gdal_driver_name:
    :param ogr_driver_name:
    :return:
    """

    logging.info('Started creating mask...')
    # Compute dimensions of masked dataset.
    xoff, yoff, win_xsize, win_ysize = bbox_for_geometry_inside_dataset(
        dataset=dataset, mask_geometry=mask_geometry)

    # For creating the actual mask we will burn a shape layer into the raster.
    # To be more precise we will burn the shape into a new raster which has the dimensions of the
    # clipping region. We will use this auxiliary raster for creating the actual mask as a numpy array.
    #shape_layer = create_layer_for_shape(
    #    geometry=mask_geometry, srs=dataset.GetProjection(), ogr_driver_name=ogr_driver_name)

    ogr_driver = ogr.GetDriverByName(ogr_driver_name)

    if ogr_driver is None:
        raise Exception('Driver not available: "{}"'.format(ogr_driver_name))

    logging.info('Started creating layer for shape.')
    # Create an in-memory shape dataset holding the specified geometry.
    shape_layer_file = tempfile.NamedTemporaryFile(delete=True)
    shape_layer_file.close()
    ogr_ds = ogr_driver.CreateDataSource(shape_layer_file.name)
    shape_layer = ogr_ds.CreateLayer(
        name='point_out', srs=osr.SpatialReference(dataset.GetProjection()),
        geom_type=ogr.wkbMultiPolygon)
    feature_definition = shape_layer.GetLayerDefn()
    out_feature = ogr.Feature(feature_definition)
    out_feature.SetGeometry(mask_geometry)
    shape_layer.CreateFeature(out_feature)
    logging.info('Finished creating layer for shape.')

    gdal_driver = gdal.GetDriverByName(gdal_driver_name)
    if gdal_driver is None:
        raise Exception('Driver not available: "{}"'.format(gdal_driver_name))

    data_type = dataset.GetRasterBand(1).DataType

    # Create the masking dataset as a temporary file
    dst_file = tempfile.NamedTemporaryFile(delete=True)
    mask_ds = gdal_driver.Create(
        utf8_path=dst_file.name,
        xsize=win_xsize,
        ysize=win_ysize,
        bands=1,
        eType=data_type)
    mask_ds.SetProjection(dataset.GetProjection())

    # Translate affine transform according to offsets
    gt = dataset.GetGeoTransform()
    upper_left = project_raster_to_geo(
        [[xoff, yoff]], affine_trans=affine_transformation(dataset))[0]
    gt_new = (upper_left[0], gt[1], gt[2], upper_left[1], gt[4], gt[5])
    mask_ds.SetGeoTransform(gt_new)

    # Burn mask_geometry to raster layer.
    gdal.RasterizeLayer(dataset=mask_ds, bands=[1], layer=shape_layer, burn_values=[-1])
    dst_mask_band = mask_ds.GetRasterBand(1)
    dst_mask_band.SetNoDataValue(nodata_value)

    logging.info('Finished creating mask.')
    return mask_ds, xoff, yoff, win_xsize, win_ysize


def clip_bands(dataset, mask_geometry, bands='ALL', nodata_value=-1, fill_value=0,
               gdal_driver_name='MEM', ogr_driver_name='Memory'):
    """Clip the bands of a dataset with respect to a mask_geometry.

    :param dataset: raster
    :param mask_geometry: mask_geometry to be used for clip_dataset.
    :param bands: indices of bands to clip or 'ALL'
    :param nodata_value: value for no data for clip_dataset.
    :param gdal_driver_name: gdal driver to use for clipping and result (default MEM)
    :param ogr_driver_name: ogr driver to use for shape layer (default Memory)
    :return: list of numpy arrays, each of which holding the clipped data of the bands

    We perform the clipping by accomplishing the following steps:

    1. Project the geometry into raster coordinates.
    2. Compute the intersection between the projected geometry's bbox and the raster's bbox.
        This will serve as the clipping region.
    3. Create an ogr layer holding the mask geometry and burn it into a fresh raster, which has the dimensions of the
        clipping region.
    4. For each band of the raster, read the clipping region and mask it with the data from the fresh raster into which
        we burned the mask geometry.
    5. Write the result to a new raster with the same meta-data as the old raster. Note that this new raster holds only
        the original data of the clipping region. The affine transformation may have been corected by the translation
        imposed by the bounding box of the clipping region.
    """

    mask_ds, xoff, yoff, win_xsize, win_ysize = create_mask_dataset(
        dataset=dataset, mask_geometry=mask_geometry, nodata_value=nodata_value,
        gdal_driver_name=gdal_driver_name, ogr_driver_name=ogr_driver_name)

    dst_mask_band = mask_ds.GetRasterBand(1)
    mask_data = dst_mask_band.ReadAsArray(
        xoff=0, yoff=0, win_xsize=mask_ds.RasterXSize, win_ysize=mask_ds.RasterYSize)
    mask_ds = None

    band_indices = None
    if bands == 'ALL':
        band_indices = range(1, dataset.RasterCount+1)
    else:
        band_indices = bands

    result = dict()
    for band_idx in band_indices:
        # The indices of the bands holding the original data are identical to those used for storing intermediate
        # results.
        src_data_band = dataset.GetRasterBand(band_idx)

        src_data = src_data_band.ReadAsArray(
            xoff=xoff, yoff=yoff, win_xsize=win_xsize, win_ysize=win_ysize)

        result[band_idx] = numpy.ma.masked_array(
            src_data,
            numpy.logical_not(mask_data),
            fill_value=fill_value)

    return result, xoff, yoff, win_xsize, win_ysize


def clip_dataset(dataset, mask_geometry, bands='ALL', nodata_value=-1, fill_value=0, gdal_driver_name='MEM', ogr_driver_name='Memory'):
    """Clip dataset with respect to a mask_geometry.

    :param dataset: raster
    :param mask_geometry: mask_geometry to be used for clip_dataset.
    :param nodata_value: value for no data for clip_dataset.
    :param gdal_driver_name: gdal driver to use for clipping and result (default MEM)
    :param ogr_driver_name: ogr driver to use for shape layer (default Memory)
    :return: dataset
    """
    logging.info('Started creating result tiff.')

    gdal_driver = gdal.GetDriverByName(gdal_driver_name)
    if gdal_driver is None:
        raise Exception('Driver not available: "{}"'.format(gdal_driver_name))

    # Compute dimensions of masked dataset.
    xoff, yoff, win_xsize, win_ysize = bbox_for_geometry_inside_dataset(
        dataset=dataset, mask_geometry=mask_geometry)

    data_type = dataset.GetRasterBand(1).DataType

    # Create result dataset to temporary file.
    result_file = tempfile.NamedTemporaryFile(delete=True)
    logging.debug('Filename of result: {}'.format(result_file.name))
    result_ds = gdal_driver.Create(
        utf8_path=result_file.name,
        xsize=win_xsize,
        ysize=win_ysize,
        bands=dataset.RasterCount,
        eType=data_type)
    result_ds.SetProjection(dataset.GetProjection())
    #result_ds.SetGeoTransform(gt_new)
    result_ds.SetMetadata(dataset.GetMetadata())
    logging.info('Finished creating result tiff.')

    band_indices = range(1, dataset.RasterCount+1)
    masked_band_data, xoff, yoff, win_xsize, win_ysize = clip_bands(
        dataset=dataset, mask_geometry=mask_geometry, bands=band_indices,
        nodata_value=nodata_value, fill_value=fill_value,
        gdal_driver_name=gdal_driver_name, ogr_driver_name=ogr_driver_name)

    band_indices = None
    if bands == 'ALL':
        band_indices = range(1, dataset.RasterCount+1)
    else:
        band_indices = bands

    dst_band_idx = 0
    # Mask all bands of the original dataset
    for src_band_idx in band_indices:
        dst_band_idx += 1
        # The indices of the bands holding the original data are identical to those used for storing intermediate
        # results.
        src_data_band = dataset.GetRasterBand(src_band_idx)

        # Fill bands of result dataset with masked values.
        result_band = result_ds.GetRasterBand(dst_band_idx)
        # TODO check which meta-data has to be copied and which not
        #result_band.SetColorTable(src_data_band.GetColorTable())
        #result_band.SetRasterColorTable(src_data_band.GetRasterColorTable())
        result_band.SetRasterColorInterpretation(src_data_band.GetRasterColorInterpretation())
        result_band.SetColorInterpretation(src_data_band.GetColorInterpretation())
        #result_band.SetDefaultRAT(src_data_band.GetDefaultRAT())
        #result_band.SetCategoryNames(src_data_band.GetCategoryNames())
        result_band.SetNoDataValue(nodata_value)
        logging.info('Started masking data for band {}'.format(src_band_idx))
        result_band.WriteArray(masked_band_data.get(src_band_idx).filled(fill_value=nodata_value))
        logging.info('Finished masking data for band {}'.format(src_band_idx))

    return result_ds
