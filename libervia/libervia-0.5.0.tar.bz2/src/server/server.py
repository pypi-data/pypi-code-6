#!/usr/bin/python
# -*- coding: utf-8 -*-

# Libervia: a Salut à Toi frontend
# Copyright (C) 2011, 2012, 2013, 2014 Jérôme Poisson <goffi@goffi.org>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from twisted.application import service
from twisted.internet import reactor, defer
from twisted.web import server
from twisted.web.static import File
from twisted.web.resource import Resource, NoResource
from twisted.web.util import Redirect, redirectTo
from twisted.python.components import registerAdapter
from twisted.python.failure import Failure
from twisted.words.protocols.jabber.jid import JID

from txjsonrpc.web import jsonrpc
from txjsonrpc import jsonrpclib

from sat.core.log import getLogger
log = getLogger(__name__)
from sat_frontends.bridge.DBus import DBusBridgeFrontend, BridgeExceptionNoService
from sat.core.i18n import _, D_
from sat.tools.xml_tools import paramsXML2XMLUI

import re
import glob
import os.path
import sys
import tempfile
import shutil
import uuid
from zope.interface import Interface, Attribute, implements
from xml.dom import minidom
from httplib import HTTPS_PORT

try:
    import OpenSSL
    from twisted.internet import ssl
    ssl_available = True
except:
    ssl_available = False

from libervia.server.constants import Const as C
from libervia.server.blog import MicroBlog

# following value are set from twisted.plugins.libervia_server initialise (see the comment there)
DATA_DIR_DEFAULT = OPT_PARAMETERS_BOTH = OPT_PARAMETERS_CFG = coerceDataDir = None

class ISATSession(Interface):
    profile = Attribute("Sat profile")
    jid = Attribute("JID associated with the profile")


class SATSession(object):
    implements(ISATSession)

    def __init__(self, session):
        self.profile = None
        self.jid = None


class LiberviaSession(server.Session):
    sessionTimeout = C.TIMEOUT

    def __init__(self, *args, **kwargs):
        self.__lock = False
        server.Session.__init__(self, *args, **kwargs)

    def lock(self):
        """Prevent session from expiring"""
        self.__lock = True
        self._expireCall.reset(sys.maxint)

    def unlock(self):
        """Allow session to expire again, and touch it"""
        self.__lock = False
        self.touch()

    def touch(self):
        if not self.__lock:
            server.Session.touch(self)


class ProtectedFile(File):
    """A File class which doens't show directory listing"""

    def directoryListing(self):
        return NoResource()


class SATActionIDHandler(object):
    """Manage SàT action action_id lifecycle"""
    ID_LIFETIME = 30  # after this time (in seconds), action_id will be suppressed and action result will be ignored

    def __init__(self):
        self.waiting_ids = {}

    def waitForId(self, callback, action_id, profile, *args, **kwargs):
        """Wait for an action result

        @param callback: method to call when action gave a result back
        @param action_id: action_id to wait for
        @param profile: %(doc_profile)s
        @param *args: additional argument to pass to callback
        @param **kwargs: idem
        """
        action_tuple = (action_id, profile)
        self.waiting_ids[action_tuple] = (callback, args, kwargs)
        reactor.callLater(self.ID_LIFETIME, self.purgeID, action_tuple)

    def purgeID(self, action_tuple):
        """Called when an action_id has not be handled in time"""
        if action_tuple in self.waiting_ids:
            log.warning("action of action_id %s [%s] has not been managed, action_id is now ignored" % action_tuple)
            del self.waiting_ids[action_tuple]

    def actionResultCb(self, answer_type, action_id, data, profile):
        """Manage the actionResult signal"""
        action_tuple = (action_id, profile)
        if action_tuple in self.waiting_ids:
            callback, args, kwargs = self.waiting_ids[action_tuple]
            del self.waiting_ids[action_tuple]
            callback(answer_type, action_id, data, *args, **kwargs)


class JSONRPCMethodManager(jsonrpc.JSONRPC):

    def __init__(self, sat_host):
        jsonrpc.JSONRPC.__init__(self)
        self.sat_host = sat_host

    def asyncBridgeCall(self, method_name, *args, **kwargs):
        """Call an asynchrone bridge method and return a deferred
        @param method_name: name of the method as a unicode
        @return: a deferred which trigger the result

        """
        d = defer.Deferred()

        def _callback(*args):
            if not args:
                d.callback(None)
            else:
                if len(args) != 1:
                    Exception("Multiple return arguments not supported")
                d.callback(args[0])

        def _errback(result):
            d.errback(Failure(jsonrpclib.Fault(C.ERRNUM_BRIDGE_ERRBACK, result.classname)))

        kwargs["callback"] = _callback
        kwargs["errback"] = _errback
        getattr(self.sat_host.bridge, method_name)(*args, **kwargs)
        return d


class MethodHandler(JSONRPCMethodManager):

    def __init__(self, sat_host):
        JSONRPCMethodManager.__init__(self, sat_host)
        self.authorized_params = None

    def render(self, request):
        self.session = request.getSession()
        profile = ISATSession(self.session).profile
        if not profile:
            #user is not identified, we return a jsonrpc fault
            parsed = jsonrpclib.loads(request.content.read())
            fault = jsonrpclib.Fault(C.ERRNUM_LIBERVIA, C.NOT_ALLOWED)  # FIXME: define some standard error codes for libervia
            return jsonrpc.JSONRPC._cbRender(self, fault, request, parsed.get('id'), parsed.get('jsonrpc'))  # pylint: disable=E1103
        return jsonrpc.JSONRPC.render(self, request)

    def jsonrpc_getProfileJid(self):
        """Return the jid of the profile"""
        sat_session = ISATSession(self.session)
        profile = sat_session.profile
        sat_session.jid = JID(self.sat_host.bridge.getParamA("JabberID", "Connection", profile_key=profile))
        return sat_session.jid.full()

    def jsonrpc_disconnect(self):
        """Disconnect the profile"""
        sat_session = ISATSession(self.session)
        profile = sat_session.profile
        self.sat_host.bridge.disconnect(profile)

    def jsonrpc_getContacts(self):
        """Return all passed args."""
        profile = ISATSession(self.session).profile
        return self.sat_host.bridge.getContacts(profile)

    def jsonrpc_addContact(self, entity, name, groups):
        """Subscribe to contact presence, and add it to the given groups"""
        profile = ISATSession(self.session).profile
        self.sat_host.bridge.addContact(entity, profile)
        self.sat_host.bridge.updateContact(entity, name, groups, profile)

    def jsonrpc_delContact(self, entity):
        """Remove contact from contacts list"""
        profile = ISATSession(self.session).profile
        self.sat_host.bridge.delContact(entity, profile)

    def jsonrpc_updateContact(self, entity, name, groups):
        """Update contact's roster item"""
        profile = ISATSession(self.session).profile
        self.sat_host.bridge.updateContact(entity, name, groups, profile)

    def jsonrpc_subscription(self, sub_type, entity, name, groups):
        """Confirm (or infirm) subscription,
        and setup user roster in case of subscription"""
        profile = ISATSession(self.session).profile
        self.sat_host.bridge.subscription(sub_type, entity, profile)
        if sub_type == 'subscribed':
            self.sat_host.bridge.updateContact(entity, name, groups, profile)

    def jsonrpc_getWaitingSub(self):
        """Return list of room already joined by user"""
        profile = ISATSession(self.session).profile
        return self.sat_host.bridge.getWaitingSub(profile)

    def jsonrpc_setStatus(self, presence, status):
        """Change the presence and/or status
        @param presence: value from ("", "chat", "away", "dnd", "xa")
        @param status: any string to describe your status
        """
        profile = ISATSession(self.session).profile
        self.sat_host.bridge.setPresence('', presence, {'': status}, profile)

    def jsonrpc_sendMessage(self, to_jid, msg, subject, type_, options={}):
        """send message"""
        profile = ISATSession(self.session).profile
        return self.asyncBridgeCall("sendMessage", to_jid, msg, subject, type_, options, profile)

    def jsonrpc_sendMblog(self, type_, dest, text, extra={}):
        """ Send microblog message
        @param type_: one of "PUBLIC", "GROUP"
        @param dest: destinees (list of groups, ignored for "PUBLIC")
        @param text: microblog's text
        """
        profile = ISATSession(self.session).profile
        extra['allow_comments'] = 'True'

        if not type_:  # auto-detect
            type_ = "PUBLIC" if dest == [] else "GROUP"

        if type_ in ("PUBLIC", "GROUP") and text:
            if type_ == "PUBLIC":
                #This text if for the public microblog
                log.debug("sending public blog")
                return self.sat_host.bridge.sendGroupBlog("PUBLIC", [], text, extra, profile)
            else:
                log.debug("sending group blog")
                dest = dest if isinstance(dest, list) else [dest]
                return self.sat_host.bridge.sendGroupBlog("GROUP", dest, text, extra, profile)
        else:
            raise Exception("Invalid data")

    def jsonrpc_deleteMblog(self, pub_data, comments):
        """Delete a microblog node
        @param pub_data: a tuple (service, comment node identifier, item identifier)
        @param comments: comments node identifier (for main item) or False
        """
        profile = ISATSession(self.session).profile
        return self.sat_host.bridge.deleteGroupBlog(pub_data, comments if comments else '', profile)

    def jsonrpc_updateMblog(self, pub_data, comments, message, extra={}):
        """Modify a microblog node
        @param pub_data: a tuple (service, comment node identifier, item identifier)
        @param comments: comments node identifier (for main item) or False
        @param message: new message
        @param extra: dict which option name as key, which can be:
            - allow_comments: True to accept an other level of comments, False else (default: False)
            - rich: if present, contain rich text in currently selected syntax
        """
        profile = ISATSession(self.session).profile
        if comments:
            extra['allow_comments'] = 'True'
        return self.sat_host.bridge.updateGroupBlog(pub_data, comments if comments else '', message, extra, profile)

    def jsonrpc_sendMblogComment(self, node, text, extra={}):
        """ Send microblog message
        @param node: url of the comments node
        @param text: comment
        """
        profile = ISATSession(self.session).profile
        if node and text:
            return self.sat_host.bridge.sendGroupBlogComment(node, text, extra, profile)
        else:
            raise Exception("Invalid data")

    def jsonrpc_getMblogs(self, publisher_jid, item_ids):
        """Get specified microblogs posted by a contact
        @param publisher_jid: jid of the publisher
        @param item_ids: list of microblogs items IDs
        @return list of microblog data (dict)"""
        profile = ISATSession(self.session).profile
        d = self.asyncBridgeCall("getGroupBlogs", publisher_jid, item_ids, profile)
        return d

    def jsonrpc_getMblogsWithComments(self, publisher_jid, item_ids):
        """Get specified microblogs posted by a contact and their comments
        @param publisher_jid: jid of the publisher
        @param item_ids: list of microblogs items IDs
        @return list of couple (microblog data, list of microblog data)"""
        profile = ISATSession(self.session).profile
        d = self.asyncBridgeCall("getGroupBlogsWithComments", publisher_jid, item_ids, profile)
        return d

    def jsonrpc_getLastMblogs(self, publisher_jid, max_item):
        """Get last microblogs posted by a contact
        @param publisher_jid: jid of the publisher
        @param max_item: number of items to ask
        @return list of microblog data (dict)"""
        profile = ISATSession(self.session).profile
        d = self.asyncBridgeCall("getLastGroupBlogs", publisher_jid, max_item, profile)
        return d

    def jsonrpc_getMassiveLastMblogs(self, publishers_type, publishers_list, max_item):
        """Get lasts microblogs posted by several contacts at once
        @param publishers_type: one of "ALL", "GROUP", "JID"
        @param publishers_list: list of publishers type (empty list of all, list of groups or list of jids)
        @param max_item: number of items to ask
        @return: dictionary key=publisher's jid, value=list of microblog data (dict)"""
        profile = ISATSession(self.session).profile
        d = self.asyncBridgeCall("getMassiveLastGroupBlogs", publishers_type, publishers_list, max_item, profile)
        self.sat_host.bridge.massiveSubscribeGroupBlogs(publishers_type, publishers_list, profile)
        return d

    def jsonrpc_getMblogComments(self, service, node):
        """Get all comments of given node
        @param service: jid of the service hosting the node
        @param node: comments node
        """
        profile = ISATSession(self.session).profile
        d = self.asyncBridgeCall("getGroupBlogComments", service, node, profile)
        return d

    def jsonrpc_getPresenceStatuses(self):
        """Get Presence information for connected contacts"""
        profile = ISATSession(self.session).profile
        return self.sat_host.bridge.getPresenceStatuses(profile)

    def jsonrpc_getHistory(self, from_jid, to_jid, size, between):
        """Return history for the from_jid/to_jid couple"""
        sat_session = ISATSession(self.session)
        profile = sat_session.profile
        sat_jid = sat_session.jid
        if not sat_jid:
            log.error("No jid saved for this profile")
            return {}
        if JID(from_jid).userhost() != sat_jid.userhost() and JID(to_jid).userhost() != sat_jid.userhost():
            log.error("Trying to get history from a different jid, maybe a hack attempt ?")
            return {}
        d = self.asyncBridgeCall("getHistory", from_jid, to_jid, size, between, profile)

        def show(result_dbus):
            result = []
            for line in result_dbus:
                #XXX: we have to do this stupid thing because Python D-Bus use its own types instead of standard types
                #     and txJsonRPC doesn't accept D-Bus types, resulting in a empty query
                timestamp, from_jid, to_jid, message, mess_type, extra = line
                result.append((float(timestamp), unicode(from_jid), unicode(to_jid), unicode(message), unicode(mess_type), dict(extra)))
            return result
        d.addCallback(show)
        return d

    def jsonrpc_joinMUC(self, room_jid, nick):
        """Join a Multi-User Chat room
        @room_jid: leave empty string to generate a unique name
        """
        profile = ISATSession(self.session).profile
        try:
            if room_jid != "":
                room_jid = JID(room_jid).userhost()
        except:
            log.warning('Invalid room jid')
            return
        d = self.asyncBridgeCall("joinMUC", room_jid, nick, {}, profile)
        return d

    def jsonrpc_inviteMUC(self, contact_jid, room_jid):
        """Invite a user to a Multi-User Chat room"""
        profile = ISATSession(self.session).profile
        try:
            room_jid = JID(room_jid).userhost()
        except:
            log.warning('Invalid room jid')
            return
        room_id = room_jid.split("@")[0]
        service = room_jid.split("@")[1]
        self.sat_host.bridge.inviteMUC(contact_jid, service, room_id, {}, profile)

    def jsonrpc_mucLeave(self, room_jid):
        """Quit a Multi-User Chat room"""
        profile = ISATSession(self.session).profile
        try:
            room_jid = JID(room_jid)
        except:
            log.warning('Invalid room jid')
            return
        self.sat_host.bridge.mucLeave(room_jid.userhost(), profile)

    def jsonrpc_getRoomsJoined(self):
        """Return list of room already joined by user"""
        profile = ISATSession(self.session).profile
        return self.sat_host.bridge.getRoomsJoined(profile)

    def jsonrpc_launchTarotGame(self, other_players, room_jid=""):
        """Create a room, invite the other players and start a Tarot game
        @param room_jid: leave empty string to generate a unique room name
        """
        profile = ISATSession(self.session).profile
        try:
            if room_jid != "":
                room_jid = JID(room_jid).userhost()
        except:
            log.warning('Invalid room jid')
            return
        self.sat_host.bridge.tarotGameLaunch(other_players, room_jid, profile)

    def jsonrpc_getTarotCardsPaths(self):
        """Give the path of all the tarot cards"""
        _join = os.path.join
        _media_dir = _join(self.sat_host.media_dir, '')
        return map(lambda x: _join(C.MEDIA_DIR, x[len(_media_dir):]), glob.glob(_join(_media_dir, C.CARDS_DIR, '*_*.png')))

    def jsonrpc_tarotGameReady(self, player, referee):
        """Tell to the server that we are ready to start the game"""
        profile = ISATSession(self.session).profile
        self.sat_host.bridge.tarotGameReady(player, referee, profile)

    def jsonrpc_tarotGamePlayCards(self, player_nick, referee, cards):
        """Tell to the server the cards we want to put on the table"""
        profile = ISATSession(self.session).profile
        self.sat_host.bridge.tarotGamePlayCards(player_nick, referee, cards, profile)

    def jsonrpc_launchRadioCollective(self, invited, room_jid=""):
        """Create a room, invite people, and start a radio collective
        @param room_jid: leave empty string to generate a unique room name
        """
        profile = ISATSession(self.session).profile
        try:
            if room_jid != "":
                room_jid = JID(room_jid).userhost()
        except:
            log.warning('Invalid room jid')
            return
        self.sat_host.bridge.radiocolLaunch(invited, room_jid, profile)

    def jsonrpc_getEntityData(self, jid, keys):
        """Get cached data for an entit
        @param jid: jid of contact from who we want data
        @param keys: name of data we want (list)
        @return: requested data"""
        profile = ISATSession(self.session).profile
        return self.sat_host.bridge.getEntityData(jid, keys, profile)

    def jsonrpc_getCard(self, jid):
        """Get VCard for entiry
        @param jid: jid of contact from who we want data
        @return: id to retrieve the profile"""
        profile = ISATSession(self.session).profile
        return self.sat_host.bridge.getCard(jid, profile)

    def jsonrpc_getAccountDialogUI(self):
        """Get the dialog for managing user account
        @return: XML string of the XMLUI"""
        profile = ISATSession(self.session).profile
        return self.sat_host.bridge.getAccountDialogUI(profile)

    def jsonrpc_getParamsUI(self):
        """Return the parameters XML for profile"""
        profile = ISATSession(self.session).profile
        d = self.asyncBridgeCall("getParams", C.SECURITY_LIMIT, C.APP_NAME, profile)

        def setAuthorizedParams(params_xml):
            if self.authorized_params is None:
                self.authorized_params = {}
                for cat in minidom.parseString(params_xml.encode('utf-8')).getElementsByTagName("category"):
                    params = cat.getElementsByTagName("param")
                    params_list = [param.getAttribute("name") for param in params]
                    self.authorized_params[cat.getAttribute("name")] = params_list
            if self.authorized_params:
                return params_xml
            else:
                return None

        d.addCallback(setAuthorizedParams)

        d.addCallback(lambda params_xml: paramsXML2XMLUI(params_xml) if params_xml else "")

        return d

    def jsonrpc_asyncGetParamA(self, param, category, attribute="value"):
        """Return the parameter value for profile"""
        profile = ISATSession(self.session).profile
        d = self.asyncBridgeCall("asyncGetParamA", param, category, attribute, C.SECURITY_LIMIT, profile_key=profile)
        return d

    def jsonrpc_setParam(self, name, value, category):
        profile = ISATSession(self.session).profile
        if category in self.authorized_params and name in self.authorized_params[category]:
            return self.sat_host.bridge.setParam(name, value, category, C.SECURITY_LIMIT, profile)
        else:
            log.warning("Trying to set parameter '%s' in category '%s' without authorization!!!"
                    % (name, category))

    def jsonrpc_launchAction(self, callback_id, data):
        #FIXME: any action can be launched, this can be a huge security issue if callback_id can be guessed
        #       a security system with authorised callback_id must be implemented, similar to the one for authorised params
        profile = ISATSession(self.session).profile
        d = self.asyncBridgeCall("launchAction", callback_id, data, profile)
        return d

    def jsonrpc_chatStateComposing(self, to_jid_s):
        """Call the method to process a "composing" state.
        @param to_jid_s: contact the user is composing to
        """
        profile = ISATSession(self.session).profile
        self.sat_host.bridge.chatStateComposing(to_jid_s, profile)

    def jsonrpc_getNewAccountDomain(self):
        """@return: the domain for new account creation"""
        d = self.asyncBridgeCall("getNewAccountDomain")
        return d

    def jsonrpc_confirmationAnswer(self, confirmation_id, result, answer_data):
        """Send the user's answer to any previous 'askConfirmation' signal"""
        profile = ISATSession(self.session).profile
        self.sat_host.bridge.confirmationAnswer(confirmation_id, result, answer_data, profile)

    def jsonrpc_syntaxConvert(self, text, syntax_from=C.SYNTAX_XHTML, syntax_to=C.SYNTAX_CURRENT):
        """ Convert a text between two syntaxes
        @param text: text to convert
        @param syntax_from: source syntax (e.g. "markdown")
        @param syntax_to: dest syntax (e.g.: "XHTML")
        @param safe: clean resulting XHTML to avoid malicious code if True (forced here)
        @return: converted text """
        profile = ISATSession(self.session).profile
        return self.sat_host.bridge.syntaxConvert(text, syntax_from, syntax_to, True, profile)

    def jsonrpc_getLastResource(self, jid_s):
        """Get the last active resource of that contact."""
        profile = ISATSession(self.session).profile
        return self.sat_host.bridge.getLastResource(jid_s, profile)

    # FIXME: as this belong to a plugin, it should be managed dynamically
    def jsonrpc_skipOTR(self):
        """Tell the backend to leave OTR handling to Libervia."""
        profile = ISATSession(self.session).profile
        return self.sat_host.bridge.skipOTR(profile)


class Register(JSONRPCMethodManager):
    """This class manage the registration procedure with SàT
    It provide an api for the browser, check password and setup the web server"""

    def __init__(self, sat_host):
        JSONRPCMethodManager.__init__(self, sat_host)
        self.profiles_waiting = {}
        self.request = None

    def getWaitingRequest(self, profile):
        """Tell if a profile is trying to log in"""
        if profile in self.profiles_waiting:
            return self.profiles_waiting[profile]
        else:
            return None

    def render(self, request):
        """
        Render method with some hacks:
           - if login is requested, try to login with form data
           - except login, every method is jsonrpc
           - user doesn't need to be authentified for explicitely listed methods, but must be for all others
        """
        if request.postpath == ['login']:
            return self.loginOrRegister(request)
        _session = request.getSession()
        parsed = jsonrpclib.loads(request.content.read())
        method = parsed.get("method")  # pylint: disable=E1103
        if  method not in ['isRegistered', 'registerParams', 'getMenus']:
            #if we don't call these methods, we need to be identified
            profile = ISATSession(_session).profile
            if not profile:
                #user is not identified, we return a jsonrpc fault
                fault = jsonrpclib.Fault(C.ERRNUM_LIBERVIA, C.NOT_ALLOWED)  # FIXME: define some standard error codes for libervia
                return jsonrpc.JSONRPC._cbRender(self, fault, request, parsed.get('id'), parsed.get('jsonrpc'))  # pylint: disable=E1103
        self.request = request
        return jsonrpc.JSONRPC.render(self, request)

    def loginOrRegister(self, request):
        """This method is called with the POST information from the registering form.

        @param request: request of the register form
        @return: a constant indicating the state:
            - C.BAD_REQUEST: something is wrong in the request (bad arguments)
            - a return value from self._loginAccount or self._registerNewAccount
        """
        try:
            submit_type = request.args['submit_type'][0]
        except KeyError:
            return C.BAD_REQUEST

        if submit_type == 'register':
            return self._registerNewAccount(request)
        elif submit_type == 'login':
            return self._loginAccount(request)
        return Exception('Unknown submit type')

    def _loginAccount(self, request):
        """Try to authenticate the user with the request information.
        @param request: request of the register form
        @return: a constant indicating the state:
            - C.BAD_REQUEST: something is wrong in the request (bad arguments)
            - C.PROFILE_AUTH_ERROR: either the profile (login) or the profile password is wrong
            - C.XMPP_AUTH_ERROR: the profile is authenticated but the XMPP password is wrong
            - C.ALREADY_WAITING: a request has already been submitted for this profile
            - server.NOT_DONE_YET: the profile is being processed, the return
                value will be given by self._logged or auth_eb
        """
        try:
            login_ = request.args['login'][0]
            password_ = request.args['login_password'][0]
        except KeyError:
            return C.BAD_REQUEST

        if login_.startswith('@'):
            raise Exception('No profile_key allowed')

        profile_check = self.sat_host.bridge.getProfileName(login_)
        if ((not profile_check or profile_check != login_) or
            (not password_ and profile_check not in self.sat_host.empty_password_allowed_warning_dangerous_list)):
            return C.PROFILE_AUTH_ERROR
            # profiles with empty passwords are restricted to local frontends

        if login_ in self.profiles_waiting:
            return C.ALREADY_WAITING

        def auth_eb(failure):
            fault = failure.value.faultString
            self.__cleanWaiting(login_)
            if fault == 'PasswordError':
                log.info("Profile %s doesn't exist or the submitted password is wrong" % login_)
                request.write(C.PROFILE_AUTH_ERROR)
            elif fault == 'SASLAuthError':
                log.info("The XMPP password of profile %s is wrong" % login_)
                request.write(C.XMPP_AUTH_ERROR)
            elif fault == 'NoReply':
                log.info(_("Did not receive a reply (the timeout expired or the connection is broken)"))
                request.write(C.NO_REPLY)
            else:
                log.error('Unmanaged fault string %s in errback for the connection of profile %s' % (fault, login_))
                request.write(C.UNKNOWN_ERROR % fault)
            request.finish()

        self.profiles_waiting[login_] = request
        d = self.asyncBridgeCall("asyncConnect", login_, password_)
        d.addCallbacks(lambda connected: self._logged(login_, request) if connected else None, auth_eb)

        return server.NOT_DONE_YET

    def _registerNewAccount(self, request):
        """Create a new account, or return error
        @param request: request of the register form
        @return: a constant indicating the state:
            - C.BAD_REQUEST: something is wrong in the request (bad arguments)
            - C.REGISTRATION_SUCCEED: new account has been successfully registered
            - C.ALREADY_EXISTS: the given profile already exists
            - C.INTERNAL_ERROR or C.UNKNOWN_ERROR
            - server.NOT_DONE_YET: the profile is being processed, the return
                value will be given later (one of those previously described)
        """
        try:
            # XXX: for now libervia forces the creation to lower case
            profile = login = request.args['register_login'][0].lower()
            password = request.args['register_password'][0]
            email = request.args['email'][0]
        except KeyError:
            return C.BAD_REQUEST
        if not re.match(r'^[a-z0-9_-]+$', login, re.IGNORECASE) or \
           not re.match(r'^.+@.+\..+', email, re.IGNORECASE) or \
           len(password) < C.PASSWORD_MIN_LENGTH:
            return C.BAD_REQUEST

        def registered(result):
            request.write(C.REGISTRATION_SUCCEED)
            request.finish()

        def registeringError(failure):
            reason = failure.value.faultString
            if reason == "ConflictError":
                request.write(C.ALREADY_EXISTS)
            elif reason == "InternalError":
                request.write(C.INTERNAL_ERROR)
            else:
                log.error('Unknown registering error: %s' % (reason,))
                request.write(C.UNKNOWN_ERROR % reason)
            request.finish()

        d = self.asyncBridgeCall("registerSatAccount", email, password, profile)
        d.addCallback(registered)
        d.addErrback(registeringError)
        return server.NOT_DONE_YET

    def __cleanWaiting(self, login):
        """Remove login from waiting queue"""
        try:
            del self.profiles_waiting[login]
        except KeyError:
            pass

    def _logged(self, profile, request):
        """Set everything when a user just logged in

        @param profile
        @param request
        @return: a constant indicating the state:
            - C.PROFILE_LOGGED
            - C.SESSION_ACTIVE
        """
        self.__cleanWaiting(profile)
        _session = request.getSession()
        sat_session = ISATSession(_session)
        if sat_session.profile:
            log.error(('/!\\ Session has already a profile, this should NEVER happen!'))
            request.write(C.SESSION_ACTIVE)
            request.finish()
            return
        sat_session.profile = profile
        self.sat_host.prof_connected.add(profile)

        def onExpire():
            log.info("Session expired (profile=%s)" % (profile,))
            try:
                #We purge the queue
                del self.sat_host.signal_handler.queue[profile]
            except KeyError:
                pass
            #and now we disconnect the profile
            self.sat_host.bridge.disconnect(profile)

        _session.notifyOnExpire(onExpire)

        request.write(C.PROFILE_LOGGED)
        request.finish()

    def jsonrpc_isConnected(self):
        _session = self.request.getSession()
        profile = ISATSession(_session).profile
        return self.sat_host.bridge.isConnected(profile)

    def jsonrpc_asyncConnect(self):
        _session = self.request.getSession()
        profile = ISATSession(_session).profile
        if profile in self.profiles_waiting:
            raise jsonrpclib.Fault(1, C.ALREADY_WAITING)  # FIXME: define some standard error codes for libervia
        self.profiles_waiting[profile] = self.request
        self.sat_host.bridge.asyncConnect(profile)
        return server.NOT_DONE_YET

    def jsonrpc_isRegistered(self):
        """
        @return: a couple (registered, message) with:
        - registered: True if the user is already registered, False otherwise
        - message: a security warning message if registered is False *and* the connection is unsecure, None otherwise
        """
        _session = self.request.getSession()
        profile = ISATSession(_session).profile
        if bool(profile):
            return (True, None)
        return (False, self.__getSecurityWarning())

    def jsonrpc_registerParams(self):
        """Register the frontend specific parameters"""
        params = """
        <params>
        <individual>
        <category name="%(category_name)s" label="%(category_label)s">
            <param name="%(enable_unibox)s" label="%(enable_unibox_label)s" value="false" type="bool" security="0"/>
         </category>
        </individual>
        </params>
        """ % {
            'category_name': C.COMPOSITION_KEY,
            'category_label': _(C.COMPOSITION_KEY),
            'enable_unibox': C.ENABLE_UNIBOX_PARAM,
            'enable_unibox_label': _(C.ENABLE_UNIBOX_PARAM),
        }

        self.sat_host.bridge.paramsRegisterApp(params, C.SECURITY_LIMIT, C.APP_NAME)

    def jsonrpc_getMenus(self):
        """Return the parameters XML for profile"""
        # XXX: we put this method in Register because we get menus before being logged
        return self.sat_host.bridge.getMenus('', C.SECURITY_LIMIT)

    def __getSecurityWarning(self):
        """@return: a security warning message, or None if the connection is secure"""
        if self.request.URLPath().scheme == 'https' or not self.sat_host.security_warning:
            return None
        text = D_("You are about to connect to an unsecured service.")
        if self.sat_host.connection_type == 'both':
            new_port = (':%s' % self.sat_host.port_https_ext) if self.sat_host.port_https_ext != HTTPS_PORT else ''
            url = "https://%s" % self.request.URLPath().netloc.replace(':%s' % self.sat_host.port, new_port)
            text += D_('<br />Secure version of this website: <a href="%(url)s">%(url)s</a>') % {'url': url}
        return text


class SignalHandler(jsonrpc.JSONRPC):

    def __init__(self, sat_host):
        Resource.__init__(self)
        self.register = None
        self.sat_host = sat_host
        self.signalDeferred = {}
        self.queue = {}

    def plugRegister(self, register):
        self.register = register

    def jsonrpc_getSignals(self):
        """Keep the connection alive until a signal is received, then send it
        @return: (signal, *signal_args)"""
        _session = self.request.getSession()
        profile = ISATSession(_session).profile
        if profile in self.queue:  # if we have signals to send in queue
            if self.queue[profile]:
                return self.queue[profile].pop(0)
            else:
                #the queue is empty, we delete the profile from queue
                del self.queue[profile]
        _session.lock()  # we don't want the session to expire as long as this connection is active

        def unlock(signal, profile):
            _session.unlock()
            try:
                source_defer = self.signalDeferred[profile]
                if source_defer.called and source_defer.result[0] == "disconnected":
                    log.info(u"[%s] disconnected" % (profile,))
                    _session.expire()
            except IndexError:
                log.error("Deferred result should be a tuple with fonction name first")

        self.signalDeferred[profile] = defer.Deferred()
        self.request.notifyFinish().addBoth(unlock, profile)
        return self.signalDeferred[profile]

    def getGenericCb(self, function_name):
        """Return a generic function which send all params to signalDeferred.callback
        function must have profile as last argument"""
        def genericCb(*args):
            profile = args[-1]
            if not profile in self.sat_host.prof_connected:
                return
            if profile in self.signalDeferred:
                self.signalDeferred[profile].callback((function_name, args[:-1]))
                del self.signalDeferred[profile]
            else:
                if profile not in self.queue:
                    self.queue[profile] = []
                self.queue[profile].append((function_name, args[:-1]))
        return genericCb

    def connected(self, profile):
        assert(self.register)  # register must be plugged
        request = self.register.getWaitingRequest(profile)
        if request:
            self.register._logged(profile, request)

    def disconnected(self, profile):
        if not profile in self.sat_host.prof_connected:
            log.error("'disconnected' signal received for a not connected profile")
            return
        self.sat_host.prof_connected.remove(profile)
        if profile in self.signalDeferred:
            self.signalDeferred[profile].callback(("disconnected",))
            del self.signalDeferred[profile]
        else:
            if profile not in self.queue:
                self.queue[profile] = []
            self.queue[profile].append(("disconnected",))

    def render(self, request):
        """
        Render method wich reject access if user is not identified
        """
        _session = request.getSession()
        parsed = jsonrpclib.loads(request.content.read())
        profile = ISATSession(_session).profile
        if not profile:
            #user is not identified, we return a jsonrpc fault
            fault = jsonrpclib.Fault(C.ERRNUM_LIBERVIA, C.NOT_ALLOWED)  # FIXME: define some standard error codes for libervia
            return jsonrpc.JSONRPC._cbRender(self, fault, request, parsed.get('id'), parsed.get('jsonrpc'))  # pylint: disable=E1103
        self.request = request
        return jsonrpc.JSONRPC.render(self, request)


class UploadManager(Resource):
    """This class manage the upload of a file
    It redirect the stream to SàT core backend"""
    isLeaf = True
    NAME = 'path'  # name use by the FileUpload

    def __init__(self, sat_host):
        self.sat_host = sat_host
        self.upload_dir = tempfile.mkdtemp()
        self.sat_host.addCleanup(shutil.rmtree, self.upload_dir)

    def getTmpDir(self):
        return self.upload_dir

    def _getFileName(self, request):
        """Generate unique filename for a file"""
        raise NotImplementedError

    def _fileWritten(self, request, filepath):
        """Called once the file is actually written on disk
        @param request: HTTP request object
        @param filepath: full filepath on the server
        @return: a tuple with the name of the async bridge method
        to be called followed by its arguments.
        """
        raise NotImplementedError

    def render(self, request):
        """
        Render method with some hacks:
           - if login is requested, try to login with form data
           - except login, every method is jsonrpc
           - user doesn't need to be authentified for isRegistered, but must be for all other methods
        """
        filename = self._getFileName(request)
        filepath = os.path.join(self.upload_dir, filename)
        #FIXME: the uploaded file is fully loaded in memory at form parsing time so far
        #       (see twisted.web.http.Request.requestReceived). A custom requestReceived should
        #       be written in the futur. In addition, it is not yet possible to get progression informations
        #       (see http://twistedmatrix.com/trac/ticket/288)

        with open(filepath, 'w') as f:
            f.write(request.args[self.NAME][0])

        def finish(d):
            error = isinstance(d, Exception) or isinstance(d, Failure)
            request.write(C.UPLOAD_KO if error else C.UPLOAD_OK)
            # TODO: would be great to re-use the original Exception class and message
            # but it is lost in the middle of the backtrace and encapsulated within
            # a DBusException instance --> extract the data from the backtrace?
            request.finish()

        d = JSONRPCMethodManager(self.sat_host).asyncBridgeCall(*self._fileWritten(request, filepath))
        d.addCallbacks(lambda d: finish(d), lambda failure: finish(failure))
        return server.NOT_DONE_YET


class UploadManagerRadioCol(UploadManager):
    NAME = 'song'

    def _getFileName(self, request):
        extension = os.path.splitext(request.args['filename'][0])[1]
        return "%s%s" % (str(uuid.uuid4()), extension)  # XXX: chromium doesn't seem to play song without the .ogg extension, even with audio/ogg mime-type

    def _fileWritten(self, request, filepath):
        """Called once the file is actually written on disk
        @param request: HTTP request object
        @param filepath: full filepath on the server
        @return: a tuple with the name of the async bridge method
        to be called followed by its arguments.
        """
        profile = ISATSession(request.getSession()).profile
        return ("radiocolSongAdded", request.args['referee'][0], filepath, profile)


class UploadManagerAvatar(UploadManager):
    NAME = 'avatar_path'

    def _getFileName(self, request):
        return str(uuid.uuid4())

    def _fileWritten(self, request, filepath):
        """Called once the file is actually written on disk
        @param request: HTTP request object
        @param filepath: full filepath on the server
        @return: a tuple with the name of the async bridge method
        to be called followed by its arguments.
        """
        profile = ISATSession(request.getSession()).profile
        return ("setAvatar", filepath, profile)




class Libervia(service.Service):


    def __init__(self, *args, **kwargs):
        self.initialised = defer.Deferred()

        # options managing
        for opt in OPT_PARAMETERS_BOTH + OPT_PARAMETERS_CFG:
            opt_name = opt[0]
            setattr(self, opt_name, kwargs.get(opt_name, opt[2]))
        if not self.port_https_ext:
            self.port_https_ext = self.port_https
        if self.data_dir == DATA_DIR_DEFAULT:
            coerceDataDir(self.data_dir)  # this is not done when using the default value

        self.html_dir = os.path.join(self.data_dir, C.HTML_DIR)
        self.server_css_dir = os.path.join(self.data_dir, C.SERVER_CSS_DIR)

        self._cleanup = []

        root = ProtectedFile(self.html_dir)

        self.signal_handler = SignalHandler(self)
        _register = Register(self)
        _upload_radiocol = UploadManagerRadioCol(self)
        _upload_avatar = UploadManagerAvatar(self)
        self.signal_handler.plugRegister(_register)
        self.sessions = {}  # key = session value = user
        self.prof_connected = set()  # Profiles connected
        self.action_handler = SATActionIDHandler()

        ## bridge ##
        try:
            self.bridge = DBusBridgeFrontend()
        except BridgeExceptionNoService:
            print(u"Can't connect to SàT backend, are you sure it's launched ?")
            sys.exit(1)

        def backendReady(dummy):
            self.bridge.register("connected", self.signal_handler.connected)
            self.bridge.register("disconnected", self.signal_handler.disconnected)
            self.bridge.register("actionResult", self.action_handler.actionResultCb)
            #core
            for signal_name in ['presenceUpdate', 'newMessage', 'subscribe', 'contactDeleted', 'newContact', 'entityDataUpdated', 'askConfirmation', 'newAlert', 'paramUpdate']:
                self.bridge.register(signal_name, self.signal_handler.getGenericCb(signal_name))
            #plugins
            for signal_name in ['personalEvent', 'roomJoined', 'roomUserJoined', 'roomUserLeft', 'tarotGameStarted', 'tarotGameNew', 'tarotGameChooseContrat',
                                'tarotGameShowCards', 'tarotGameInvalidCards', 'tarotGameCardsPlayed', 'tarotGameYourTurn', 'tarotGameScore', 'tarotGamePlayers',
                                'radiocolStarted', 'radiocolPreload', 'radiocolPlay', 'radiocolNoUpload', 'radiocolUploadOk', 'radiocolSongRejected', 'radiocolPlayers',
                                'roomLeft', 'roomUserChangedNick', 'chatStateReceived']:
                self.bridge.register(signal_name, self.signal_handler.getGenericCb(signal_name), "plugin")
            self.media_dir = self.bridge.getConfig('', 'media_dir')
            self.local_dir = self.bridge.getConfig('', 'local_dir')
            root.putChild('', Redirect('libervia.html'))
            root.putChild('json_signal_api', self.signal_handler)
            root.putChild('json_api', MethodHandler(self))
            root.putChild('register_api', _register)
            root.putChild('upload_radiocol', _upload_radiocol)
            root.putChild('upload_avatar', _upload_avatar)
            root.putChild('blog', MicroBlog(self))
            root.putChild('css', ProtectedFile(self.server_css_dir))
            root.putChild(os.path.dirname(C.MEDIA_DIR), ProtectedFile(self.media_dir))
            root.putChild(os.path.dirname(C.AVATARS_DIR), ProtectedFile(os.path.join(self.local_dir, C.AVATARS_DIR)))
            root.putChild('radiocol', ProtectedFile(_upload_radiocol.getTmpDir(), defaultType="audio/ogg"))  # We cheat for PoC because we know we are on the same host, so we use directly upload dir
            self.site = server.Site(root)
            self.site.sessionFactory = LiberviaSession

        self.bridge.getReady(lambda: self.initialised.callback(None),
                             lambda failure: self.initialised.errback(Exception(failure)))
        self.initialised.addCallback(backendReady)
        self.initialised.addErrback(lambda failure: log.error("Init error: %s" % failure))

    def addCleanup(self, callback, *args, **kwargs):
        """Add cleaning method to call when service is stopped
        cleaning method will be called in reverse order of they insertion
        @param callback: callable to call on service stop
        @param *args: list of arguments of the callback
        @param **kwargs: list of keyword arguments of the callback"""
        self._cleanup.insert(0, (callback, args, kwargs))

    def startService(self):
        """Connect the profile for Libervia and start the HTTP(S) server(s)"""
        def eb(e):
            log.error(_("Connection failed: %s") % e)
            self.stop()

        def initOk(dummy):
            if not self.bridge.isConnected(C.SERVICE_PROFILE):
                self.bridge.asyncConnect(C.SERVICE_PROFILE, self.passphrase,
                                         callback=self._startService, errback=eb)
            else:
                self._startService()

        self.initialised.addCallback(initOk)

    def _startService(self, dummy=None):
        """Actually start the HTTP(S) server(s) after the profile for Libervia is connected.
        @raise IOError: the certificate file doesn't exist
        @raise OpenSSL.crypto.Error: the certificate file is invalid
        """
        if self.connection_type in ('https', 'both'):
            if not ssl_available:
                raise(ImportError(_("Python module pyOpenSSL is not installed!")))
            try:
                with open(os.path.expanduser(self.ssl_certificate)) as keyAndCert:
                    try:
                        cert = ssl.PrivateCertificate.loadPEM(keyAndCert.read())
                    except OpenSSL.crypto.Error as e:
                        log.error(_("The file '%s' must contain both private and public parts of the certificate") % self.ssl_certificate)
                        raise e
            except IOError as e:
                log.error(_("The file '%s' doesn't exist") % self.ssl_certificate)
                raise e
            reactor.listenSSL(self.port_https, self.site, cert.options())
        if self.connection_type in ('http', 'both'):
            if self.connection_type == 'both' and self.redirect_to_https:
                reactor.listenTCP(self.port, server.Site(RedirectToHTTPS(self.port, self.port_https_ext)))
            else:
                reactor.listenTCP(self.port, self.site)

    def stopService(self):
        log.info(_("launching cleaning methods"))
        for callback, args, kwargs in self._cleanup:
            callback(*args, **kwargs)
        self.bridge.disconnect(C.SERVICE_PROFILE)

    def run(self):
        reactor.run()

    def stop(self):
        reactor.stop()


class RedirectToHTTPS(Resource):

    def __init__(self, old_port, new_port):
        Resource.__init__(self)
        self.isLeaf = True
        self.old_port = old_port
        self.new_port = new_port

    def render(self, request):
        netloc = request.URLPath().netloc.replace(':%s' % self.old_port, ':%s' % self.new_port)
        url = "https://" + netloc + request.uri
        return redirectTo(url, request)


registerAdapter(SATSession, server.Session, ISATSession)
