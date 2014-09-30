#!/usr/bin/env python2

'''Read and write image files as NumPy arrays'''


from numpy import asarray, float32
from PIL import Image

from . import np
from . import utils


_DEFAULT_DTYPE = float32

_PIL_RGB = {
    'R': 0,
    'G': 1,
    'B': 2,
}


def get_channels(img):
    '''Return a list of channels of an image array.'''
    if utils.depth(img) == 1:
        yield img
    else:
        for i in xrange(utils.depth(img)):
            yield img[:, :, i]


def swap_rgb(img, rgb):
    '''Swap the RBG channels of an image array.'''
    if utils.depth(img) == 3 and not rgb == utils._PREFERRED_RGB:
        rgb_inv = utils._invert_dict(rgb)
        rgb_order = [rgb_inv[k] for k in [0, 1, 2]]
        swap_indices = [utils._PREFERRED_RGB[k] for k in rgb_order]
        img = img[:, :, swap_indices]
    return img


def read(filename, dtype=_DEFAULT_DTYPE):
    '''Read an image file as an array.'''
    img = Image.open(filename)
    arr = asarray(img, dtype=dtype)
    arr = swap_rgb(arr, _PIL_RGB)
    return arr


def _pil_save(img, filename):
    pil_img = Image.fromarray(img)
    pil_img.save(filename)
    return


def save(img, filename, random=False):
    '''Save an image array and return its path.'''
    if random:
        newfile = utils.rand_filename(filename)
    else:
        newfile = filename
    np.normalize(img)
    uint8img = np.to_uint8(img)
    _pil_save(uint8img, newfile)
    return newfile


if __name__ == '__main__':
    pass
