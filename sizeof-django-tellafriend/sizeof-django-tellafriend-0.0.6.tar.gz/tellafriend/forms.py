# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Copyright (c) 2010-2014 Mariusz Smenzyk <mariusz.smenzyk@sizeof.pl>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""

@author: Mariusz Smenzyk
@license: MIT License
@contact: mariusz.smenzyk@sizeof.pl
"""
from django import forms
from django.utils.translation import ugettext as _
from .models import Tellafriend

try:
    from captcha.fields import CaptchaField
except ImportError:
    raise ImportError("sizeof-django-tellafriend requires django-simple-captcha")


class TellAFriendForm(forms.ModelForm):
    url = forms.CharField(max_length=200, label=_("URL"), widget=forms.HiddenInput, required=False)
    sender_email = forms.EmailField(max_length=100, label=_("Sender"))
    recipient_email = forms.EmailField(max_length=100, label=_("Recipient"))
    message = forms.CharField(required=False, widget=forms.Textarea, label=_("Message"))
    captcha = CaptchaField(help_text=_("Please enter the characters shown in the image in the field next to it."),
                           label=_("Captcha"))

    class Meta:
        model = Tellafriend
        exclude = ('user', 'user_agent')