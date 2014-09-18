#!/usr/bin/python
# -*- coding: utf-8 -*-

# SAT plugin for OTR encryption
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

# XXX: thanks to Darrik L Mazey for his documentation (https://blog.darmasoft.net/2013/06/30/using-pure-python-otr.html)
#      this implentation is based on it

from sat.core.i18n import _, D_
from sat.core.constants import Const as C
from sat.core.log import getLogger
from sat.core import exceptions
log = getLogger(__name__)
from sat.tools import xml_tools
from twisted.words.protocols.jabber import jid
from twisted.python import failure
from twisted.internet import defer
import potr
from sat.memory import persistent

NS_OTR = "otr_plugin"
PRIVATE_KEY = "PRIVATE KEY"
MAIN_MENU = D_('OTR')
AUTH_TXT = D_("To authenticate your correspondent, you need to give your below fingerprint *BY AN EXTERNAL CANAL* (i.e. not in this chat), and check that the one he give you is the same as below. If there is a mismatch, there can be a spy between you !")
DROP_TXT = D_("You private key is used to encrypt messages for your correspondent, nobody except you must know it, if you are in doubt, you should drop it !\n\nAre you sure you want to drop your private key ?")

DEFAULT_POLICY_FLAGS = {
  'ALLOW_V1':False,
  'ALLOW_V2':True,
  'REQUIRE_ENCRYPTION':True,
}

PLUGIN_INFO = {
    "name": "OTR",
    "import_name": "OTR",
    "type": "SEC",
    "protocols": [],
    "dependencies": [],
    "main": "OTR",
    "handler": "no",
    "description": _("""Implementation of OTR""")
}


class Context(potr.context.Context):
    def __init__(self, host, account, other_jid):
        super(Context, self).__init__(account, other_jid)
        self.host = host

    def getPolicy(self, key):
        if key in DEFAULT_POLICY_FLAGS:
            return DEFAULT_POLICY_FLAGS[key]
        else:
            return False

    def inject(self, msg_str, appdata=None):
        assert isinstance(self.peer, jid.JID)
        msg = msg_str.decode('utf-8')
        client = self.user.client
        log.debug(u'inject(%s, appdata=%s, to=%s)' % (msg, appdata, self.peer))
        mess_data = {'message': msg,
                     'type': 'chat',
                     'from': client.jid,
                      'to': self.peer,
                      'subject': None,
                    }
        self.host.generateMessageXML(mess_data)
        client.xmlstream.send(mess_data['xml'])

    def setState(self, state):
        old_state = self.state
        super(Context, self).setState(state)
        log.debug(u"setState: %s (old_state=%s)" % (state, old_state))

        if state == potr.context.STATE_PLAINTEXT:
            feedback = _(u"/!\\ conversation with %(other_jid)s is now UNENCRYPTED") % {'other_jid': self.peer.full()}
        elif state == potr.context.STATE_ENCRYPTED:
            try:
                trusted = self.getCurrentTrust()
            except TypeError:
                trusted = False
            trusted_str = _(u"trusted") if trusted else _(u"untrusted")

            if old_state == potr.context.STATE_ENCRYPTED:
                feedback = _(u"%(trusted)s OTR conversation with %(other_jid)s REFRESHED") % {'trusted': trusted_str, 'other_jid': self.peer.full()}
            else:
                feedback = _(u"%(trusted)s Encrypted OTR conversation started with %(other_jid)s\n/!\\ Your history is not logged anymore, and most of advanced features are disabled !") % {'trusted': trusted_str, 'other_jid': self.peer.full()}
        elif state == potr.context.STATE_FINISHED:
            feedback = _(u"OTR conversation with %(other_jid)s is FINISHED") % {'other_jid': self.peer.full()}
        else:
            log.error(_(u"Unknown OTR state"))
            return

        client = self.user.client
        self.host.bridge.newMessage(client.jid.full(),
                                    feedback,
                                    mess_type=C.MESS_TYPE_INFO,
                                    to_jid=self.peer.full(),
                                    extra={},
                                    profile=client.profile)
        # TODO: send signal to frontends

    def disconnect(self):
        """Disconnect the session."""
        if self.state != potr.context.STATE_PLAINTEXT:
            super(Context, self).disconnect()

    def finish(self):
        """Finish the session - avoid to send any message but the user still has to end the session himself."""
        if self.state == potr.context.STATE_ENCRYPTED:
            self.processTLVs([potr.proto.DisconnectTLV()])


class Account(potr.context.Account):
    #TODO: manage trusted keys: if a fingerprint is not used anymore, we have no way to remove it from database yet (same thing for a correspondent jid)

    def __init__(self, host, client):
        log.debug(u"new account: %s" % client.jid)
        if not client.jid.resource:
            log.warning("Account created without resource")
        super(Account, self).__init__(unicode(client.jid), "xmpp", 1024)
        self.host = host
        self.client = client

    def loadPrivkey(self):
        log.debug(u"loadPrivkey")
        return self.privkey

    def savePrivkey(self):
        log.debug(u"savePrivkey")
        if self.privkey is None:
            raise exceptions.InternalError(_("Save is called but privkey is None !"))
        priv_key = self.privkey.serializePrivateKey().encode('hex')
        d = self.host.memory.encryptValue(priv_key, self.client.profile)
        def save_encrypted_key(encrypted_priv_key):
            self.client.otr_data[PRIVATE_KEY] = encrypted_priv_key
        d.addCallback(save_encrypted_key)

    def loadTrusts(self):
        trust_data = self.client.otr_data.get('trust', {})
        for jid_, jid_data in trust_data.iteritems():
            for fingerprint, trust_level in jid_data.iteritems():
                log.debug('setting trust for {jid}: [{fingerprint}] = "{trust_level}"'.format(jid=jid_, fingerprint=fingerprint, trust_level=trust_level))
                self.trusts.setdefault(jid.JID(jid_), {})[fingerprint] = trust_level

    def saveTrusts(self):
        log.debug("saving trusts for {profile}".format(profile=self.client.profile))
        log.debug("trusts = {}".format(self.client.otr_data['trust']))
        self.client.otr_data.force('trust')

    def setTrust(self, other_jid, fingerprint, trustLevel):
        try:
            trust_data = self.client.otr_data['trust']
        except KeyError:
            trust_data = {}
            self.client.otr_data['trust'] = trust_data
        jid_data = trust_data.setdefault(other_jid.full(), {})
        jid_data[fingerprint] = trustLevel
        super(Account, self).setTrust(other_jid, fingerprint, trustLevel)


class ContextManager(object):

    def __init__(self, host, client):
        self.host = host
        self.account = Account(host, client)
        self.contexts = {}

    def startContext(self, other_jid):
        assert isinstance(other_jid, jid.JID)
        context = self.contexts.setdefault(other_jid, Context(self.host, self.account, other_jid))
        return context

    def getContextForUser(self, other):
        log.debug(u"getContextForUser [%s]" % other)
        if not other.resource:
            log.warning("getContextForUser called with a bare jid")
        return self.startContext(other)


class OTR(object):

    def __init__(self, host):
        log.info(_(u"OTR plugin initialization"))
        self._fixPotr() # FIXME: to be removed when potr will be fixed
        self.host = host
        self.context_managers = {}
        self.skipped_profiles = set()
        host.trigger.add("MessageReceived", self.MessageReceivedTrigger, priority=100000)
        host.trigger.add("sendMessage", self.sendMessageTrigger, priority=100000)
        host.bridge.addMethod("skipOTR", ".plugin", in_sign='s', out_sign='', method=self._skipOTR)
        host.importMenu((MAIN_MENU, D_("Start/Refresh")), self._startRefresh, security_limit=0, help_string=D_("Start or refresh an OTR session"), type_=C.MENU_SINGLE)
        host.importMenu((MAIN_MENU, D_("End session")), self._endSession, security_limit=0, help_string=D_("Finish an OTR session"), type_=C.MENU_SINGLE)
        host.importMenu((MAIN_MENU, D_("Authenticate")), self._authenticate, security_limit=0, help_string=D_("Authenticate user/see your fingerprint"), type_=C.MENU_SINGLE)
        host.importMenu((MAIN_MENU, D_("Drop private key")), self._dropPrivKey, security_limit=0, type_=C.MENU_SINGLE)
        host.trigger.add("presenceReceived", self.presenceReceivedTrigger)

    def _fixPotr(self):
        # FIXME: potr fix for bad unicode handling
        # this method monkeypatch it, must be removed when potr
        # is fixed

        def getDefaultQueryMessage(self, policy):
            defaultQuery = '?OTRv{versions}?\nI would like to start ' \
                           'an Off-the-Record private conversation. However, you ' \
                           'do not have a plugin to support that.\nSee '\
                           'https://otr.cypherpunks.ca/ for more information.'
            v = '2' if policy('ALLOW_V2') else ''
            msg = defaultQuery.format(versions=v)
            return msg.encode('ascii')

        potr.context.Account.getDefaultQueryMessage = getDefaultQueryMessage

    def _skipOTR(self, profile):
        """Tell the backend to not handle OTR for this profile.

        @param profile (str): %(doc_profile)s
        """
        self.skipped_profiles.add(profile)

    @defer.inlineCallbacks
    def profileConnected(self, profile):
        if profile in self.skipped_profiles:
            return
        client = self.host.getClient(profile)
        ctxMng = self.context_managers[profile] = ContextManager(self.host, client)
        client.otr_data = persistent.PersistentBinaryDict(NS_OTR, profile)
        yield client.otr_data.load()
        encrypted_priv_key = client.otr_data.get(PRIVATE_KEY, None)
        if encrypted_priv_key is not None:
            priv_key = yield self.host.memory.decryptValue(encrypted_priv_key, profile)
            ctxMng.account.privkey = potr.crypt.PK.parsePrivateKey(priv_key.decode('hex'))[0]
        else:
            ctxMng.account.privkey = None
        ctxMng.account.loadTrusts()

    def profileDisconnected(self, profile):
        try:
            for context in self.context_managers[profile].contexts.values():
                context.disconnect()
            del self.context_managers[profile]
        except KeyError:
            pass
        try:
            self.skipped_profiles.remove(profile)
        except KeyError:
            pass

    def _startRefresh(self, menu_data, profile):
        """Start or refresh an OTR session

        @param menu_data: %(menu_data)s
        @param profile: %(doc_profile)s
        """
        try:
            to_jid = jid.JID(menu_data['jid'])
            if not to_jid.resource:
                to_jid.resource = self.host.memory.getLastResource(to_jid, profile) # FIXME: temporary and unsecure, must be changed when frontends are refactored
        except KeyError:
            log.error(_("jid key is not present !"))
            return defer.fail(exceptions.DataError)
        otrctx = self.context_managers[profile].getContextForUser(to_jid)
        query = otrctx.sendMessage(0, '?OTRv?')
        otrctx.inject(query)
        return {}

    def _endSession(self, menu_data, profile):
        """End an OTR session

        @param menu_data: %(menu_data)s
        @param profile: %(doc_profile)s
        """
        try:
            to_jid = jid.JID(menu_data['jid'])
            if not to_jid.resource:
                to_jid.resource = self.host.memory.getLastResource(to_jid, profile) # FIXME: temporary and unsecure, must be changed when frontends are refactored
        except KeyError:
            log.error(_("jid key is not present !"))
            return defer.fail(exceptions.DataError)
        otrctx = self.context_managers[profile].getContextForUser(to_jid)
        otrctx.disconnect()
        return {}

    def _authenticate(self, menu_data, profile):
        """Authenticate other user and see our own fingerprint

        @param menu_data: %(menu_data)s
        @param profile: %(doc_profile)s
        """
        try:
            to_jid = jid.JID(menu_data['jid'])
            if not to_jid.resource:
                to_jid.resource = self.host.memory.getLastResource(to_jid, profile) # FIXME: temporary and unsecure, must be changed when frontends are refactored
        except KeyError:
            log.error(_("jid key is not present !"))
            return defer.fail(exceptions.DataError)
        ctxMng = self.context_managers[profile]
        otrctx = ctxMng.getContextForUser(to_jid)
        priv_key = ctxMng.account.privkey

        if priv_key is None:
            # we have no private key yet
            dialog = xml_tools.XMLUI(C.XMLUI_DIALOG,
                     dialog_opt = {C.XMLUI_DATA_TYPE: C.XMLUI_DIALOG_MESSAGE,
                                   C.XMLUI_DATA_MESS: _("You have no private key yet, start an OTR conversation to have one"),
                                   C.XMLUI_DATA_LVL: C.XMLUI_DATA_LVL_WARNING
                                  },
                     title = _("No private key"),
                     )
            return {'xmlui': dialog.toXml()}

        other_fingerprint = otrctx.getCurrentKey()

        if other_fingerprint is None:
            # we have a private key, but not the fingerprint of our correspondent
            dialog = xml_tools.XMLUI(C.XMLUI_DIALOG,
                     dialog_opt = {C.XMLUI_DATA_TYPE: C.XMLUI_DIALOG_MESSAGE,
                                   C.XMLUI_DATA_MESS: _("Your fingerprint is\n{fingerprint}\n\nStart an OTR conversation to have your correspondent one.").format(fingerprint=priv_key),
                                   C.XMLUI_DATA_LVL: C.XMLUI_DATA_LVL_INFO
                                  },
                     title = _("Fingerprint"),
                     )
            return {'xmlui': dialog.toXml()}

        def setTrust(raw_data, profile):
            # This method is called when authentication form is submited
            data = xml_tools.XMLUIResult2DataFormResult(raw_data)
            if data['match'] == 'yes':
                otrctx.setCurrentTrust('verified')
                note_msg = _("Your correspondant {correspondent} is now TRUSTED")
            else:
                otrctx.setCurrentTrust('')
                note_msg = _("Your correspondant {correspondent} is now UNTRUSTED")
            note = xml_tools.XMLUI(C.XMLUI_DIALOG, dialog_opt = {
                                   C.XMLUI_DATA_TYPE: C.XMLUI_DIALOG_NOTE,
                                   C.XMLUI_DATA_MESS: note_msg.format(correspondent=otrctx.peer)}
                                   )
            return {'xmlui': note.toXml()}

        submit_id = self.host.registerCallback(setTrust, with_data=True, one_shot=True)
        trusted = bool(otrctx.getCurrentTrust())

        xmlui = xml_tools.XMLUI(C.XMLUI_FORM, title=_('Authentication (%s)') % to_jid.full(), submit_id=submit_id)
        xmlui.addText(_(AUTH_TXT))
        xmlui.addDivider()
        xmlui.addText(_("Your own fingerprint is:\n{fingerprint}").format(fingerprint=priv_key))
        xmlui.addText(_("Your correspondent fingerprint should be:\n{fingerprint}").format(fingerprint=other_fingerprint))
        xmlui.addDivider('blank')
        xmlui.changeContainer('pairs')
        xmlui.addLabel(_('Is your correspondent fingerprint the same as here ?'))
        xmlui.addList("match", [('yes', _('yes')),('no', _('no'))], ['yes' if trusted else 'no'])
        return {'xmlui': xmlui.toXml()}

    def _dropPrivKey(self, menu_data, profile):
        """Drop our private Key

        @param menu_data: %(menu_data)s
        @param profile: %(doc_profile)s
        """
        try:
            to_jid = jid.JID(menu_data['jid'])
            if not to_jid.resource:
                to_jid.resource = self.host.memory.getLastResource(to_jid, profile) # FIXME: temporary and unsecure, must be changed when frontends are refactored
        except KeyError:
            log.error(_("jid key is not present !"))
            return defer.fail(exceptions.DataError)

        ctxMng = self.context_managers[profile]
        if ctxMng.account.privkey is None:
            return {'xmlui': xml_tools.note(_("You don't have a private key yet !")).toXml()}

        def dropKey(data, profile):
            if C.bool(data['answer']):
                # we end all sessions
                for context in ctxMng.contexts.values():
                    context.disconnect()
                ctxMng.account.privkey = None
                ctxMng.account.getPrivkey()  # as account.privkey is None, getPrivkey will generate a new key, and save it
                return {'xmlui': xml_tools.note(_("Your private key has been dropped")).toXml()}
            return {}

        submit_id = self.host.registerCallback(dropKey, with_data=True, one_shot=True)

        confirm = xml_tools.XMLUI(C.XMLUI_DIALOG, title=_('Confirm private key drop'), dialog_opt = {'type': C.XMLUI_DIALOG_CONFIRM, 'message': _(DROP_TXT)}, submit_id = submit_id)
        return {'xmlui': confirm.toXml()}

    def _receivedTreatment(self, data, profile):
        from_jid = jid.JID(data['from'])
        log.debug(u"_receivedTreatment [from_jid = %s]" % from_jid)
        otrctx = self.context_managers[profile].getContextForUser(from_jid)
        encrypted = True

        try:
            res = otrctx.receiveMessage(data['body'].encode('utf-8'))
        except potr.context.UnencryptedMessage:
            if otrctx.state == potr.context.STATE_ENCRYPTED:
                log.warning(u"Received unencrypted message in an encrypted context (from %(jid)s)" % {'jid': from_jid.full()})
                client = self.host.getClient(profile)
                self.host.bridge.newMessage(from_jid.full(),
                                            _(u"WARNING: received unencrypted data in a supposedly encrypted context"),
                                            mess_type=C.MESS_TYPE_INFO,
                                            to_jid=client.jid.full(),
                                            extra={},
                                            profile=client.profile)
            encrypted = False

        if not encrypted:
            return data
        else:
            if res[0] != None:
                # decrypted messages handling.
                # receiveMessage() will return a tuple, the first part of which will be the decrypted message
                data['body'] = res[0].decode('utf-8')
                raise failure.Failure(exceptions.SkipHistory()) # we send the decrypted message to frontends, but we don't want it in history
            else:
                raise failure.Failure(exceptions.CancelError()) # no message at all (no history, no signal)

    def _receivedTreatmentForSkippedProfiles(self, data, profile):
        """This profile must be skipped because the frontend manages OTR itself,
        but we still need to check if the message must be stored in history or not"""
        body = data['body'].encode('utf-8')
        if body.startswith(potr.proto.OTRTAG):
            raise failure.Failure(exceptions.SkipHistory())
        return data

    def MessageReceivedTrigger(self, message, post_treat, profile):
        if profile in self.skipped_profiles:
            post_treat.addCallback(self._receivedTreatmentForSkippedProfiles, profile)
        else:
            post_treat.addCallback(self._receivedTreatment, profile)
        return True

    def sendMessageTrigger(self, mess_data, pre_xml_treatments, post_xml_treatments, profile):
        if profile in self.skipped_profiles:
            return True
        to_jid = mess_data['to']
        if mess_data['type'] != 'groupchat' and not to_jid.resource:
            to_jid.resource = self.host.memory.getLastResource(to_jid, profile) # FIXME: it's dirty, but frontends don't manage resources correctly now, refactoring is planed
        otrctx = self.context_managers[profile].getContextForUser(to_jid)
        if mess_data['type'] != 'groupchat' and otrctx.state != potr.context.STATE_PLAINTEXT:
            if otrctx.state == potr.context.STATE_ENCRYPTED:
                log.debug(u"encrypting message")
                otrctx.sendMessage(0, mess_data['message'].encode('utf-8'))
                client = self.host.getClient(profile)
                self.host.sendMessageToBridge(mess_data, client)
            else:
                feedback = D_("Your message was not sent because your correspondent closed the encrypted conversation on his/her side. Either close your own side, or refresh the session.")
                client = self.host.getClient(profile)
                self.host.bridge.newMessage(to_jid.full(),
                                            feedback,
                                            mess_type=C.MESS_TYPE_INFO,
                                            to_jid=client.jid.full(),
                                            extra={},
                                            profile=client.profile)
            return False
        else:
            log.debug(u"sending message unencrypted")
            return True

    def presenceReceivedTrigger(self, entity, show, priority, statuses, profile):
        if show != "unavailable":
            return
        if not entity.resource:
            entity.resource = self.host.memory.getLastResource(entity, profile)  # FIXME: temporary and unsecure, must be changed when frontends are refactored
        otrctx = self.context_managers[profile].getContextForUser(entity)
        otrctx.disconnect()
        return True
