#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from bottle import run

from wsgi import settings, application

run(application, host=settings.HOST, port=settings.PORT, server="gunicorn")