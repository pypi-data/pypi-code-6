# -*- coding: utf-8 -*-
from flask.globals import g


def     flask_after_peewee_close(response):
    if hasattr(g, 'db') and g.db is not None:
        g.db.close()
    return response
