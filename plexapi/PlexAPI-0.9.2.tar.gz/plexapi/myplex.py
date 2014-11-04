"""
PlexAPI MyPlex
"""
import plexapi, requests
from requests.status_codes import _codes as codes
from plexapi.exceptions import BadRequest
from xml.etree import ElementTree

MYPLEX_LOGIN = 'https://my.plexapp.com/users/sign_in.xml'


class MyPlexUser:
    """ Logs into my.plexapp.com. """

    def __init__(self, username, password):
        data = self.sign_in(username, password)
        self.email = data.attrib.get('email')
        self.id = data.attrib.get('id')
        self.thumb = data.attrib.get('thumb')
        self.username = data.attrib.get('username')
        self.title = data.attrib.get('title')
        self.cloudSyncDevice = data.attrib.get('cloudSyncDevice')
        self.authenticationToken = data.attrib.get('authenticationToken')
        self.queueEmail = data.attrib.get('queueEmail')
        self.queueUid = data.attrib.get('queueUid')

    def sign_in(self, username, password):
        headers = {
            'X-Plex-Platform': plexapi.X_PLEX_PLATFORM,
            'X-Plex-Platform-Version': plexapi.X_PLEX_PLATFORM_VERSION,
            'X-Plex-Provides': plexapi.X_PLEX_PROVIDES,
            'X-Plex-Product': plexapi.X_PLEX_PRODUCT,
            'X-Plex-Version': plexapi.X_PLEX_VERSION,
            'X-Plex-Device': plexapi.X_PLEX_DEVICE,
            'X-Plex-Client-Identifier': plexapi.X_PLEX_IDENTIFIER,
        }
        response = requests.post(MYPLEX_LOGIN, headers=headers, auth=(username, password), timeout=5)
        if response.status_code != requests.codes.created:
            codename = codes.get(response.status_code)[0]
            raise BadRequest('(%s) %s' % (response.status_code, codename))
        data = response.text.encode('utf8')
        return ElementTree.fromstring(data) if data else None


class MyPlexAccount:
    """ Represents the myPlex account registered on the server. """

    def __init__(self, server, data):
        self.authToken = data.attrib.get('authToken')
        self.username = data.attrib.get('username')
        self.mappingState = data.attrib.get('mappingState')
        self.mappingError = data.attrib.get('mappingError')
        self.mappingErrorMessage = data.attrib.get('mappingErrorMessage')
        self.signInState = data.attrib.get('signInState')
        self.publicAddress = data.attrib.get('publicAddress')
        self.publicPort = data.attrib.get('publicPort')
        self.privateAddress = data.attrib.get('privateAddress')
        self.privatePort = data.attrib.get('privatePort')
        self.subscriptionFeatures = data.attrib.get('subscriptionFeatures')
        self.subscriptionActive = data.attrib.get('subscriptionActive')
        self.subscriptionState = data.attrib.get('subscriptionState')


if __name__ == '__main__':
    import sys
    myplex = MyPlexUser(sys.argv[1], sys.argv[2])
    print myplex.__dict__
