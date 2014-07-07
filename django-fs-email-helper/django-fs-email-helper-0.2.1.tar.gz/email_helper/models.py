# coding=utf-8

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils import timezone


class Email(models.Model):
    when = models.DateTimeField(verbose_name=_(u'when'), default=timezone.now())
    whom = models.CharField(verbose_name=_(u'whom'), max_length=254)
    subject = models.CharField(verbose_name=_(u'subject'), max_length=254)
    body = models.TextField(verbose_name=_(u'body'))
    status = models.CharField(verbose_name=_(u'status'), max_length=254)

    class Meta:
        verbose_name = _(u'email')
        verbose_name_plural = _(u'emails')

    def __unicode__(self):
        return ugettext(u'Email #{0}').format(self.id)
