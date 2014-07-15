from django.conf import settings
from PIL import Image
import os

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

class ImageDescriptor(object):
    name = None
    url = None
    fullname = None
    width = None
    height = None

    @classmethod
    def create_from_file(cls, filename, parse=True):
        image = cls()
        image.name = filename
        image.url = urljoin(settings.MEDIA_URL, 'thumbs/' + filename)
        image.fullname = os.path.join(settings.MEDIA_ROOT, 'thumbs', filename)

        # get image size
        # TODO: Add exception handling
        if parse:
            image.update()

        # return result image
        return image


    @classmethod
    def create_from_image(cls, fullname, result_image):
        image = cls()
        image.fullname = fullname
        image.name = os.path.basename(fullname)
        image.url = urljoin(settings.MEDIA_URL, 'thumbs/' + image.name)

        # get image size
        # TODO: Add exception handling
        image.update(result_image)

        # return result image
        return image

    def update(self, image=None):
        if not image:
            image = Image.open(self.fullname)
        image.width, image.height = image.size

    def __str__(self):
        return "%s: %sx%s" % (self.url, self.width, self.height)