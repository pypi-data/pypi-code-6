from __future__ import unicode_literals

from django import forms
from django.contrib import admin

from ckeditor.widgets import CKEditorWidget
from .models import EmailTemplate


class EmailTemplateAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = EmailTemplate


class EmailTemplateAdmin(admin.ModelAdmin):
    form = EmailTemplateAdminForm


admin.site.register(EmailTemplate, EmailTemplateAdmin)
