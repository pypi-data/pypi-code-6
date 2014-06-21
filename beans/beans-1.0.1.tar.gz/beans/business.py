try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

try:
    from urllib2 import Request, urlopen
except ImportError:
    from urllib.request import Request, urlopen

import json

from .exception import BeansException


class Business(object):

    ENDPOINT = "http://business.loyalbeans.com/api/v1/"

    cookie_user = ''
    cookie_reward = ''
    version = ''

    def __init__(self, secret):
        self.__secret__ = secret
        
    def set_cookies(self, cookies=None):
        if cookies is None:
            return
        if 'beans_user' in cookies:
            self.cookie_user = cookies['beans_user']
        if 'beans_reward' in cookies:
            self.cookie_reward = cookies['beans_reward']

    def call(self, function, params=None, cookies=None):
        self.set_cookies(cookies)
        
        if params is None:
            params = {}

        if not 'user' in params:
            params['user'] = self.cookie_user

        if not 'reward' in params:
            params['reward'] = self.cookie_reward

        params = urlencode(params).encode('utf-8')
        headers = {'api-key': self.__secret__, 'signature': 'PYTHON_SDK', 'version': self.version}
        request = Request(self.ENDPOINT+function, params, headers=headers)
        r = urlopen(request)

        r_type = ''
        if hasattr(r.info(), 'gettype'):
            r_type = r.info().gettype()
        elif hasattr(r.info(), 'get_content_type'):
            r_type = r.info().get_content_type()

        if r_type != 'application/json':
            raise BeansException({'message': 'HTTP Error: '+str(r.getcode()), 'code': r.getcode()})

        r = json.loads(r.read().decode('utf-8'))

        if r['error']:
            raise BeansException(r['error'])
        else:
            return r['result']
