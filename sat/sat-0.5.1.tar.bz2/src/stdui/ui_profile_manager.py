#!/usr/bin/python
# -*- coding: utf-8 -*-

# SAT standard user interface for managing contacts
# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014 Jérôme Poisson (goffi@goffi.org)
# Copyright (C) 2013, 2014 Adrien Cossa (souliane@mailoo.org)

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

from sat.core.i18n import D_
from sat.core.constants import Const as C
from sat.tools import xml_tools
from sat.memory.crypto import PasswordHasher
from sat.memory.memory import ProfileSessions
from twisted.internet import defer
from twisted.words.protocols.jabber import jid


class ProfileManager(object):
    """Manage profiles."""

    def __init__(self, host):
        self.host = host
        self.profile_ciphers = {}
        self._sessions = ProfileSessions()
        host.registerCallback(self._authenticateProfile, force_id=C.AUTHENTICATE_PROFILE_ID, with_data=True)
        host.registerCallback(self._changeXMPPPassword, force_id=C.CHANGE_XMPP_PASSWD_ID, with_data=True)
        self.__new_xmpp_passwd_id = host.registerCallback(self._changeXMPPPasswordCb, with_data=True)

    def _authenticateProfile(self, data, profile):
        """Get the data/dialog for connecting a profile

        @param data (dict)
        @param profile: %(doc_profile)s
        @return: deferred dict
        """
        def gotProfileCipher(profile_cipher):
            if self.host.memory.auth_sessions.profileGetUnique(profile):
                # case 1: profile already authenticated
                return {'authenticated_profile': profile, 'caller': data['caller']}
            self.profile_ciphers[profile] = profile_cipher
            if 'profile_password' in data:
                # case 2: password is provided by the caller
                return self._verifyPassword(data, profile)

            def check_empty_password(empty_password_result):
                if 'authenticated_profile' in empty_password_result:
                    # case 3: there's no password for this profile
                    return empty_password_result

                # case 4: prompt the user for a password
                def xmlui_cb(data_, profile):
                    data_['caller'] = data['caller']
                    return self._verifyPassword(data_, profile)

                callback_id = self.host.registerCallback(xmlui_cb, with_data=True, one_shot=True)
                form_ui = xml_tools.XMLUI("form", title=D_('Profile password for %s') % profile, submit_id=callback_id)
                form_ui.addPassword('profile_password', value='')
                return {'xmlui': form_ui.toXml()}

            check_empty_data = {'profile_password': '', 'caller': data['caller']}
            d = self._verifyPassword(check_empty_data, profile)
            return d.addCallback(check_empty_password)

        assert(data['caller'])
        d = self.host.memory.asyncGetStringParamA(C.PROFILE_PASS_PATH[1], C.PROFILE_PASS_PATH[0], profile_key=profile)
        d.addCallback(gotProfileCipher)
        d.addErrback(self.getParamError)
        return d

    def getParamError(self, failure):
        _dialog = xml_tools.XMLUI('popup', title=D_('Error'))
        _dialog.addText(D_("Can't get profile parameter."))
        return {'xmlui': _dialog.toXml()}

    @defer.inlineCallbacks
    def _verifyPassword(self, data, profile):
        """Verify the given password

        @param data (dict)
        @param profile: %(doc_profile)s
        @return: deferred dict
        """
        assert(profile in self.profile_ciphers)
        assert(data['caller'])

        try:
            profile_password = data[xml_tools.formEscape('profile_password')]
        except KeyError:
            profile_password = data['profile_password']  # not received from a user input
        verified = yield PasswordHasher.verify(profile_password, self.profile_ciphers[profile])
        if not verified:
            _dialog = xml_tools.XMLUI('popup', title=D_('Connection error'))
            _dialog.addText(D_("The provided profile password doesn't match."))
            defer.returnValue({'xmlui': _dialog.toXml()})

        yield self.host.memory.newAuthSession(profile_password, profile)
        defer.returnValue({'authenticated_profile': profile, 'caller': data['caller']})

    def _changeXMPPPassword(self, data, profile):
        session_data = self._sessions.profileGetUnique(profile)
        if not session_data:
            server = self.host.memory.getParamA(C.FORCE_SERVER_PARAM, "Connection", profile_key=profile)
            if not server:
                server = jid.parse(self.host.memory.getParamA('JabberID', "Connection", profile_key=profile))[1]
            session_id, session_data = self._sessions.newSession({'count': 0, 'server': server}, profile)
        if session_data['count'] > 2:  # 3 attempts with a new password after the initial try
            self._sessions.profileDelUnique(profile)
            _dialog = xml_tools.XMLUI('popup', title=D_('Connection error'))
            _dialog.addText(D_("Can't connect to %s. Please check your connection details.") % session_data['server'])
            return {'xmlui': _dialog.toXml()}
        session_data['count'] += 1
        counter = ' (%d)' % session_data['count'] if session_data['count'] > 1 else ''
        title = D_('XMPP password for %(profile)s%(counter)s') % {'profile': profile, 'counter': counter}
        form_ui = xml_tools.XMLUI("form", title=title, submit_id=self.__new_xmpp_passwd_id)
        form_ui.addText(D_("Can't connect to %s. Please check your connection details or try with another password.") % session_data['server'])
        form_ui.addPassword('xmpp_password', value='')
        return {'xmlui': form_ui.toXml()}

    def _changeXMPPPasswordCb(self, data, profile):
        xmpp_password = data[xml_tools.formEscape('xmpp_password')]
        d = self.host.memory.setParam("Password", xmpp_password, "Connection", profile_key=profile)
        d.addCallback(lambda dummy: self.host.asyncConnect(profile))
        d.addCallback(lambda dummy: {})
        d.addErrback(lambda dummy: self._changeXMPPPassword({}, profile))
        return d
