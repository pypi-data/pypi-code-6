from django import forms


class ImportTagsForm(forms.Form):
    file = forms.FileField()

