#!/usr/bin/python
# -*- coding:utf-8 -*-
# This Python file uses the following encoding: utf-8

from django.conf.urls.defaults import *

urlpatterns = patterns('easy_contact',
                        (r'^success/$', 'views.thanks'),
                        (r'^contact/$', 'views.contact'),
                        )
