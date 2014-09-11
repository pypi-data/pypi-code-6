import requests
from requests.auth import HTTPBasicAuth


class TokenAuth(requests.auth.AuthBase):

    """AccessToken Auth."""

    def __init__(self, access_token):
        self.access_token = access_token

    def __call__(self, r):
        r.headers['Authorization'] = 'Bearer ' + self.access_token
        return r


class Client(object):

    """Client. All API calls are made by this class.

    :param str database: Database's name.
    :param str client_id: Database's client_id.
    :param str client_secret: Database's client_secret.
    :param str access_token: Database's access_token.
    :param str host: Server's hostname, default 'api.dotide.com'.
    :param str version: API version, default 'v1'.
    :param bool secure: Whether use ssl, default True.

    Usage::

      >>> import dotide
      >>> client = dotide.Client('your_database_name', client_id='your_client_id', client_secret='your_client_secret')
    """

    def __init__(self,
                 database,
                 client_id=None,
                 client_secret=None,
                 access_token=None,
                 host='api.dotide.com',
                 version='v2',
                 secure=True):
        self.database = database  # : Database's name.
        self.client_id = client_id  # : Database's client_id.
        self.client_secret = client_secret  #: Database's client_secret.
        self.access_token = access_token  #: Database's access_token.
        self.host = host  #: Server's hostname.
        self.version = version  #: API version.
        self.secure = secure  #: Whether use ssl.
        self.session = requests.Session()
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'dotide.py',
            'Time-Zone': 'UTC'
        }

    def _build_base_url(self):
        """Build base url."""
        schema = 'https' if self.secure else 'http'
        return '{schema}://{host}/{ver}/{db}'.format(schema=schema,
                                                     host=self.host,
                                                     ver=self.version,
                                                     db=self.database)

    def _build_full_url(self, path):
        """Build full url."""
        return self._build_base_url() + path

    def _build_auth(self):
        """Build auth."""
        if self.client_id and self.client_secret:
            auth = HTTPBasicAuth(self.client_id, self.client_secret)
        elif self.access_token:
            auth = TokenAuth(self.access_token)
        else:
            auth = None
        return auth

    def request(self, method, path, params=None, data=None):
        """An internal method that send request to server.
        It is exposed if you need to make API calls not implemented in this
        library or if you need to debug requests.

        :param str method: An HTTP method (e.g. 'GET' or 'POST').
        :param str path: The path URL with leading slash (e.g. '/datastreams').
        :param dict params: A dictionary of parameters to add to the request.
        :param str data: A json string. This is the body of the request.
        :returns: Parsed body.
        :rtype: dict or list.
        """
        r = self.session.request(method,
                                 self._build_full_url(path),
                                 params=params,
                                 data=data,
                                 headers=self.headers,
                                 auth=self._build_auth())

        data = r.json() if r.content else None
        if r.status_code >= 400:
            raise requests.exceptions.HTTPError(data['message'], response=r)
        return data

    def get(self, path, params=None):
        """GET request."""
        return self.request('GET', path, params=params)

    def post(self, path, data=None):
        """POST request."""
        return self.request('POST', path, data=data)

    def put(self, path, data=None):
        """PUT request."""
        return self.request('PUT', path, data=data)

    def delete(self, path, params=None):
        """DELETE request."""
        return self.request('DELETE', path, params=params) is None
