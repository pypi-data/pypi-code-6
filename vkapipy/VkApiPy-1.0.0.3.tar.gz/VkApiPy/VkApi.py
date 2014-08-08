from pprint import pprint

import json
import os
import logging
from time import sleep as time_sleep

from ._FormParser import _FormParser

from six.moves.http_cookiejar import CookieJar
from six.moves.urllib.parse import urlparse, urlencode, parse_qs
from six.moves.urllib.request import (urlopen, build_opener, 
    HTTPCookieProcessor, HTTPRedirectHandler, urlretrieve)

class VkApi():
    # for support calls like this: vk_obj.audio.search(params)
    def __getattr__(self, item):
        if item in self.scope:
            if self.scope_wrappers.get(item) is not None:
                return self.scope_wrappers.get(item)
            else:
                class _ApiSectionWrapper(object):
                    def __init__(self, callback_class):
                        self.section = item
                        self.callback_class = callback_class
                    def __getattr__(self, item):
                        return self.callback_class.api_call_wrapper(self.section, item)

                wrapper = _ApiSectionWrapper(callback_class=self)
                self.scope_wrappers[item] = wrapper
                return self.scope_wrappers[item]

    # for support calls like this: vk_obj.audio.search(params)
    def api_call_wrapper(self,section, name):
        def call_func(f_name=name, **kwargs):
            api_func_name = '.'.join([section, f_name])
            api_params = list(kwargs.items())
            return self.call_api(api_func_name, api_params)
        return call_func


    def __init__(self, email, password, token_file, client_id='2892861',
                 scope='audio', captcher=None, debug=False, log_file=None):

        if not all([email, password, token_file, scope, client_id]):
            raise ValueError(
                'email, password, token_file, scope and client_id required')
                        
        self.email = email
        self.password = password
        self.token_file = token_file
        self.client_id = client_id
        self.scope = scope if isinstance(scope, list) else [scope]
        self.scope_wrappers = {}
        self.captcher = captcher
        self.debug = debug

        self.log = logging.getLogger('VkApi')
        self.log.setLevel(logging.DEBUG if debug else logging.CRITICAL)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(message)s')
        if log_file:
            fh = logging.FileHandler(log_file)
            fh.setLevel(logging.DEBUG if debug else logging.CRITICAL)
            fh.setFormatter(formatter)
            self.log.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG if debug else logging.CRITICAL)
        ch.setFormatter(formatter)
        self.log.addHandler(ch)
        
        self.token = ''

        self.opener = build_opener(
            HTTPCookieProcessor(CookieJar()), HTTPRedirectHandler())
        self.log.debug('Opener created')
        if os.path.exists(self.token_file):
            try:
                self.log.debug('Try open token file')
                self.token = open(self.token_file, 'r+').read()
                self.log.debug('Token read success - {}'.format(self.token))
            except IOError:
                self.log.debug('Cannon read token, but file exists')
                raise IOError('File exists, but cannot read')
        
        if not self.token:
            self.log.debug('Token is empty, start auth')
            self.auth()

    def _auth_user(self):
        # PRIVATE METHOD
        self.log.debug('Auth user')
        print('==============AUTH================')
        response = self.opener.open(
            'http://oauth.vk.com/oauth/authorize?'+\
            'redirect_uri=http://oauth.vk.com/blank.html&response_type=token&'+\
            'client_id=%s&scope=%s&display=wap'%
            (self.client_id, ','.join(self.scope))
        )
        doc = response.read()
        print('url: ')
        print('http://oauth.vk.com/oauth/authorize?redirect_uri=http://oauth.vk.com/blank.html&response_type=token&client_id=%s&scope=%s&display=wap'%(self.client_id, ','.join(self.scope)))
        print('-------------')
        print(doc)
        print('-------------')

        parser = _FormParser()
        parser.feed(doc.decode('utf-8'))
        parser.close()
        if (not parser.form_parsed or parser.url is None or
                'pass' not in parser.params or 'email' not in parser.params):
            self.log.debug('Error on auth user. Login-form not correct')
            raise RuntimeError('Auth user error')

        parser.params['email'] = self.email
        parser.params['pass'] = self.password
        if parser.method == 'POST':
            self.log.debug('Send auth-data')
            print('==============SEND AUTH================')
            print('url: {}'.format(parser.url))
            response = self.opener.open(
                parser.url, urlencode(parser.params).encode('utf-8'))
        else:
            self.log.debug('Form wants undefined request method')
            raise NotImplementedError('Method %s' % parser.method)
        resp = response.read()
        print('-------------')
        print(resp)
        print('-------------')
        print('Redirect: {}'.format(response.geturl()))

        return resp, response.geturl()

    def _give_access(self, doc):
        # PRIVATE METHOD
        self.log.debug('Give access method')
        parser = _FormParser()
        print('==============GIVE_ACCESS================')

        parser.feed(doc.decode('utf-8'))
        parser.close()
        if not parser.form_parsed or parser.url is None:
            self.log.debug('Give access parse fails')
            raise RuntimeError('Give access error')

        if parser.method == 'POST':
            self.log.debug('Send give-access answer')
            print('url: {}'.format(parser.url))
            response = self.opener.open(
                parser.url, urlencode(parser.params).encode('utf-8'))
        else:
            raise NotImplementedError('Method %s' % parser.method)
        print('--------------')
        print(response.read())
        print('-----------')
        print('Redirect: {}'.format(response.geturl()))

        return response.geturl()

    def auth(self):
        self.log.debug('Main auth method starts')
        doc, url = self._auth_user()
        print(doc)
        if urlparse(url).path != '/blank.html':
            self.log.debug('Auth successful')
            url = self._give_access(doc)

        if urlparse(url).path != '/blank.html':
            self.log.debug('Give access error')
            raise RuntimeError('Auth error')

        if '#' in url:
            answer = {k:v[0] for k,v in parse_qs(url.split('#')[1]).items()}
        else:
            answer = {}

        if 'access_token' not in answer or 'user_id' not in answer:
            raise RuntimeError('Auth error vk.com banned us. Please waiting.')

        self.token = answer['access_token']
        self.log.debug('Access token - {}'.format(self.token))
        if self.token_file:
            try:
                open(self.token_file, 'w+').write(self.token)
                self.log.debug(
                    'Access token saved to {}'.format(self.token_file)
                )
            except IOError:
                self.log.debug(
                    'Cannot write token file {}'.format(
                        self.token_file))

        return answer['access_token']

    def check_for_errors(self, response):
        try:
            response_object = json.loads(response.decode('utf-8'))
        except:
            raise ValueError('Cannot parse response-json')

        if 'error' in response_object:
            if response_object['error']['error_code'] == 14:
                if self.captcher:
                    self.captcher.process_captcha(
                        url=response_object['error']['captcha_img'],
                        sid=response_object['error']['captcha_sid'],
                        callback=self.send_captcha)
                else:
                    raise RuntimeError('Captcha needed')
            elif response_object['error']['error_code'] == 5:
                self.log.debug('Our token expired. Try re-auth')
                if self.auth():
                    self.log.debug(
                        'Succes renew token. '
                        'Retry call method {}'.format(self.last_method))

                    return self.call_api(self.last_method, self.last_params)
                else:
                    raise RuntimeError('Renew token error')
            elif response_object['error']['error_code'] == 6:
                self.log.debug(
                    'Too many requests per second. Sleep second and try again')
                time_sleep(1)
                return self.call_api(self.last_method, self.last_params)
            else:
                print(response_object)
                raise NotImplementedError(
                    'Vk-error:{}'.format(response_object['error']['error_msg']))

        return response_object.get('response')

    def call_api(self, method, params=[], captcha=False):
        if captcha:
            self.log.debug('Send captcha')

        self.log.debug('Call method {}, params {}'.format(method,repr(params)))
        self.last_method = method
        self.last_params = params
        
        params.append(('access_token', self.token))

        url = 'https://api.vk.com/method/%s' % (method)
        self.log.debug('Open url {}'.format(url))
        res = urlopen(url, data=urlencode(params).encode('utf-8')).read()
        self.log.debug('Response received')
        response = self.check_for_errors(res)
        self.log.debug('Response checked for errors success.')
        return response

    def send_captcha(self, captcha_sid, captcha_key):
        params = [(k,v) for k,v in self.last_params]
        params.append(('captcha_sid', captcha_sid))
        params.append(('captcha_key', captcha_key))
        result = self.call_api(self.last_method, params, captcha=True)
