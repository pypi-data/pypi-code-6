import logging

from ..datetime import now

from django.template.defaultfilters import date as datefilter

from django import template


__all__ = ['sicklenow', 'sickletoday']


register = template.Library()


@register.simple_tag
def sicklenow(format_string="SHORT_DATETIME_FORMAT"):
    s = datefilter(now(), format_string)
    return s
