"""
These tests are originally part of CellProfiler, code licensed under both GPL and BSD licenses.

Website: http://www.cellprofiler.org
Copyright (c) 2003-2009 Massachusetts Institute of Technology
Copyright (c) 2009-2011 Broad Institute
All rights reserved.
Original author: Lee Kamentsky
"""
import numpy as np
from numpy.testing import (assert_array_almost_equal as assert_close,
                           assert_raises)

from skimage.morphology.greyreconstruct import reconstruction


def test_zeros():
    """Test reconstruction with image and mask of zeros"""
    assert_close(reconstruction(np.zeros((5, 7)), np.zeros((5, 7))), 0)


def test_image_equals_mask():
    """Test reconstruction where the image and mask are the same"""
    assert_close(reconstruction(np.ones((7, 5)), np.ones((7, 5))), 1)


def test_image_less_than_mask():
    """Test reconstruction where the image is uniform and less than mask"""
    image = np.ones((5, 5))
    mask = np.ones((5, 5)) * 2
    assert_close(reconstruction(image, mask), 1)


def test_one_image_peak():
    """Test reconstruction with one peak pixel"""
    image = np.ones((5, 5))
    image[2, 2] = 2
    mask = np.ones((5, 5)) * 3
    assert_close(reconstruction(image, mask), 2)


def test_two_image_peaks():
    """Test reconstruction with two peak pixels isolated by the mask"""
    image = np.array([[1, 1, 1, 1, 1, 1, 1, 1],
                      [1, 2, 1, 1, 1, 1, 1, 1],
                      [1, 1, 1, 1, 1, 1, 1, 1],
                      [1, 1, 1, 1, 1, 1, 1, 1],
                      [1, 1, 1, 1, 1, 1, 3, 1],
                      [1, 1, 1, 1, 1, 1, 1, 1]])

    mask = np.array([[4, 4, 4, 1, 1, 1, 1, 1],
                     [4, 4, 4, 1, 1, 1, 1, 1],
                     [4, 4, 4, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 4, 4, 4],
                     [1, 1, 1, 1, 1, 4, 4, 4],
                     [1, 1, 1, 1, 1, 4, 4, 4]])

    expected = np.array([[2, 2, 2, 1, 1, 1, 1, 1],
                         [2, 2, 2, 1, 1, 1, 1, 1],
                         [2, 2, 2, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 3, 3, 3],
                         [1, 1, 1, 1, 1, 3, 3, 3],
                         [1, 1, 1, 1, 1, 3, 3, 3]])
    assert_close(reconstruction(image, mask), expected)


def test_zero_image_one_mask():
    """Test reconstruction with an image of all zeros and a mask that's not"""
    result = reconstruction(np.zeros((10, 10)), np.ones((10, 10)))
    assert_close(result, 0)


def test_fill_hole():
    """Test reconstruction by erosion, which should fill holes in mask."""
    seed = np.array([0, 8, 8, 8, 8, 8, 8, 8, 8, 0])
    mask = np.array([0, 3, 6, 2, 1, 1, 1, 4, 2, 0])
    result = reconstruction(seed, mask, method='erosion')
    assert_close(result, np.array([0, 3, 6, 4, 4, 4, 4, 4, 2, 0]))


def test_invalid_seed():
    seed = np.ones((5, 5))
    mask = np.ones((5, 5))
    assert_raises(ValueError, reconstruction, seed * 2, mask,
                  method='dilation')
    assert_raises(ValueError, reconstruction, seed * 0.5, mask,
                  method='erosion')


def test_invalid_selem():
    seed = np.ones((5, 5))
    mask = np.ones((5, 5))
    assert_raises(ValueError, reconstruction, seed, mask,
                  selem=np.ones((4, 4)))
    assert_raises(ValueError, reconstruction, seed, mask,
                  selem=np.ones((3, 4)))
    reconstruction(seed, mask, selem=np.ones((3, 3)))


if __name__ == '__main__':
    from numpy import testing
    testing.run_module_suite()
