from alurinium.image.base import Engine


def process_image(original_filename, output_filename=None, **options):
    engine = Engine()
    return engine.process_image(original_filename, output_filename, **options)