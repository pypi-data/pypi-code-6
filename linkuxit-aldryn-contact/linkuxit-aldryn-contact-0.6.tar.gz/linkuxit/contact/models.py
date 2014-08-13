# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin


class ContactPlugin(CMSPlugin):
    site_email = models.EmailField(_('Email reciepient'))
    email_label = models.CharField(_('Email sender label'), max_length=100)
    subject_label = models.CharField(_('Subject label'), max_length=200)
    content_label = models.CharField(_('Message content label'), max_length=100)
    thanks = models.CharField(_('Message displayed on successful submit'), max_length=200)
    submit = models.CharField(_('Submit button value'), blank=True, max_length=30)

    def __unicode__(self):
        return self.site_email


class Message(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    content = models.TextField()

    def __unicode__(self):
        return u'%s(%s)' % (self.subject, self.email)
