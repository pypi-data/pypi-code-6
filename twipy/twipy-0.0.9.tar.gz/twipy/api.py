# -*- coding: utf-8 -*-

import oauth2
import re

from directory import DirectoryApi
from keys import KeyFiles
from capture import servernotfound_exception


RESPONSE_OK = 200
RESPONSE_TOO_MANY_REQUEST = 429
STATUS_OK = 'ok'
REGEXP_URL = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

COUNT_MAX = 20


class ApiTwip(object):
    """
    Api class
    """

    def __init__(self,
                 consumer_key,
                 consumer_secret,
                 oauth_token=None,
                 oauth_token_secret=None):

        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self._oauth_token = oauth_token
        self._oauth_token_secret = oauth_token_secret
        self.is_authenticated = False
        self._client = None
        self._directory_api = DirectoryApi()

    def _authenticate(self):
        if not self._client:
            key_files = KeyFiles()

            if not self._oauth_token:
                self._oauth_token, self._oauth_token_secret = key_files.open_token_file()

            self._client = self._get_client()
            self.is_authenticated = True

    def _get_client(self):
        try:
            consumer = oauth2.Consumer(key=self._consumer_key, secret=self._consumer_secret)
            access_token = oauth2.Token(key=self._oauth_token, secret=self._oauth_token_secret)
            client = oauth2.Client(consumer=consumer, token=access_token)
        except ValueError as e:  # pragma: no cover
            raise Exception(e.message)  # pragma: no cover

        # client object. To access the TW API: client.request(url)
        return client

    def update_status(self, text, reply_to=None):
        if not self.is_authenticated:
            self._authenticate()
        uri = self._directory_api.get_url_update_status()

        if len(text) >= 140:
            print 'Text length has to be less than 140 characters'
            return None

        urls = re.findall(REGEXP_URL, text)

        if urls and len(text) > 120:
            print 'Text length with URL hast to be less than 120 characters'
            return None

        body = 'status=' + text.decode('utf-8')

        if reply_to:
            body += '&in_reply_to_status_id=' + reply_to

        try:
            response, content = self._client.request(uri=uri, body=body, method='POST')

            response_status = is_response_ok(response)

            if STATUS_OK != response_status:
                print 'Response not ok %s' % response_status  # pragma: no cover
                return None  # pragma: no cover
        except Exception:
            servernotfound_exception()

    def send_direct_message(self, text, screen_name):
        if not self.is_authenticated:
            self._authenticate()
        uri = self._directory_api.get_url_send_dm()

        if len(text) >= 140:
            print 'Text length has to be less than 140 characters'
            return None

        body = 'text=' + text.decode('utf-8')
        body += '&screen_name=' + screen_name

        try:
            response, content = self._client.request(uri=uri, body=body, method='POST')

            response_status = is_response_ok(response)

            if STATUS_OK != response_status:
                print 'Response not ok %s' % response_status  # pragma: no cover
                return None  # pragma: no cover
            else:
                print 'DM Sent'  # pragma: no cover
        except Exception:
            servernotfound_exception()

    def get_home_time_line(self):
        if not self.is_authenticated:
            self._authenticate()
        uri = self._directory_api.get_url_home_timeline()
        uri += '?count=%s' % COUNT_MAX

        try:
            response, content = self._client.request(uri=uri)

            response_status = is_response_ok(response)

            if STATUS_OK != response_status:
                print 'Response not ok %s' % response_status  # pragma: no cover
                return None

            return content
        except Exception:
            servernotfound_exception()

    def get_direct_messages(self):
        pass

    def get_mentions(self):
        if not self.is_authenticated:
            self._authenticate()

        uri = self._directory_api.get_url_read_mentions()

        uri += '?count=%s' % COUNT_MAX

        try:
            response, content = self._client.request(uri=uri)

            response_status = is_response_ok(response)

            if STATUS_OK != response_status:
                print 'Response not ok: %s' % response_status  # pragma: no cover
                return None  # pragma: no cover

            return content
        except Exception:  # pragma: no cover
            servernotfound_exception()

    def create_fav(self, tweet_id):
        if not self.is_authenticated:
            self._authenticate()

        uri = self._directory_api.get_url_new_fav()
        body = 'id=' + tweet_id

        try:
            response, content = self._client.request(uri=uri, body=body, method='POST')

            response_status = is_response_ok(response)

            if STATUS_OK != response_status:
                print 'Response not ok: %s' % response_status  # pragma: no cover
                return None  # pragma: no cover
            else:
                print 'FV successful'  # pragma: no cover
        except Exception:  # pragma: no cover
            servernotfound_exception()

    def get_favs(self):
        pass

    def retweet(self, tweet_id):
        if not self.is_authenticated:
            self._authenticate()

        uri = self._directory_api.get_url_retweet() + '/%s.json' % tweet_id

        try:
            response, content = self._client.request(uri=uri, method='POST')

            response_status = is_response_ok(response)

            if STATUS_OK != response_status:
                print 'Response not ok: %s' % response_status  # pragma: no cover
                return None
            else:
                print 'RT successful'  # pragma: no cover
        except Exception:  # pragma: no cover
            servernotfound_exception()  # pragma: no cover


def is_response_ok(response):
    response_status = int(response['status'])

    if response_status == RESPONSE_OK:
        return STATUS_OK  # pragma: no cover
    elif response_status == RESPONSE_TOO_MANY_REQUEST:
        return 'Too many request. Wait 15 minutes and try again'  # pragma: no cover
    return response_status  # pragma: no cover
