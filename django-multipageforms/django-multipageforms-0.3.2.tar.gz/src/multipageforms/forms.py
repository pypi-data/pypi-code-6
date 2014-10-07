from __future__ import unicode_literals

from collections import OrderedDict
import logging
import copy

from django import forms
from django.utils.safestring import mark_safe

LOGGER = logging.getLogger(__name__)

class ControlFormMixin(forms.Form):
    seen = forms.NullBooleanField(widget=forms.HiddenInput)

    def initialize(self, initial=None, instance=None, **kwargs):
        self.instance = instance or self.instance or None
        self.initial = initial or self.initial or None
        form_initial = {}
        prefix = self.prefix
        if self.initial is not None:
            form_initial = self.initial or {}
        form = Form(prefix=prefix, initial=form_initial)
        return self

    @property
    def is_seen(self):
        if self.is_valid() and self.cleaned_data['seen']:
            return True
        return False

    def seen(self):
        # Set seen status in ControlForm
        if not self.is_bound:
            return
        data = self.data.copy()
        data[self.prefix+'-seen'] = True
        self.data = data

class PreviewMixin(object):

    def preview(self):
        lines = []
        for field in self:
            label = field.label
            data = ''
            name = field.name
            if self.is_valid():
                data = form.cleaned_data[name]
            lines.append((label, data))
        return lines
