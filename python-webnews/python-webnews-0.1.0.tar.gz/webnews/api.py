import json
import enum
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib import request

class APINonSingle:

    def __init__(self, api_key, agent = "webnews-python", webnews_base = "https://webnews.csh.rit.edu/"):
        self.agent = agent
        self.api_key = api_key
        self.webnews_base = webnews_base

    class Actions(enum.Enum):
        user = "user"
        unread_counts = "unread_counts"
        newsgroups = "newsgroups"
        search = "search"
        compose = "compose"

    def POST(self, action, args={}):
        if type(action) == API.Actions:
            action = action.value
        args['api_key'] = self.api_key
        args['api_agent'] = self.agent
        args = urlencode(args).encode('utf-8')
        req = request.Request(self.webnews_base+ action)
        req.add_header('Accept', 'application/json')
        resp = urlopen(req, args).read().decode('utf-8')
        return json.loads(resp)


    def GET(self, action, args={}):
        if type(action) == API.Actions:
            action = action.value
        args['api_key'] = self.api_key
        args['api_agent'] = self.agent
        args = urlencode(args)
        req = request.Request(self.webnews_base + action + '?' + args)
        req.add_header('Accept', 'application/json')
        resp = urlopen(req).read().decode('utf-8')
        return json.loads(resp)

    def user(self):
        return self.GET(API.Actions.user)

    def unread_counts(self):
        return self.GET(API.Actions.unread_counts)

    def newsgroups(self):
        return self.GET(API.Actions.newsgroups)

    def newsgroups_search(self, newsgroup):
        return self.GET("newsgroups/" + newsgroup)

    def newsgroup_posts(self, newsgroup, params={}):
        return self.GET(newsgroup + '/index', params)

    def search(self, params = {}):
        return self.GET(API.Actions.search, params)

    def post_specifics(self, newsgroup, index, params={}):
        return self.GET(str(newsgroup)+"/"+str(index), params)

    def compose(self, newsgroup, subject, body, params={}):
        params['subject'] = subject
        params['body'] = body
        params['newsgroup'] = newsgroup
        return self.POST(API.Actions.compose, params)

"""
Wrap the APINonSingle object so that
only a single object for each key will exist.

Optimization for object implementation
"""
class API(APINonSingle):
    _instance = {}
    def __new__(cls, *args, **kwargs):
        if not args[0] in cls._instance:
            cls._instance[args[0]] = APINonSingle(*args, **kwargs)
        return cls._instance[args[0]]
