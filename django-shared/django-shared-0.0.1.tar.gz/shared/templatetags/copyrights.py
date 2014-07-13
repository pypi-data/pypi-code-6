from django import template
from django.utils.timezone import now

from shared import app_settings


register = template.Library()


@register.simple_tag(takes_context=False)
def copyright_years():
    year_start = app_settings.COPYRIGHT_YEAR_START
    return year_start if year_start == now().year else '%s - %s' % (year_start, now().year)
