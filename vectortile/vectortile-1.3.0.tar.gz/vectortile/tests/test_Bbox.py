import unittest2
from .. import Bbox


class TileTest(unittest2.TestCase):
    def test_bbox(self):
        b = Bbox(1.2345678, -2.34, 3, 4)
        self.assertEqual('Bbox(+001.23457,-002.34000,+003.00000,+004.00000)', repr(b))
        self.assertEqual('+001.23457,-002.34000,+003.00000,+004.00000', str(b))
        self.assertEqual('Bbox(+001.23457,-002.34000,+003.00000,+004.00000)', repr(eval(repr(b))))

        self.assertDictEqual(Bbox(2,2,4,4).center, dict(lat=3.0, lon=3.0))