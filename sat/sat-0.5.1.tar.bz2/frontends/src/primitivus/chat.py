#!/usr/bin/python
# -*- coding: utf-8 -*-

# Primitivus: a SAT frontend
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
from sat.core import log as logging
log = logging.getLogger(__name__)
import urwid
from urwid_satext import sat_widgets
from urwid_satext.files_management import FileDialog
from sat_frontends.quick_frontend.quick_chat import QuickChat
from sat_frontends.primitivus.card_game import CardGame
from sat_frontends.quick_frontend.quick_utils import escapePrivate, unescapePrivate
from sat_frontends.primitivus.constants import Const as C
from sat_frontends.primitivus.keys import action_key_map as a_key
import time
from sat_frontends.tools.jid  import JID


class ChatText(urwid.FlowWidget):
    """Manage the printing of chat message"""

    def __init__(self, parent, timestamp, nick, my_mess, message, align='left', is_info=False):
        self.parent = parent
        self.timestamp = time.localtime(timestamp)
        self.nick = nick
        self.my_mess = my_mess
        self.message = unicode(message)
        self.align = align
        self.is_info = is_info

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key

    def rows(self,size,focus=False):
        return self.display_widget(size, focus).rows(size, focus)

    def render(self, size, focus=False):
        canvas = urwid.CompositeCanvas(self.display_widget(size, focus).render(size, focus))
        if focus:
            canvas.set_cursor(self.get_cursor_coords(size))
        return canvas

    def get_cursor_coords(self, size):
        #(maxcol,) = size
        return 0, 0

    def display_widget(self, size, focus):
        render_txt = []
        if not self.is_info:
            if self.parent.show_timestamp:
                time_format = "%c" if self.timestamp < self.parent.day_change else "%H:%M" #if the message was sent before today, we print the full date
                render_txt.append(('date',"[%s]" % time.strftime(time_format, self.timestamp).decode('utf-8')))
            if self.parent.show_short_nick:
                render_txt.append(('my_nick' if self.my_mess else 'other_nick',"**" if self.my_mess else "*"))
            else:
                render_txt.append(('my_nick' if self.my_mess else 'other_nick',"[%s] " % self.nick))
        render_txt.append(self.message)
        txt_widget = urwid.Text(render_txt, align=self.align)
        if self.is_info:
            return urwid.AttrMap(txt_widget, 'info_msg')
        return txt_widget


class Chat(urwid.WidgetWrap, QuickChat):

    def __init__(self, target, host, type_='one2one'):
        self.target = target
        QuickChat.__init__(self, target, host, type_)
        self.content = urwid.SimpleListWalker([])
        self.text_list = urwid.ListBox(self.content)
        self.chat_widget = urwid.Frame(self.text_list)
        self.chat_colums = urwid.Columns([('weight', 8, self.chat_widget)])
        self.chat_colums = urwid.Columns([('weight', 8, self.chat_widget)])
        self.pile = urwid.Pile([self.chat_colums])
        urwid.WidgetWrap.__init__(self, self.__getDecoration(self.pile))
        self.setType(type_)
        self.day_change = time.strptime(time.strftime("%a %b %d 00:00:00  %Y")) #struct_time of day changing time
        self.show_timestamp = True
        self.show_short_nick = False
        self.show_title = 1 #0: clip title; 1: full title; 2: no title
        self.subject = None

    def keypress(self, size, key):
        if key == a_key['OCCUPANTS_HIDE']: #user wants to (un)hide the presents panel
            if self.type == 'group':
                widgets = [widget for (widget, options) in self.chat_colums.contents]
                if self.present_panel in widgets:
                    self.__removePresentPanel()
                else:
                    self.__appendPresentPanel()
        elif key == a_key['TIMESTAMP_HIDE']: #user wants to (un)hide timestamp
            self.show_timestamp = not self.show_timestamp
            for wid in self.content:
                wid._invalidate()
        elif key == a_key['SHORT_NICKNAME']: #user wants to (not) use short nick
            self.show_short_nick = not self.show_short_nick
            for wid in self.content:
                wid._invalidate()
        elif key == a_key['DECORATION_HIDE']: #user wants to (un)hide widget decoration
            show = not isinstance(self._w, sat_widgets.LabelLine)
            self.showDecoration(show)
            self._invalidate()
        elif key == a_key['SUBJECT_SWITCH']: #user wants to (un)hide group's subject or change its apperance
            if self.subject:
                self.show_title = (self.show_title + 1) % 3
                if self.show_title == 0:
                    self.setSubject(self.subject,'clip')
                elif self.show_title == 1:
                    self.setSubject(self.subject,'space')
                elif self.show_title == 2:
                    self.chat_widget.header = None
                self._invalidate()


        return super(Chat, self).keypress(size, key)

    def getMenu(self):
        """Return Menu bar"""
        menu = sat_widgets.Menu(self.host.loop)
        if self.type == 'group':
            self.host.addMenus(menu, C.MENU_ROOM, {'room_jid': self.target.bare})
            game = _("Game")
            menu.addMenu(game, "Tarot", self.onTarotRequest)
        elif self.type == 'one2one':
            self.host.addMenus(menu, C.MENU_SINGLE, {'jid': unescapePrivate(self.target)})
            menu.addMenu(_("Action"), _("Send file"), self.onSendFileRequest)
        return menu

    def setType(self, type_):
        QuickChat.setType(self, type_)
        if type_ == 'one2one':
            self.historyPrint(profile=self.host.profile)
        elif type_ == 'group':
            if len(self.chat_colums.contents) == 1:
                present_widget = self.__buildPresentList()
                self.present_panel = sat_widgets.VerticalSeparator(present_widget)
                self.__appendPresentPanel()

    def __getDecoration(self, widget):
        return sat_widgets.LabelLine(widget, self.__getSurrendedText())

    def __getSurrendedText(self):
        """Get the text to be displayed as the dialog title."""
        if not hasattr(self, "surrended_text"):
            self.__setSurrendedText()
        return self.surrended_text

    def __setSurrendedText(self, state=None):
        """Set the text to be displayed as the dialog title
        @param stat: chat state of the contact
        """
        text = unicode(unescapePrivate(self.target))
        if state:
            text += " (" + state + ")"
        self.surrended_text = sat_widgets.SurroundedText(text)

    def showDecoration(self, show=True):
        """Show/Hide the decoration around the chat window"""
        if show:
            main_widget = self.__getDecoration(self.pile)
        else:
            main_widget = self.pile
        self._w = main_widget

    def updateChatState(self, state, nick=None):
        """Set the chat state (XEP-0085) of the contact. Leave nick to None
        to set the state for a one2one conversation, or give a nickname or
        C.ALL_OCCUPANTS to set the state of a participant within a MUC.
        @param state: the new chat state
        @param nick: None for one2one, the MUC user nick or C.ALL_OCCUPANTS
        """
        if nick:
            assert(self.type == 'group')
            occupants = self.occupants if nick == C.ALL_OCCUPANTS else [nick]
            options = self.present_wid.getAllValues()
            for index in xrange(0, len(options)):
                nick = options[index].value
                if nick in occupants:
                    options[index] = (nick, '%s %s' % (C.MUC_USER_STATES[state], nick))
            self.present_wid.changeValues(options)
            self.host.redraw()
        else:
            assert(self.type == 'one2one')
            self.__setSurrendedText(state)
            self.showDecoration()
            self.host.redraw()

    def _presentClicked(self, list_wid, clicked_wid):
        assert(self.type == 'group')
        nick = clicked_wid.getValue().value
        if nick == self.getUserNick():
            #We ignore click on our own nick
            return
        #we have a click on a nick, we add the private conversation to the contact_list
        full_jid = JID("%s/%s" % (self.target.bare, nick))
        new_jid = escapePrivate(full_jid)
        if new_jid not in self.host.contact_list:
            self.host.contact_list.add(new_jid, [C.GROUP_NOT_IN_ROSTER])

        #now we select the new window
        self.host.contact_list.setFocus(full_jid, True)

    def __buildPresentList(self):
        self.present_wid = sat_widgets.GenericList([],option_type = sat_widgets.ClickableText, on_click=self._presentClicked)
        return self.present_wid

    def __appendPresentPanel(self):
        self.chat_colums.contents.append((self.present_panel,('weight', 2, False)))

    def __removePresentPanel(self):
        for widget, options in self.chat_colums.contents:
            if widget is self.present_panel:
                self.chat_colums.contents.remove((widget, options))
                break

    def __appendGamePanel(self, widget):
        assert (len(self.pile.contents) == 1)
        self.pile.contents.insert(0,(widget,('weight', 1)))
        self.pile.contents.insert(1,(urwid.Filler(urwid.Divider('-'),('fixed', 1))))
        self.host.redraw()

    def __removeGamePanel(self):
        assert (len(self.pile.contents) == 3)
        del self.pile.contents[0]
        self.host.redraw()

    def setSubject(self, subject, wrap='space'):
        """Set title for a group chat"""
        QuickChat.setSubject(self, subject)
        self.subject = subject
        self.subj_wid = urwid.Text(unicode(subject.replace('\n','|') if wrap == 'clip' else subject ),
                                  align='left' if wrap=='clip' else 'center',wrap=wrap)
        self.chat_widget.header = urwid.AttrMap(self.subj_wid,'title')
        self.host.redraw()

    def setPresents(self, param_nicks):
        """Set the users presents in the contact list for a group chat
        @param nicks: list of nicknames
        """
        nicks = [unicode(nick) for nick in param_nicks] #FIXME: should be done in DBus bridge
        nicks.sort()
        QuickChat.setPresents(self, nicks)
        self.present_wid.changeValues(nicks)
        self.host.redraw()

    def replaceUser(self, param_nick, show_info=True):
        """Add user if it is not in the group list"""
        nick = unicode(param_nick) #FIXME: should be done in DBus bridge
        QuickChat.replaceUser(self, nick, show_info)
        presents = self.present_wid.getAllValues()
        if nick not in [present.value for present in presents]:
            presents.append(nick)
            presents.sort(cmp=lambda a, b: cmp(a.value if hasattr(a, 'value') else a, b.value if hasattr(b, 'value') else b))
            self.present_wid.changeValues(presents)
        self.host.redraw()

    def removeUser(self, param_nick, show_info=True):
        """Remove a user from the group list"""
        nick = unicode(param_nick) #FIXME: should be done in DBus bridge
        QuickChat.removeUser(self, nick, show_info)
        self.present_wid.deleteValue(nick)
        self.host.redraw()

    def clearHistory(self):
        """Clear the content of this chat."""
        del self.content[:]

    def afterHistoryPrint(self):
        """Refresh or scroll down the focus after the history is printed"""
        if len(self.content):
            self.text_list.focus_position = len(self.content) - 1  # scroll down
        self.host.redraw()

    def printMessage(self, from_jid, msg, profile, timestamp=""):
        assert isinstance(from_jid, JID)
        try:
            jid, nick, mymess = QuickChat.printMessage(self, from_jid, msg, profile, timestamp)
        except TypeError:
            return

        new_text = ChatText(self, timestamp or None, nick, mymess, msg)

        if timestamp and self.content:
            for idx in range(len(self.content) - 1, -1, -1):
                current_text = self.content[idx]
                older = new_text.timestamp < current_text.timestamp
                if older and idx > 0:
                    continue  # the new message is older, we need to insert it upper

                #we discard double messages, to avoid backlog / history conflict
                if ((idx and self.content[idx - 1].message == msg) or
                    (self.content[idx].message == msg) or
                    (idx < len(self.content) - 2 and self.content[idx + 1].message)):
                    return

                self.content.insert(0 if older else idx + 1, new_text)
                break
        else:
            self.content.append(new_text)
        if not timestamp:
            # XXX: do not send notifications for each line of the history being displayed
            # FIXME: this must be changed in the future if the timestamp is passed with
            # all messages and not only with the messages coming from the history.
            self._notify(from_jid, msg)

    def printInfo(self, msg, type_='normal', timestamp=""):
        """Print general info
        @param msg: message to print
        @type_: one of:
            normal: general info like "toto has joined the room"
            me: "/me" information like "/me clenches his fist" ==> "toto clenches his fist"
        """
        _widget = ChatText(self, timestamp or None, None, False, msg, is_info=True)
        self.content.append(_widget)
        self._notify(msg=msg)

    def _notify(self, from_jid="somebody", msg=""):
        """Notify the user of a new message if primitivus doesn't have the focus.
        @param from_jid: contact who wrote to the users
        @param msg: the message that has been received
        """
        if msg == "":
            return
        if self.text_list.get_focus()[1] == len(self.content) - 2:
            #we don't change focus if user is not at the bottom
            #as that mean that he is probably watching discussion history
            self.text_list.focus_position = len(self.content) - 1
        self.host.redraw()
        if not self.host.x_notify.hasFocus():
            if self.type == "one2one":
                self.host.x_notify.sendNotification(_("Primitivus: %s is talking to you") % from_jid)
            elif self.getUserNick().lower() in msg.lower():
                self.host.x_notify.sendNotification(_("Primitivus: %(user)s mentioned you in room '%(room)s'") % {'user': from_jid, 'room': self.target})

    def startGame(self, game_type, referee, players):
        """Configure the chat window to start a game"""
        if game_type=="Tarot":
            self.tarot_wid = CardGame(self, referee, players, self.nick)
            self.__appendGamePanel(self.tarot_wid)

    def getGame(self, game_type):
        """Return class managing the game type"""
        #TODO: check that the game is launched, and manage errors
        if game_type=="Tarot":
            return self.tarot_wid

    #MENU EVENTS#
    def onTarotRequest(self, menu):
        # TODO: move this to plugin_misc_tarot with dynamic menu
        if len(self.occupants) != 4:
            self.host.showPopUp(sat_widgets.Alert(_("Can't start game"), _("You need to be exactly 4 peoples in the room to start a Tarot game"), ok_cb=self.host.removePopUp))
        else:
            self.host.bridge.tarotGameCreate(self.id, list(self.occupants), self.host.profile)

    def onSendFileRequest(self, menu):
        # TODO: move this to core with dynamic menus
        dialog = FileDialog(ok_cb=self.onFileSelected, cancel_cb=self.host.removePopUp)
        self.host.showPopUp(dialog, 80, 80)

    #MISC EVENTS#
    def onFileSelected(self, filepath):
        self.host.removePopUp()
        try:
            filepath = filepath.decode('utf-8') # FIXME: correctly manage unicode
        except UnicodeError:
            log.error("FIXME: filepath with unicode error are not managed yet")
            self.host.showDialog(_(u"File has a unicode error in its name, it's not yet managed by SàT"), title=_("Can't send file"), type_="error")
            return
        #FIXME: check last_resource: what if self.target.resource exists ?
        last_resource = self.host.bridge.getLastResource(unicode(self.target.bare), self.host.profile)
        if last_resource:
            full_jid = JID("%s/%s" % (self.target.bare, last_resource))
        else:
            full_jid = self.target
        progress_id = self.host.bridge.sendFile(full_jid, filepath, {}, self.host.profile)
        self.host.addProgress(progress_id,filepath)
        self.host.showDialog(_(u"You file request has been sent, we are waiting for your contact answer"), title=_("File request sent"))
