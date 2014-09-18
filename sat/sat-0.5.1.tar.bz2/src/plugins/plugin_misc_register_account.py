#!/usr/bin/python
# -*- coding: utf-8 -*-

# SàT plugin for registering a new XMPP account
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

from sat.core.i18n import _, D_
from sat.core.log import getLogger
log = getLogger(__name__)
from sat.core.constants import Const as C
from twisted.words.protocols.jabber import jid, xmlstream
from sat.core import xmpp
from sat.memory.memory import Sessions
from twisted.internet import reactor, defer
from sat.tools import xml_tools
from sat.tools.xml_tools import SAT_FORM_PREFIX, SAT_PARAM_SEPARATOR


PLUGIN_INFO = {
    "name": "Register Account Plugin",
    "import_name": "REGISTER-ACCOUNT",
    "type": "MISC",
    "protocols": [],
    "dependencies": [],
    "recommendations": [],
    "main": "RegisterAccount",
    "handler": "no",
    "description": _(u"""Register XMPP account""")
}


class RegisterAccount(object):

    def __init__(self, host):
        log.info(_(u"Plugin Register Account initialization"))
        self.host = host
        self._sessions = Sessions()
        host.registerCallback(self.registerNewAccountCB, with_data=True, force_id="registerNewAccount")
        self.__register_account_id = host.registerCallback(self._registerConfirmation, with_data=True)

    def registerNewAccountCB(self, data, profile):
        """Called when the use click on the "New account" button."""
        session_data = {}
        for param in ('JabberID', 'Password', C.FORCE_PORT_PARAM, C.FORCE_SERVER_PARAM):
            try:
                session_data[param] = data["%s%s%s%s" % (SAT_FORM_PREFIX, "Connection", SAT_PARAM_SEPARATOR, param)]
            except KeyError:
                if param in (C.FORCE_PORT_PARAM, C.FORCE_SERVER_PARAM):
                    session_data[param] = ''

        for param in ('JabberID', 'Password'):
            if not session_data[param]:
                form_ui = xml_tools.XMLUI("popup", title=D_("Missing values"))
                form_ui.addText(D_("No user JID or password given: can't register new account."))
                return  {'xmlui': form_ui.toXml()}

        session_data['user'], host, resource = jid.parse(session_data['JabberID'])
        session_data['server'] = session_data[C.FORCE_SERVER_PARAM] or host
        session_id, dummy = self._sessions.newSession(session_data, profile)
        form_ui = xml_tools.XMLUI("form", title=D_("Register new account"), submit_id=self.__register_account_id, session_id=session_id)
        form_ui.addText(D_("Do you want to register a new XMPP account [%(user)s] on server %(server)s ?") % {'user': session_data['user'], 'server': session_data['server']})
        return  {'xmlui': form_ui.toXml()}

    def _registerConfirmation(self, data, profile):
        """Save the related parameters and proceed the registration."""
        session_data = self._sessions.profileGet(data['session_id'], profile)

        self.host.memory.setParam("JabberID", session_data["JabberID"], "Connection", profile_key=profile)
        self.host.memory.setParam("Password", session_data["Password"], "Connection", profile_key=profile)
        self.host.memory.setParam(C.FORCE_SERVER_PARAM, session_data[C.FORCE_SERVER_PARAM], "Connection", profile_key=profile)
        self.host.memory.setParam(C.FORCE_PORT_PARAM, session_data[C.FORCE_PORT_PARAM], "Connection", profile_key=profile)

        d = self._registerNewAccount(session_data['user'], session_data["Password"], None, session_data['server'], profile_key=profile)
        del self._sessions[data['session_id']]
        return d

    def _registerNewAccount(self, user, password, email, host, port=C.XMPP_C2S_PORT, profile_key=C.PROF_KEY_NONE):
        """Connect to a server and create a new account using in-band registration.
        @param user: login of the account
        @param password: password of the account
        @param email: email of the account
        @param host: host of the server to register to
        @param port: port of the server to register to
        @param profile_key: %(doc_profile_key)s
        """
        profile = self.host.memory.getProfileName(profile_key)

        d = defer.Deferred()
        serverRegistrer = xmlstream.XmlStreamFactory(xmpp.RegisteringAuthenticator(self, host, user, password, email, d, profile))
        connector = reactor.connectTCP(host, port or C.XMPP_C2S_PORT, serverRegistrer)
        serverRegistrer.clientConnectionLost = lambda conn, reason: connector.disconnect()

        def cb(dummy):
            xmlui = xml_tools.XMLUI("popup", title=D_("Confirmation"))
            xmlui.addText(D_("Registration successful."))
            return ({'xmlui': xmlui.toXml()})

        def eb(failure):
            xmlui = xml_tools.XMLUI("popup", title=D_("Failure"))
            xmlui.addText(D_("Registration failed: %s") % failure.getErrorMessage())
            try:
                if failure.value.condition == 'conflict':
                    xmlui.addText(D_("Username already exists, please choose an other one."))
            except AttributeError:
                pass
            return ({'xmlui': xmlui.toXml()})

        d.addCallbacks(cb, eb)
        return d
