# -*- coding: utf-8 -*-
"""
    line.client
    ~~~~~~~~~~~

    LineClient for sending and receiving message from LINE server.

    :copyright: (c) 2014 by Taehoon Kim.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import unicode_literals
import re
import rsa
import requests
from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift.transport import THttpClient
from thrift.protocol import TCompactProtocol
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#from curve import CurveThrift
from curve import CurveThrift

try:
    import simplejson as json
except ImportError:
    import json

__all__ = ['LineClient']

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

class LineContact(object):
    """Contact object for LINE"""
    def __init__(self, client, contact):
        self._client  = client
        self._contact = contact

        self.mid           = contact.mid
        self.displayName   = contact.displayName
        self.statusMessage = contact.statusMessage

    def sendMessage(self, text):
        try:
            self._client.sendMessage(id=self.mid, text=text)
            return True
        except Exception as e:
            raise e

    def __repr__(self):
        return '<LineContact %s (%s)>' % (self.displayName, self.mid)

    def __lt__(self, other):
        return self.mid < other.mid

class LineClient(object):
    """This class proviede you a way to communicate with LINE server.

        >>> client = LineClient(\'carpedm20\', \'xxxxxxxxxx\')
        Enter PinCode '9779' to your mobile phone in 2 minutes
        >>> print client.getProfile()
    """

    LINE_DOMAIN = "http://gd2.line.naver.jp"

    LINE_HTTP_URL          = LINE_DOMAIN + "/api/v4/TalkService.do"
    LINE_HTTP_IN_URL       = LINE_DOMAIN + "/P4"
    LINE_CERTIFICATE_URL   = LINE_DOMAIN + "/Q"
    LINE_SESSION_LINE_URL  = LINE_DOMAIN + "/authct/v1/keys/line"
    LINE_SESSION_NAVER_URL = LINE_DOMAIN + "/authct/v1/keys/naver"

    ip          = "127.0.0.1"
    version     = "3.7.0"
    com_name    = ""

    contacts = []
    rooms    = []
    groups   = []

    _session = requests.session()
    _headers = {}

    def __init__(self, id=None, password=None, authToken=None, is_mac=True, com_name="carpedm20"):
        """Initialize LINE instance with provided information

        :param id: `NAVER id` or `LINE email`
        :param password: LINE account password
        :param authToken: LINE session key
        :param is_mac: (optional) os setting
        :param com_name: (optional) name of your system
        """

        if not (authToken or id and password):
            msg = "id and password or authToken is needed"
            self.raise_error(msg)

        if is_mac:
            os_version = "10.9.4-MAVERICKS-x64"
            user_agent = "DESKTOP:MAC:%s(%s)" % (os_version, self.version)
            app = "DESKTOPMAC\t%s\tMAC\t%s" % (self.version, os_version)
        else:
            os_version = "5.1.2600-XP-x64"
            user_agent = "DESKTOP:WIN:%s(%s)" % (os_version, self.version)
            app = "DESKTOPWIN\t%s\tWINDOWS\t%s" % (self.version, os_version)

        if com_name:
            self.com_name = com_name

        self._headers['User-Agent']         = user_agent
        self._headers['X-Line-Application'] = app

        if authToken:
            self.authToken = self._headers['X-Line-Access'] = authToken

            self._ready()
        else:
            if EMAIL_REGEX.match(id):
                self.provider = CurveThrift.Provider.LINE # LINE
            else:
                self.provider = CurveThrift.Provider.NAVER_KR # NAVER

            self.id = id
            self.password = password
            self.is_mac = is_mac

            self._login()
            self._ready()

        self.refreshContacts()

    def raise_error(self, msg):
        raise Exception("Error: %s" % msg)

    def get_json(self, url):
        """Get josn from given url with saved session and headers"""
        return json.loads(self._session.get(url, headers=self._headers).text)

    def check_auth(self):
        """Check if client is logged in or not"""
        if self.authToken:
            return True
        else:
            msg = "you need to login"
            self.raise_error(msg)

    def getProfile(self):
        """Get profile information
        
        :returns: Profile object
                    - picturePath
                    - displayName
                    - phone (base64 encoded?)
                    - allowSearchByUserid
                    - pictureStatus
                    - userid
                    - mid # used for unique id for account
                    - phoneticName
                    - regionCode
                    - allowSearchByEmail
                    - email
                    - statusMessage
        """
        if self.check_auth():
            return self.client.getProfile()

    def refreshContacts(self):
        contact_ids = self.getAllContactIds()
        contacts    = self.getContacts(contact_ids)

        self.contacts = []

        for contact in contacts:
            self.contacts.append(LineContact(self, contact))

        self.profile  = self.getProfile()
        self.contacts.append(LineContact(self, self.profile))
        self.contacts.sort()

    def getAllContactIds(self):
        """Get all contacts of your LINE account"""
        if self.check_auth():
            return self.client.getAllContactIds()

    def getContacts(self, ids):
        """Get contact information list from ids
        
        :returns: List of Contact list
                    - status
                    - capableVideoCall
                    - dispalyName
                    - settings
                    - pictureStatus
                    - capableVoiceCall
                    - capableBuddy
                    - mid
                    - displayNameOverridden
                    - relation
                    - thumbnailUrl_
                    - createdTime
                    - facoriteTime
                    - capableMyhome
                    - attributes
                    - type
                    - phoneticName
                    - statusMessage
        """
        if type(ids) != list:
            msg = "argument should be list of contact ids"
            raise_error(msg)

        if self.check_auth():
            return self.client.getContacts(ids)

    def getGroupIdsJoined(self):
        """Get group id that you joined"""
        if self.check_auth():
            return self.client.getGroupIdsJoined()

    def getGroups(self, ids):
        if type(ids) != list:
            msg = "argument should be list of group ids"
            raise_error(msg)

        if self.check_auth():
            return self.client.getGroups(ids)

    def getRecentMessages(self, id, count=1):
        if self.check_auth():
            return self.client.getRecentMessages(id, count)

    def sendMessage(self, id, text, seq=0):
        if self.check_auth():
            message = CurveThrift.Message(to=id,text=text)

            return self.client.sendMessage(seq, message)

    def getLastOpRevision(self):
        if self.check_auth():
            return self.client.getLastOpRevision()

    def _ready(self):
        self.transport    = THttpClient.THttpClient(self.LINE_HTTP_URL)
        self.transport_in = THttpClient.THttpClient(self.LINE_HTTP_IN_URL)

        self.transport.setCustomHeaders(self._headers)
        self.transport_in.setCustomHeaders(self._headers)

        self.protocol    = TCompactProtocol.TCompactProtocol(self.transport)
        self.protocol_in = TCompactProtocol.TCompactProtocol(self.transport_in)

        self.client    = CurveThrift.Client(self.protocol)
        self.client_in = CurveThrift.Client(self.protocol_in)

        self.transport.open()
        self.transport_in.open()

    def _login(self):
        """Login to LINE server."""
        if self.provider == CurveThrift.Provider.LINE: # LINE
            j = self.get_json(self.LINE_SESSION_LINE_URL)
        else: # NAVER
            j = self.get_json(self.LINE_SESSION_NAVER_URL)

        session_key = j['session_key']
        message     = (chr(len(session_key)) + session_key +
                       chr(len(self.id)) + self.id +
                       chr(len(self.password)) + self.password).encode('utf-8')

        keyname, n, e = j['rsa_key'].split(",")
        pub_key       = rsa.PublicKey(int(n,16), int(e,16))
        crypto        = rsa.encrypt(message, pub_key).encode('hex')

        self.transport = THttpClient.THttpClient(self.LINE_HTTP_URL)
        self.transport.setCustomHeaders(self._headers)

        self.protocol = TCompactProtocol.TCompactProtocol(self.transport)
        self.client   = CurveThrift.Client(self.protocol)

        msg = self.client.loginWithIdentityCredentialForCertificate(
                self.id, self.password, keyname, crypto, False, self.ip,
                self.com_name, self.provider, "")
        
        self._headers['X-Line-Access'] = msg.verifier
        self._pinCode = msg.pinCode

        print "Enter PinCode '%s' to your mobile phone in 2 minutes"\
                % self._pinCode

        j = self.get_json(self.LINE_CERTIFICATE_URL)
        self.verifier = j['result']['verifier']

        msg = self.client.loginWithVerifierForCertificate(self.verifier)

        if msg.type == 1:
            self.certificate = msg.certificate
            self.authToken = self._headers['X-Line-Access'] = msg.authToken
        elif msg.type == 2:
            msg = "require QR code"
            self.raise_error(msg)
        else:
            msg = "require device confirm"
            self.raise_error(msg)
