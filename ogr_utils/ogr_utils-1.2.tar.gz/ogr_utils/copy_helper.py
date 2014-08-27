import os
from collections import namedtuple
from ogr_utils import OgrUtils

try:
    import ogr
except ImportError:
    pass
try:
    from osgeo import ogr
except ImportError, err:
    print err


class CopyHelper(OgrUtils):
    """
    Intended to function as convienence class that helps to save en convert
    files and selections on them.
    Only knows one method so far that saves an ogr layer as a shapefile.
    """

    def lyr_2_shp(self, in_lyr, out_shp, geom_type):
        """
        input:
        in_lyr    --> ogr layer object
        out_shp   --> name of the output shape file (with full path)
        geom_type --> key as inherited from ogrUtils (either 'point','line','polygon' or 'ring')

        returns None

        Easily saves some attribute or spatial selection to a shape file. Example usage:

        import ogr
        from ogr_utils.copy_helper import CopyHelper
        c = CopyHelper()
        f = '/home/.../border_segs.shp'
        shp =ogr.Open(f,0)
        lyr = shp.GetLayer()
        lyr.GetFeatureCount()
        >>> 13411
        fo = '/home/.../border_segs_test.shp'
        lyr_sel = shp.ExecuteSQL("select * from 'border_segs' where 'FID' < 100 ")
        lyr_sel.GetFeatureCount()
        >>> 100
        c.lyr_2_shp(lyr_sel,fo,'line')
        """

        out_driver = ogr.GetDriverByName("ESRI Shapefile")

        spatial_ref = ogr.osr.SpatialReference()
        spatial_ref.SetWellKnownGeogCS("WGS84")

        # Remove output shapefile if it already exists
        if os.path.exists(out_shp):
            out_driver.DeleteDataSource(out_shp)

        # Create the output shapefile and layer
        out_ds = out_driver.CreateDataSource(out_shp)
        out_lyr = out_ds.CreateLayer(out_shp, spatial_ref, self.geo_type[geom_type])

        # Add all input layer fields to the output layer
        in_lyr_defn = in_lyr.GetLayerDefn()
        for i in range(0, in_lyr_defn.GetFieldCount()):
            field_defn = in_lyr_defn.GetFieldDefn(i)
            # field_name = field_defn.GetName()
            out_lyr.CreateField(field_defn)

        # Get the output layer's feature definition
        out_lyr_defn = out_lyr.GetLayerDefn()

        # Add features to the ouput layer
        for feat in in_lyr:
            # Create output feature
            feat_out = ogr.Feature(out_lyr_defn)

            # Add field values from input layer
            for i in range(0, out_lyr_defn.GetFieldCount()):
                field_defn = out_lyr_defn.GetFieldDefn(i)
                # field_name = field_defn.GetName()
                value = feat.GetField(i)
                feat_out.SetField(out_lyr_defn.GetFieldDefn(i).GetNameRef(), value)

            geom = feat.GetGeometryRef()
            if geom:
                feat_out.SetGeometry(geom.Clone())
                # Add new feature to output Layer
                out_lyr.CreateFeature(feat_out)
            else:
                print 'WARNING. NULL geometry found! Will be skipped.'

        # create a spatial index on the output table
        table_name = os.path.splitext(os.path.basename(out_shp))[0]
        out_ds.ExecuteSQL('CREATE SPATIAL INDEX ON %s' % (table_name,))

        # close datasource
        out_ds.Destroy()

        print 'Created %s successfully...' % table_name

    def copy_field_info(self, in_lyr, dest='plain'):
        res = None
        Entry = namedtuple("Entry", 'field_type field_width field_precision')

        in_lyr_defn = in_lyr.GetLayerDefn()
        for i in range(0, in_lyr_defn.GetFieldCount()):
            field_defn = in_lyr_defn.GetFieldDefn(i)
            field_name = field_defn.GetName()
            field_type = field_defn.GetTypeName()
            field_width = field_defn.GetWidth()
            field_precision = field_defn.GetPrecision()
            if dest.lower() == 'plain':
                print 'Field name: ', field_name
                print 'Field type: ', field_type
                print 'Field width: ', field_width
                print 'Field precision: ', field_precision
                print '\n'
                res = "printed"
            elif dest.lower() == 'dict':
                if res is None:
                    res = {}
                res[field_name] = Entry(field_type, field_width, field_precision)
            elif dest.lower() == 'tup':
                if res is None:
                    res = []
                res.append((field_name, field_type, field_width, field_precision))
            else:
                raise Exception("dest parameter must be: 'plain', 'dict' or 'tup'")

        if dest == 'tup':
            return tuple(res)
        else:
            return res


        # fd.Destroy
        # fd.GetName
        # fd.GetType
        # fd.IsIgnored
        # fd.SetName
        # fd.SetWidth
        # fd.precision
        # fd.width
        # fd.GetFieldTypeName
        # fd.GetNameRef
        # fd.GetTypeName
        # fd.SetIgnored
        # fd.SetPrecision
        # fd.justify
        # fd.this
        # fd.GetJustify
        # fd.GetPrecision
        # fd.GetWidth
        # fd.SetJustify
        # fd.SetType
        # fd.name
        # fd.type
