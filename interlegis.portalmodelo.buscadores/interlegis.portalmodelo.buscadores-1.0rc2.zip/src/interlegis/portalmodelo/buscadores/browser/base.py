# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView


class BaseView(BrowserView):
    """Define the page used to return the results of the external search on
    the Buscador Legislativo site. The implementation is iframe-based on
    ``buscaleg.pt``.
    """

    base_url = ''

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self._path = []
        request.set('disable_plone.rightcolumn', 1)

    @property
    def traverse_subpath(self):
        return self._path

    def publishTraverse(self, request, name):
        self._path.append(name)
        return self

    def _subpath(self):
        return getattr(self, 'traverse_subpath', [])

    @property
    def keywords(self):
        subpath = self._subpath()
        keywords = ''
        if len(subpath) > 0:
            keywords = subpath[0]
        else:
            keywords = self.request.get('keywords', '')
        return keywords

    def iframe_src(self):
        keywords = self.keywords
        return self.base_url % keywords
