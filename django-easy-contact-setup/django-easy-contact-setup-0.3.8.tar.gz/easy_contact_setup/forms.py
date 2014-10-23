#!/usr/bin/python
# -*- coding:utf-8 -*-
# This Python file uses the following encoding: utf-8

from django.forms import ModelForm, PasswordInput


class SetupForm(ModelForm):
    class Meta:
        widgets = {
            'mail_host_pass': PasswordInput(render_value=True),
        }
