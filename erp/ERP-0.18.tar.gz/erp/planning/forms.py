__author__ = 'cltanuki'
from django import forms

from . import models


class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = '__all__'
        widgets = {'prj': forms.HiddenInput()}


class TmplTaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = '__all__'
        widgets = {
            'prj': forms.HiddenInput(),
            'responsible': forms.HiddenInput(),
            'performer': forms.HiddenInput(),
            'prj': forms.HiddenInput()

        }


class PrjTmplForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = '__all__'