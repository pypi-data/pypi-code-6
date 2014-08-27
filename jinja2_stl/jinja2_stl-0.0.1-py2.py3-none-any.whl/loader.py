# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from jinja2 import BaseLoader, TemplateNotFound


class FilestorageTemplateLoader(BaseLoader):
    def __init__(self, storage):
        self._storage = storage

    def get_source(self, environment, template):
        if not self._storage.exists(template):
            raise TemplateNotFound(template)
        size = self._storage.size(template)
        with self._storage.open(template) as f:
            source = f.read()
        return source, None, lambda: size == self._storage.size(template)
