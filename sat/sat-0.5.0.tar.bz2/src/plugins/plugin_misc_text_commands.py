#!/usr/bin/python
# -*- coding: utf-8 -*-

# SàT plugin for managing text commands
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
from sat.core import exceptions
from twisted.words.protocols.jabber import jid
from twisted.internet import defer
from sat.core.log import getLogger
log = getLogger(__name__)
from twisted.python import failure

PLUGIN_INFO = {
    "name": "Text commands",
    "import_name": C.TEXT_CMDS,
    "type": "Misc",
    "protocols": [],
    "dependencies": [],
    "main": "TextCommands",
    "handler": "no",
    "description": _("""IRC like text commands""")
}


class TextCommands(object):
    #FIXME: doc strings for commands have to be translatable
    #       plugins need a dynamic translation system (translation
    #       should be downloadable independently)

    HELP_SUGGESTION = _("Type '/help' to get a list of the available commands. If you didn't want to use a command, please start your message with '//' to escape the slash.")

    def __init__(self, host):
        log.info(_("Text commands initialization"))
        self.host = host
        host.trigger.add("sendMessage", self.sendMessageTrigger)
        self._commands = {}
        self._whois = []
        self.registerTextCommands(self)

    def registerTextCommands(self, instance):
        """ Add a text command
        @param instance: instance of a class containing text commands

        """
        for attr in dir(instance):
            if attr.startswith('cmd_'):
                cmd = getattr(instance, attr)
                if not callable(cmd):
                    log.warning(_("Skipping not callable [%s] attribute") % attr)
                    continue
                cmd_name = attr[4:]
                if not cmd_name:
                    log.warning(_("Skipping cmd_ method"))
                if cmd_name in self._commands:
                    suff=2
                    while (cmd_name + str(suff)) in self._commands:
                        suff+=1
                    new_name = cmd_name + str(suff)
                    log.warning(_("Conflict for command [%(old_name)s], renaming it to [%(new_name)s]") % {'old_name': cmd_name, 'new_name': new_name})
                    cmd_name = new_name
                self._commands[cmd_name] = cmd
                log.info(_("Registered text command [%s]") % cmd_name)

    def addWhoIsCb(self, callback, priority=0):
        """Add a callback which give information to the /whois command
        @param callback: a callback which will be called with the following arguments
            - whois_msg: list of information strings to display, callback need to append its own strings to it
            - target_jid: full jid from who we want informations
            - profile: %(doc_profile)s
        @param priority: priority of the information to show (the highest priority will be displayed first)

        """
        self._whois.append((priority, callback))
        self._whois.sort(key=lambda item: item[0], reverse=True)

    def sendMessageTrigger(self, mess_data, pre_xml_treatments, post_xml_treatments, profile):
        """ Install SendMessage command hook """
        pre_xml_treatments.addCallback(self._sendMessageCmdHook, profile)
        return True

    def _sendMessageCmdHook(self, mess_data, profile):
        """ Check text commands in message, and react consequently
        msg starting with / are potential command. If a command is found, it is executed, else message is sent normally
        msg starting with // are escaped: they are sent with a single /
        commands can abord message sending (if they return anything evaluating to False), or continue it (if they return True), eventually after modifying the message
        an "unparsed" key is added to message, containing part of the message not yet parsed
        commands can be deferred or not

        """
        msg = mess_data["message"]
        try:
            if msg[:2] == '//':
                # we have a double '/', it's the escape sequence
                mess_data["message"] = msg[1:]
                return mess_data
            if msg[0] != '/':
                return mess_data
        except IndexError:
            return mess_data

        # we have a command
        d = None
        command = msg[1:].partition(' ')[0].lower()
        if command.isalpha():
            # looks like an actual command, we try to call the corresponding method
            def retHandling(ret):
                """ Handle command return value:
                if ret is True, normally send message (possibly modified by command)
                else, abord message sending

                """
                if ret:
                    return mess_data
                else:
                    log.debug("text commands took over")
                    raise failure.Failure(exceptions.CancelError())

            def genericErrback(failure):
                self.feedBack("Command failed with condition '%s'" % failure.value.condition, mess_data, profile)
                return False

            try:
                mess_data["unparsed"] = msg[1 + len(command):]  # part not yet parsed of the message
                d = defer.maybeDeferred(self._commands[command], mess_data, profile)
                d.addCallbacks(lambda ret: ret, genericErrback)  # XXX: dummy callback is needed
                d.addCallback(retHandling)

            except KeyError:
                self.feedBack(_("Unknown command /%s. ") % command + self.HELP_SUGGESTION, mess_data, profile)
                log.debug("text commands took over")
                raise failure.Failure(exceptions.CancelError())

        return d or mess_data  # if a command is detected, we should have a deferred, else we send the message normally

    def getRoomJID(self, arg, service_jid):
        """Return a room jid with a shortcut
        @param arg: argument: can be a full room jid (e.g.: sat@chat.jabberfr.org)
                    or a shortcut (e.g.: sat or sat@ for sat on current service)
        @param service_jid: jid of the current service (e.g.: chat.jabberfr.org)
        """
        nb_arobas = arg.count('@')
        if nb_arobas == 1:
            if arg[-1] != '@':
                return jid.JID(arg)
            return jid.JID(arg + service_jid)
        return jid.JID(u"%s@%s" % (arg, service_jid))

    def feedBack(self, message, mess_data, profile):
        """Give a message back to the user"""
        if mess_data["type"] == 'groupchat':
            _from = mess_data["to"].userhostJID()
        else:
            _from = self.host.getJidNStream(profile)[0]

        self.host.bridge.newMessage(unicode(mess_data["to"]), message, C.MESS_TYPE_INFO, unicode(_from), {}, profile=profile)

    def feedBackWrongContext(self, command, types, mess_data, profile):
        """Give a generic message to the user when a command has been used in a wrong context.

        @param command (string): the command name (without the slash)
        @param types (string, list): the message types to which the command applies.
        @param mess_data (dict): original message data
        @param profile: %(doc_profile)s
        """
        if not isinstance(types, str):
            types = _(' or ').join(types)
        feedback = _("/%(command)s command only applies on %(type)s messages. ") % {'command': command, 'type': types}
        self.host.plugins[C.TEXT_CMDS].feedBack(feedback + self.HELP_SUGGESTION, mess_data, profile)

    def cmd_whois(self, mess_data, profile):
        """show informations on entity"""
        log.debug("Catched whois command")

        entity = mess_data["unparsed"].strip()

        if mess_data['type'] == "groupchat":
            room = mess_data["to"].userhostJID()
            try:
                if self.host.plugins["XEP-0045"].isNickInRoom(room, entity, profile):
                    entity = u"%s/%s" % (room, entity)
            except KeyError:
                log.warning("plugin XEP-0045 is not present")

        if not entity:
            target_jid = mess_data["to"]
        else:
            try:
                target_jid = jid.JID(entity)
                if not target_jid.user or not target_jid.host:
                    raise jid.InvalidFormat
            except (jid.InvalidFormat, RuntimeError):
                self.feedBack(_("Invalid jid, can't whois"), mess_data, profile)
                return False

        if not target_jid.resource:
            target_jid.resource = self.host.memory.getLastResource(target_jid, profile)

        whois_msg = [_(u"whois for %(jid)s") % {'jid': target_jid}]

        d = defer.succeed(None)
        for ignore, callback in self._whois:
            d.addCallback(lambda ignore: callback(whois_msg, mess_data, target_jid, profile))

        def feedBack(ignore):
            self.feedBack(u"\n".join(whois_msg), mess_data, profile)
            return False

        d.addCallback(feedBack)
        return d

    def cmd_help(self, mess_data, profile):
        """show help on available commands"""
        commands = filter(lambda method: method.startswith('cmd_'), dir(self))
        longuest = max([len(command) for command in commands])
        help_cmds = []

        for command in sorted(self._commands):
            method = self._commands[command]
            try:
                help_str = method.__doc__.split('\n')[0]
            except AttributeError:
                help_str = ''
            spaces = (longuest - len(command)) * ' '
            help_cmds.append("    /%s: %s %s" % (command, spaces, help_str))

        help_mess = _(u"Text commands available:\n%s") % (u'\n'.join(help_cmds), )
        self.feedBack(help_mess, mess_data, profile)

    def cmd_me(self, mess_data, profile):
        """Display a message at third person"""
        # We just catch the method and continue it as the frontends should manage /me display
        return True
