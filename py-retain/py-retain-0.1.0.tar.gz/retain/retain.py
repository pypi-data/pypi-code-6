# -*- coding: utf-8 -*-
""" Retain module

All of the API requests are created, and the API responses are parsed here.

>>> from retain import Retain
>>> Retain.app_id = 'app-id'
>>> Retain.api_key = 'api-key'

"""

__version__ = '0.1.0'

import json
import requests

DEFAULT_TIMEOUT = 10  # seconds


class RetainError(Exception):
    """ Request error. """
    def __init__(self, message, result=None):
        super(RetainError, self).__init__(message)
        self.result = result


class Retaincc(object):
    """ Retain.cc API Wrapper """

    app_id = None
    api_key = None
    api_version = 1
    api_endpoint = 'https://app.retain.cc/api/v' + str(api_version) + '/'
    timeout = DEFAULT_TIMEOUT
    s = requests.Session()
    request_map = {
        'get': s.get,
        'post': s.post,
        'put': s.put,
        'delete': s.delete
    }

    @classmethod
    def _do_call(cls, method, url, params={}):
        """
        Do the actual request and parse the response
        """
        headers = {
            'User-Agent': 'py-retain/' + __version__,
            'content-type': 'application/json'
        }
        try:
            r = cls.request_map[method.lower()]
        except KeyError:
            raise ValueError("Unknow HTTP Method")
        response = r(
            url,
            auth=(cls.app_id, cls.api_key),
            headers=headers,
            data=json.dumps(params),
            timeout=cls.timeout)
        return response.json()

    @classmethod
    def create_user(cls, **kwargs):
        """ Creates a user.

        N.B. Social and geo location data is fetched asynchronously, so a
        secondary call to users will be required to fetch it.

        **Arguments**

        - `user_id`: required (if no email) — a unique string identifier
          for the user
        - `email`: required (if no user_id) — the user's email address
        - `name`: The user's full name
        - `created_at`: A UNIX timestamp representing the date the user was
          created
        - `custom_data`: A hash of key/value pairs containing any other data
          about the user you want Retaincc to store.
        - `last_seen_ip`: An ip address (e.g. "1.2.3.4") representing the
          last ip address the user visited your application from. (Used for
          updating location_data)
        - `last_seen_user_agent`: The user agent the user last visited your
          application with.
        -  `last_impression_at`: Last time user use your app/


        >>> user = Retaincc.create_user(user_id='7902', email='ben@retain.cc',
        ... name='Somebody', created_at=1270000000, last_seen_ip='1.2.3.4',
        ... custom_data={'app_name': 'Genesis'}, last_impression_at=1300000000)
        >>> user['name']
        u'Somebody'
        >>> user['custom_data']['app_name']
        u'Genesis'
        >>> user['last_impression_at']
        1300000000

        """
        return cls._do_call(
            'POST', Retaincc.api_endpoint + 'users', params=kwargs)

    @classmethod
    def get_user(cls, email=None, user_id=None):
        """ Return a dict for the user represented by the specified email
        or user_id.

        >>> user = Retaincc.get_user(user_id='123')
        >>> user['name']
        u'Somebody'

        """

        params = {'email': email, 'user_id': user_id}
        user_dict = cls._do_call(
            'GET', cls.api_endpoint + 'users', params=params)
        return user_dict

    @classmethod
    def update_user(cls, **kwargs):
        """ Update a user with the available parameters.

        >>> user = Retaincc.get_user(user_id='123')
        >>> user['name']
        u'Somebody'
        >>> user = Retaincc.update_user(user_id='123', name='Guido')
        >>> user['name']
        u'Guido'

        """
        return cls._do_call(
            'PUT', cls.api_endpoint + 'users', params=kwargs)

    @classmethod
    def delete_user(cls, user_id=None, email=None):
        """ Delete a user.

        >>> user = Retaincc.get_user(user_id='123')
        >>> user['email']
        u'somebody@example.com'

        """
        params = {
            'email': email,
            'user_id': user_id
        }
        user_dict = cls._do_call(
            'DELETE', cls.api_endpoint + 'users', params)
        return user_dict

    @classmethod
    def create_company(cls, **kwargs):
        """ Creates a company.

        **Arguments**

        - `id`: required — a unique string identifier for the company
        - `name`: The company name
        - `created_at`: A UNIX timestamp representing the date the company was
          created
        - `plan`: Plan of a company
        - `spending`: The total spending of the company
        - `custom_data`: A hash of key/value pairs containing any other data
          about the user you want Retaincc to store.
        - `last_impression_at`: Last time any user belongs to the company


        >>> company = Retaincc.create_company(id='7902', name='Oursky',
        ... created_at=1359510808, plan='Starter',
        ... custom_data={"submittsion_usage":201,"submission_quota":500,"disk_usage":63,"disk_quota":500})
        >>> company['name']
        u'Oursky'
        >>> company['custom_data']['submittsion_usage']
        201

        """
        return cls._do_call(
            'POST', Retaincc.api_endpoint + 'companies', params=kwargs)

    @classmethod
    def update_company(cls, **kwargs):
        """ Update a user with the available parameters.

        >>> company = Retaincc.update_company(id='7902', name='Oursky Ltd')
        >>> company['name']
        u'Guido'

        """
        return cls._do_call(
            'PUT', cls.api_endpoint + 'companies', params=kwargs)
