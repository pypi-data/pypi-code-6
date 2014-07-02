# -*- coding: utf-8 -*-
from django.contrib import admin
from email_filter.models import EmailLog, EmailRedirect, EmailAttachment


class EmailAttachmentInline(admin.TabularInline):
    model = EmailAttachment


class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'subject', 'created']
    search_fields = ['sender', 'recipient', 'subject']
    list_filter = ['created', ]
    inlines = [EmailAttachmentInline]


admin.site.register(EmailLog, EmailLogAdmin)
admin.site.register(EmailAttachment)
admin.site.register(EmailRedirect, admin.ModelAdmin)
