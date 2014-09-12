#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_featurevectormatrix
----------------------------------

Tests for `featurevectormatrix` module.
"""

import unittest

from featurevectormatrix import FeatureVectorMatrix

v3 = [1, 2, 3]
v4 = [1, 2, 3, 4]
c3 = ['a', 'b', 'c']
c4 = ['a', 'b', 'c', 'd']
d3 = {
    'a': 1,
    'b': 2,
    'c': 3,
}
d4 = {
    'a': 1,
    'b': 2,
    'c': 3,
    'd': 4,
}
d2_4 = {
    'e': 1,
    'f': 2,
    'g': 3,
    'h': 4,
}


class TestFeatureVectorMatrix(unittest.TestCase):

    def test_exceptions(self):
        fvm = FeatureVectorMatrix()
        caught = False
        try:
            fvm.add_row(v3)
        except IndexError:
            caught = True

        self.assertTrue(caught, "You can't add a list to a fvm with no columns defined")

        fvm.set_column_names(c3)
        self.assertEquals(3, fvm.column_count())

        fvm.add_row(v3)
        self.assertEquals(1, fvm.row_count())

        caught = False
        try:
            print fvm.keys()
        except NotImplementedError:
            caught = True

        self.assertTrue(caught, "You can't get keys without all rows keyed")

        caught = False
        try:
            fvm.transpose()
        except NotImplementedError:
            caught = True

        self.assertTrue(caught, "You can't rotate a fvm without all rows keyed")

        caught = False
        try:
            fvm.add_row(v4)
        except IndexError:
            caught = True

        self.assertTrue(caught, "You can't add a list to a fvm with more columns than the given list")

        fvm.add_row(d4)
        self.assertEquals(len(fvm.column_names()), 4)

        # test that the already added row gets the extra 0 appended
        self.assertEquals(fvm.get_row_list(0), [1, 2, 3,0])

    def test_fill_small_list(self):
        fvm = FeatureVectorMatrix()
        fvm.set_column_names(c4)

        fvm.add_row(v3)
        self.assertEquals(fvm.get_row_list(0), [1, 2, 3, 0])

    def test_fill_small_dict(self):
        fvm = FeatureVectorMatrix()
        fvm.add_row(d3)
        self.assertEquals(fvm.get_row_dict(0), d3)

        fvm.add_row(d4)
        self.assertEquals(fvm.get_row_dict(1), d4)

        self.assertEquals(fvm.get_row_list(0), [ d3[c] if c in d3 else fvm._default_value for c in fvm.column_names() ])

    def test2(self):
        fvm = FeatureVectorMatrix()
        fvm.set_column_names(c3)
        self.assertEquals(c3, fvm.column_names())

        fvm.add_row(d3)
        self.assertEquals(3, fvm.column_count())

        self.assertEquals(fvm.get_row_list(0), v3)

        fvm.add_row(d2_4)
        self.assertEquals(7, fvm.column_count())
        self.assertEquals(fvm.get_row_list(0), v3 + [0,0,0,0])
        self.assertEquals(fvm.get_row_dict(0), d3)

    def test_exceptions_key(self):
        fvm = FeatureVectorMatrix()
        caught = False
        try:
            fvm.add_row(v3, 'a')
        except IndexError:
            caught = True

        self.assertTrue(caught, "You can't add a list to a fvm with no columns defined")

        fvm.set_column_names(c3)
        self.assertEquals(3, fvm.column_count())

        fvm.add_row(v3, 'a')
        self.assertEquals(1, fvm.row_count())

        fvm.add_row(v3, 'a')
        self.assertEquals(1, fvm.row_count())

        caught = False
        try:
            fvm.add_row(v4, 'b')
        except IndexError:
            caught = True

        self.assertTrue(caught, "You can't add a list to a fvm with more columns than the given list")

        fvm.add_row(d4, 'c')
        self.assertEquals(len(fvm.column_names()), 4)
        self.assertEquals(2, fvm.row_count())

        # test that the already added row gets the extra 0 appended
        self.assertEquals(fvm.get_row_list(0), [1, 2, 3,0])

    def test_fill_small_list_key(self):
        fvm = FeatureVectorMatrix()
        fvm.set_column_names(c4)

        fvm.add_row(v3, 'a')
        self.assertEquals(fvm.get_row_list(0), [1, 2, 3, 0])

    def test_fill_small_dict_key(self):
        fvm = FeatureVectorMatrix()
        fvm.add_row(d3, 'a')
        self.assertEquals(fvm.get_row_dict(0), d3)

        fvm.add_row(d4, 'b')
        self.assertEquals(fvm.get_row_dict(1), d4)

        self.assertEquals(fvm.get_row_list(0), [ d3[c] if c in d3 else fvm._default_value for c in fvm.column_names() ])

    def test2_key(self):
        fvm = FeatureVectorMatrix()
        fvm.set_column_names(c3)
        self.assertEquals(c3, fvm.column_names())

        fvm.add_row(d3, 'a')
        self.assertEquals(3, fvm.column_count())

        self.assertEquals(fvm.get_row_list('a'), v3)

        fvm.add_row(d2_4, 'b')
        self.assertEquals(7, fvm.column_count())
        self.assertEquals(fvm.get_row_list('a'), v3 + [0,0,0,0])
        self.assertEquals(fvm['a'], v3 + [0,0,0,0])
        self.assertEquals(fvm[0], v3 + [0,0,0,0])

        self.assertEquals(fvm.get_row_dict('a'), d3)

        self.assertEquals([ k for k in fvm ], ['a', 'b'])

    def test_getitem(self):
        fvm = FeatureVectorMatrix(default_to_hashed_rows=True)
        fvm.set_column_names(c3)
        self.assertEquals(c3, fvm.column_names())
        fvm.add_row(v3, 'first')
        self.assertEquals(fvm[0], d3)

        tfvm = fvm.transpose()
        self.assertEquals(tfvm[0], {'first': 1})

    def test_transpose_default_value(self):
        fvm = FeatureVectorMatrix(default_value=-1)
        fvm.set_column_names(c3)
        self.assertEquals(c3, fvm.column_names())
        fvm.add_row(v3, 'first')
        fvm.add_row(d4, 'second')
        self.assertEquals(fvm[0], [1, 2, 3, -1])

        tfvm = fvm.transpose()

        for key in tfvm:
            self.assertIsNotNone(tfvm[key])

        self.assertEquals(tfvm.get_row_dict(3), {'second': 4})

    def test_matrix(self):
        fvm = FeatureVectorMatrix()
        fvm.set_column_names(c3)
        fvm.add_row(d3, 'one')
        fvm.add_row(d4, 'two')
        fvm.add_row(d4, 'three')

        self.assertEquals(4, fvm.column_count())
        self.assertEquals(3, fvm.row_count())

        v3_old = fvm.get_row_list(0)
        self.assertEquals(fvm.get_row_dict('two'), d4)

        rfvm = fvm.transpose()
        self.assertEquals(3, rfvm.column_count())
        self.assertEquals(4, rfvm.row_count())

        self.assertEquals(rfvm.get_row_dict(2), {'three': 3, 'two': 3, 'one': 3})
        self.assertEquals(rfvm.get_row_dict(3), {'two': 4, 'three': 4})

        self.assertEquals(rfvm.column_names(), ['one', 'two', 'three'])
        self.assertEquals(rfvm.get_row_list(2), [3, 3, 3])
        self.assertEquals(rfvm.get_row_list(3), [0, 4, 4])

        fvm2 = rfvm.transpose()
        self.assertEquals(4, fvm2.column_count())
        self.assertEquals(3, fvm2.row_count())

        self.assertEquals(fvm2.get_row_dict(2), d4)
        self.assertEquals(fvm2.get_row_dict(0), d3)
        self.assertEquals(fvm2.get_row_list(0), v3_old)

        self.assertEquals(fvm2.get_row_dict('two'), d4)

    def test_len(self):
        fvm = FeatureVectorMatrix()
        fvm.add_row(d3, 'one')

        self.assertEquals(1, len(fvm))
        self.assertEquals(fvm.keys(), ['one'])

if __name__ == '__main__':
    unittest.main()