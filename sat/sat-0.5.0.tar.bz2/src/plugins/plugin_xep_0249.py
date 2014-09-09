#!/usr/bin/python
# -*- coding: utf-8 -*-

# SAT plugin for managing xep-0249
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

from sat.core.i18n import _
from sat.core.constants import Const as C
from sat.core.log import getLogger
log = getLogger(__name__)
from twisted.words.xish import domish
from twisted.words.protocols.jabber import jid

from zope.interface import implements

from wokkel import disco, iwokkel


try:
    from twisted.words.protocols.xmlstream import XMPPHandler
except ImportError:
    from wokkel.subprotocols import XMPPHandler

MESSAGE = '/message'
NS_DIRECT_MUC_INVITATION = 'jabber:x:conference'
DIRECT_MUC_INVITATION_REQUEST = MESSAGE + '/x[@xmlns="' + NS_DIRECT_MUC_INVITATION + '"]'
AUTOJOIN_KEY = "Misc"
AUTOJOIN_NAME = "Auto-join MUC on invitation"
AUTOJOIN_VALUES = ["ask", "always", "never"]

PLUGIN_INFO = {
    "name": "XEP 0249 Plugin",
    "import_name": "XEP-0249",
    "type": "XEP",
    "protocols": ["XEP-0249"],
    "dependencies": ["XEP-0045"],
    "recommendations": [C.TEXT_CMDS],
    "main": "XEP_0249",
    "handler": "yes",
    "description": _("""Implementation of Direct MUC Invitations""")
}


class XEP_0249(object):

    params = """
    <params>
    <individual>
    <category name="%(category_name)s" label="%(category_label)s">
        <param name="%(param_name)s" label="%(param_label)s" type="list" security="0">
            %(param_options)s
        </param>
     </category>
    </individual>
    </params>
    """ % {
        'category_name': AUTOJOIN_KEY,
        'category_label': _("Misc"),
        'param_name': AUTOJOIN_NAME,
        'param_label': _("Auto-join MUC on invitation"),
        'param_options': '\n'.join(['<option value="%s" %s/>' % \
                                   (value, 'selected="true"' if value == AUTOJOIN_VALUES[0] else '') \
                                   for value in AUTOJOIN_VALUES])
    }

    def __init__(self, host):
        log.info(_("Plugin XEP_0249 initialization"))
        self.host = host
        host.memory.updateParams(self.params)
        host.bridge.addMethod("inviteMUC", ".plugin", in_sign='sssa{ss}s', out_sign='', method=self._invite)
        try:
            self.host.plugins[C.TEXT_CMDS].registerTextCommands(self)
        except KeyError:
            log.info(_("Text commands not available"))

    def getHandler(self, profile):
        return XEP_0249_handler(self)

    def invite(self, target, room, options={}, profile_key=C.PROF_KEY_NONE):
        """
        Invite a user to a room
        @param target: jid of the user to invite
        @param room: jid of the room where the user is invited
        @options: attribute with extra info (reason, password) as in #XEP-0249
        @profile_key: %(doc_profile_key)s
        """
        profile = self.host.memory.getProfileName(profile_key)
        if not profile:
            log.error(_("Profile doesn't exists !"))
            return
        message = domish.Element((None, 'message'))
        message["to"] = target.full()
        x_elt = message.addElement('x', NS_DIRECT_MUC_INVITATION)
        x_elt['jid'] = room.userhost()
        for opt in options:
            x_elt[opt] = options[opt]
        self.host.profiles[profile].xmlstream.send(message)

    def _invite(self, target, service, roomId, options={}, profile_key=C.PROF_KEY_NONE):
        """
        Invite an user to a room
        @param target: jid of the user to invite
        @param service: jid of the MUC service
        @param roomId: name of the room
        @param profile_key: %(doc_profile_key)s
        """
        #TODO: check parameters validity
        self.invite(jid.JID(target), jid.JID("%s@%s" % (roomId, service)), options, profile_key)

    def _accept(self, room, profile_key=C.PROF_KEY_NONE):
        """
        Accept the invitation to join a MUC
        @param room: room jid as string
        """
        profile = self.host.memory.getProfileName(profile_key)
        if not profile:
            log.error(_("Profile doesn't exists !"))
            return
        log.info(_('Invitation accepted for room %(room)s [%(profile)s]') % {'room': room, 'profile': profile})
        _jid, xmlstream = self.host.getJidNStream(profile)
        d = self.host.plugins["XEP-0045"].join(jid.JID(room), _jid.user, {}, profile)
        return d

    def onInvitation(self, message, profile):
        """
        called when an invitation is received
        @param message: message element
        @profile: %(doc_profile)s
        """
        try:
            room = message.firstChildElement()['jid']
            log.info(_('Invitation received for room %(room)s [%(profile)s]') % {'room': room, 'profile': profile})
        except:
            log.error(_('Error while parsing invitation'))
            return
        from_ = message["from"]
        if room in self.host.plugins["XEP-0045"].clients[profile].joined_rooms:
            log.info(_("Invitation silently discarded because user is already in the room."))
            return
        autojoin = self.host.memory.getParamA(AUTOJOIN_NAME, AUTOJOIN_KEY, profile_key=profile)

        def accept_cb(conf_id, accepted, data, profile):
            if conf_id == room and accepted:
                self._accept(room, profile)

        if autojoin == "always":
            self._accept(room, profile)
        elif autojoin == "never":
            self.host.bridge.newAlert(_("An invitation from %(user)s to join the room %(room)s has been declined according to your personal settings.") % {'user': from_, 'room': room}, _("MUC invitation"), "INFO", profile)
        else:  # leave the default value here
            data = {"message": _("You have been invited by %(user)s to join the room %(room)s. Do you accept?") % {'user': from_, 'room': room}, "title": _("MUC invitation")}
            self.host.askConfirmation(room, "YES/NO", data, accept_cb, profile)

    def cmd_invite(self, mess_data, profile):
        """invite someone in the room

        @command (group): (JID)
            - JID: the JID of the person to invite
        """
        log.debug("Catched invite command")

        if mess_data['type'] != "groupchat":
            self.host.plugins[C.TEXT_CMDS].feedBackWrongContext('invite', 'groupchat', mess_data, profile)
            return False

        jid_s = mess_data["unparsed"].strip()
        try:
            assert(jid_s)
            jid_ = jid.JID(jid_s)
            assert(jid_.user)
            assert(jid_.host)
        except (jid.InvalidFormat, AssertionError):
            feedback = _(u"You must provide a valid JID to invite, like in '/invite contact@example.net'")
            self.host.plugins[C.TEXT_CMDS].feedBack(feedback, mess_data, profile)
            return False

        self.invite(jid_, mess_data["to"], {}, profile)
        return False


class XEP_0249_handler(XMPPHandler):
    implements(iwokkel.IDisco)

    def __init__(self, plugin_parent):
        self.plugin_parent = plugin_parent
        self.host = plugin_parent.host

    def connectionInitialized(self):
        self.xmlstream.addObserver(DIRECT_MUC_INVITATION_REQUEST, self.plugin_parent.onInvitation, profile=self.parent.profile)

    def getDiscoInfo(self, requestor, target, nodeIdentifier=''):
        return [disco.DiscoFeature(NS_DIRECT_MUC_INVITATION)]

    def getDiscoItems(self, requestor, target, nodeIdentifier=''):
        return []
