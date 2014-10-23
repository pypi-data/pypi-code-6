#!/usr/bin/python
# -*- coding:utf-8 -*-
# This Python file uses the following encoding: utf-8

VERSION = (0, 3, 7)
APPLICATION_NAME = "django-easy-contact"
VERSION_str = str(VERSION).strip('()').replace(',', '.').replace(' ', '')
VERSION_INFO = """
"Version: %s

Application description: "A small contact form application".
- Works together with django-contact-form-setup app
- Translated in to german



0.3.3 src folder removed so readme is on the toplevel
0.3.2 Flexible sending methodes
0.3.1 Use smtplib directly instead of django.mail

TODO:
    - write unittests
""" % (VERSION_str,)
