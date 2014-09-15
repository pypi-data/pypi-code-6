import json
import base64
from urllib import urlencode

import requests

from twitter_apponly_auth.models import User
from twitter_apponly_auth.exceptions import ScreenNameRequiredException


# API TODO:
# Pull user timelines; (serialize)
# Access lists resources;
# Search in tweets;
# Retrieve any user information;
# and serialize it all


class Client(object):

    TWITTER_BASE_API = "https://api.twitter.com/"
    TWITTER_API_VERSION = "1.1"
    TWITTER_TOKEN_REQUEST = "oauth2/token"

    def __init__(self, consumer_key="", consumer_secret=""):
        self.encoded_key = base64.b64encode("{}:{}".format(consumer_key, consumer_secret))
        self.bearer_token_request_headers = {
            'Authorization': 'Basic {}'.format(self.encoded_key),
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        }
        token_response = requests.post(
            '{}{}'.format(self.TWITTER_BASE_API,
            self.TWITTER_TOKEN_REQUEST),
            data={'grant_type': 'client_credentials'},
            headers=self.bearer_token_request_headers
        )
        self.access_token = json.loads(token_response.content)['access_token']
        self.api_headers = {'Authorization': 'Bearer {}'.format(self.access_token)}

    @property
    def api_url(self):
        return "{}{}".format(self.TWITTER_BASE_API, self.TWITTER_API_VERSION)

    def get_timeline(self, screen_name="", count=""):
        qs = urlencode({"screen_name": screen_name, "count": count})
        timeline_response = requests.get('{}/statuses/user_timeline.json?{}'.format(self.api_url, qs), headers=self.api_headers)
        return json.loads(timeline_response.content)

    def get_followers(self, screen_name=""):
        return self._get_acquaintences(screen_name, 'followers')

    def get_friends(self, screen_name=""):
        return self._get_acquaintences(screen_name, 'friends')

    def _get_acquaintences(self, screen_name="", key=""):
        if not screen_name:
            raise ScreenNameRequiredException("You must provide a screen name to search on")
        qs = urlencode({"screen_name": screen_name})
        followers_response = requests.get('{}/{}/list.json?{}'.format(self.api_url, key, qs), headers=self.api_headers)
        users = json.loads(followers_response.content)['users']
        return [User(data) for data in users]
