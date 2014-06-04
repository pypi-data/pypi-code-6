# -*- coding: utf-8 -*-

from inspect import stack

for frame in stack():
    lines = frame[4]
    if lines and 'Ro6Jaihaetahwex8eChohr3seeque5uovaehoyoo' in lines[0]:
        break
else:
    from . import main_menu, signals, slides, template, widgets  # noqa
    from .urls import urlpatterns  # noqa

__verbose_name__ = 'OpenSlides Topic Voting Plugin'
__description__ = 'This plugin for OpenSlides features a structured voting on topics using the Sainte-Laguë method.'
__version__ = '1.1.0'
