import os
import errno
from PIL import Image
from alurinium.image.filters.base import ImageOptions
from alurinium.image.filters.grayscale import GrayscaleFilter
from alurinium.image.filters.resize import ResizeFilter


BUILTIN_FILTERS = (
    ResizeFilter,
    GrayscaleFilter,
)


def mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exc:      # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class ImageProcessor(object):
    filters = None

    def __init__(self):
        self.filters = []

    def initialize(self, **options):
        """
        Initialize all filters

        :param options: dict with image processing options
        """
        for filter_class in BUILTIN_FILTERS:
            filter = filter_class()
            filter.initialize(**options)
            self.filters.append(filter)

    def process_image(self, image):
        """
        Process image over filters.

        :param image: Initial image for processing
        :return: Return image in input image mode
        """
        # Convert image copy to RGBA mode
        process_image = image.convert('RGBA')

        # Process image over filters
        options = ImageOptions()
        for filter in self.filters:
            if filter.is_enabled:
                process_image = filter.process_image(process_image, options)

        # Return final image ant it options
        return options, process_image

    def process_file(self, original_filename, output_filename):
        # process image
        original = Image.open(original_filename)
        options, result = self.process_image(original)

        # preserve format if required
        if options.is_preserve_format:
            output_mode = original.mode
            output_extension = os.path.splitext(original_filename)[1]
        else:
            output_mode = "PNG"
            output_extension = ".png"
        output_filename += output_extension

        # save result image
        mkdir(os.path.dirname(output_filename))
        result.save(output_filename, mode=output_mode)
        return output_filename, result
