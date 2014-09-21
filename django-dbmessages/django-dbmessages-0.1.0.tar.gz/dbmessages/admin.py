#coding: utf-8

from django.contrib import admin
from .models import Message


class MessageAdmin(admin.ModelAdmin):
    raw_id_fields = ['to_user']
    list_filter = ['level']


admin.site.register(Message, MessageAdmin)
