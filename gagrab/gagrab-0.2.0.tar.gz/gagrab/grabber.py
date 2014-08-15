from datetime import datetime

from six.moves import zip


class Grabber(object):
    """A ``Grabber`` object stores authetication information, and provides
    a convenient interface to query data from google analytics.

    An ``authorized_service`` object must be set up first, according
    to the steps shown in the `gclient-service-account-auth
    <https://github.com/ambitioninc/gclient-service-account-auth>`_
    docs.

    """
    def __init__(self, authorized_service):
        self.project_id = authorized_service.project_id
        self.service = authorized_service.service

    def query(self, view, dimensions, metrics, start_date, end_date, **kwargs):
        """Run a query on the account's Google Analytics data.

        Queries run with this method are subject to the sampling
        imposed by the core-reporting api.

        :param view: The integer id representing the view to be
            queried. This can be found in the Google Analytics admin
            section "View Settings" and will look similar to
            "UA-00000-1"

        :param dimensions: A list of dimensions to aggregate
            on. E.g. ``['operatingSystem', 'dimension1']``

        :param metrics: A list of the names ometrics to be included in
            the query. E.g. ``['pageviews', 'timeOnPage']``

        :param start_date: A date for the start of the query.

        :param end_date: A date for the end of the query.

        Any additional query parameter can be passed in to the keyword
        arguments of this this function, and will be passed along to
        the underlying google analytics query. These will not be
        automatically converted from python datatypes into appropriate
        google syntax. These should only be passed if you know what
        yo're doing.

        :returns: A list of dictionaries mapping each requested
            dimension/metric to its value for each row.

        A query like

        .. code-block:: python

            my_grabber.query(
                view='UA-00000-1',
                dimensions=['browser'],
                metrics=['pageviews'],
                start_date='2014-07-01',
                end_date='2014-07-01'
            )

        Would return data like

        .. code-block:: python

            [{'browser': 'firefox', 'pageviews': 1264},
             {'browser': 'chrome', 'pageviews': 2782},
             {'browser': 'safari', 'pageviews': 805},
             {'browser': 'internet explorer', 'pageviews': 3397},
            ]
        """
        query_response = self._query_response(
            view, dimensions, metrics, start_date, end_date, **kwargs
        )
        data = data_from_query_response(query_response)
        next_index = query_response['itemsPerPage'] + 1
        while query_response.get('nextLink'):
            query_response = self._query_response(
                view, dimensions, metrics, start_date, end_date, start_index=next_index, **kwargs
            )
            data += data_from_query_response(query_response)
            next_index += query_response['itemsPerPage']
        return data

    def _query_response(self, view, dimensions, metrics, start_date, end_date, **kwargs):
        """Get the raw data for a query.
        """
        if isinstance(start_date, datetime):
            start_date = datetime.strftime(start_date, '%Y-%m-%d')
        if isinstance(end_date, datetime):
            end_date = datetime.strftime(end_date, '%Y-%m-%d')
        formatted_view = 'ga:' + str(view)
        formatted_dimensions = ','.join(['ga:' + dim for dim in dimensions])
        formatted_metrics = ','.join(['ga:' + metric for metric in metrics])
        query_response = self.service.data().ga().get(
            ids=formatted_view,
            dimensions=formatted_dimensions,
            metrics=formatted_metrics,
            start_date=start_date,
            end_date=end_date,
            **kwargs
        ).execute()
        return query_response


def data_from_query_response(query_response):
    """Format a GA query response to a list of dicts.

    :type query_response: dict
    :param query_response: The raw response returned by the google
        analytics api.

    The structure returned by the google analytics api contains a lot
    of superfluous data, most of which is not in native python
    formats. This function converts the data to an appropriate python
    format and retuns a nice list of dictionaries.
    """
    convert = {
        'STRING': lambda x: x,
        'INTEGER': lambda x: int(x),
        'FLOAT': lambda x: float(x),
        'CURRENCY': lambda x: float(x),
        'TIME': lambda x: float(x),
        'PERCENT': lambda x: float(x)
    }
    headers = [h['name'].split(':')[1] for h in query_response['columnHeaders']]
    data_types = [h['dataType'] for h in query_response['columnHeaders']]
    rows = query_response['rows']
    data = []
    for row in rows:
        data_row = {}
        for header, data_type, value in zip(headers, data_types, row):
            data_row[header] = convert[data_type](value)
        data.append(data_row)
    return data
