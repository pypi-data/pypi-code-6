from __future__ import absolute_import

from django import forms

from .models import GenericPhoto


class PhotoForm(forms.ModelForm):
    class Meta:
        model = GenericPhoto
        exclude = ('main', 'content_type', 'object_id', 'crop_from', 'effect')
