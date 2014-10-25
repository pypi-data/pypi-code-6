# -*- coding: utf-8 -*-

import oauth2
import os
from urlparse import urljoin, parse_qsl
import ConfigParser
from directory import DirectoryApi

CONSUMER_KEY = 'zLs5P3Mk1eQxTmdLSX6VqpDXj'
CONSUMER_SECRET = 'HCkA4cRitOvHic7V3k2PZxAZS9ZZX1YqLRGgkHvZ2CijUBEdI9'

RESPONSE_OK = '200'

TWIPPY_DIR = '.twipy'
TWIPPY_PATH = os.path.join(os.getenv('HOME'), TWIPPY_DIR)
TOKEN_PATH = os.path.join(TWIPPY_PATH, 'access_token')
CONFIG_PATH = os.path.join(TWIPPY_PATH, 'config')

SECTION_ACCESS_TOKEN = 'access_token'
SECTION_TOKEN_SECRET = 'token_secret'

OPTION_ACCESS = 'token'
OPTTION_SECRET = 'secret'


class Keys():
    """
    Keys class for auth
    """

    def __init__(self,
                 consumer_key=CONSUMER_KEY,
                 consumer_secret=CONSUMER_SECRET,
                 access_token=None,
                 access_token_secret=None):
        """
        Construct Keys
        :param consumer_key:
        :param consumer_secret:
        :param access_token:
        :param access_token_secret:
        """

        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self._access_token = access_token
        self._access_token_secret = access_token_secret
        self._oauth_consumer = None

    def get_auth_token(self):
        """
        Gets temporal auth token
        :return: auth token
        """

        oauth_consumer = oauth2.Consumer(key=self._consumer_key, secret=self._consumer_secret)
        self._oauth_consumer = oauth_consumer

        oauth_client = oauth2.Client(oauth_consumer)

        return oauth_client

    def get_token(self, oauth_client):
        """
        Gets the access token and token access secret
        :param oauth_client: auth token
        :exception: response status != 200
        """

        directory_api = DirectoryApi()
        request_token_url = directory_api.get_url_request_token()

        response, content = oauth_client.request(request_token_url)

        if response['status'] == RESPONSE_OK:
            response_content = dict(parse_qsl(content))

            self._access_token = response_content['oauth_token']
            self._access_token_secret = response_content['oauth_token_secret']
        else:
            raise Exception('Twitter response: %s' % str(response['status']))

    def authorize(self):
        """
        Authorizes the access with the access token
        :return: oauth_client and pin_code
        """

        directory_api = DirectoryApi()
        authorize_url = directory_api.get_url_authorize_url()
        authorize_with_token_url = urljoin(authorize_url, '?oauth_token=%s' % self._access_token)

        print 'Visit the url to obtain the auth code:'
        print
        print authorize_with_token_url
        print

        pin_code = raw_input('Enter code: ')

        token = oauth2.Token(self._access_token, self._access_token_secret)
        token.set_verifier(pin_code)

        oauth_client = oauth2.Client(self._oauth_consumer, token)

        return oauth_client, pin_code

    def get_access(self, oauth_client, pin_code):
        """
        Gets access
        :param oauth_client:
        :param pin_code:
        """

        directory_api = DirectoryApi()
        access_token_url = directory_api.get_url_access_token()

        response, content = oauth_client.request(access_token_url, method='POST', body='oauth_verifier=%s' % pin_code)

        if response['status'] == RESPONSE_OK:
            dict_token = dict(parse_qsl(content))
            self._access_token = dict_token['oauth_token']
            self._access_token_secret = dict_token['oauth_token_secret']
        else:
            raise Exception('Twitter response: %s' % str(response['status']))

    @property
    def get_consumer_keys(self):
        return self._consumer_key, self._consumer_secret

    def save_keys(self):
        """
        Saves the keys in a file
        """

        key_files = KeyFiles()

        key_files.create_folder()
        key_files.create_token_file(self._access_token, self._access_token_secret)

    def open_keys(self):
        """
        Open the file and gets the keys
        :return: tuple with keys or None
        """

        key_files = KeyFiles()

        self._access_token, self._access_token_secret = key_files.open_token_file()

        if self._access_token is not None and self._access_token_secret is not None:
            return self._access_token, self._access_token_secret
        else:
            return None


class KeyFiles():
    """
    KeyFiles class
    """

    def __init__(self):
        """
        Constructor
        """

        self._home_path = TWIPPY_PATH
        self._file_storage_keys = TOKEN_PATH
        self._config_file = CONFIG_PATH
        self._oauth_token = None
        self._oauth_secret_token = None

    def create_folder(self):
        """
        Creates the folder
        """

        if not os.path.isdir(self._home_path):
            try:
                os.makedirs(self._home_path)
            except Exception:
                raise Exception('Not enough privileges on %s' % TWIPPY_PATH)

    def create_token_file(self, access_token, token_secret):
        """
        Creates the file which saves the tokens
        :param access_token:
        :param token_secret:
        """

        self._oauth_token = access_token
        self._oauth_secret_token = token_secret

        self.create_folder()

        config_parser = ConfigParser.RawConfigParser()

        try:
            config_parser.add_section(SECTION_ACCESS_TOKEN)
            config_parser.set(SECTION_ACCESS_TOKEN, OPTION_ACCESS, self._oauth_token)
            config_parser.add_section(SECTION_TOKEN_SECRET)
            config_parser.set(SECTION_TOKEN_SECRET, OPTTION_SECRET, self._oauth_secret_token)
            with open(self._file_storage_keys, 'wb') as config_file:
                config_parser.write(config_file)
        except (IOError, TypeError) as e:
            print e.message
            raise Exception('Cannot create the file in %s' % TOKEN_PATH)

    def open_token_file(self):
        """
        Gets the tokens from file
        :return: tuple of tokens
        """

        config_parser = ConfigParser.RawConfigParser()

        try:
            config_parser.read(self._file_storage_keys)
            if not config_parser.has_section(SECTION_ACCESS_TOKEN) or not config_parser.has_section(SECTION_TOKEN_SECRET):
                raise Exception('No sections in file %s' % TOKEN_PATH)

            self._oauth_token = config_parser.get(SECTION_ACCESS_TOKEN, OPTION_ACCESS)
            self._oauth_secret_token = config_parser.get(SECTION_TOKEN_SECRET, OPTTION_SECRET)

            return self._oauth_token, self._oauth_secret_token
        except (IOError, TypeError) as e:
            print e.message
        except Exception as e:
            print e.message

    def exists_token_file(self):
        """
        :return: {boolean}
        """

        if os.path.isfile(self._file_storage_keys):
            return True
        else:
            return False
