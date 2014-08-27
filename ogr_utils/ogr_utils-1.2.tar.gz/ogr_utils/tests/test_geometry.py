import unittest
import os
from ogr_utils.geometry import Geometry
from tempfile import mkstemp


class TestGeometry(unittest.TestCase):

    def setUp(self):
        self.geom = Geometry((0, 0, 1, 1, 2, 2, 7, 6, 0, 0))
        self.output = mkstemp(suffix="", prefix="test-geometry-")[-1]

    def tearDown(self):
        # remove temp files
        try:
            os.remove("%s" % (self.output))
        except OSError:
            pass
        for a in ['-lines', '-points', '-polygons']:
            for b in ['.shp', '.shx', '.dbf', '.prj']:
                try:
                    os.remove("%s%s%s" % (self.output, a, b))
                except OSError:
                    pass

    def it_can_make_lines(self):
        self.geom.make_lines("%s-lines.shp" % self.output)
        # check for files
        nm = self.output.split('/')[-1]
        self.assertIn(nm, os.listdir("/tmp/"))
        nm2 = "%s-lines.shp" % self.output
        self.assertIn(nm2.split('/')[-1], os.listdir("/tmp/"))

    def it_can_make_points(self):
        my_geom = Geometry(((0,0), (1,1), (2,2)))
        my_geom.make_points("%s-points.shp" % self.output)
        nm = self.output.split('/')[-1]
        self.assertIn(nm, os.listdir("/tmp/"))
        nm2 = "%s-points.shp" % self.output
        print os.listdir("/tmp/")
        self.assertIn(nm2.split('/')[-1], os.listdir("/tmp/"))

    def it_can_make_polygons(self):
        #print self.geom
        self.geom.make_polygons("%s-polygons.shp" % self.output)
        nm = self.output.split('/')[-1]
        self.assertIn(nm, os.listdir("/tmp/"))
        nm2 = "%s-polygons.shp" % self.output
        print os.listdir("/tmp/")
        self.assertIn(nm2.split('/')[-1], os.listdir("/tmp/"))
