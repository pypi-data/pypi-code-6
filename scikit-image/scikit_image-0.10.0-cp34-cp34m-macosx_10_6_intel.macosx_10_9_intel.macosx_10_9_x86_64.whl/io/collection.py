"""Data structures to hold collections of images, with optional caching."""

from __future__ import with_statement

import os
from glob import glob
import re
from copy import copy

import numpy as np
import six


__all__ = ['MultiImage', 'ImageCollection', 'concatenate_images',
           'imread_collection_wrapper']


def concatenate_images(ic):
    """Concatenate all images in the image collection into an array.

    Parameters
    ----------
    ic: an iterable of images (including ImageCollection and MultiImage)
        The images to be concatenated.

    Returns
    -------
    ar : np.ndarray
        An array having one more dimension than the images in `ic`.

    See Also
    --------
    ImageCollection.concatenate, MultiImage.concatenate

    Raises
    ------
    ValueError
        If images in `ic` don't have identical shapes.
    """
    all_images = [img[np.newaxis, ...] for img in ic]
    try:
        ar = np.concatenate(all_images)
    except ValueError:
        raise ValueError('Image dimensions must agree.')
    return ar


def alphanumeric_key(s):
    """Convert string to list of strings and ints that gives intuitive sorting.

    Parameters
    ----------
    s: string

    Returns
    -------
    k: a list of strings and ints

    Examples
    --------
    >>> alphanumeric_key('z23a')
    ['z', 23, 'a']
    >>> filenames = ['f9.10.png', 'e10.png', 'f9.9.png', 'f10.10.png',
    ...              'f10.9.png']
    >>> sorted(filenames)
    ['e10.png', 'f10.10.png', 'f10.9.png', 'f9.10.png', 'f9.9.png']
    >>> sorted(filenames, key=alphanumeric_key)
    ['e10.png', 'f9.9.png', 'f9.10.png', 'f10.9.png', 'f10.10.png']
    """
    k = [int(c) if c.isdigit() else c for c in re.split('([0-9]+)', s)]
    return k


class MultiImage(object):
    """A class containing a single multi-frame image.

    Parameters
    ----------
    filename : str
        The complete path to the image file.
    conserve_memory : bool, optional
        Whether to conserve memory by only caching a single frame. Default is
        True.

    Notes
    -----
    If ``conserve_memory=True`` the memory footprint can be reduced, however
    the performance can be affected because frames have to be read from file
    more often.

    The last accessed frame is cached, all other frames will have to be read
    from file.

    The current implementation makes use of PIL.

    Examples
    --------
    >>> from skimage import data_dir

    >>> img = MultiImage(data_dir + '/multipage.tif') # doctest: +SKIP
    >>> len(img) # doctest: +SKIP
    2
    >>> for frame in img: # doctest: +SKIP
    ...     print(frame.shape) # doctest: +SKIP
    (15, 10)
    (15, 10)

    """
    def __init__(self, filename, conserve_memory=True, dtype=None):
        """Load a multi-img."""
        self._filename = filename
        self._conserve_memory = conserve_memory
        self._dtype = dtype
        self._cached = None

        from PIL import Image
        img = Image.open(self._filename)
        if self._conserve_memory:
            self._numframes = self._find_numframes(img)
        else:
            self._frames = self._getallframes(img)
            self._numframes = len(self._frames)

    @property
    def filename(self):
        return self._filename

    @property
    def conserve_memory(self):
        return self._conserve_memory

    def _find_numframes(self, img):
        """Find the number of frames in the multi-img."""
        i = 0
        while True:
            i += 1
            try:
                img.seek(i)
            except EOFError:
                break
        return i

    def _getframe(self, framenum):
        """Open the image and extract the frame."""
        from PIL import Image
        img = Image.open(self.filename)
        img.seek(framenum)
        return np.asarray(img, dtype=self._dtype)

    def _getallframes(self, img):
        """Extract all frames from the multi-img."""
        frames = []
        try:
            i = 0
            while True:
                frames.append(np.asarray(img, dtype=self._dtype))
                i += 1
                img.seek(i)
        except EOFError:
            return frames

    def __getitem__(self, n):
        """Return the n-th frame as an array.

        Parameters
        ----------
        n : int
            Number of the required frame.

        Returns
        -------
        frame : ndarray
           The n-th frame.
        """
        numframes = self._numframes
        if -numframes <= n < numframes:
            n = n % numframes
        else:
            raise IndexError("There are only %s frames in the image"
                             % numframes)

        if self.conserve_memory:
            if not self._cached == n:
                frame = self._getframe(n)
                self._cached = n
                self._cachedframe = frame
            return self._cachedframe
        else:
            return self._frames[n]

    def __iter__(self):
        """Iterate over the frames."""
        for i in range(len(self)):
            yield self[i]

    def __len__(self):
        """Number of images in collection."""
        return self._numframes

    def __str__(self):
        return str(self.filename) + ' [%s frames]' % self._numframes

    def concatenate(self):
        """Concatenate all images in the multi-image into an array.

        Returns
        -------
        ar : np.ndarray
            An array having one more dimension than the images in `self`.

        See Also
        --------
        concatenate_images

        Raises
        ------
        ValueError
            If images in the `MultiImage` don't have identical shapes.
        """
        return concatenate_images(self)


class ImageCollection(object):
    """Load and manage a collection of image files.

    Note that files are always stored in alphabetical order. Also note that
    slicing returns a new ImageCollection, *not* a view into the data.

    Parameters
    ----------
    load_pattern : str or list
        Pattern glob or filenames to load. The path can be absolute or
        relative.  Multiple patterns should be separated by os.pathsep,
        e.g. '/tmp/work/*.png:/tmp/other/*.jpg'.  Also see
        implementation notes below.
    conserve_memory : bool, optional
        If True, never keep more than one in memory at a specific
        time.  Otherwise, images will be cached once they are loaded.

    Other parameters
    ----------------
    load_func : callable
        ``imread`` by default.  See notes below.

    Attributes
    ----------
    files : list of str
        If a glob string is given for `load_pattern`, this attribute
        stores the expanded file list.  Otherwise, this is simply
        equal to `load_pattern`.

    Notes
    -----
    ImageCollection can be modified to load images from an arbitrary
    source by specifying a combination of `load_pattern` and
    `load_func`.  For an ImageCollection ``ic``, ``ic[5]`` uses
    ``load_func(file_pattern[5])`` to load the image.

    Imagine, for example, an ImageCollection that loads every tenth
    frame from a video file::

      class AVILoader:
          video_file = 'myvideo.avi'

          def __call__(self, frame):
              return video_read(self.video_file, frame)

      avi_load = AVILoader()

      frames = range(0, 1000, 10) # 0, 10, 20, ...
      ic = ImageCollection(frames, load_func=avi_load)

      x = ic[5] # calls avi_load(frames[5]) or equivalently avi_load(50)

    Another use of ``load_func`` would be to convert all images to ``uint8``::

      def imread_convert(f):
          return imread(f).astype(np.uint8)

      ic = ImageCollection('/tmp/*.png', load_func=imread_convert)

    Examples
    --------
    >>> import skimage.io as io
    >>> from skimage import data_dir

    >>> coll = io.ImageCollection(data_dir + '/lena*.png')
    >>> len(coll)
    2
    >>> coll[0].shape
    (512, 512, 3)

    >>> ic = io.ImageCollection('/tmp/work/*.png:/tmp/other/*.jpg')

    """
    def __init__(self, load_pattern, conserve_memory=True, load_func=None):
        """Load and manage a collection of images."""
        if isinstance(load_pattern, six.string_types):
            load_pattern = load_pattern.split(os.pathsep)
            self._files = []
            for pattern in load_pattern:
                self._files.extend(glob(pattern))
            self._files = sorted(self._files, key=alphanumeric_key)
        else:
            self._files = load_pattern

        if conserve_memory:
            memory_slots = 1
        else:
            memory_slots = len(self._files)

        self._conserve_memory = conserve_memory
        self._cached = None

        if load_func is None:
            from ._io import imread
            self.load_func = imread
        else:
            self.load_func = load_func

        self.data = np.empty(memory_slots, dtype=object)

    @property
    def files(self):
        return self._files

    @property
    def conserve_memory(self):
        return self._conserve_memory

    def __getitem__(self, n):
        """Return selected image(s) in the collection.

        Loading is done on demand.

        Parameters
        ----------
        n : int or slice
            The image number to be returned, or a slice selecting the images
            and ordering to be returned in a new ImageCollection.

        Returns
        -------
        img : ndarray or ImageCollection.
            The `n`-th image in the collection, or a new ImageCollection with
            the selected images.

        """
        if hasattr(n, '__index__'):
            n = n.__index__()

        if type(n) not in [int, slice]:
            raise TypeError('slicing must be with an int or slice object')

        if type(n) is int:
            n = self._check_imgnum(n)
            idx = n % len(self.data)

            if (self.conserve_memory and n != self._cached) or \
                (self.data[idx] is None):
                self.data[idx] = self.load_func(self.files[n])
                self._cached = n

            return self.data[idx]
        else:
            # A slice object was provided, so create a new ImageCollection
            # object. Any loaded image data in the original ImageCollection
            # will be copied by reference to the new object.  Image data
            # loaded after this creation is not linked.
            fidx = range(len(self.files))[n]
            new_ic = copy(self)
            new_ic._files = [self.files[i] for i in fidx]
            if self.conserve_memory:
                if self._cached in fidx:
                    new_ic._cached = fidx.index(self._cached)
                    new_ic.data = np.copy(self.data)
                else:
                    new_ic.data = np.empty(1, dtype=object)
            else:
                new_ic.data = self.data[fidx]
            return new_ic

    def _check_imgnum(self, n):
        """Check that the given image number is valid."""
        num = len(self.files)
        if -num <= n < num:
            n = n % num
        else:
            raise IndexError("There are only %s images in the collection"
                             % num)
        return n

    def __iter__(self):
        """Iterate over the images."""
        for i in range(len(self)):
            yield self[i]

    def __len__(self):
        """Number of images in collection."""
        return len(self.files)

    def __str__(self):
        return str(self.files)

    def reload(self, n=None):
        """Clear the image cache.

        Parameters
        ----------
        n : None or int
            Clear the cache for this image only. By default, the
            entire cache is erased.

        """
        self.data = np.empty_like(self.data)

    def concatenate(self):
        """Concatenate all images in the collection into an array.

        Returns
        -------
        ar : np.ndarray
            An array having one more dimension than the images in `self`.

        See Also
        --------
        concatenate_images

        Raises
        ------
        ValueError
            If images in the `ImageCollection` don't have identical shapes.
        """
        return concatenate_images(self)


def imread_collection_wrapper(imread):
    def imread_collection(load_pattern, conserve_memory=True):
        """Return an `ImageCollection` from files matching the given pattern.

        Note that files are always stored in alphabetical order. Also note that
        slicing returns a new ImageCollection, *not* a view into the data.

        See `skimage.io.ImageCollection` for details.

        Parameters
        ----------
        load_pattern : str or list
            Pattern glob or filenames to load. The path can be absolute or
            relative.  Multiple patterns should be separated by a colon,
            e.g. '/tmp/work/*.png:/tmp/other/*.jpg'.  Also see
            implementation notes below.
        conserve_memory : bool, optional
            If True, never keep more than one in memory at a specific
            time.  Otherwise, images will be cached once they are loaded.

        """
        return ImageCollection(load_pattern, conserve_memory=conserve_memory,
                               load_func=imread)
    return imread_collection
