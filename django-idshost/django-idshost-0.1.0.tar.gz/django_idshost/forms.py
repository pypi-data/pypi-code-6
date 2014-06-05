from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django_idshost.models import IdsUser


class IdsUserForm(forms.ModelForm):

    confirm_password = forms.CharField(widget=forms.PasswordInput,
                                       label=_("Confirm the password."),
                                       required=True)
    with_named_cert = forms.BooleanField(initial=False, required=False)

    class Meta:
        model = IdsUser
        fields = ['username', 'email', 'password', 'confirm_password',
                  'with_named_cert']

    def __init__(self, *args, **kwargs):
        super(IdsUserForm, self).__init__(*args, **kwargs)
        if self.fields.get('username'):
            self.fields['username'].help_text = ''
        if self.fields.get('email'):
            self.fields['email'].required = True
        if self.fields.get('password'):
            self.fields['password'].widget = forms.PasswordInput()
            self.fields['password'].label = _("Password")

    def clean(self, *args, **kwargs):
        cleaned_data = super(IdsUserForm, self).clean(*args, **kwargs)
        pwd = cleaned_data.get('password')
        conf_pwd = cleaned_data.get('confirm_password')
        if pwd and conf_pwd and pwd != conf_pwd:
            self.errors['confirm_password'] = self.error_class(
                [_('Different')])
        return self.cleaned_data

    def save(self, commit=True):
        mask = 8 if self.cleaned_data['with_named_cert'] else None
        user = get_user_model(
        ).objects.create_user(self.cleaned_data['username'],
                              mask, self.cleaned_data['email'],
                              self.cleaned_data['password'],
                              commit=commit)
        return user
