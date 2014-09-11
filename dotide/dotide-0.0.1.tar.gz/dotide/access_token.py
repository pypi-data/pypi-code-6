import json
from .utils import format_params


class AccessToken(object):

    """AccessToken."""

    def __init__(self, client):
        self.client = client

    def filter(self, params=None):
        """Filter AccessTokens.

        :returns: List of access_token.

        Usage::

            >>> access_tokens = client.access_tokens.filter({'limit': 10, 'offset': 0})
        """
        if params is None:
            params = {}
        return self.client.get('/access_tokens', params=format_params(params))

    def create(self, data):
        """Create an access_token.

        :param dict data: access_token.
        :returns: Created access_token.

        Usage::

            >>> access_token = client.access_tokens.create({'scopes': [{
                               'permissions': ['read', 'write', 'delete'],
                               'global': False,
                               'ids': ['id0'],
                               'tags': ['tag0']}]})
        """
        return self.client.post('/access_tokens', data=json.dumps(data))

    def get(self, access_token):
        """Get an access_token.

        :param str access_token: access_token's access_token.
        :returns: access_token.

        Usage::

            >>> access_token = client.access_tokens.get('your_access_token')
        """
        return self.client.get('/access_tokens/{access_token}'.format(
            access_token=access_token))

    def update(self, access_token, data):
        """Update an access_token.

        :param str access_token: access_token's access_token.
        :param dict data: access_token
        :returns: access_token.

        Usage::

            >>> access_token = client.access_tokens.update('61e13e47ed0b1b6f6a0ebe598d5ddba0c386a0d856\
                            487ec84e973d06b1848221',
                            {'scopes': [
                                {'permissions': ['read', 'write', 'delete'],
                                 'global': True}
                            ]})
        """
        return self.client.put('/access_tokens/{access_token}'.format(
            access_token=access_token),
            data=json.dumps(data))

    def delete(self, access_token):
        """Delete an access_token.

        :param str access_token: access_token's access_token.
        :returns: True if sucess.

        Usage::

            >>> client.access_tokens.delete('your_access_token')
        """
        return self.client.delete('/access_tokens/{access_token}'.format(
            access_token=access_token))
