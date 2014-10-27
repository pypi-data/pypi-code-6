# -*- coding: utf-8 -*-

"""
Models for the "rstamper" project
"""

import time
import socket
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.template.defaultfilters import slugify
from django.conf import settings as conf

from rtimes import worktime, humanize_time


class Customer(models.Model):

    """
    Modelo that defines a customer.
    """

    name = models.CharField(_(u'Customer'), max_length=255, unique=True)

    def __unicode__(self):
        return str(self.name)

    class Meta:
        verbose_name = _(u'Customer')
        verbose_name_plural = _(u'Customers')


class Stamp(models.Model):

    """
    Modelo that defines a stamp.
    """

    action = models.TextField(_(u'Action'), max_length=255, null=True)
    customer = models.ForeignKey(Customer, related_name='customer')
    start = models.DateTimeField(_(u'Start date'))
    end = models.DateTimeField(_(u'End date'), null=True)

    def __unicode__(self):
        return "[%s - %s] %s - %s" % (self.start, self.end, self.customer,
                                      self.action)

    def mins(self):
        mins = worktime(self.start.strftime("%Y-%m-%d %H:%M"),
                        self.end.strftime("%Y-%m-%d %H:%M"))
        return humanize_time(mins)

    class Meta:
        verbose_name = _(u'Stamp')
        verbose_name_plural = _(u'Stamps')

