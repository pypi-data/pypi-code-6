#!/usr/bin/python
# -*- coding:utf-8 -*-
# This Python file uses the following encoding: utf-8

VERSION = (0, 3, 7)
APPLICATION_NAME = "contact-form-setup"
VERSION_str = str(VERSION).strip('()').replace(',', '.').replace(' ', '')
Application_description = "App for setting up the email-host"
VERSION_INFO = """
"Version: %s
Modification date: 15.08.2011

0.3.3 Readme and license in root dir moved. EmailField now unencrypted.
      src folder removed so readme is on the toplevel.
0.3.1 Mail host can also be set.
0.3.0 Now data encrypted saved in to database

TODO:
    - write unittests
""" % (VERSION_str,)
