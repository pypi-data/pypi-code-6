# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext as _

class ImportDataForm(forms.Form):
    required_css_class = 'required'
    def __init__(self, *args, **kws):
        super(ImportDataForm, self).__init__(*args, **kws)
        self.fields['import_file'] = forms.FileField(
            label=_('File Data to upload'),
        )

    def clean_import_file(self):
        if not self.cleaned_data['import_file']:
            raise forms.ValidationError(_('Upload excel file'))
        return self.cleaned_data['import_file']

class ExportDataForm(forms.Form):
    required_css_class = 'required'