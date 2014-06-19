import unittest

from ogr_utils.ogr_utils import OgrUtils


class test_OgrUtils(unittest.TestCase):

    def setUp(self):
        self.my_ogr_utils = OgrUtils()
        self.my_ogr_utils2 = OgrUtils(ordered=True)

    def tearDown(self):
        pass

    def it_can_list_drivers(self):
        r = self.my_ogr_utils.list_drivers()
        self.assertEqual(str(type(r)), "<type 'list'>")
        self.assertEqual(len(r), 35)
        self.assertIn('ESRI Shapefile', r)
        self.assertIn('GeoJSON', r)

    def it_checks_wether_arg_is_sequence(self):
        s = "This is a string"
        l = [1, 2, 3, 4, 5]
        t = (1, 2, 3, 4, 5)
        d = {'a': 1, 'b': 2, 'c': 3}
        self.assertFalse(OgrUtils.is_sequence(s))
        self.assertTrue(OgrUtils.is_sequence(l))
        self.assertTrue(OgrUtils.is_sequence(t))
        self.assertTrue(OgrUtils.is_sequence(d))

    def it_can_set_fields(self):
        # this only operates on subclasses, but is defined in OgrUtils
        self.assertEqual(self.my_ogr_utils._set_fields(), None)
        #self.assertEqual(self.my_ogr_utils2._set_fields(), None)

    def it_supplies_a_geo_type_dict(self):
        ob = self.my_ogr_utils.geo_type
        self.assertEqual(str(type(ob)), "<type 'dict'>")
        self.assertIn('line', ob)
        self.assertIn('polygon', ob)
        self.assertIn('ring', ob)
        self.assertIn('point', ob)

    #def it_can_test_set_field(self):
    #    self.my_ogr_utils._test_set_field()

    # def it_can_make_a_geometry(self):
    #     print self._make_geometry
    #     assert False
