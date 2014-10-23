# This Python file uses the following encoding: utf-8

__author__="A. Fritz - c.a.t.forge.eu"
__date__ ="$09.09.2009 20:35:14$"
__doc__="Zur Zeit noch keine Dokumentation."

from django import forms
from django.utils.translation import ugettext_lazy as _
#from sitecode.captcha.fields import CaptchaField

class ContactForm(forms.Form):
    """
    Einfaches Mailformular ohne Betreff.
    """
    email = forms.EmailField(required=True)
    subject = forms.Field(required=True)
    message = forms.CharField(widget=forms.Textarea)
#    captcha = CaptchaField()

    def clean_message(self):
        """Prüft auf mindest Wort anzahl"""
        message = self.cleaned_data['message']
        num_words = len(message.split())
        if num_words < 4:
            raise forms.ValidationError(_("Not enough words!"))
        return message
