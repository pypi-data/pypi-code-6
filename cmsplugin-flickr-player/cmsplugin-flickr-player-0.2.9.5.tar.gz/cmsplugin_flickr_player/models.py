# coding: utf-8
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin


class FlickrLink(CMSPlugin):
    url = models.URLField(
        _("link"),
        help_text=_(u"Format: https://www.flickr.com/photos/#username#/sets/#id#"))
    width = models.CharField(
        _(u"width"),
        default=getattr(settings, "CMS_FLICKR_PLAYER_WIDTH", "100%"),
        max_length=5,
        null=True,
        blank=True)
    height = models.CharField(
        _(u"height"),
        default=getattr(settings, "CMS_FLICKR_PLAYER_HEIGHT", "500"),
        max_length=5,
        null=True,
        blank=True)

    class Meta:
        verbose_name, verbose_name_plural = _(u"flickr link"), _(u"flickr links")

    def __unicode__(self):
        return self.url

    search_fields = ('url', )
