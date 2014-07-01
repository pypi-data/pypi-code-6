from __future__ import unicode_literals

from pyramid.scaffolds import PyramidTemplate


class APITemplate(PyramidTemplate):
    _template_dir = 'api'
    summary = 'Basic HTTP API'
