from tessera.api.model import *
import requests

class TesseraClient(object):
    """An API client for Tessera.

    This is rudimentary to start with, but will support the full range
    of API operations.
    """
    def __init__(self, rooturi):
        if rooturi[-1] == '/':
            rooturi = rooturi[:-1]
        self.rooturi = rooturi

    def _get(self, path, **kwargs):
        return requests.get('{0}{1}'.format(self.rooturi, path), params=kwargs).json()

    def list_dashboards(self, tag=None, category=None, definition=False):
        path = '/api/dashboard/'
        if tag:
            path = path + 'tagged/' + tag
        elif category:
            path = path + 'category/' + category
        response = self._get(path, definition=definition)
        print response
        return [Dashboard.from_json(d) for d in response['dashboards']]

    def list_tags(self):
        response = self._get('/api/tag/')
        return [Tag.from_json(t) for t in response['tags']]

    def list_categories(self):
        response = self._get('/api/dashboard/category/')
        return response['categories']
