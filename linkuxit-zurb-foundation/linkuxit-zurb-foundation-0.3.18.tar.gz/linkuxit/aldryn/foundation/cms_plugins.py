# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import OrbitItemPlugin
from .models import OrbitPlugin


class FoundationBase(CMSPluginBase):
    module = 'Foundation'


class OrbitItemInline(admin.StackedInline):
    model = OrbitItemPlugin
    extra = 0


class OrbitCMSPlugin(FoundationBase):
    name = _('Orbit')
    model = OrbitPlugin
    render_template = 'aldryn/plugins/foundation/orbit.html'

    inlines = [
        OrbitItemInline,
    ]

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context

plugin_pool.register_plugin(OrbitCMSPlugin)
