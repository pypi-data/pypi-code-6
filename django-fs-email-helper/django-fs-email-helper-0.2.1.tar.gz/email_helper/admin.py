# coding=utf-8

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from email_helper.models import Email


class EmailAdmin(admin.ModelAdmin):
    list_display = ['when', 'whom', 'subject', 'status']
    search_fields = ['whom', 'subject']
    readonly_fields = ['_body']
    fieldsets = [
        [None, {'fields': ['when', 'whom', 'subject', 'status']}],
        [None, {'fields': ['_body']}],
    ]

    def _body(self, obj):
        return obj.body
    _body.short_description = _(u'body')
    _body.allow_tags = True


admin.site.register(Email, EmailAdmin)
