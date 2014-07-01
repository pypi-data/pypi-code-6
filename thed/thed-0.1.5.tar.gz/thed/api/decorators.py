from __future__ import unicode_literals


class ViewConfig(object):

    def __init__(self, **settings):
        self.settings = settings

    def __call__(self, wrapped):
        wrapped.view_config = self.settings
        return wrapped


view_config = ViewConfig
