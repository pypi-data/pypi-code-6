"""
PlexServer
"""
import requests, urllib
from requests.status_codes import _codes as codes
from plexapi import video
from plexapi.client import Client
from plexapi.exceptions import BadRequest, NotFound
from plexapi.library import Library
from plexapi.myplex import MyPlexAccount
from plexapi.playqueue import PlayQueue
from xml.etree import ElementTree

TOTAL_QUERIES = 0


class PlexServer(object):
    
    def __init__(self, host='localhost', port=32400):
        self.host = self._cleanHost(host)
        self.port = port
        self.data = self.query('/')
        self.friendlyName = self.data.attrib.get('friendlyName')
        self.machineIdentifier = self.data.attrib.get('machineIdentifier')
        self.myPlex = bool(self.data.attrib.get('myPlex'))
        self.myPlexMappingState = self.data.attrib.get('myPlexMappingState')
        self.myPlexSigninState = self.data.attrib.get('myPlexSigninState')
        self.myPlexSubscription = self.data.attrib.get('myPlexSubscription')
        self.myPlexUsername = self.data.attrib.get('myPlexUsername')
        self.platform = self.data.attrib.get('platform')
        self.platformVersion = self.data.attrib.get('platformVersion')
        self.transcoderActiveVideoSessions = int(self.data.attrib.get('transcoderActiveVideoSessions'))
        self.updatedAt = int(self.data.attrib.get('updatedAt'))
        self.version = self.data.attrib.get('version')
        self.token = None

    def __repr__(self):
        return '<%s:%s:%s>' % (self.__class__.__name__, self.host, self.port)

    def _cleanHost(self, host):
        host = host.lower().strip('/')
        if host.startswith('http://'):
            host = host[8:]
        return host
    
    @property
    def library(self):
        return Library(self, self.query('/library'))

    def account(self):
        data = self.query('/myplex/account')
        return MyPlexAccount(self, data)

    def clients(self):
        items = []
        for elem in self.query('/clients'):
            items.append(Client(self, elem))
        return items

    def client(self, name):
        for elem in self.query('/clients'):
            if elem.attrib.get('name') == name:
                return Client(self, elem)
        raise NotFound('Unknown client name: %s' % name)

    def createPlayQueue(self, video):
        return PlayQueue.create(self, video)

    def query(self, path, method=requests.get):
        global TOTAL_QUERIES; TOTAL_QUERIES += 1
        response = method(self.url(path), timeout=5)
        if response.status_code not in [200, 201]:
            codename = codes.get(response.status_code)[0]
            raise BadRequest('(%s) %s' % (response.status_code, codename))
        data = response.text.encode('utf8')
        return ElementTree.fromstring(data) if data else None

    def search(self, query, videotype=None):
        query = urllib.quote(query)
        items = video.list_items(self, '/search?query=%s' % query)
        if videotype:
            return [item for item in items if item.type == videotype]
        return items

    def url(self, path):
        return 'http://%s:%s/%s' % (self.host, self.port, path.lstrip('/'))
