# coding: utf-8
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .forms import FlickrLinkForm
from .models import FlickrLink


class FlickrPlayerPlugin(CMSPluginBase):
    model = FlickrLink
    form = FlickrLinkForm
    name = _(u"Flickr player")
    render_template = "cms/plugins/flickr_player.html"

    def render(self, context, instance, placeholder):
        width = instance.width or getattr(settings, "CMS_FLICKR_PLAYER_WIDTH", "100%")
        height = instance.height or getattr(settings, "CMS_FLICKR_PLAYER_HEIGHT", "500")

        url = instance.url
        if url.startswith(u"http://") or url.startswith(u"https://"):
            url = url.replace(u"http://", u"//").replace(u"https://", u"//")
        url = u"%s/player" % url

        context.update({
            'width': width,
            'height': height,
            'url': url,
            'placeholder': placeholder,
            'object': instance
        })
        return context

plugin_pool.register_plugin(FlickrPlayerPlugin)
