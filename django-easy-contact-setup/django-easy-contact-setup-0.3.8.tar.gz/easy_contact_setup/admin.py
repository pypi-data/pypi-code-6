#!/usr/bin/python
# -*- coding:utf-8 -*-
# This Python file uses the following encoding: utf-8

from models import Setup
from django.contrib import admin
from forms import SetupForm
from django.utils.translation import ugettext_lazy as _


class SetupAdmin(admin.ModelAdmin):
    list_display = ('slug', 'active')

    fieldsets = (
            (_(u'Settings'), {
                'fields': ('active', 'slug', 'mail_to',)
            }),
            (_(u'Optional settings - custom smtp server setup'), {
                'classes': ('collapse',),
                'fields': ('mail_host', 'mail_host_user', 'mail_host_pass')
            }),
            )

    form = SetupForm
admin.site.register(Setup, SetupAdmin)
