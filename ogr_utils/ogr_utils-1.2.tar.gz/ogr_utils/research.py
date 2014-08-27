try:
    import ogr
except ImportError:
    pass
try:
    from osgeo import ogr
except ImportError, err:
    print err


class Research(object):
    """
    Research class as in the QGIS Vector/Reseach Tools menue.
    """

    def __init__(self):
        pass

    def get_bounding_box(self, ll_corner, ur_corner):
        """
        Based on the coordinates of the lower left and upper right corner this method will return
        an ogr geometry object of the corresponding bounding box. Default it will use shapely's envelope
        function. If this fails it will create the bounding box polygon using ogr.
        """
        try:
            from shapely.geometry import MultiPoint
            mp_env = MultiPoint([ll_corner, ur_corner]).envelope
            return ogr.CreateGeometryFromWkt(mp_env.to_wkt())

        except ImportError:
            p_ll = ogr.Geometry(ogr.wkbPoint)
            p_ur = ogr.Geometry(ogr.wkbPoint)

            mpoint = ogr.Geometry(ogr.wkbMultiPoint)
            x_ll, y_ll = ll_corner
            x_ur, y_ur = ur_corner
            p_ll.AddPoint(x_ll, y_ll)
            mpoint.AddGeometry(p_ll)

            p_ur.AddPoint(x_ur, y_ur)
            mpoint.AddGeometry(p_ur)
            min_x, max_x, min_y, max_y = mpoint.GetEnvelope()

            # Create ring
            ring = ogr.Geometry(ogr.wkbLinearRing)
            ring.AddPoint(min_x, min_y)
            ring.AddPoint(max_x, min_y)
            ring.AddPoint(max_x, max_y)
            ring.AddPoint(min_x, max_y)
            ring.AddPoint(min_x, min_y)

            # Create polygon
            poly_envelope = ogr.Geometry(ogr.wkbPolygon)
            poly_envelope.AddGeometry(ring)
            return poly_envelope
