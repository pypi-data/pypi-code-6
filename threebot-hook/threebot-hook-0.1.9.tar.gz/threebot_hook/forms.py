from django import forms
from .models import Hook


class HookCreateForm(forms.ModelForm):
    class Meta:
        model = Hook
        fields = ['slug', 'slug', 'repo', 'secret', 'workflow', 'worker', 'param_list', ]
        widgets = {
            'slug': forms.TextInput(attrs={'class': 'form-control', }),
            'user': forms.TextInput(attrs={'class': 'form-control', }),
            'repo': forms.TextInput(attrs={'class': 'form-control', }),
            'secret': forms.TextInput(attrs={'class': 'form-control', }),
            'workflow': forms.HiddenInput(),
            'worker': forms.Select(attrs={'class': 'form-control', }),
            'param_list': forms.Select(attrs={'class': 'form-control', }),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.workflow = kwargs.pop('workflow')
        super(HookCreateForm, self).__init__(*args, **kwargs)
        self.fields['workflow'].initial = self.workflow


class HookEditForm(HookCreateForm):
    class Meta(HookCreateForm.Meta):
        exclude = ('owner',)
