from .models import Message

from django.contrib import admin

class MessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'email']


admin.site.register(Message, MessageAdmin)
