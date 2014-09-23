from django import forms
from django.contrib import admin

from emailer.models import ConnectionProfile, EmailTemplate


class ConnectionProfileAdmin(admin.ModelAdmin):

    class form(forms.ModelForm):

        class Meta:
            model = ConnectionProfile
            widgets = {
                'password': forms.PasswordInput,
            }


class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'connection_profile',)


admin.site.register(ConnectionProfile, ConnectionProfileAdmin)
admin.site.register(EmailTemplate, EmailTemplateAdmin)
