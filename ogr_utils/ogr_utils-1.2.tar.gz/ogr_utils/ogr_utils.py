import os
try:
    import ogr
except ImportError:
    pass
try:
    from osgeo import ogr
except ImportError, err:
    print err

# from gdalconst import *


class OgrUtils(object):
    '''
    OFTInteger 	Simple 32bit integer
    OFTIntegerList  List of 32bit integers
    OFTReal 	Double Precision floating point
    OFTRealList 	List of doubles
    OFTString 	String of ASCII chars
    OFTStringList 	Array of strings
    OFTWideString 	!deprecated!
    OFTWideStringList !deprecated!
    OFTBinary 	Raw Binary data
    OFTDate 	Date
    OFTTime 	Time
    OFTDateTime 	Date and Time
    see http://www.gdal.org/ogr/ogr__core_8h.html#a787194bea637faf12d61643124a7c9fca87c732175b3e99aeebca957ada1f6a2c
    '''


    field_type = {
        'int': ogr.OFTInteger,
        'str': ogr.OFTString,
        'float': ogr.OFTReal,
        'date': ogr.OFTDate,
        'time': ogr.OFTTime}

    geo_type = {
        'point': ogr.wkbPoint,
        'line': ogr.wkbLineString,
        'polygon': ogr.wkbPolygon,
        'ring': ogr.wkbLinearRing}

    def __init__(self,
                 fields=None,
                 attr=None,
                 driver='ESRI Shapefile',
                 ordered=False):

        self.fields = fields
        self.attr = attr
        self.driver = driver
        self.ordered = ordered
        if self.fields and len(fields[0]) >= 3:
            self.custom_width = True
        else:
            self.custom_width = False 



    def list_drivers(self):
        return [ogr.GetDriver(i).name for i in range(ogr.GetDriverCount())]

    @staticmethod
    def is_sequence(arg):
        '''
        testing behavoirs instead of types to use a sort of duck typing, that is to be able
        to process different types of input. 'If it has a .strip() method, it's a string, so don't
        consider it a sequence; otherwise, if it is indexable or iterable, it's a sequence'
        (http://stackoverflow.com/questions/1835018/python-check-if-an-object-is-a-list-or-tuple-but-not-string)
        '''
        return (not hasattr(arg, "strip") and
                hasattr(arg, "__getitem__") or
                hasattr(arg, "__iter__"))

    def _set_fields(self):
        # data should be passed as a list of list
        # if ordered is true...
        if self.ordered is True:
            # ...so should be possible to zip
            try:
                return zip(*self.attr)
            # if fails anyhow, convert to a list
            except TypeError, terr:
                return zip(*[self.attr])
        elif self.ordered is False:
            return self.attr

    def _test_set_field(self, res):
        for a in res:
            if a is False:
                print "SetField failed.\n"
                return

    def _make_geometry(self, gt):
        '''
        fields is a tuple or list of field name and field type. Type can be
        - str
        - int
        - float
        - date
        - time

        xy_pairs is a tuple/list of tuples/lists of coordinates
        attr is tuple/list of tuples/lists. They are ordered by default, which means their realtionship
        to each other is best described by the index they share.
        Example: attr = [[0,1,2,...],['heute','morgen','gestern',...]]
        by setting the ordered argument to False it is also possible to pass the attributes unorderd,
        which means their relationship is best described by the fact that they belong to the same row
        Example: attr = [(0,'heute'),(1,'morgen'),(2,'gestern'),...]
        '''

        # lint never used -> proj4_str = "+proj=sterea +lat_0=52.15616055555555 +lon_0=5.38763888888889 +k=0.9999079 +x_0=155000 +y_0=463000 +ellps=bessel +units=m +no_defs"

        if self.vertex_arrays is None or not OgrUtils.is_sequence(self.vertex_arrays):
            print 'vertex_arrays is None or not of type list or tuple...\n'
            return

        driver = ogr.GetDriverByName(self.driver)
        ds = driver.CreateDataSource(self.shape)
        spatialReference = ogr.osr.SpatialReference()
        spatialReference.SetWellKnownGeogCS("WGS84")  # "Amersfoort / RD New" EPSG:28992; http://spatialreference.org/ref/epsg/28992/
        # spatialReference.ImportFromEPSG(28992)
        # spatialReference.ImportFromProj4(proj4_str)
        layer = ds.CreateLayer(self.shape, spatialReference, self.geo_type[gt])
        if layer is None:
            print 'layer is: ', layer
            return

        for para in (self.fields, self.attr):
            if not OgrUtils.is_sequence(para):
                print 'fields or attributes is None or not of type tuple or list:'
                print 'only geometry is created...\n'
                self.fields = None
                break
            else:
                if self.custom_width is True:
                    field_def = []
                    for field in self.fields:
                        fd = ogr.FieldDefn(field[0], self.field_type[field[1]]) 
                        fd.SetWidth( int(field[2]) )
                        if field[1] == 'float':
                            if len(field) == 4:
                                precision = field[3]
                                fd.SetPrecision( int(precision) )
                        field_def.append(fd)
                    #field_def = [ogr.FieldDefn(field[0], self.field_type[field[1]]).SetWidth(field[2]) for field in self.fields]
                else:
                    field_def = [ogr.FieldDefn(field[0], self.field_type[field[1]]) for field in self.fields]
                for fd in field_def:
                    if layer.CreateField(fd) is False:
                        print "Creating Name field failed.\n"
                        return
                break

        for i, xy_sub in enumerate(self.vertex_arrays):
            # to create a polygon, first one needs to create a
            # sub geomtry called 'ring'
            if gt == 'polygon':
                geom = ogr.Geometry(self.geo_type['ring'])
            else:
                geom = ogr.Geometry(self.geo_type[gt])
            geom.AssignSpatialReference(spatialReference)

            if gt == 'line' or gt == 'polygon':
                if not OgrUtils.is_sequence(xy_sub):
                    print 'vertex_arrays has to be a list/tuple of list/tuples.\n'
                    return
                else:
                    feature = ogr.Feature(layer.GetLayerDefn())
                    if self.fields:
                        z_attr = self._set_fields()
                        res = [feature.SetField(field[0], z_attr[i][ind]) for ind, field in enumerate(self.fields)]
                        self._test_set_field(res)
                    for xy in xy_sub:
                        geom.AddPoint(float(xy[0]), float(xy[1]))
                    if gt == 'polygon':
                        poly = ogr.Geometry(self.geo_type[gt])
                        poly.AssignSpatialReference(spatialReference)
                        poly.AddGeometry(geom)
                        feature.SetGeometry(poly)
                    else:
                        feature.SetGeometry(geom)
                    if layer.CreateFeature(feature) is False:
                        print "Creating feature failed.\n"
                        return

            elif gt == 'point':
                feature = ogr.Feature(layer.GetLayerDefn())
                if self.fields:
                    z_attr = self._set_fields()
                    res = [feature.SetField(field[0], z_attr[i][ind]) for ind, field in enumerate(self.fields)]
                    self._test_set_field(res)
                geom.AddPoint(float(xy_sub[0]), float(xy_sub[1]))
                feature.SetGeometry(geom)
                if layer.CreateFeature(feature) is False:
                    print "Creating feature failed.\n"
                    return

        table_name = os.path.splitext(os.path.basename(self.shape))[0]
        ds.ExecuteSQL('CREATE SPATIAL INDEX ON %s' % (table_name,))
        geom.Destroy()
        feature.Destroy()
        ds.Destroy()
        return
