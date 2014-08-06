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
from datetime import datetime

from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift.transport import THttpClient
from thrift.protocol import TCompactProtocol

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#from curve import CurveThrift
from curve import CurveThrift
from curve.ttypes import TalkException

try:
    import simplejson as json
except ImportError:
    import json

__all__ = ['LineClient']

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

class LineMessage:
    """LineMessage wrapper"""

    TEXT      = 0
    IMAGE     = 1
    VIDEO     = 2
    AUDIO     = 3
    HTML      = 4
    PDF       = 5
    CALL      = 6
    STICKER   = 7
    PRESENCE  = 8
    GIFT      = 9
    GROUBOARD = 10
    APPLINK   = 11

    def __init__(self, client, message):
        self._client = client
        self.type = message.type
        self.text = message.text
        self.id   = message.id

        self.sender   = client.getContactFromId(message._from)
        self.receiver = client.getContactFromId(message.to)

        self.sendTime = datetime.fromtimestamp(message.createdTime/1000)
        self.contentPreview = message.contentPreview

    def __repr__(self):
        return 'LineMessage (type=%s, sender=%s, receiver=%s) "%s"' % (
                    self.type,
                    self.sender,
                    self.receiver,
                    self.text
                )

class LineGroup(object):
    """LineGroup wrapper
    
    :param client: LineClient instance
    :param group: Group instace
    """
    def __init__(self, client, group):
        self._client  = client
        self._group   = group

        self.id      = group.id
        self.name    = group.name
        self.creator = LineContact(client, group.creator)

        self.members = []
        for member in group.members:
            self.members.append(LineContact(client, member))

        self.invitee = []
        if group.invitee:
            for member in group.invitee:
                self.invitee.append(LineContact(client, member))

    def sendMessage(self, text):
        try:
            message = CurveThrift.Message(to=self.id, text=text)
            self._client._sendMessage(message)

            return True
        except Exception as e:
            raise e

    def sendSticker(self,
                    stickerId = "1",
                    stickerPackageId = "1",
                    stickerVersion = "100",
                    stickerText="[null]"):
        try:
            message = CurveThrift.Message(to=self.id, text="")
            message.contentType = CurveThrift.ContentType.STICKER

            message.contentMetadata = {
                'STKID': stickerId,
                'STKPKGID': stickerPackageId,
                'STKVER': stickerVersion,
                'STKTXT': stickerText,
            }

            self._client._sendMessage(message)

            return True
        except Exception as e:
            raise e

    def getRecentMessages(self, count=1):
        """Get recent messages"""
        try:
            messages = self._client._getRecentMessages(self.messageBox.id, count)
            return messages
        except:
            messageBoxWrapUp = self._client._getMessageBoxCompactWrapUp(self.id)
            self.messageBox = messageBoxWrapUp.messageBox

            messages = self._client._getRecentMessages(self.messageBox.id, count)
            return messages

    def __repr__(self):
        """Name of Group and number of group members"""
        return '<LineGroup %s #%s>' % (self.name, len(self.members))

    def __lt__(self, other):
        return self.id < other.id

class LineContact(object):
    """LineContact wrapper
    
    :param client: LineClient instance
    :param contact: Conatct instace
    """
    def __init__(self, client, contact):
        self._client  = client
        self._contact = contact

        self.id           = contact.mid
        self.displayName   = contact.displayName
        self.statusMessage = contact.statusMessage

    def getRecentMessages(self, count=1):
        try:
            messages = self._client._getRecentMessages(self.messageBox.id, count)
            return messages
        except:
            messageBoxWrapUp = self._client._getMessageBoxCompactWrapUp(self.id)
            self.messageBox = messageBoxWrapUp.messageBox

            messages = self._client._getRecentMessages(self.messageBox.id, count)
            return messages

    def sendSticker(self,
                    stickerId = "1",
                    stickerPackageId = "1",
                    stickerVersion = "100",
                    stickerText="[null]"):
        try:
            message = CurveThrift.Message(to=self.id, text="")
            message.contentType = CurveThrift.ContentType.STICKER

            message.contentMetadata = {
                'STKID': stickerId,
                'STKPKGID': stickerPackageId,
                'STKVER': stickerVersion,
                'STKTXT': stickerText,
            }

            self._client._sendMessage(message)

            return True
        except Exception as e:
            raise e

    def sendImage(self, path):
        try:
            img = open(path, 'r')

            message = CurveThrift.Message(to=self.id, text=text)
            message.contentType = CurveThrift.ContentType.IMAGE
            message.contentPreview = img.read().encode('utf-8')

            self.raise_error("not implemented yet")

            url = None

            message.contentMetadata = {
                'PREVIEW_URL': url,
                'DOWNLOAD_URL': url,
                'PUBLIC': True,
            }

            self._client._sendMessage(message)

            return True
        except Exception as e:
            raise e

    def sendImageWithURL(self, url):
        try:
            response = requests.get(url, stream=True)

            message = CurveThrift.Message(to=self.id, text=None)
            message.contentType = CurveThrift.ContentType.IMAGE
            message.contentPreview = response.raw.read()
            #message.contentPreview = url.encode('utf-8')

            message.contentMetadata = {
                'PREVIEW_URL': url,
                'DOWNLOAD_URL': url,
                'PUBLIC': "True",
            }

            self._client._sendMessage(message, seq=1)

            return True
        except Exception as e:
            raise e

    def sendMessage(self, text):
        try:
            message = CurveThrift.Message(to=self.id, text=text)
            self._client._sendMessage(message)

            return True
        except Exception as e:
            raise e

    def __repr__(self):
        return '<LineContact %s (%s)>' % (self.displayName, self.id)

    def __lt__(self, other):
        return self.id < other.id

class LineClient(object):
    """This class proviede you a way to communicate with LINE server.

        >>> client = LineClient(\'carpedm20\', \'xxxxxxxxxx\')
        Enter PinCode '9779' to your mobile phone in 2 minutes
        >>> print client.profile
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

    revision = 0
    profile  = None
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

            self.ready()
        else:
            if EMAIL_REGEX.match(id):
                self.provider = CurveThrift.Provider.LINE # LINE
            else:
                self.provider = CurveThrift.Provider.NAVER_KR # NAVER

            self.id = id
            self.password = password
            self.is_mac = is_mac

            self.login()
            self.ready()

        self.revision = self._getLastOpRevision()
        self.refreshContacts()
        self.refreshGroups()

    def ready(self):
        """
        After login, make `client` and `client_in` instance
        to communicate with LINE server
        """
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

    def login(self):
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

    def refreshGroups(self):
        """Refresh groups of LineClient """
        if self.check_auth():
            group_ids = self._getGroupIdsJoined()
            groups    = self._getGroups(group_ids)

            self.groups = []

            for group in groups:
                self.groups.append(LineGroup(self, group))

            self.groups.sort()

    def refreshContacts(self):
        """Refresh contacts of LineClient """
        if self.check_auth():
            contact_ids = self._getAllContactIds()
            contacts    = self._getContacts(contact_ids)

            self.contacts = []

            for contact in contacts:
                self.contacts.append(LineContact(self, contact))

            self.profile = LineContact(self, self._getProfile())

            self.contacts.append(self.profile)
            self.contacts.sort()

    def getContactFromId(self, id):
        for contact in self.contacts:
            if contact.id == id:
                return contact

        return None

    def getGroupFromId(self, id):
        for group in self.groups:
            if group.id == id:
                return group

        return None

    def getContactOrGroupFromId(self, id):
        for contact in self.contacts:
            if contact.id == id:
                return contact

        for group in self.groups:
            if group.id == id:
                return group

        return None

    def longPoll(self, count=10, func=None):
        """Check is there any operations from LINE server"""
        OT = CurveThrift.OperationType

        operations = self.client_in.fetchOperations(self.revision, count)

        for operation in operations:
            if operation.type == OT.END_OF_OPERATION:
                pass
            elif operation.type == OT.SEND_MESSAGE:
                pass
            elif operation.type == OT.RECEIVE_MESSAGE:
                message = operation.message
                group_or_contact = self.getContactOrGroupFromId(message.to)

                if func != None:
                    func(group_or_contact, message)

                yield (group_or_contact, message)
            else:
                print operation

            self.revision = max(operation.revision, self.revision)

    def raise_error(self, msg):
        """Fix a error format"""
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

    def _getProfile(self):
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

    def _getAllContactIds(self):
        """Get all contacts of your LINE account"""
        if self.check_auth():
            return self.client.getAllContactIds()

    def _getContacts(self, ids):
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

    def _getGroupIdsJoined(self):
        """Get group id that you joined"""
        if self.check_auth():
            return self.client.getGroupIdsJoined()

    def _getGroups(self, ids):
        if type(ids) != list:
            msg = "argument should be list of group ids"
            raise_error(msg)

        if self.check_auth():
            return self.client.getGroups(ids)

    def _getRecentMessages(self, id, count=1):
        """Get recent messages from `id`"""
        if self.check_auth():
            return self.client.getRecentMessages(id, count)

    def _sendMessage(self, message, seq=0):
        """Send a message to `id`. `id` could be contact id or group id

        :param id: `contact` id or `group` id
        :param message: `message` instance
        """
        if self.check_auth():
            return self.client.sendMessage(seq, message)

    def _getLastOpRevision(self):
        if self.check_auth():
            return self.client.getLastOpRevision()

    def _fetchOperations(self, revision, count=50):
        if self.check_auth():
            return self.client.fetchOperations(revision, count)

    def _getMessageBoxCompactWrapUp(self, id):
        if self.check_auth():
            try:
                return self.client.getMessageBoxCompactWrapUp(id)
            except Exception as e:
                msg = e
                raise_error(msg)

