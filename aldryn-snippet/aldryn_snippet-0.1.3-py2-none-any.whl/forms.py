# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings

from .models import SnippetPlugin


class SnippetForm(forms.ModelForm):
    class Meta:
        model = SnippetPlugin
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'rows': '30',
                    'data-editor': True,
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super(SnippetForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({
            'data-mode': getattr(settings, 'ALDRYN_SNIPPET_ACE_MODE', 'ace/mode/html'),
            'data-theme': getattr(settings, 'ALDRYN_SNIPPET_ACE_THEME', 'ace/theme/monokai'),
        })
