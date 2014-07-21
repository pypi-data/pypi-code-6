
import requests
import logging
from tessera.api.model import *

log = logging.getLogger(__name__)

class TesseraClient(object):
    """An API client for Tessera.

    This is rudimentary to start with, but will support the full range
    of API operations.
    """

    def __init__(self, rooturi):
        if rooturi[-1] == '/':
            rooturi = rooturi[:-1]
        self.rooturi = rooturi

        #
        # Helpers
        #

    def _uri(self, path):
        if path.startswith(self.rooturi):
            return path
        return '{0}{1}'.format(self.rooturi, path)

    def _get(self, path, **kwargs):
        log.debug('GET {0}'.format(path))
        return self._process_response(requests.get(self._uri(path), params=kwargs))

    def _delete(self, path, **kwargs):
        log.debug('DELETE {0}'.format(path))
        return self._process_response(requests.delete(self._uri(path), params=kwargs))

    def _post(self, path, body, **kwargs):
        log.debug('POST {0}'.format(path))
        return self._process_response(requests.get(self._uri(path),
                                                   data=body,
                                                   params=kwargs,
                                                   headers={
                                                       'Content-Type' : 'application/json'
                                                   }))

    def _put(self, path, body, **kwargs):
        log.debug('PUT {0}'.format(path))
        return self._process_response(requests.put(self._uri(path),
                                                   data=body,
                                                   params=kwargs,
                                                   headers={
                                                       'Content-Type' : 'application/json'
                                                   }))

    def _process_response(self, response):
        # TODO - error dispatching
        return response.json()



    def list_dashboards(self, tag=None, category=None, definition=False):
        if tag:
            path = '/api/dashboard/tagged/{0}'.format(tag)
        elif category:
            path = '/api/dashboard/category/{0}'.format(category)
        response = self._get(self._uri(path), definition=definition)
        return [ Dashboard.from_json(d) for d in response['dashboards'] ]

    def get_dashboard(self, path, definition=False):
        return Dashboard.from_json(self._get(path, definition=definition)['dashboards'][0])

    def create_dashboard(self, dashboard):
        return self._post(self._uri('/api/dashboard/'),
                          json.dumps(dashboard, cls=EntityEncoder))

    def update_dashboard(self, dashboard):
        return self._put(dashboard.href,
                         json.dumps(dashboard, cls=EntityEncoder))

    def delete_dashboard(self, dashboard):
        return self._delete(dashboard.href)




    def list_tags(self):
        response = self._get(self._uri('/api/tag/'))
        return [ Tag.from_json(t) for t in response['tags'] ]

    def list_categories(self):
        response = self._get(self._uri('/api/dashboard/category/'))
        return response['categories']
