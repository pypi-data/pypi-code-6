from alurinium.image.color import Color


class ImageOptions(object):
    """
    :ivar is_preserve_format: Preserve image mode
    """
    is_preserve_format = True


class ImageFilter(object):
    def __init__(self):
        self.is_enabled = False

    def initialize(self, **options):
        """
        Initialize image filter and enabled it, if required

        :param options: dict with image processing options
        :return:
        """
        pass

    def process_image(self, image, options):
        """
        Process image over filter

        :param image: Input image, before filtering
        :return: Output image, after filtering
        """
        raise NotImplementedError()


class PixelImageFilter(ImageFilter):
    def process_pixel(self, color, options):
        raise NotImplementedError()

    def process_image(self, image, options):
        new_data = []
        for item in image.getdata():
            old_color = Color(item[0], item[1], item[2], item[3])
            new_color = self.process_pixel(old_color, options)
            new_color.normalize()
            new_data.append(new_color.to_tuple)
        image.putdata(new_data)
        return image
