import os

try:
    import ogr
except ImportError:
    pass
try:
    from osgeo import ogr
except ImportError, err:
    print err

from copy_helper import CopyHelper


class AttributeExtractor(object):

    def __init__(self, shp_file, out_path=None):
        """

        :param shp_file:
        :return:
        """
        self.shp_file = shp_file
        self.ds = ogr.Open(self.shp_file, 0)
        self.layer_name = self.ds.GetLayer().GetName()
        p, self._base_file = os.path.split(self.shp_file)
        if not out_path:
            self._out_path = p
        self.out_shp = None

    def extract_by_attribute(self, attribute_name, attribute_value, operator='='):
        """

        :param attribute_name:
        :param attribute_value:
        :param out_path:
        :return:
        """
        my_copyhelper = CopyHelper()
        self.out_shp = '{0:s}/{1:s}_{2:s}{3:s}.shp'.format(self._out_path,
                                                           self._base_file[:-4],
                                                           attribute_name,
                                                           attribute_value)

        sql_str = "SELECT * FROM {0:s} WHERE {1:s}{3:s}'{2:s}'".format(self.layer_name,
                                                                   attribute_name,
                                                                   attribute_value,
                                                                   operator)
        lyr = self.ds.ExecuteSQL(sql_str)
        if os.path.exists(self.out_shp):
            driver = ogr.GetDriverByName("ESRI Shapefile")
            driver.DeleteDataSource(self.out_shp)
        my_copyhelper.lyr_2_shp(lyr, self.out_shp, 'line')

    def feature_count(self):
        ds = ogr.Open(self.out_shp, 0)
        lyr = ds.GetLayer()
        return lyr.GetFeatureCount()

if __name__ == '__main__':

    pass