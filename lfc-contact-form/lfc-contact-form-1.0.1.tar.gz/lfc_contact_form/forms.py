from django import forms
from django.utils.translation import ugettext_lazy as _


class ContactForm(forms.Form):
    name = forms.CharField(label=_(u'Your name'))
    email = forms.EmailField(label=_(u'Your email address'))
    message = forms.CharField(label=_(u'Your message'), widget=forms.Textarea())
