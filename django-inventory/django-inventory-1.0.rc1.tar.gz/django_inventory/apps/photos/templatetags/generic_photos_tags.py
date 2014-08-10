from __future__ import absolute_import

from django.template import Library, Node, Variable
from django.template.defaultfilters import stringfilter

from ..models import GenericPhoto

register = Library()


@register.filter
def get_photos_for_object(value):
    return GenericPhoto.objects.photos_for_object(value)
