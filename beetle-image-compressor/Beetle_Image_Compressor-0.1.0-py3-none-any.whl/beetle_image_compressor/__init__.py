from PIL import Image
from io import BytesIO


def compress(content, suggested_path):
    buffer_file = BytesIO(content)
    img = Image.open(buffer_file)
    img.save(buffer_file, 'JPEG', quality=60)
    return suggested_path, buffer_file.getvalue()


def register(context, plugin_config):
    jpeg_extensions = ['jpeg', 'jpg']
    context.includer.add(jpeg_extensions, compress)
