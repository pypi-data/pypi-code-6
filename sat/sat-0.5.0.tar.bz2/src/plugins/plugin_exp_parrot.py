#!/usr/bin/python
# -*- coding: utf-8 -*-

# SAT plugin for parrot mode (experimental)
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
from twisted.words.protocols.jabber import jid

from sat.core.exceptions import UnknownEntityError
#from sat.tools.misc import SkipOtherTriggers

PLUGIN_INFO = {
    "name": "Parrot Plugin",
    "import_name": "EXP-PARROT",
    "type": "EXP",
    "protocols": [],
    "dependencies": ["XEP-0045"],
    "recommendations": [C.TEXT_CMDS],
    "main": "Exp_Parrot",
    "handler": "no",
    "description": _("""Implementation of parrot mode (repeat messages between 2 entities)""")
}


class Exp_Parrot(object):
    """Parrot mode plugin: repeat messages from one entity or MUC room to another one"""
    #XXX: This plugin can be potentially dangerous if we don't trust entities linked
    #     this is specially true if we have other triggers.
    #     sendMessageTrigger avoid other triggers execution, it's deactivated to allow
    #     /unparrot command in text commands plugin.

    def __init__(self, host):
        log.info(_("Plugin Parrot initialization"))
        self.host = host
        host.trigger.add("MessageReceived", self.MessageReceivedTrigger, priority=100)
        #host.trigger.add("sendMessage", self.sendMessageTrigger, priority=100)
        try:
            self.host.plugins[C.TEXT_CMDS].registerTextCommands(self)
        except KeyError:
            log.info(_("Text commands not available"))

    #def sendMessageTrigger(self, mess_data, treatments, profile):
    #    """ Deactivate other triggers if recipient is in parrot links """
    #    client = self.host.getClient(profile)
    #    try:
    #        _links = client.parrot_links
    #    except AttributeError:
    #        return True
    #
    #    if mess_data['to'].userhostJID() in _links.values():
    #        log.debug("Parrot link detected, skipping other triggers")
    #        raise SkipOtherTriggers

    def MessageReceivedTrigger(self, message, post_treat, profile):
        """ Check if source is linked and repeat message, else do nothing  """
        client = self.host.getClient(profile)
        from_jid = jid.JID(message["from"])

        try:
            _links = client.parrot_links
        except AttributeError:
            return True

        if not from_jid.userhostJID() in _links:
            return True

        for e in message.elements():
            if e.name == "body":
                mess_body = e.children[0] if e.children else ""

                try:
                    entity_type = self.host.memory.getEntityData(from_jid, ['type'], profile)["type"]
                except (UnknownEntityError, KeyError):
                    entity_type = "contact"
                if entity_type == 'chatroom':
                    src_txt = from_jid.resource
                    if src_txt == self.host.plugins["XEP-0045"].getRoomNick(from_jid.userhost(), profile):
                        #we won't repeat our own messages
                        return True
                else:
                    src_txt = from_jid.user
                msg = "[%s] %s" % (src_txt, mess_body)

                linked = _links[from_jid.userhostJID()]

                self.host.sendMessage(jid.JID(unicode(linked)), msg, None, "auto", no_trigger=True, profile_key=profile)
        else:
            log.warning("No body element found in message, following normal behaviour")

        return True

    def addParrot(self, source_jid, dest_jid, profile):
        """Add a parrot link from one entity to another one
        @param source_jid: entity from who messages will be repeated
        @param dest_jid: entity where the messages will be repeated
        @param profile: %(doc_profile_key)s"""
        client = self.host.getClient(profile)
        try:
            _links = client.parrot_links
        except AttributeError:
            _links = client.parrot_links = {}

        _links[source_jid.userhostJID()] = dest_jid
        log.info("Parrot mode: %s will be repeated to %s" % (source_jid.userhost(), unicode(dest_jid)))

    def removeParrot(self, source_jid, profile):
        """Remove parrot link
        @param source_jid: this entity will no more be repeated
        @param profile: %(doc_profile_key)s"""
        client = self.host.getClient(profile)
        try:
            del client.parrot_links[source_jid.userhostJID()]
        except (AttributeError, KeyError):
            pass

    def cmd_parrot(self, mess_data, profile):
        """activate Parrot mode between 2 entities, in both directions."""
        log.debug("Catched parrot command")
        txt_cmd = self.host.plugins[C.TEXT_CMDS]

        try:
            link_left_jid = jid.JID(mess_data["unparsed"].strip())
            if not link_left_jid.user or not link_left_jid.host:
                raise jid.InvalidFormat
        except jid.InvalidFormat:
            txt_cmd.feedBack("Can't activate Parrot mode for invalid jid", mess_data, profile)
            return False

        link_right_jid = mess_data['to']

        self.addParrot(link_left_jid, link_right_jid, profile)
        self.addParrot(link_right_jid, link_left_jid, profile)

        txt_cmd.feedBack("Parrot mode activated for %s" % (unicode(link_left_jid), ), mess_data, profile)

        return False

    def cmd_unparrot(self, mess_data, profile):
        """remove Parrot mode between 2 entities, in both directions."""
        log.debug("Catched unparrot command")
        txt_cmd = self.host.plugins[C.TEXT_CMDS]

        try:
            link_left_jid = jid.JID(mess_data["unparsed"].strip())
            if not link_left_jid.user or not link_left_jid.host:
                raise jid.InvalidFormat
        except jid.InvalidFormat:
            txt_cmd.feedBack("Can't deactivate Parrot mode for invalid jid", mess_data, profile)
            return False

        link_right_jid = mess_data['to']

        self.removeParrot(link_left_jid, profile)
        self.removeParrot(link_right_jid, profile)

        txt_cmd.feedBack("Parrot mode deactivated for %s and %s" % (unicode(link_left_jid), unicode(link_right_jid)), mess_data, profile)

        return False
