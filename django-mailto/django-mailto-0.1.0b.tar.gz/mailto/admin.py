# -*- coding: utf-8 -*-
from django.contrib import admin
from mailto.forms import MailAdminForm

from mailto.models import Mail, UserOptin


class MailAdmin(admin.ModelAdmin):
    form = MailAdminForm
    list_display = ['slug', 'subject', 'active', 'optout', 'language_code']
    list_filter = ['slug', 'active', 'optout', 'language_code']
    fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': (
                    'active', 'slug', 'language_code', 'template',
            )
        }),
        (None, {
            'classes': ('wide', ),
            'fields': (
                ('sender_email', 'sender_name', ),
                'reply_to',
                'cc', 'bcc',
            )
        }),
        (None, {
            'classes': ('wide', ),
            'fields': (
                'subject', 'plain', 'html',
            )
        }),
        ('Advanced options', {
            'classes': ('wide', 'collapse',),
            'fields': ('optout',)
        }),
    )

    class Media:
        js = (
            'mailto/js/mail.js',
        )
        css = {
            'all': ('mailto/css/mail.css', )
        }


class UserOptinAdmin(admin.ModelAdmin):
    list_display = ['user', 'optin', 'date_added', 'date_changed']


admin.site.register(Mail, MailAdmin)
admin.site.register(UserOptin, UserOptinAdmin)