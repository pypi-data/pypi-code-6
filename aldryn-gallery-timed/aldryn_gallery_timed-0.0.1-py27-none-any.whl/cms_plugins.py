# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from .models import TimedSlidePlugin
from aldryn_gallery.models import GalleryPlugin

class TimedSlideCMSPlugin(CMSPluginBase):
    module = _('Gallery')
    name = _('Timed Slide')
    parent_classes = ['GalleryCMSPlugin']
    require_parent = True
    model = TimedSlidePlugin
    render_template = False

    def render(self, context, instance, placeholder):
        # get style from parent plugin, render chosen template
        self.render_template = self.get_slide_template(instance)
        context['instance'] = instance
        context['image'] = instance.image
        return context

    def get_slide_template(self, instance):
        if instance.is_published:
            return 'aldryn_gallery/plugins/%s/slide.html' % getattr(
            instance.parent.get_plugin_instance()[0], 'style',  GalleryPlugin.STANDARD)
        else:
            return 'aldryn_gallery/empty.html'


plugin_pool.register_plugin(TimedSlideCMSPlugin)

from aldryn_gallery.cms_plugins import GalleryCMSPlugin

if not 'TimedSlideCMSPlugin' in GalleryCMSPlugin.child_classes:
    GalleryCMSPlugin.child_classes.append('TimedSlideCMSPlugin')
