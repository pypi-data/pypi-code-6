import json
from alurinium.image.processor import ImageProcessor

from django.core.files.images import ImageFile
from alurinium.image.keystores import RedisKeystore
from alurinium.image.image import ImageDescriptor
from six import string_types
import hashlib


class Engine(object):
    """
    Instance of this class is represented image processing engine for use within Django or Jinja environment
    """
    keystore = None

    def __init__(self):
        self.keystore = RedisKeystore()

    def get_output_filename(self, original_filename, **options):
        token = json.dumps(options, sort_keys=True)
        token = u"%s.%s" % (original_filename, token)
        token = token.encode("utf-8")

        m = hashlib.sha256()
        m.update(token)
        return m.hexdigest()

    def get_image_descriptor(self, image):
        if isinstance(image, ImageFile):
            return ImageDescriptor.create_from_file(image.path)
        elif isinstance(image, string_types):
            return ImageDescriptor.create_from_file(image)
        elif not image:
            return None
        raise ValueError("")

    def process_image(self, original_image, **options):
        # Returns descriptor for original image descriptor
        original = self.get_image_descriptor(original_image)
        if original:
            # Generate result filename
            result_filename = self.get_output_filename(original.url, **options)

            # Check if result filename is exist, by cache
            result_image = self.keystore.get(result_filename)
            if not result_image:
                result_image = ImageDescriptor.create_from_file(result_filename, parse=False)
                result_image = self.do_process_image(result_filename, original, result_image, **options)
            return result_image
        return None

    def do_process_image(self, id, original, result, **options):
        # initialize image processor
        processor = ImageProcessor()
        processor.initialize(**options)

        # process image and store information in keystore
        output_filename, output_image = processor.process_file(original.fullname, result.fullname)
        result = ImageDescriptor.create_from_image(output_filename, output_image)
        self.keystore.set(id, result)
        return result


def get_engine():
    return Engine()
