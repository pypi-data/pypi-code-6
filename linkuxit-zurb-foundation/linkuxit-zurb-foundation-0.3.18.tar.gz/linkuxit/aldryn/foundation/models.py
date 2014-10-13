# -*- coding: utf-8 -*-
from django.utils.html import strip_tags
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin

from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField


class OrbitItemPlugin(models.Model):
    orbit = models.ForeignKey('foundation.OrbitPlugin', related_name='items')
    image = FilerImageField(verbose_name=_('image'), blank=True, null=True)
    content = HTMLField("Content", blank=True, null=True)

    def __unicode__(self):
        name = u'%s' % (self.image.name or self.image.original_filename) if self.image else 'No image'
        if self.content:
            text = strip_tags(self.content).strip()
            if len(text) > 100:
                name += u' (%s...)' % text[:100]
            else:
                name += u' (%s)' % text
        return name


class OrbitPlugin(CMSPlugin):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

    def copy_relations(self, oldinstance):
        for item in oldinstance.items.all():
            # instance.pk = None; instance.pk.save() is the slightly odd but
            # standard Django way of copying a saved model instance
            item.pk = None
            item.orbit = self
            item.save()
