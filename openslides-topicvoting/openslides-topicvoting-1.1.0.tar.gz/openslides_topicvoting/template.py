# -*- coding: utf-8 -*-

from django.dispatch import receiver

from openslides.utils.signals import template_manipulation


@receiver(template_manipulation, dispatch_uid="add_topicvoting_stylesheets")
def add_topicvoting_stylesheets(sender, request, context, **kwargs):
    """
    Adds the openslides_topicvoting.css to the context.
    """
    context['extra_stylefiles'].append('styles/openslides_topicvoting.css')
