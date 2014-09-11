import json
from .utils import format_params, format_time


class Datapoint(object):

    """Datapoint."""

    def __init__(self, client):
        self.client = client

    def _format_data(self, data):
        return [[format_time(e[0]), e[1]] for e in data]

    def filter(self, id, params=None):
        """Filter Datapoints.

        :param str id: Datastream id.
        :param dict params: Params.
        :returns: List of datapoints.

        Usage::

            >>> datapoints = client.datapoints.filter(id='id0',
                                params={'start': datetime(2014, 1, 1),
                                        'end': datetime.utcnow(),
                                        'order': 'asc',
                                        'limit': 1000,
                                        'offset': 0})
        """
        if params is None:
            params = {}
        return self.client.get('/datastreams/{id}/datapoints'.format(id=id),
                               params=format_params(params))

    def create(self, id, data):
        """Create datapoint(s).

        :param str id: Datastream id.
        :param list data: List of datapoints.
        :returns: Created datapoint(s).

        Usage::

            >>> datapoints = client.datapoints.create(id='id0',
                                data=[[datetime.utcnow(), 1],
                                    [datetime.utcnow(), 2]])
        """
        return self.client.post('/datastreams/{id}/datapoints'.format(id=id),
                                data=json.dumps(self._format_data(data)))

    def get(self, id, timestamp):
        """Get datapoint by timestamp.

        :param str id: Datastream id.
        :param datetime timestamp: timestamp.
        :returns: A datapoint.

        Usage::

            >>> datapoint = client.datapoints.get(id='id0',
                      timestamp=datetime(2014, 1, 2, 3, 4, 5, 6000))
        """
        return self.client.get('/datastreams/{id}/datapoints/{t}'.format(
                               id=id, t=format_time(timestamp)))

    def delete(self, id, params):
        """Delete datapoints.

        :param str id: Datastream id.
        :param dict params: Params.
        :returns: True if success. Else False.

        Usage::

            >>> client.datapoints.delete(id='id0',
                         params={'start': datetime(2014, 1, 1),
                                 'end': datetime.utcnow()})
        """
        if params is None:
            params = {}
        return self.client.delete('/datastreams/{id}/datapoints'.format(id=id),
                                  params=format_params(params))
