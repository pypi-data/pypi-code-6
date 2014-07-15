from alurinium.image.color import Color
from alurinium.image.filters.base import PixelImageFilter


class GrayscaleFilter(PixelImageFilter):
    def __init__(self):
        super(GrayscaleFilter, self).__init__()
        self.mode = None

    def initialize(self, grayscale=None, **options):
        if grayscale in ('lightness', 'averages', 'luminosity'):
            self.mode = grayscale
        elif grayscale:
            self.mode = 'luminosity'
        self.is_enabled = bool(self.mode)

    @staticmethod
    def lightness(c):
        i = (max(c.r, c.g, c.b) + min(c.r, c.g, c.b)) / 2
        return Color(i, i, i, c.a)

    @staticmethod
    def averages(c):
        i = (c.r + c.g + c.b) / 3
        return Color(i, i, i, c.a)

    @staticmethod
    def luminosity(c):
        i = 0.21 * c.r + 0.72 * c.g + 0.07 * c.b
        return Color(i, i, i, c.a)

    def process_pixel(self, c, options):
        process_pixel = getattr(self, self.mode, None)
        return process_pixel(c)
