import unittest
from ecosynth.postprocess import io
import numpy as np
from numpy import testing


# Here's our "unit tests".
class LoadPLYTests(unittest.TestCase):

    def setUp(self):
        pass

    def testOne(self):
        a = np.array([[1.0, 2.0, 3.0, 4, 5, 6], [1.0, 2.0, 3.0, 4, 5, 6]])
        f = open("sample.ply", "r")
        ply_tuple = io.load_ply(f)
        print "total points:", ply_tuple.points_total
        print "output array:", ply_tuple.xyzrgb_array
        print "expected array:", a
        self.assertTrue(ply_tuple.points_total == a.shape[0])
        testing.assert_array_equal(a, ply_tuple.xyzrgb_array)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
