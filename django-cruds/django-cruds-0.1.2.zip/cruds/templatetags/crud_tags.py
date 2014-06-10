# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import six

from django.db.models import Model
from django import template
from django.core.urlresolvers import (
    NoReverseMatch,
    reverse,
)
from django.utils.html import escape
from django.utils.safestring import mark_safe

from cruds import utils


register = template.Library()


@register.filter
def get_attr(obj, attr):
    """
    Filter returns obj attribute.
    """
    return getattr(obj, attr)


@register.assignment_tag
def crud_url(obj, action):
    try:
        url = reverse(
            utils.crud_url_name(type(obj), action),
            kwargs={'pk': obj.pk})
    except NoReverseMatch:
        url = None
    return url


@register.filter
def format_value(obj, field_name):
    """
    Simple value formatting.

    If value is model instance returns link to detail view if exists.
    """
    value = getattr(obj, field_name)
    if isinstance(value, Model):
        url = crud_url(value, utils.ACTION_DETAIL)
        if url:
            return mark_safe('<a href="%s">%s</a>' % (url, escape(value)))
    return value


@register.inclusion_tag('cruds/templatetags/crud_fields.html')
def crud_fields(obj, fields=None):
    """
    Display object fields in table rows::

        <table>
            {% crud_fields object 'id, %}
        </table>

    * ``fields`` fields to include

        If fields is ``None`` all fields will be displayed.
        If fields is ``string`` comma separated field names will be
        displayed.
        if field is dictionary, key should be field name and value
        field verbose name.
    """
    if fields is None:
        fields = utils.get_fields(type(obj))
    elif isinstance(fields, six.string_types):
        field_names = [f.strip() for f in fields.split(',')]
        fields = utils.get_fields(type(obj), include=field_names)
    return {
        'object': obj,
        'fields': fields,
    }
