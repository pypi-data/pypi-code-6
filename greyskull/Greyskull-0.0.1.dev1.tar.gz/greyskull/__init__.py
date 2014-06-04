# -*- coding: utf-8 -*-
"""
Greyskull: A better NTrack tracker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from tornado.web import Application

from greyskull.urls import urlpatterns

application = Application(urlpatterns)
