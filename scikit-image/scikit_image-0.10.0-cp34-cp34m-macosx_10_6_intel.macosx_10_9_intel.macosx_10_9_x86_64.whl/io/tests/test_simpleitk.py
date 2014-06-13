import os.path
import numpy as np
from numpy.testing.decorators import skipif

from tempfile import NamedTemporaryFile

from skimage import data_dir
from skimage.io import imread, imsave, use_plugin, reset_plugins

try:
    import SimpleITK as sitk
    use_plugin('simpleitk')
except ImportError:
    sitk_available = False
else:
    sitk_available = True


def teardown():
    reset_plugins()


def setup_module(self):
    """The effect of the `plugin.use` call may be overridden by later imports.
    Call `use_plugin` directly before the tests to ensure that sitk is used.

    """
    try:
        use_plugin('simpleitk')
    except ImportError:
        pass


@skipif(not sitk_available)
def test_imread_flatten():
    # a color image is flattened
    img = imread(os.path.join(data_dir, 'color.png'), flatten=True)
    assert img.ndim == 2
    assert img.dtype == np.float64
    img = imread(os.path.join(data_dir, 'camera.png'), flatten=True)
    # check that flattening does not occur for an image that is grey already.
    assert np.sctype2char(img.dtype) in np.typecodes['AllInteger']


@skipif(not sitk_available)
def test_bilevel():
    expected = np.zeros((10, 10))
    expected[::2] = 255

    img = imread(os.path.join(data_dir, 'checker_bilevel.png'))
    np.testing.assert_array_equal(img, expected)


@skipif(not sitk_available)
def test_imread_uint16():
    expected = np.load(os.path.join(data_dir, 'chessboard_GRAY_U8.npy'))
    img = imread(os.path.join(data_dir, 'chessboard_GRAY_U16.tif'))
    assert np.issubdtype(img.dtype, np.uint16)
    np.testing.assert_array_almost_equal(img, expected)


@skipif(not sitk_available)
def test_imread_uint16_big_endian():
    expected = np.load(os.path.join(data_dir, 'chessboard_GRAY_U8.npy'))
    img = imread(os.path.join(data_dir, 'chessboard_GRAY_U16B.tif'))
    np.testing.assert_array_almost_equal(img, expected)


class TestSave:
    def roundtrip(self, dtype, x):
        f = NamedTemporaryFile(suffix='.mha')
        fname = f.name
        f.close()
        imsave(fname, x)
        y = imread(fname)

        np.testing.assert_array_almost_equal(x, y)

    @skipif(not sitk_available)
    def test_imsave_roundtrip(self):
        for shape in [(10, 10), (10, 10, 3), (10, 10, 4)]:
            for dtype in (np.uint8, np.uint16, np.float32, np.float64):
                x = np.ones(shape, dtype=dtype) * np.random.random(shape)

                if np.issubdtype(dtype, float):
                    yield self.roundtrip, dtype, x
                else:
                    x = (x * 255).astype(dtype)
                    yield self.roundtrip, dtype, x

if __name__ == "__main__":
    from numpy.testing import run_module_suite
    run_module_suite()
