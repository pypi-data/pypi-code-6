#!/usr/bin/python
# -*- coding:utf-8 -*-
# This Python file uses the following encoding: utf-8

from django.forms import ModelForm, PasswordInput
from models import Setup

class SetupForm(ModelForm):
    class Meta:
        model = Setup
        widgets = {
            'mail_host_pass': PasswordInput(),
        }
