import unittest
import os

try:
    import ogr
except ImportError:
    pass
try:
    from osgeo import ogr
except ImportError, err:
    print err


from ogr_utils.copy_helper import CopyHelper
from tempfile import mkstemp


class test_CopyHelper(unittest.TestCase):

    def setUp(self):
        self.cp_helper = CopyHelper()

        # find the fixtures path
        self.here = os.path.abspath(os.path.dirname(__file__)).split('/')[:-1]
        self.here.append('fixtures')
        self.fixtures = "/".join(self.here)

    def tearDown(self):
        pass

    def it_saves_and_converts_files_and_selections_to_shape_files(self):
        my_input = ogr.Open("%s/seg_testing_links.shp" % self.fixtures)
        my_layer = my_input.GetLayer()
        my_feature_count = my_layer.GetFeatureCount()
        self.assertEqual(my_feature_count, 500001)
        # now select the first 1000 features in my_layer
        my_layer_selection = my_input.ExecuteSQL("select * from 'seg_testing_links' where 'FID' < 1000")
        self.assertEqual(my_layer_selection.GetFeatureCount(), 1000)
        # save the resulting layer_selection
        my_output = mkstemp(suffix=".shp", prefix="test-cp-helper-")[-1]
        self.cp_helper.lyr_2_shp(my_layer_selection, my_output, 'line')

        # check the output, it should have 1000 features
        my_output_chk = ogr.Open(my_output)
        my_layer_chk = my_output_chk.GetLayer()
        self.assertEqual(my_layer_chk.GetFeatureCount(), 1000)

        # clean up
        os.remove(my_output)
        os.remove(my_output[:-4] + ".dbf")
        os.remove(my_output[:-4] + ".prj")
        os.remove(my_output[:-4] + ".qix")
        os.remove(my_output[:-4] + ".shx")

    def it_can_extract_field_info(self):
        my_input = ogr.Open("%s/seg_testing_links.shp" % self.fixtures)
        my_layer = my_input.GetLayer()
        field_count = my_layer.GetLayerDefn().GetFieldCount()
        self.assertEqual(field_count, 12)

        res_dict = self.cp_helper.copy_field_info(my_layer, "dict")
        self.assertEqual(len(res_dict), 12)

        self.assertIn("RD_ID", res_dict)
        self.assertIn("RD_FROM", res_dict)
        self.assertIn("RD_TO", res_dict)
        self.assertIn("RD_LENGTH", res_dict)
        self.assertIn("RD_DIR", res_dict)
        self.assertIn("RD_TYPE", res_dict)
        self.assertIn("RD_NATION", res_dict)
        self.assertIn("RD_LEVEL", res_dict)
        self.assertIn("RD_DEL", res_dict)
        self.assertIn("RD_SNAME", res_dict)
        self.assertIn("RD_NAME", res_dict)
        self.assertIn("RD_RN", res_dict)

        res_tup = self.cp_helper.copy_field_info(my_layer, "tup")
        self.assertEqual(len(res_tup), 12)

        res_plain = self.cp_helper.copy_field_info(my_layer, "plain")
        self.assertEqual(res_plain, "printed")

        # check if exception is raised.
        self.assertRaises(Exception,
                          self.cp_helper.copy_field_info, my_layer, "dit-gaat-fout",
                          msg="dest parameter must be: 'plain', 'dict' or 'tup'")
