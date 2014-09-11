import json
from .utils import format_params


class Datastream(object):

    """Datastream."""

    def __init__(self, client):
        self.client = client

    def filter(self, params=None):
        """Filter Datastreams.

        :param dict params: params.
        :returns: List of datastreams.

        Usage::

            >>> datastreams = client.datastreams.filter({'ids': ['id0', 'id1'],
                         'tags': ['tag0', 'tag1'],
                         'limit': 10,
                         'offset': 0
                         })
        """
        if params is None:
            params = {}
        return self.client.get('/datastreams', params=format_params(params))

    def create(self, data):
        """Create Datastream.

        :param dict data: datastream.
        :returns: Created datastream.

        Usage::

            >>> datastream = client.datastreams.create({'id': 'id0',
                           'name': 'name0',
                           'tags': ['tag0'],
                           'properties': {'prop0': 1}
                           })
        """
        return self.client.post('/datastreams', data=json.dumps(data))

    def get(self, id):
        """Get a Datastream.

        :param str id: Datastream's id.
        :returns: A datastream.

        Usage::

            >>> datastream = client.datastreams.get('id0')
        """
        return self.client.get('/datastreams/{id}'.format(id=id))

    def update(self, id, data):
        """Update a Datastream.

        :param str id: Datastream's id.
        :param dict data: Datastream.
        :returns: A datastream.

        Usage::

            >>> datastream = client.datastreams.update('id0', {
                          'name': 'name0',
                          'tags': ['tag0'],
                          'properties': {'prop0': 1}
                          })
        """
        return self.client.put('/datastreams/{id}'.format(id=id),
                               data=json.dumps(data))

    def delete(self, id):
        """Delete a Datastream.

        :param str id: Datastream's id.
        :returns: True if success.

        Usage::

            >>> client.datastreams.delete('id0')
        """
        return self.client.delete('/datastreams/{id}'.format(id=id))
