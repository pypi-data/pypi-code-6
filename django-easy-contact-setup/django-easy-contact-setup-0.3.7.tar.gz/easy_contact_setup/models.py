#!/usr/bin/python
# -*- coding:utf-8 -*-
# This Python file uses the following encoding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_fields.fields import EncryptedCharField


class Setup(models.Model):
    active = models.BooleanField(help_text=_(u'Activate or disable this settings object.'),
                                verbose_name=_('Active'))
    slug = models.SlugField(verbose_name=_('Name'), unique=True,
                                help_text=_(u'Give this setting an uniqe name. '\
                                    u'No spaces and special character allowed.'))
    mail_to = models.EmailField(max_length=50, verbose_name=_('Your email'),
            help_text=_(u' This will be the email adress your mails are going to. '\
            u'If necessary the application also use it as sender adress.'))
    mail_host = EncryptedCharField(blank=True, max_length=50, verbose_name=_('Mail server'),
            help_text=_(u'Your smtp server, i.e.: mail.yourprovider.something '\
            u'or smtp.yourprovider.something. Make shure that the specified server '\
            u'belongs to the mail adress your specified above!'))
    mail_host_user = EncryptedCharField(blank=True, max_length=50, verbose_name=_('Username'),
                    help_text=_(u'Smptp server user name. Mostly user or login '\
                    u'name to your mail account. Usaly your email adress'))
    mail_host_pass = EncryptedCharField(
                        blank=True, max_length=50, verbose_name=_('Password'),
                        help_text=_(u'Smtp server password. Mostly the login '\
                        u'password to your mail account.'))

    class Meta:
        verbose_name = _('Contact form setting')
        verbose_name_plural = _('Contact form settings')

    def __unicode__(self):
        return self.slug
