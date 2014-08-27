from ogr_utils import OgrUtils


class Geometry(OgrUtils):

    def __init__(self,
                 vertex_arrays,
                 fields=None,
                 attr=None,
                 driver='ESRI Shapefile',
                 ordered=True):
        '''
        fields is a tuple or list of field name and field type. Type can be
        - str
        - int
        - float
        - date
        - time

        vertex_array is a tuple/list of tuples/lists with all coordinates making
        the line attr is tuple/list of tuples/lists. They are ordered by default,
        which means their realtionship to each other is best described by the index
        they share.
        Example:
            attr = [[0,1,2,...],['heute','morgen','gestern',...]]

        by setting the ordered argument to False it is also possible to pass
        the attributes unordered, which means their relationship is best described
        by the fact that they belong to the same row.
        Example:
            attr = [(0,'heute'),(1,'morgen'),(2,'gestern'),...]
        '''
        super(self.__class__, self).__init__(fields, attr, driver, ordered)
        self.vertex_arrays = vertex_arrays

    def make_lines(self, shape):
        "shape is filename of type .shp"
        self.shape = str(shape)
        self._make_geometry('line')
        return

    def make_points(self, shape):
        "shape is filename of type .shp"
        self.shape = str(shape)
        self._make_geometry('point')
        return

    def make_polygons(self, shape):
        "shape is filename of type .shp"
        self.shape = str(shape)
        self._make_geometry('polygon')
        return
