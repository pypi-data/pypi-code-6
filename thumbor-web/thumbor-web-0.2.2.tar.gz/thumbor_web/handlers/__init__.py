#!/usr/bin/python
# -*- coding: utf-8 -*-

from thumbor_web.handlers import home


def init_app(app):
    app.register_blueprint(home.mod)
