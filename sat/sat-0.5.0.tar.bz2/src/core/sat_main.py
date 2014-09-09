#!/usr/bin/python
# -*- coding: utf-8 -*-

# SAT: a jabber client
# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014 Jérôme Poisson (goffi@goffi.org)

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

from sat.core.i18n import _, D_, languageSwitch
from twisted.application import service
from twisted.internet import defer
from twisted.words.protocols.jabber import jid
from twisted.words.xish import domish
from twisted.internet import reactor
from wokkel.xmppim import RosterItem
from sat.bridge.DBus import DBusBridge
from sat.core import xmpp
from sat.core import exceptions
from sat.core.log import getLogger
log = getLogger(__name__)
from sat.core.constants import Const as C
from sat.memory.memory import Memory
from sat.memory.crypto import PasswordHasher
from sat.tools.misc import TriggerManager
from sat.stdui import ui_contact_list, ui_profile_manager
from glob import glob
from uuid import uuid4
import sys
import os.path

try:
    from collections import OrderedDict # only available from python 2.7
except ImportError:
    from ordereddict import OrderedDict


sat_id = 0


def sat_next_id():
    global sat_id
    sat_id += 1
    return "sat_id_" + str(sat_id)


class SAT(service.Service):

    @property
    def __version__(self):
        return C.APP_VERSION

    def get_next_id(self):
        return sat_next_id()

    def __init__(self):
        self._cb_map = {}  # map from callback_id to callbacks
        self._menus = OrderedDict()  # dynamic menus. key: callback_id, value: menu data (dictionnary)
        self.__private_data = {}  # used for internal callbacks (key = id) FIXME: to be removed
        self._initialised = defer.Deferred()
        self.profiles = {}
        self.plugins = {}

        self.memory = Memory(self)
        self.trigger = TriggerManager()  # trigger are used to change SàT behaviour

        try:
            self.bridge = DBusBridge()
        except exceptions.BridgeInitError:
            log.error(u"Bridge can't be initialised, can't start SàT core")
            sys.exit(1)
        self.bridge.register("getReady", lambda: self._initialised)
        self.bridge.register("getVersion", lambda: C.APP_VERSION)
        self.bridge.register("getProfileName", self.memory.getProfileName)
        self.bridge.register("getProfilesList", self.memory.getProfilesList)
        self.bridge.register("getEntityData", lambda _jid, keys, profile: self.memory.getEntityData(jid.JID(_jid), keys, profile))
        self.bridge.register("asyncCreateProfile", self.memory.asyncCreateProfile)
        self.bridge.register("asyncDeleteProfile", self.memory.asyncDeleteProfile)
        self.bridge.register("asyncConnect", self.asyncConnect)
        self.bridge.register("disconnect", self.disconnect)
        self.bridge.register("getContacts", self.getContacts)
        self.bridge.register("getContactsFromGroup", self.getContactsFromGroup)
        self.bridge.register("getLastResource", self.memory._getLastResource)
        self.bridge.register("getPresenceStatuses", self.memory._getPresenceStatuses)
        self.bridge.register("getWaitingSub", self.memory.getWaitingSub)
        self.bridge.register("getWaitingConf", self.getWaitingConf)
        self.bridge.register("sendMessage", self._sendMessage)
        self.bridge.register("getConfig", self.memory.getConfig)
        self.bridge.register("setParam", self.setParam)
        self.bridge.register("getParamA", self.memory.getStringParamA)
        self.bridge.register("asyncGetParamA", self.memory.asyncGetStringParamA)
        self.bridge.register("getParamsUI", self.memory.getParamsUI)
        self.bridge.register("getParams", self.memory.getParams)
        self.bridge.register("getParamsForCategory", self.memory.getParamsForCategory)
        self.bridge.register("getParamsCategories", self.memory.getParamsCategories)
        self.bridge.register("paramsRegisterApp", self.memory.paramsRegisterApp)
        self.bridge.register("getHistory", self.memory.getHistory)
        self.bridge.register("setPresence", self._setPresence)
        self.bridge.register("subscription", self.subscription)
        self.bridge.register("addContact", self._addContact)
        self.bridge.register("updateContact", self._updateContact)
        self.bridge.register("delContact", self._delContact)
        self.bridge.register("isConnected", self.isConnected)
        self.bridge.register("launchAction", self.launchCallback)
        self.bridge.register("confirmationAnswer", self.confirmationAnswer)
        self.bridge.register("getProgress", self.getProgress)
        self.bridge.register("getMenus", self.getMenus)
        self.bridge.register("getMenuHelp", self.getMenuHelp)
        self.bridge.register("discoInfos", self.memory.disco._discoInfos)
        self.bridge.register("discoItems", self.memory.disco._discoItems)
        self.bridge.register("saveParamsTemplate", self.memory.save_xml)
        self.bridge.register("loadParamsTemplate", self.memory.load_xml)

        self.memory.initialized.addCallback(self._postMemoryInit)

    def _postMemoryInit(self, ignore):
        """Method called after memory initialization is done"""
        log.info(_("Memory initialised"))
        self._import_plugins()
        ui_contact_list.ContactList(self)
        ui_profile_manager.ProfileManager(self)
        self._initialised.callback(None)
        log.info(_("Backend is ready"))

    def _import_plugins(self):
        """Import all plugins found in plugins directory"""
        import sat.plugins
        plugins_path = os.path.dirname(sat.plugins.__file__)
        plug_lst = [os.path.splitext(plugin)[0] for plugin in map(os.path.basename, glob(os.path.join(plugins_path, "plugin*.py")))]
        __plugins_to_import = {}  # plugins we still have to import
        for plug in plug_lst:
            plugin_path = 'sat.plugins.' + plug
            try:
                __import__(plugin_path)
            except ImportError as e:
                log.error(_("Can't import plugin [%(path)s]: %(error)s") % {'path': plugin_path, 'error':e})
                continue
            mod = sys.modules[plugin_path]
            plugin_info = mod.PLUGIN_INFO
            __plugins_to_import[plugin_info['import_name']] = (plugin_path, mod, plugin_info)
        while True:
            self._import_plugins_from_dict(__plugins_to_import)
            if not __plugins_to_import:
                break

    def _import_plugins_from_dict(self, plugins_to_import, import_name=None, optional=False):
        """Recursively import and their dependencies in the right order
        @param plugins_to_import: dict where key=import_name and values= (plugin_path, module, plugin_info)
        @param import_name: name of the plugin to import as found in PLUGIN_INFO['import_name']
        @param optional: if False and plugin is not found, an ImportError exception is raised

        """
        if import_name in self.plugins:
            log.debug('Plugin [%s] already imported, passing' % import_name)
            return
        if not import_name:
            import_name, (plugin_path, mod, plugin_info) = plugins_to_import.popitem()
        else:
            if not import_name in plugins_to_import:
                if optional:
                    log.warning(_("Recommended plugin not found: %s") % import_name)
                    return
                log.error(_("Dependency not found: %s") % import_name)
                raise ImportError(_('Dependency plugin not found: [%s]') % import_name)
            plugin_path, mod, plugin_info = plugins_to_import.pop(import_name)
        dependencies = plugin_info.setdefault("dependencies", [])
        recommendations = plugin_info.setdefault("recommendations", [])
        for to_import in dependencies + recommendations:
            if to_import not in self.plugins:
                log.debug('Recursively import dependency of [%s]: [%s]' % (import_name, to_import))
                try:
                    self._import_plugins_from_dict(plugins_to_import, to_import, to_import not in dependencies)
                except ImportError as e:
                    log.error(_("Can't import plugin %(name)s: %(error)s") % {'name':plugin_info['name'], 'error':e})
                    return
        log.info(_("importing plugin: %s") % plugin_info['name'])
        self.plugins[import_name] = getattr(mod, plugin_info['main'])(self)
        if 'handler' in plugin_info and plugin_info['handler'] == 'yes':
            self.plugins[import_name].is_handler = True
        else:
            self.plugins[import_name].is_handler = False
        #TODO: test xmppclient presence and register handler parent

    def asyncConnect(self, profile_key=C.PROF_KEY_NONE, password=''):
        """Retrieve the individual parameters, authenticate the profile
        and initiate the connection to the associated XMPP server.

        @param password (string): the SàT profile password
        @param profile_key: %(doc_profile_key)s
        @return: Deferred:
            - a deferred boolean if the profile authentication succeed:
                - True if the XMPP connection was already established
                - False if the XMPP connection has been initiated (it may still fail)
            - a Failure if the profile authentication failed
        """
        def backendInitialised(dummy):
            profile = self.memory.getProfileName(profile_key)
            if not profile:
                log.error(_('Trying to connect a non-existant profile'))
                raise exceptions.ProfileUnknownError(profile_key)

            def connectXMPPClient(dummy=None):
                if self.isConnected(profile):
                    log.info(_("already connected !"))
                    return True
                self.memory.startProfileSession(profile)
                d = self.memory.loadIndividualParams(profile)
                d.addCallback(lambda dummy: self._connectXMPPClient(profile))
                return d.addCallback(lambda dummy: False)

            d = self._authenticateProfile(password, profile)
            d.addCallback(connectXMPPClient)
            return d

        self._initialised.addErrback(lambda dummy: None)  # allow successive attempts
        return self._initialised.addCallback(backendInitialised)

    @defer.inlineCallbacks
    def _connectXMPPClient(self, profile):
        """This part is called from asyncConnect when we have loaded individual parameters from memory"""
        try:
            port = int(self.memory.getParamA(C.FORCE_PORT_PARAM, "Connection", profile_key=profile))
        except ValueError:
            log.debug(_("Can't parse port value, using default value"))
            port = None  # will use default value 5222 or be retrieved from a DNS SRV record

        password = yield self.memory.asyncGetParamA("Password", "Connection", profile_key=profile)
        current = self.profiles[profile] = xmpp.SatXMPPClient(self, profile,
            jid.JID(self.memory.getParamA("JabberID", "Connection", profile_key=profile)),
            password, self.memory.getParamA(C.FORCE_SERVER_PARAM, "Connection", profile_key=profile), port)

        current.messageProt = xmpp.SatMessageProtocol(self)
        current.messageProt.setHandlerParent(current)

        current.roster = xmpp.SatRosterProtocol(self)
        current.roster.setHandlerParent(current)

        current.presence = xmpp.SatPresenceProtocol(self)
        current.presence.setHandlerParent(current)

        current.fallBack = xmpp.SatFallbackHandler(self)
        current.fallBack.setHandlerParent(current)

        current.versionHandler = xmpp.SatVersionHandler(C.APP_NAME_FULL,
                                                        C.APP_VERSION)
        current.versionHandler.setHandlerParent(current)

        current.identityHandler = xmpp.SatIdentityHandler()
        current.identityHandler.setHandlerParent(current)

        log.debug(_("setting plugins parents"))

        plugin_conn_cb = []
        for plugin in self.plugins.iteritems():
            if plugin[1].is_handler:
                plugin[1].getHandler(profile).setHandlerParent(current)
            connected_cb = getattr(plugin[1], "profileConnected", None)
            if connected_cb:
                plugin_conn_cb.append((plugin[0], connected_cb))

        current.startService()

        yield current.getConnectionDeferred()
        yield current.roster.got_roster  # we want to be sure that we got the roster

        # Call profileConnected callback for all plugins, and print error message if any of them fails
        conn_cb_list = []
        for dummy, callback in plugin_conn_cb:
            conn_cb_list.append(defer.maybeDeferred(callback, profile))
        list_d = defer.DeferredList(conn_cb_list)

        def logPluginResults(results):
            all_succeed = all([success for success, result in results])
            if not all_succeed:
                log.error(_("Plugins initialisation error"))
                for idx, (success, result) in enumerate(results):
                    if not success:
                        log.error("error (plugin %(name)s): %(failure)s" %
                                  {'name': plugin_conn_cb[idx][0], 'failure': result})

        yield list_d.addCallback(logPluginResults) # FIXME: we should have a timeout here, and a way to know if a plugin freeze
        # TODO: mesure time to launch of each plugin

    def _authenticateProfile(self, password, profile):
        """Authenticate the profile.

        @param password (string): the SàT profile password
        @param profile: %(doc_profile)s
        @return: Deferred: a deferred None in case of success, a failure otherwise.
        """
        session_data = self.memory.auth_sessions.profileGetUnique(profile)
        if not password and session_data:
            # XXX: this allows any frontend to connect with the empty password as soon as
            # the profile has been authenticated at least once before. It is OK as long as
            # submitting a form with empty passwords is restricted to local frontends.
            return defer.succeed(None)

        def check_result(result):
            if not result:
                log.warning(_('Authentication failure of profile %s') % profile)
                raise exceptions.PasswordError(D_("The provided profile password doesn't match."))
            if not session_data:  # avoid to create two profile sessions when password if specified
                return self.memory.newAuthSession(password, profile)

        d = self.memory.asyncGetParamA(C.PROFILE_PASS_PATH[1], C.PROFILE_PASS_PATH[0], profile_key=profile)
        d.addCallback(lambda sat_cipher: PasswordHasher.verify(password, sat_cipher))
        return d.addCallback(check_result)

    def disconnect(self, profile_key):
        """disconnect from jabber server"""
        if not self.isConnected(profile_key):
            log.info(_("not connected !"))
            return
        profile = self.memory.getProfileName(profile_key)
        log.info(_("Disconnecting..."))
        self.profiles[profile].stopService()
        for plugin in self.plugins.iteritems():
            disconnected_cb = getattr(plugin[1], "profileDisconnected", None)
            if disconnected_cb:
                disconnected_cb(profile)

    def getContacts(self, profile_key):
        client = self.getClient(profile_key)
        ret = []
        for item in client.roster.getItems():  # we get all items for client's roster
            # and convert them to expected format
            attr = client.roster.getAttributes(item)
            ret.append([item.jid.userhost(), attr, item.groups])
        return ret

    def getContactsFromGroup(self, group, profile_key):
        client = self.getClient(profile_key)
        return [jid_.full() for jid_ in client.roster.getJidsFromGroup(group)]

    def purgeClient(self, profile):
        """Remove reference to a profile client and purge cache
        the garbage collector can then free the memory"""
        try:
            del self.profiles[profile]
        except KeyError:
            log.error(_("Trying to remove reference to a client not referenced"))
        self.memory.purgeProfileSession(profile)

    def startService(self):
        log.info(u"Salut à toi ô mon frère !")

    def stopService(self):
        log.info(u"Salut aussi à Rantanplan")

    def run(self):
        log.debug(_("running app"))
        reactor.run()

    def stop(self):
        log.debug(_("stopping app"))
        reactor.stop()

    ## Misc methods ##

    def getJidNStream(self, profile_key):
        """Convenient method to get jid and stream from profile key
        @return: tuple (jid, xmlstream) from profile, can be None"""
        profile = self.memory.getProfileName(profile_key)
        if not profile or not self.profiles[profile].isConnected():
            return (None, None)
        return (self.profiles[profile].jid, self.profiles[profile].xmlstream)

    def getClient(self, profile_key):
        """Convenient method to get client from profile key
        @return: client or None if it doesn't exist"""
        profile = self.memory.getProfileName(profile_key)
        if not profile:
            raise exceptions.ProfileKeyUnknownError
        return self.profiles[profile]

    def getClients(self, profile_key):
        """Convenient method to get list of clients from profile key (manage list through profile_key like @ALL@)
        @param profile_key: %(doc_profile_key)s
        @return: list of clients"""
        profile = self.memory.getProfileName(profile_key, True)
        if not profile:
            return []
        if profile == "@ALL@":
            return self.profiles.values()
        if profile.count('@') > 1:
            raise exceptions.ProfileKeyUnknownError
        return [self.profiles[profile]]

    ## Client management ##

    def setParam(self, name, value, category, security_limit, profile_key):
        """set wanted paramater and notice observers"""
        self.memory.setParam(name, value, category, security_limit, profile_key)

    def isConnected(self, profile_key):
        """Return connection status of profile
        @param profile_key: key_word or profile name to determine profile name
        @return: True if connected
        """
        profile = self.memory.getProfileName(profile_key)
        if not profile:
            log.error(_('asking connection status for a non-existant profile'))
            raise exceptions.ProfileUnknownError(profile_key)
        if profile not in self.profiles:
            return False
        return self.profiles[profile].isConnected()


    ## XMPP methods ##

    def getWaitingConf(self, profile_key=None):
        assert(profile_key)
        client = self.getClient(profile_key)
        ret = []
        for conf_id in client._waiting_conf:
            conf_type, data = client._waiting_conf[conf_id][:2]
            ret.append((conf_id, conf_type, data))
        return ret

    def generateMessageXML(self, mess_data):
        mess_data['xml'] = domish.Element((None, 'message'))
        mess_data['xml']["to"] = mess_data["to"].full()
        mess_data['xml']["from"] = mess_data['from'].full()
        mess_data['xml']["type"] = mess_data["type"]
        mess_data['xml']['id'] = str(uuid4())
        if mess_data["subject"]:
            mess_data['xml'].addElement("subject", None, mess_data['subject'])
        if mess_data["message"]: # message without body are used to send chat states
            mess_data['xml'].addElement("body", None, mess_data["message"])
        return mess_data

    def _sendMessage(self, to_s, msg, subject=None, mess_type='auto', extra={}, profile_key=C.PROF_KEY_NONE):
        to_jid = jid.JID(to_s)
        #XXX: we need to use the dictionary comprehension because D-Bus return its own types, and pickle can't manage them. TODO: Need to find a better way
        return self.sendMessage(to_jid, msg, subject, mess_type, {unicode(key): unicode(value) for key, value in extra.items()}, profile_key=profile_key)

    def sendMessage(self, to_jid, msg, subject=None, mess_type='auto', extra={}, no_trigger=False, profile_key=C.PROF_KEY_NONE):
        #FIXME: check validity of recipient
        profile = self.memory.getProfileName(profile_key)
        assert(profile)
        client = self.profiles[profile]
        if extra is None:
            extra = {}
        mess_data = {  # we put data in a dict, so trigger methods can change them
            "to": to_jid,
            "from": client.jid,
            "message": msg,
            "subject": subject,
            "type": mess_type,
            "extra": extra,
        }
        pre_xml_treatments = defer.Deferred() # XXX: plugin can add their pre XML treatments to this deferred
        post_xml_treatments = defer.Deferred() # XXX: plugin can add their post XML treatments to this deferred

        if mess_data["type"] == "auto":
            # we try to guess the type
            if mess_data["subject"]:
                mess_data["type"] = 'normal'
            elif not mess_data["to"].resource:  # if to JID has a resource, the type is not 'groupchat'
                # we may have a groupchat message, we check if the we know this jid
                try:
                    entity_type = self.memory.getEntityData(mess_data["to"], ['type'], profile)["type"]
                    #FIXME: should entity_type manage ressources ?
                except (exceptions.UnknownEntityError, KeyError):
                    entity_type = "contact"

                if entity_type == "chatroom":
                    mess_data["type"] = 'groupchat'
                else:
                    mess_data["type"] = 'chat'
            else:
                mess_data["type"] == 'chat'
            mess_data["type"] == "chat" if mess_data["subject"] else "normal"

        send_only = mess_data['extra'].get('send_only', None)

        if not no_trigger and not send_only:
            if not self.trigger.point("sendMessage", mess_data, pre_xml_treatments, post_xml_treatments, profile):
                return defer.succeed(None)

        log.debug(_("Sending jabber message of type [%(type)s] to %(to)s...") % {"type": mess_data["type"], "to": to_jid.full()})

        def cancelErrorTrap(failure):
            """A message sending can be cancelled by a plugin treatment"""
            failure.trap(exceptions.CancelError)

        pre_xml_treatments.addCallback(lambda dummy: self.generateMessageXML(mess_data))
        pre_xml_treatments.chainDeferred(post_xml_treatments)
        post_xml_treatments.addCallback(self._sendMessageToStream, client)
        if send_only:
            log.debug(_("Triggers, storage and echo have been inhibited by the 'send_only' parameter"))
        else:
            post_xml_treatments.addCallback(self._storeMessage, client)
            post_xml_treatments.addCallback(self.sendMessageToBridge, client)
            post_xml_treatments.addErrback(cancelErrorTrap)
        pre_xml_treatments.callback(mess_data)
        return pre_xml_treatments

    def _sendMessageToStream(self, mess_data, client):
        """Actualy send the message to the server

        @param mess_data: message data dictionnary
        @param client: profile's client
        """
        client.xmlstream.send(mess_data['xml'])
        return mess_data

    def _storeMessage(self, mess_data, client):
        """Store message into database (for local history)

        @param mess_data: message data dictionnary
        @param client: profile's client
        """
        if mess_data["type"] != "groupchat":
            # we don't add groupchat message to history, as we get them back
            # and they will be added then
            if mess_data['message']: # we need a message to save something
                self.memory.addToHistory(client.jid, mess_data['to'],
                                     unicode(mess_data["message"]),
                                     unicode(mess_data["type"]),
                                     mess_data['extra'],
                                     profile=client.profile)
            else:
               log.warning(_("No message found")) # empty body should be managed by plugins before this point
        return mess_data

    def sendMessageToBridge(self, mess_data, client):
        """Send message to bridge, so frontends can display it

        @param mess_data: message data dictionnary
        @param client: profile's client
        """
        if mess_data["type"] != "groupchat":
            # we don't send groupchat message back to bridge, as we get them back
            # and they will be added the
            if mess_data['message']: # we need a message to save something
                # We send back the message, so all clients are aware of it
                self.bridge.newMessage(mess_data['from'].full(),
                                       unicode(mess_data["message"]),
                                       mess_type=mess_data["type"],
                                       to_jid=mess_data['to'].full(),
                                       extra=mess_data['extra'],
                                       profile=client.profile)
            else:
               log.warning(_("No message found"))
        return mess_data

    def _setPresence(self, to="", show="", statuses=None, profile_key=C.PROF_KEY_NONE):
        return self.setPresence(jid.JID(to) if to else None, show, statuses, profile_key)

    def setPresence(self, to_jid=None, show="", statuses=None, profile_key=C.PROF_KEY_NONE):
        """Send our presence information"""
        if statuses is None:
            statuses = {}
        profile = self.memory.getProfileName(profile_key)
        assert(profile)
        priority = int(self.memory.getParamA("Priority", "Connection", profile_key=profile))
        self.profiles[profile].presence.available(to_jid, show, statuses, priority)
        #XXX: FIXME: temporary fix to work around openfire 3.7.0 bug (presence is not broadcasted to generating resource)
        if '' in statuses:
            statuses['default'] = statuses['']
            del statuses['']
        self.bridge.presenceUpdate(self.profiles[profile].jid.full(), show,
                                   int(priority), statuses, profile)

    def subscription(self, subs_type, raw_jid, profile_key):
        """Called to manage subscription
        @param subs_type: subsciption type (cf RFC 3921)
        @param raw_jid: unicode entity's jid
        @param profile_key: profile"""
        profile = self.memory.getProfileName(profile_key)
        assert(profile)
        to_jid = jid.JID(raw_jid)
        log.debug(_('subsciption request [%(subs_type)s] for %(jid)s') % {'subs_type': subs_type, 'jid': to_jid.full()})
        if subs_type == "subscribe":
            self.profiles[profile].presence.subscribe(to_jid)
        elif subs_type == "subscribed":
            self.profiles[profile].presence.subscribed(to_jid)
        elif subs_type == "unsubscribe":
            self.profiles[profile].presence.unsubscribe(to_jid)
        elif subs_type == "unsubscribed":
            self.profiles[profile].presence.unsubscribed(to_jid)

    def _addContact(self, to_jid_s, profile_key):
        return self.addContact(jid.JID(to_jid_s), profile_key)

    def addContact(self, to_jid, profile_key):
        """Add a contact in roster list"""
        profile = self.memory.getProfileName(profile_key)
        assert(profile)
        #self.profiles[profile].roster.addItem(to_jid)  #XXX: disabled (cf http://wokkel.ik.nu/ticket/56))
        self.profiles[profile].presence.subscribe(to_jid)

    def _updateContact(self, to_jid_s, name, groups, profile_key):
        return self.updateContact(jid.JID(to_jid_s), name, groups, profile_key)

    def updateContact(self, to_jid, name, groups, profile_key):
        """update a contact in roster list"""
        profile = self.memory.getProfileName(profile_key)
        assert(profile)
        groups = set(groups)
        roster_item = RosterItem(to_jid)
        roster_item.name = name or None
        roster_item.groups = set(groups)
        self.profiles[profile].roster.updateItem(roster_item)

    def _delContact(self, to_jid_s, profile_key):
        return self.delContact(jid.JID(to_jid_s), profile_key)

    def delContact(self, to_jid, profile_key):
        """Remove contact from roster list"""
        profile = self.memory.getProfileName(profile_key)
        assert(profile)
        self.profiles[profile].roster.removeItem(to_jid)
        self.profiles[profile].presence.unsubscribe(to_jid)


    ## Discovery ##
    # discovery methods are shortcuts to self.memory.disco
    # the main difference with client.disco is that self.memory.disco manage cache

    def hasFeature(self, *args, **kwargs):
        return self.memory.disco.hasFeature(*args, **kwargs)

    def checkFeature(self, *args, **kwargs):
        return self.memory.disco.checkFeature(*args, **kwargs)

    def getDiscoInfos(self, *args, **kwargs):
        return self.memory.disco.getInfos(*args, **kwargs)

    def getDiscoItems(self, *args, **kwargs):
        return self.memory.disco.getItems(*args, **kwargs)

    def findServiceEntities(self, *args, **kwargs):
        return self.memory.disco.findServiceEntities(*args, **kwargs)

    def findFeaturesSet(self, *args, **kwargs):
        return self.memory.disco.findFeaturesSet(*args, **kwargs)


    ## Generic HMI ##

    def actionResult(self, action_id, action_type, data, profile):
        """Send the result of an action
        @param action_id: same action_id used with action
        @param action_type: result action_type ("PARAM", "SUCCESS", "ERROR", "XMLUI")
        @param data: dictionary
        """
        self.bridge.actionResult(action_type, action_id, data, profile)

    def actionResultExt(self, action_id, action_type, data, profile):
        """Send the result of an action, extended version
        @param action_id: same action_id used with action
        @param action_type: result action_type /!\ only "DICT_DICT" for this method
        @param data: dictionary of dictionaries
        """
        if action_type != "DICT_DICT":
            log.error(_("action_type for actionResultExt must be DICT_DICT, fixing it"))
            action_type = "DICT_DICT"
        self.bridge.actionResultExt(action_type, action_id, data, profile)

    def askConfirmation(self, conf_id, conf_type, data, cb, profile):
        """Add a confirmation callback
        @param conf_id: conf_id used to get answer
        @param conf_type: confirmation conf_type ("YES/NO", "FILE_TRANSFER")
        @param data: data (depend of confirmation conf_type)
        @param cb: callback called with the answer
        """
        # FIXME: use XMLUI and *callback methods for dialog
        client = self.getClient(profile)
        if conf_id in client._waiting_conf:
            log.error(_("Attempt to register two callbacks for the same confirmation"))
        else:
            client._waiting_conf[conf_id] = (conf_type, data, cb)
            self.bridge.askConfirmation(conf_id, conf_type, data, profile)

    def confirmationAnswer(self, conf_id, accepted, data, profile):
        """Called by frontends to answer confirmation requests"""
        client = self.getClient(profile)
        log.debug(_("Received confirmation answer for conf_id [%(conf_id)s]: %(success)s") % {'conf_id': conf_id, 'success': _("accepted") if accepted else _("refused")})
        if conf_id not in client._waiting_conf:
            log.error(_("Received an unknown confirmation (%(id)s for %(profile)s)") % {'id': conf_id, 'profile': profile})
        else:
            cb = client._waiting_conf[conf_id][-1]
            del client._waiting_conf[conf_id]
            cb(conf_id, accepted, data, profile)

    def registerProgressCB(self, progress_id, CB, profile):
        """Register a callback called when progress is requested for id"""
        client = self.getClient(profile)
        client._progress_cb_map[progress_id] = CB

    def removeProgressCB(self, progress_id, profile):
        """Remove a progress callback"""
        client = self.getClient(profile)
        if progress_id not in client._progress_cb_map:
            log.error(_("Trying to remove an unknow progress callback"))
        else:
            del client._progress_cb_map[progress_id]

    def getProgress(self, progress_id, profile):
        """Return a dict with progress information
        data['position'] : current possition
        data['size'] : end_position
        """
        client = self.getClient(profile)
        data = {}
        try:
            client._progress_cb_map[progress_id](progress_id, data, profile)
        except KeyError:
            pass
            #log.debug("Requested progress for unknown progress_id")
        return data

    def registerCallback(self, callback, *args, **kwargs):
        """ Register a callback.
        Use with_data=True in kwargs if the callback use the optional data dict
        use force_id=id to avoid generated id. Can lead to name conflict, avoid if possible
        use one_shot=True to delete callback once it have been called
        @param callback: any callable
        @return: id of the registered callback
        """
        callback_id = kwargs.pop('force_id', None)
        if callback_id is None:
            callback_id = str(uuid4())
        else:
            if callback_id in self._cb_map:
                raise exceptions.ConflictError(_(u"id already registered"))
        self._cb_map[callback_id] = (callback, args, kwargs)

        if "one_shot" in kwargs: # One Shot callback are removed after 30 min
            def purgeCallback():
                try:
                    self.removeCallback(callback_id)
                except KeyError:
                    pass
            reactor.callLater(1800, purgeCallback)

        return callback_id

    def removeCallback(self, callback_id):
        """ Remove a previously registered callback
        @param callback_id: id returned by [registerCallback] """
        log.debug("Removing callback [%s]" % callback_id)
        del self._cb_map[callback_id]

    def launchCallback(self, callback_id, data=None, profile_key=C.PROF_KEY_NONE):
        """Launch a specific callback
        @param callback_id: id of the action (callback) to launch
        @param data: optional data
        @profile_key: %(doc_profile_key)s
        @return: a deferred which fire a dict where key can be:
            - xmlui: a XMLUI need to be displayed
        """
        profile = self.memory.getProfileName(profile_key)
        if not profile:
            raise exceptions.ProfileUnknownError(_('trying to launch action with a non-existant profile'))

        try:
            callback, args, kwargs = self._cb_map[callback_id]
        except KeyError:
            raise exceptions.DataError("Unknown callback id")

        if kwargs.get("with_data", False):
            if data is None:
                raise exceptions.DataError("Required data for this callback is missing")
            args,kwargs=list(args)[:],kwargs.copy() # we don't want to modify the original (kw)args
            args.insert(0, data)
            kwargs["profile"] = profile
            del kwargs["with_data"]

        if kwargs.pop('one_shot', False):
            self.removeCallback(callback_id)

        return defer.maybeDeferred(callback, *args, **kwargs)

    #Menus management

    def importMenu(self, path, callback, security_limit=C.NO_SECURITY_LIMIT, help_string="", type_=C.MENU_GLOBAL):
        """register a new menu for frontends
        @param path: path to go to the menu (category/subcategory/.../item), must be an iterable (e.g.: ("File", "Open"))
            /!\ use D_() instead of _() for translations (e.g. (D_("File"), D_("Open")))
        @param callback: method to be called when menuitem is selected, callable or a callback id (string) as returned by [registerCallback]
        @param security_limit: %(doc_security_limit)s
            /!\ security_limit MUST be added to data in launchCallback if used #TODO
        @param help_string: string used to indicate what the menu do (can be show as a tooltip).
            /!\ use D_() instead of _() for translations
        @param type: one of:
            - C.MENU_GLOBAL: classical menu, can be shown in a menubar on top (e.g. something like File/Open)
            - C.MENU_ROOM: like a global menu, but only shown in multi-user chat
                menu_data must contain a "room_jid" data
            - C.MENU_SINGLE: like a global menu, but only shown in one2one chat
                menu_data must contain a "jid" data
            - C.MENU_JID_CONTEXT: contextual menu, used with any jid (e.g.: ad hoc commands, jid is already filled)
                menu_data must contain a "jid" data
            - C.MENU_ROSTER_JID_CONTEXT: like JID_CONTEXT, but restricted to jids in roster.
                menu_data must contain a "room_jid" data
            - C.MENU_ROSTER_GROUP_CONTEXT: contextual menu, used with group (e.g.: publish microblog, group is already filled)
                menu_data must contain a "group" data
        @return: menu_id (same as callback_id)
        """

        if callable(callback):
            callback_id = self.registerCallback(callback, with_data=True)
        elif isinstance(callback, basestring):
            # The callback is already registered
            callback_id = callback
            try:
                callback, args, kwargs = self._cb_map[callback_id]
            except KeyError:
                raise exceptions.DataError("Unknown callback id")
            kwargs["with_data"] = True # we have to be sure that we use extra data
        else:
            raise exceptions.DataError("Unknown callback type")

        for menu_data in self._menus.itervalues():
            if menu_data['path'] == path and menu_data['type'] == type_:
                raise exceptions.ConflictError(_("A menu with the same path and type already exists"))

        menu_data = {'path': path,
                     'security_limit': security_limit,
                     'help_string': help_string,
                     'type': type_
                    }

        self._menus[callback_id] = menu_data

        return callback_id

    def getMenus(self, language='', security_limit=C.NO_SECURITY_LIMIT):
        """Return all menus registered
        @param language: language used for translation, or empty string for default
        @param security_limit: %(doc_security_limit)s
        @return: array of tuple with:
            - menu id (same as callback_id)
            - menu type
            - raw menu path (array of strings)
            - translated menu path

        """
        ret = []
        for menu_id, menu_data in self._menus.iteritems():
            type_ = menu_data['type']
            path = menu_data['path']
            menu_security_limit = menu_data['security_limit']
            if security_limit!=C.NO_SECURITY_LIMIT and (menu_security_limit==C.NO_SECURITY_LIMIT or menu_security_limit>security_limit):
                continue
            languageSwitch(language)
            path_i18n = [_(elt) for elt in path]
            languageSwitch()
            ret.append((menu_id, type_, path, path_i18n))

        return ret

    def getMenuHelp(self, menu_id, language=''):
        """
        return the help string of the menu
        @param menu_id: id of the menu (same as callback_id)
        @param language: language used for translation, or empty string for default
        @param return: translated help

        """
        try:
            menu_data = self._menus[menu_id]
        except KeyError:
            raise exceptions.DataError("Trying to access an unknown menu")
        languageSwitch(language)
        help_string = _(menu_data['help_string'])
        languageSwitch()
        return help_string
