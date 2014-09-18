#!/usr/bin/python
# -*- coding: utf-8 -*-

# helper class for making a SAT frontend
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
import sys
from sat.core.log import getLogger
log = getLogger(__name__)
from sat_frontends.tools.jid import JID
from sat_frontends.bridge.DBus import DBusBridgeFrontend
from sat.core import exceptions
from sat_frontends.quick_frontend.quick_utils import escapePrivate, unescapePrivate
from optparse import OptionParser

from sat_frontends.quick_frontend.constants import Const as C


class QuickApp(object):
    """This class contain the main methods needed for the frontend"""

    def __init__(self, single_profile=True):
        self.profiles = {}
        self.single_profile = single_profile
        self.check_options()

        ## bridge ##
        try:
            self.bridge = DBusBridgeFrontend()
        except exceptions.BridgeExceptionNoService:
            print(_(u"Can't connect to SàT backend, are you sure it's launched ?"))
            sys.exit(1)
        except exceptions.BridgeInitError:
            print(_(u"Can't init bridge"))
            sys.exit(1)
        self.registerSignal("connected")
        self.registerSignal("disconnected")
        self.registerSignal("newContact")
        self.registerSignal("newMessage", self._newMessage)
        self.registerSignal("newAlert")
        self.registerSignal("presenceUpdate")
        self.registerSignal("subscribe")
        self.registerSignal("paramUpdate")
        self.registerSignal("contactDeleted")
        self.registerSignal("entityDataUpdated")
        self.registerSignal("askConfirmation")
        self.registerSignal("actionResult")
        self.registerSignal("actionResultExt", self.actionResultHandler)
        self.registerSignal("roomJoined", iface="plugin")
        self.registerSignal("roomLeft", iface="plugin")
        self.registerSignal("roomUserJoined", iface="plugin")
        self.registerSignal("roomUserLeft", iface="plugin")
        self.registerSignal("roomUserChangedNick", iface="plugin")
        self.registerSignal("roomNewSubject", iface="plugin")
        self.registerSignal("tarotGameStarted", iface="plugin")
        self.registerSignal("tarotGameNew", iface="plugin")
        self.registerSignal("tarotGameChooseContrat", iface="plugin")
        self.registerSignal("tarotGameShowCards", iface="plugin")
        self.registerSignal("tarotGameYourTurn", iface="plugin")
        self.registerSignal("tarotGameScore", iface="plugin")
        self.registerSignal("tarotGameCardsPlayed", iface="plugin")
        self.registerSignal("tarotGameInvalidCards", iface="plugin")
        self.registerSignal("quizGameStarted", iface="plugin")
        self.registerSignal("quizGameNew", iface="plugin")
        self.registerSignal("quizGameQuestion", iface="plugin")
        self.registerSignal("quizGamePlayerBuzzed", iface="plugin")
        self.registerSignal("quizGamePlayerSays", iface="plugin")
        self.registerSignal("quizGameAnswerResult", iface="plugin")
        self.registerSignal("quizGameTimerExpired", iface="plugin")
        self.registerSignal("quizGameTimerRestarted", iface="plugin")
        self.registerSignal("chatStateReceived", iface="plugin")

        self.current_action_ids = set()
        self.current_action_ids_cb = {}
        self.media_dir = self.bridge.getConfig('', 'media_dir')

    def registerSignal(self, functionName, handler=None, iface="core", with_profile=True):
        """Register a handler for a signal

        @param functionName (str): name of the signal to handle
        @param handler (instancemethod): method to call when the signal arrive, None for calling an automatically named handler (functionName + 'Handler')
        @param iface (str): interface of the bridge to use ('core' or 'plugin')
        @param with_profile (boolean): True if the signal concerns a specific profile, in that case the profile name has to be passed by the caller
        """
        if handler is None:
            handler = getattr(self, "%s%s" % (functionName, 'Handler'))
        if not with_profile:
            self.bridge.register(functionName, handler, iface)
            return

        def signalReceived(*args, **kwargs):
            profile = kwargs.get('profile')
            if profile is None:
                if not args:
                    raise exceptions.ProfileNotSetError
                profile = args[-1]
            if profile is not None and not self.check_profile(profile):
                return  # we ignore signal for profiles we don't manage
            handler(*args, **kwargs)
        self.bridge.register(functionName, signalReceived, iface)

    def check_profile(self, profile):
        """Tell if the profile is currently followed by the application"""
        return profile in self.profiles.keys()

    def postInit(self):
        """Must be called after initialization is done, do all automatic task (auto plug profile)"""
        if self.options.profile:
            if not self.bridge.getProfileName(self.options.profile):
                log.error(_("Trying to plug an unknown profile (%s)" % self.options.profile))
            else:
                self.plug_profile(self.options.profile)

    def check_options(self):
        """Check command line options"""
        usage = _("""
        %prog [options]

        %prog --help for options list
        """)
        parser = OptionParser(usage=usage)

        parser.add_option("-p", "--profile", help=_("Select the profile to use"))

        (self.options, args) = parser.parse_args()
        if self.options.profile:
            self.options.profile = self.options.profile.decode('utf-8')
        return args

    def _getParamError(self, ignore):
        log.error(_("Can't get profile parameter"))

    def plug_profile(self, profile_key='@DEFAULT@'):
        """Tell application which profile must be used"""
        if self.single_profile and self.profiles:
            log.error(_('There is already one profile plugged (we are in single profile mode) !'))
            return
        profile = self.bridge.getProfileName(profile_key)
        if not profile:
            log.error(_("The profile asked doesn't exist"))
            return
        if profile in self.profiles:
            log.warning(_("The profile is already plugged"))
            return
        self.profiles[profile] = {}
        if self.single_profile:
            self.profile = profile # FIXME: must be refactored (multi profiles are not managed correclty)
        raw_menus = self.bridge.getMenus("", C.NO_SECURITY_LIMIT )
        menus = self.profiles[profile]['menus'] = {}
        for raw_menu in raw_menus:
            id_, type_, path, path_i18n  = raw_menu
            menus_data = menus.setdefault(type_, [])
            menus_data.append((id_, path, path_i18n))
        self.launchAction(C.AUTHENTICATE_PROFILE_ID, {'caller': 'plug_profile'}, profile_key=profile)

    def plug_profile_1(self, profile):
        ###now we get the essential params###
        self.bridge.asyncGetParamA("JabberID", "Connection", profile_key=profile,
                                   callback=lambda _jid: self.plug_profile_2(_jid, profile), errback=self._getParamError)

    def plug_profile_2(self, _jid, profile):
        self.profiles[profile]['whoami'] = JID(_jid)
        self.bridge.asyncGetParamA("autoconnect", "Connection", profile_key=profile,
                                   callback=lambda value: self.plug_profile_3(value == "true", profile), errback=self._getParamError)

    def plug_profile_3(self, autoconnect, profile):
        self.bridge.asyncGetParamA("Watched", "Misc", profile_key=profile,
                                   callback=lambda watched: self.plug_profile_4(watched, autoconnect, profile), errback=self._getParamError)

    def asyncConnect(self, profile, callback=None, errback=None):
        if not callback:
            callback = lambda dummy: None
        if not errback:
            def errback(failure):
                log.error(_(u"Can't connect profile [%s]") % failure)
                if failure.module.startswith('twisted.words.protocols.jabber') and failure.condition == "not-authorized":
                    self.launchAction(C.CHANGE_XMPP_PASSWD_ID, {}, profile_key=profile)
                else:
                    self.showDialog(failure.message, failure.fullname, 'error')
        self.bridge.asyncConnect(profile, callback=callback, errback=errback)

    def plug_profile_4(self, watched, autoconnect, profile):
        if autoconnect and not self.bridge.isConnected(profile):
            #Does the user want autoconnection ?
            self.asyncConnect(profile, callback=lambda dummy: self.plug_profile_5(watched, autoconnect, profile))
        else:
            self.plug_profile_5(watched, autoconnect, profile)

    def plug_profile_5(self, watched, autoconnect, profile):
        self.profiles[profile]['watched'] = watched.split()  # TODO: put this in a plugin

        ## misc ##
        self.profiles[profile]['onlineContact'] = set()  # FIXME: temporary

        #TODO: manage multi-profiles here
        if not self.bridge.isConnected(profile):
            self.setStatusOnline(False)
        else:
            self.setStatusOnline(True)

            ### now we fill the contact list ###
            for contact in self.bridge.getContacts(profile):
                self.newContactHandler(*contact, profile=profile)

            presences = self.bridge.getPresenceStatuses(profile)
            for contact in presences:
                for res in presences[contact]:
                    jabber_id = contact + ('/' + res if res else '')
                    show = presences[contact][res][0]
                    priority = presences[contact][res][1]
                    statuses = presences[contact][res][2]
                    self.presenceUpdateHandler(jabber_id, show, priority, statuses, profile)
                data = self.bridge.getEntityData(contact, ['avatar', 'nick'], profile)
                for key in ('avatar', 'nick'):
                    if key in data:
                        self.entityDataUpdatedHandler(contact, key, data[key], profile)

            #The waiting subscription requests
            waitingSub = self.bridge.getWaitingSub(profile)
            for sub in waitingSub:
                self.subscribeHandler(waitingSub[sub], sub, profile)

            #Now we open the MUC window where we already are:
            for room_args in self.bridge.getRoomsJoined(profile):
                self.roomJoinedHandler(*room_args, profile=profile)

            for subject_args in self.bridge.getRoomsSubjects(profile):
                self.roomNewSubjectHandler(*subject_args, profile=profile)

            #Finaly, we get the waiting confirmation requests
            for confirm_id, confirm_type, data in self.bridge.getWaitingConf(profile):
                self.askConfirmationHandler(confirm_id, confirm_type, data, profile)

    def unplug_profile(self, profile):
        """Tell the application to not follow anymore the profile"""
        if not profile in self.profiles:
            log.warning(_("This profile is not plugged"))
            return
        self.profiles.remove(profile)

    def clear_profile(self):
        self.profiles.clear()

    def connectedHandler(self, profile):
        """called when the connection is made"""
        log.debug(_("Connected"))
        self.setStatusOnline(True)

    def disconnectedHandler(self, profile):
        """called when the connection is closed"""
        log.debug(_("Disconnected"))
        self.contact_list.clearContacts()
        self.setStatusOnline(False)

    def newContactHandler(self, JabberId, attributes, groups, profile):
        entity = JID(JabberId)
        _groups = list(groups)
        self.contact_list.replace(entity, _groups, attributes)

    def _newMessage(self, from_jid_s, msg, type_, to_jid_s, extra, profile):
        """newMessage premanagement: a dirty hack to manage private messages

        if a private MUC message is detected, from_jid or to_jid is prefixed and resource is escaped
        """
        # FIXME: must be refactored for 0.6
        from_jid = JID(from_jid_s)
        to_jid = JID(to_jid_s)

        from_me = from_jid.bare == self.profiles[profile]['whoami'].bare
        win = to_jid if from_me else from_jid

        if ((type_ != "groupchat" and self.contact_list.getSpecial(win) == "MUC") and
            (type_ != C.MESS_TYPE_INFO or (type_ == C.MESS_TYPE_INFO and win.resource))):
            #we have a private message in a MUC room
            #XXX: normaly we use bare jid as key, here we need the full jid
            #     so we cheat by replacing the "/" before the resource by
            #     a "@", so the jid is invalid,
            new_jid = escapePrivate(win)
            if from_me:
                to_jid = new_jid
            else:
                from_jid = new_jid
            if new_jid not in self.contact_list:
                self.contact_list.add(new_jid, [C.GROUP_NOT_IN_ROSTER])

        self.newMessageHandler(from_jid, to_jid, msg, type_, extra, profile)

    def newMessageHandler(self, from_jid, to_jid, msg, type_, extra, profile):
        from_me = from_jid.bare == self.profiles[profile]['whoami'].bare
        win = to_jid if from_me else from_jid

        self.current_action_ids = set()
        self.current_action_ids_cb = {}

        timestamp = extra.get('archive')
        if type_ == C.MESS_TYPE_INFO:
            self.chat_wins[win.bare].printInfo( msg, timestamp = float(timestamp) if timestamp else '')
        else:
            self.chat_wins[win.bare].printMessage(from_jid, msg, profile, float(timestamp) if timestamp else '')

    def sendMessage(self, to_jid, message, subject='', mess_type="auto", extra={}, callback=None, errback=None, profile_key="@NONE@"):
        if to_jid.startswith(C.PRIVATE_PREFIX):
            to_jid = unescapePrivate(to_jid)
            mess_type = "chat"
        if callback is None:
            callback = lambda: None
        if errback is None:
            errback = lambda failure: self.showDialog(failure.fullname, failure.message, "error")
        self.bridge.sendMessage(to_jid, message, subject, mess_type, extra, profile_key, callback=callback, errback=errback)

    def newAlertHandler(self, msg, title, alert_type, profile):
        assert alert_type in ['INFO', 'ERROR']
        self.showDialog(unicode(msg), unicode(title), alert_type.lower())

    def setStatusOnline(self, online=True, show="", statuses={}):
        raise NotImplementedError

    def presenceUpdateHandler(self, jabber_id, show, priority, statuses, profile):

        log.debug(_("presence update for %(jid)s (show=%(show)s, priority=%(priority)s, statuses=%(statuses)s) [profile:%(profile)s]")
              % {'jid': jabber_id, 'show': show, 'priority': priority, 'statuses': statuses, 'profile': profile})
        from_jid = JID(jabber_id)

        if from_jid == self.profiles[profile]['whoami']:
            if show == "unavailable":
                self.setStatusOnline(False)
            else:
                self.setStatusOnline(True, show, statuses)
            return

        presences = self.profiles[profile].setdefault('presences', {})

        if show != 'unavailable':

            #FIXME: must be moved in a plugin
            if from_jid.bare in self.profiles[profile].get('watched',[]) and not from_jid.bare in self.profiles[profile]['onlineContact']:
                self.showAlert(_("Watched jid [%s] is connected !") % from_jid.bare)

            presences[jabber_id] = {'show': show, 'priority': priority, 'statuses': statuses}
            self.profiles[profile].setdefault('onlineContact',set()).add(from_jid)  # FIXME onlineContact is useless with CM, must be removed

            #TODO: vcard data (avatar)

        if show == "unavailable" and from_jid in self.profiles[profile].get('onlineContact',set()):
            try:
                del presences[jabber_id]
            except KeyError:
                pass
            self.profiles[profile]['onlineContact'].remove(from_jid)

        # check if the contact is connected with another resource, use the one with highest priority
        jids = [jid for jid in presences if JID(jid).bare == from_jid.bare]
        if jids:
            max_jid = max(jids, key=lambda jid: presences[jid]['priority'])
            data = presences[max_jid]
            max_priority = data['priority']
            if show == "unavailable":  # do not check the priority here, because 'unavailable' has a dummy one
                from_jid = JID(max_jid)
                show, priority, statuses = data['show'], data['priority'], data['statuses']
        if not jids or priority >= max_priority:
            # case 1: not jids means all resources are disconnected, send the 'unavailable' presence
            # case 2: update (or confirm) with the values of the resource which takes precedence
            self.contact_list.updatePresence(from_jid, show, priority, statuses)

    def roomJoinedHandler(self, room_jid, room_nicks, user_nick, profile):
        """Called when a MUC room is joined"""
        log.debug(_("Room [%(room_jid)s] joined by %(profile)s, users presents:%(users)s") % {'room_jid': room_jid, 'profile': profile, 'users': room_nicks})
        self.chat_wins[room_jid].setUserNick(user_nick)
        self.chat_wins[room_jid].setType("group")
        self.chat_wins[room_jid].id = room_jid
        self.chat_wins[room_jid].setPresents(list(set([user_nick] + room_nicks)))
        self.contact_list.setSpecial(JID(room_jid), "MUC", show=True)

    def roomLeftHandler(self, room_jid_s, profile):
        """Called when a MUC room is left"""
        log.debug(_("Room [%(room_jid)s] left by %(profile)s") % {'room_jid': room_jid_s, 'profile': profile})
        del self.chat_wins[room_jid_s]
        self.contact_list.remove(JID(room_jid_s))

    def roomUserJoinedHandler(self, room_jid, user_nick, user_data, profile):
        """Called when an user joined a MUC room"""
        if room_jid in self.chat_wins:
            self.chat_wins[room_jid].replaceUser(user_nick)
            log.debug(_("user [%(user_nick)s] joined room [%(room_jid)s]") % {'user_nick': user_nick, 'room_jid': room_jid})

    def roomUserLeftHandler(self, room_jid, user_nick, user_data, profile):
        """Called when an user joined a MUC room"""
        if room_jid in self.chat_wins:
            self.chat_wins[room_jid].removeUser(user_nick)
            log.debug(_("user [%(user_nick)s] left room [%(room_jid)s]") % {'user_nick': user_nick, 'room_jid': room_jid})

    def roomUserChangedNickHandler(self, room_jid, old_nick, new_nick, profile):
        """Called when an user joined a MUC room"""
        if room_jid in self.chat_wins:
            self.chat_wins[room_jid].changeUserNick(old_nick, new_nick)
            log.debug(_("user [%(old_nick)s] is now known as [%(new_nick)s] in room [%(room_jid)s]") % {'old_nick': old_nick, 'new_nick': new_nick, 'room_jid': room_jid})

    def roomNewSubjectHandler(self, room_jid, subject, profile):
        """Called when subject of MUC room change"""
        if room_jid in self.chat_wins:
            self.chat_wins[room_jid].setSubject(subject)
            log.debug(_("new subject for room [%(room_jid)s]: %(subject)s") % {'room_jid': room_jid, "subject": subject})

    def tarotGameStartedHandler(self, room_jid, referee, players, profile):
        log.debug(_("Tarot Game Started \o/"))
        if room_jid in self.chat_wins:
            self.chat_wins[room_jid].startGame("Tarot", referee, players)
            log.debug(_("new Tarot game started by [%(referee)s] in room [%(room_jid)s] with %(players)s") % {'referee': referee, 'room_jid': room_jid, 'players': [str(player) for player in players]})

    def tarotGameNewHandler(self, room_jid, hand, profile):
        log.debug(_("New Tarot Game"))
        if room_jid in self.chat_wins:
            self.chat_wins[room_jid].getGame("Tarot").newGame(hand)

    def tarotGameChooseContratHandler(self, room_jid, xml_data, profile):
        """Called when the player has to select his contrat"""
        log.debug(_("Tarot: need to select a contrat"))
        if room_jid in self.chat_wins:
            self.chat_wins[room_jid].getGame("Tarot").chooseContrat(xml_data)

    def tarotGameShowCardsHandler(self, room_jid, game_stage, cards, data, profile):
        log.debug(_("Show cards"))
        if room_jid in self.chat_wins:
            self.chat_wins[room_jid].getGame("Tarot").showCards(game_stage, cards, data)

    def tarotGameYourTurnHandler(self, room_jid, profile):
        log.debug(_("My turn to play"))
        if room_jid in self.chat_wins:
            self.chat_wins[room_jid].getGame("Tarot").myTurn()

    def tarotGameScoreHandler(self, room_jid, xml_data, winners, loosers, profile):
        """Called when the game is finished and the score are updated"""
        log.debug(_("Tarot: score received"))
        if room_jid in self.chat_wins:
            self.chat_wins[room_jid].getGame("Tarot").showScores(xml_data, winners, loosers)

    def tarotGameCardsPlayedHandler(self, room_jid, player, cards, profile):
        log.debug(_("Card(s) played (%(player)s): %(cards)s") % {"player": player, "cards": cards})
        if room_jid in self.chat_wins:
            self.chat_wins[room_jid].getGame("Tarot").cardsPlayed(player, cards)

    def tarotGameInvalidCardsHandler(self, room_jid, phase, played_cards, invalid_cards, profile):
        log.debug(_("Cards played are not valid: %s") % invalid_cards)
        if room_jid in self.chat_wins:
            self.chat_wins[room_jid].getGame("Tarot").invalidCards(phase, played_cards, invalid_cards)

    def quizGameStartedHandler(self, room_jid, referee, players, profile):
        log.debug(_("Quiz Game Started \o/"))
        if room_jid in self.chat_wins:
            self.chat_wins[room_jid].startGame("Quiz", referee, players)
            log.debug(_("new Quiz game started by [%(referee)s] in room [%(room_jid)s] with %(players)s") % {'referee': referee, 'room_jid': room_jid, 'players': [str(player) for player in players]})

    def quizGameNewHandler(self, room_jid, data, profile):
        log.debug(_("New Quiz Game"))
        if room_jid in self.chat_wins:
            self.chat_wins[room_jid].getGame("Quiz").quizGameNewHandler(data)

    def quizGameQuestionHandler(self, room_jid, question_id, question, timer, profile):
        """Called when a new question is asked"""
        log.debug(_(u"Quiz: new question: %s") % question)
        if room_jid in self.chat_wins:
            self.chat_wins[room_jid].getGame("Quiz").quizGameQuestionHandler(question_id, question, timer)

    def quizGamePlayerBuzzedHandler(self, room_jid, player, pause, profile):
        """Called when a player pushed the buzzer"""
        if room_jid in self.chat_wins:
            self.chat_wins[room_jid].getGame("Quiz").quizGamePlayerBuzzedHandler(player, pause)

    def quizGamePlayerSaysHandler(self, room_jid, player, text, delay, profile):
        """Called when a player say something"""
        if room_jid in self.chat_wins:
            self.chat_wins[room_jid].getGame("Quiz").quizGamePlayerSaysHandler(player, text, delay)

    def quizGameAnswerResultHandler(self, room_jid, player, good_answer, score, profile):
        """Called when a player say something"""
        if room_jid in self.chat_wins:
            self.chat_wins[room_jid].getGame("Quiz").quizGameAnswerResultHandler(player, good_answer, score)

    def quizGameTimerExpiredHandler(self, room_jid, profile):
        """Called when nobody answered the question in time"""
        if room_jid in self.chat_wins:
            self.chat_wins[room_jid].getGame("Quiz").quizGameTimerExpiredHandler()

    def quizGameTimerRestartedHandler(self, room_jid, time_left, profile):
        """Called when the question is not answered, and we still have time"""
        if room_jid in self.chat_wins:
            self.chat_wins[room_jid].getGame("Quiz").quizGameTimerRestartedHandler(time_left)

    def chatStateReceivedHandler(self, from_jid_s, state, profile):
        """Callback when a new chat state is received.
        @param from_jid_s: JID of the contact who sent his state, or '@ALL@'
        @param state: new state (string)
        @profile: current profile
        """

        if from_jid_s == '@ALL@':
            target = '@ALL@'
            nick = C.ALL_OCCUPANTS
        else:
            from_jid = JID(from_jid_s)
            target = from_jid.bare
            nick = from_jid.resource

        for bare in self.chat_wins.keys():
            if target == '@ALL' or target == bare:
                chat_win = self.chat_wins[bare]
                if chat_win.type == 'one2one':
                    chat_win.updateChatState(state)
                elif chat_win.type == 'group':
                    chat_win.updateChatState(state, nick=nick)

    def _subscribe_cb(self, answer, data):
        entity, profile = data
        if answer:
            self.bridge.subscription("subscribed", entity.bare, profile_key=profile)
        else:
            self.bridge.subscription("unsubscribed", entity.bare, profile_key=profile)

    def subscribeHandler(self, type, raw_jid, profile):
        """Called when a subsciption management signal is received"""
        entity = JID(raw_jid)
        if type == "subscribed":
            # this is a subscription confirmation, we just have to inform user
            self.showDialog(_("The contact %s has accepted your subscription") % entity.bare, _('Subscription confirmation'))
        elif type == "unsubscribed":
            # this is a subscription refusal, we just have to inform user
            self.showDialog(_("The contact %s has refused your subscription") % entity.bare, _('Subscription refusal'), 'error')
        elif type == "subscribe":
            # this is a subscriptionn request, we have to ask for user confirmation
            self.showDialog(_("The contact %s wants to subscribe to your presence.\nDo you accept ?") % entity.bare, _('Subscription confirmation'), 'yes/no', answer_cb=self._subscribe_cb, answer_data=(entity, profile))

    def showDialog(self, message, title, type="info", answer_cb=None):
        raise NotImplementedError

    def showAlert(self, message):
        pass  #FIXME

    def paramUpdateHandler(self, name, value, namespace, profile):
        log.debug(_("param update: [%(namespace)s] %(name)s = %(value)s") % {'namespace': namespace, 'name': name, 'value': value})
        if (namespace, name) == ("Connection", "JabberID"):
            log.debug(_("Changing JID to %s") % value)
            self.profiles[profile]['whoami'] = JID(value)
        elif (namespace, name) == ("Misc", "Watched"):
            self.profiles[profile]['watched'] = value.split()

    def contactDeletedHandler(self, jid, profile):
        target = JID(jid)
        self.contact_list.remove(target)
        try:
            self.profiles[profile]['onlineContact'].remove(target.bare)
        except KeyError:
            pass

    def entityDataUpdatedHandler(self, jid_str, key, value, profile):
        jid = JID(jid_str)
        if key == "nick":
            if jid in self.contact_list:
                self.contact_list.setCache(jid, 'nick', value)
                self.contact_list.replace(jid)
        elif key == "avatar":
            if jid in self.contact_list:
                filename = self.bridge.getAvatarFile(value)
                self.contact_list.setCache(jid, 'avatar', filename)
                self.contact_list.replace(jid)

    def askConfirmationHandler(self, confirm_id, confirm_type, data, profile):
        raise NotImplementedError

    def actionResultHandler(self, type, id, data, profile):
        raise NotImplementedError

    def launchAction(self, callback_id, data=None, profile_key="@NONE@"):
        """ Launch a dynamic action
        @param callback_id: id of the action to launch
        @param data: data needed only for certain actions
        @param profile_key: %(doc_profile_key)s

        """
        raise NotImplementedError

    def onExit(self):
        """Must be called when the frontend is terminating"""
        #TODO: mange multi-profile here
        try:
            if self.bridge.isConnected(self.profile):
                if self.bridge.getParamA("autodisconnect", "Connection", profile_key=self.profile) == "true":
                    #The user wants autodisconnection
                    self.bridge.disconnect(self.profile)
        except:
            pass
