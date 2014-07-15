from __future__ import division
from PIL import Image
from alurinium.image.filters.base import ImageFilter
from six import string_types
import re
import sys
import math


SIZE_PATTERN = re.compile(r"^(?P<width>\d+)?(x(?P<height>\d+))?$")
INTEGER_MAX = getattr(sys, 'maxsize', getattr(sys, 'maxint', None))


class ResizeFilter(ImageFilter):
    """
    Create thumbnail for image
    """
    def __init__(self):
        super(ResizeFilter, self).__init__()

        self.size = None
        self.is_full = False

    @staticmethod
    def reinterpret_size(size):
        """ Parse size as sorl.thumbnail"""
        if isinstance(size, string_types):
            result = SIZE_PATTERN.match(size)
            if result:
                width = int(result.group('width')) if result.group('width') else None
                height = int(result.group('height')) if result.group('height') else None
                return (width, height)
        elif isinstance(size, tuple):
            if len(size) == 2:
                return size
        raise ValueError("Size must be tuple of two elements or string in '[width]x[height]' format")

    def initialize(self, size=None, **options):
        if size:
            self.size = self.reinterpret_size(size)
            self.is_full = self.normalize_size == self.size
        self.is_enabled = bool(self.size)

    @property
    def normalize_size(self):
        """
        Correct size

        :return: correct size
        """
        size = self.size
        size = (INTEGER_MAX, size[1]) if not size[0] else size
        size = (size[0], INTEGER_MAX) if not size[1] else size

        return size

    def process_image(self, image, options):
        thumbnail_image = image.copy()
        thumbnail_image.thumbnail(self.normalize_size, Image.ANTIALIAS)

        if self.is_full:
            # preserve image format
            options.is_preserve_format = False

            # expand image to size
            size = thumbnail_image.size
            x = int(math.ceil(float(self.size[0] - size[0]) / 2))
            y = int(math.ceil(float(self.size[1] - size[1]) / 2))
            resize_image = Image.new(thumbnail_image.mode, self.size)
            resize_image.paste(thumbnail_image, (x, y, x + size[0], y + size[1]))
            thumbnail_image = resize_image
        return thumbnail_image
