import unittest
import datetools

class TestConvert(unittest.TestCase):
    def test_convert_from_ymd_to_ym(self):
        date = "20140101"
        result = datetools.convert(date, "%Y%m%d", "%Y%m")
        expect = "201401"
        self.assertEqual(expect, result)
