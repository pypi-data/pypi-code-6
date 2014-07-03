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
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Tellafriend(models.Model):
    url = models.CharField(max_length=255)
    sender_email = models.EmailField(verbose_name=_(u'Sender e-mail'))
    recipient_email = models.EmailField(verbose_name=_(u'Friend e-mail'))
    message = models.TextField(blank=True, default="", verbose_name=_(u'Message from you'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_(u'Sending date'))
    user_agent = models.CharField(max_length=255, verbose_name=_(u'User agent'))
    user = models.ForeignKey(User, blank=True, null=True)

    def get_sender_fullname(self):
        raise NotImplementedError

    def get_sender_email(self):
        raise NotImplementedError