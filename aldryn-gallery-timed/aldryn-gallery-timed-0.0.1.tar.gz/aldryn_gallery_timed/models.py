# -*- coding: utf-8 -*-
from django.db import models
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin
from cms.models.fields import PageField

from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField
from django.utils.timezone import now



class TimedSlidePlugin(CMSPlugin):
    LINK_TARGETS = (
        ('', _('same window')),
        ('_blank', _('new window')),
        ('_parent', _('parent window')),
        ('_top', _('topmost frame')),
    )
    publication_start = models.DateTimeField(_('Published Since'),
                                             default=now)
    publication_end = models.DateTimeField(_('Published Until'),
                                           null=True, blank=True)
    image = FilerImageField(verbose_name=_('image'), blank=True, null=True)
    content = HTMLField("Content", blank=True, null=True)
    url = models.URLField(_("Link"), blank=True, null=True)
    page_link = PageField(
        verbose_name=_('Page'),
        blank=True,
        null=True,
        help_text=_("A link to a page has priority over a text link.")
    )
    target = models.CharField(
        verbose_name=_("target"),
        max_length=100,
        blank=True,
        choices=LINK_TARGETS,
    )


    def __unicode__(self):
        image_text = content_text = None

        if self.image_id:
            image_text = u'%s' % (self.image.name or self.image.original_filename)
        if self.content:
            text = strip_tags(self.content).strip()
            if len(text) > 100:
                content_text = u'%s...' % text[:100]
            else:
                content_text = u'%s' % text

        if image_text and content_text:
            return u'%s (%s)' % (image_text, content_text)
        else:
            return image_text or content_text

    def get_link(self):
        if self.page_link_id:
            return self.page_link.get_absolute_url()
        if self.url:
            return self.url
        return False

    @property
    def is_published(self):
        start = self.publication_start
        end = (self.publication_end
               if self.publication_end else None)
        if start <= now() and (not end or end >= now()):
            return True
        return False


