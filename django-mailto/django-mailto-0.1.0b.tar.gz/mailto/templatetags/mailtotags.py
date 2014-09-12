# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.inclusion_tag('mailto/includes/placeholder.html', takes_context=True)
def placeholder(context, placeholder_name, *args, **kwargs):
    context['placeholder_id'] = placeholder_name
    context['placeholder'] = mark_safe(context.get('placeholder-%s' % placeholder_name, ''))
    return context