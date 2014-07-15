from alurinium.image.base import get_engine
from django import template


register = template.Library()


@register.assignment_tag()
def process_image(image, **options):
    # try:
    engine = get_engine()
    return engine.process_image(image, **options)
    # except Exception as e:
    #     pass
