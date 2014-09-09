#!/usr/bin/python
# -*- coding: utf-8 -*-

# SAT plugin for managing xep-0115
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
from twisted.internet import defer
from zope.interface import implements
from wokkel import disco, iwokkel

try:
    from twisted.words.protocols.xmlstream import XMPPHandler
except ImportError:
    from wokkel.subprotocols import XMPPHandler

PRESENCE = '/presence'
NS_ENTITY_CAPABILITY = 'http://jabber.org/protocol/caps'
NS_CAPS_OPTIMIZE = 'http://jabber.org/protocol/caps#optimize'
CAPABILITY_UPDATE = PRESENCE + '/c[@xmlns="' + NS_ENTITY_CAPABILITY + '"]'

PLUGIN_INFO = {
    "name": "XEP 0115 Plugin",
    "import_name": "XEP-0115",
    "type": "XEP",
    "protocols": ["XEP-0115"],
    "dependencies": [],
    "main": "XEP_0115",
    "handler": "yes",
    "description": _("""Implementation of entity capabilities""")
}


class XEP_0115(object):
    cap_hash = None  # capabilities hash is class variable as it is common to all profiles

    def __init__(self, host):
        log.info(_("Plugin XEP_0115 initialization"))
        self.host = host
        host.trigger.add("Disco handled", self._checkHash)
        host.trigger.add("Presence send", self._presenceTrigger)

    def getHandler(self, profile):
        return XEP_0115_handler(self, profile)

    def _checkHash(self, disco_d, profile):
        client = self.host.getClient(profile)
        client.caps_optimize = None

        if XEP_0115.cap_hash is None:
            disco_d.addCallback(lambda dummy: self.host.hasFeature(NS_CAPS_OPTIMIZE, profile_key=profile))
            def updateOptimize(optimize):
                client.caps_optimize = optimize
                if optimize:
                    log.info(_("Caps optimisation enabled"))
                    client.caps_sent = False
                else:
                    log.warning(_("Caps optimisation not available"))
            disco_d.addCallback(updateOptimize)
            disco_d.addCallback(lambda dummy: self.recalculateHash(profile))
        return True

    def _presenceTrigger(self, client, obj):
        if XEP_0115.cap_hash is not None:
            if client.caps_optimize:
                if client.caps_sent:
                    return True
                client.caps_sent = True
            obj.addChild(XEP_0115.c_elt)
        return True

    @defer.inlineCallbacks
    def recalculateHash(self, profile):
        client = self.host.getClient(profile)
        _infos = yield client.discoHandler.info(client.jid, client.jid, '')
        disco_infos = disco.DiscoInfo()
        for item in _infos:
            disco_infos.append(item)
        cap_hash = self.host.memory.disco.generateHash(disco_infos)
        log.info("Our capability hash has been generated: [%s]" % cap_hash)
        log.debug("Generating capability domish.Element")
        c_elt = domish.Element((NS_ENTITY_CAPABILITY, 'c'))
        c_elt['hash'] = 'sha-1'
        c_elt['node'] = C.APP_URL
        c_elt['ver'] = cap_hash
        XEP_0115.cap_hash = cap_hash
        XEP_0115.c_elt = c_elt
        if client.caps_optimize:
            client.caps_sent = False
        if cap_hash not in self.host.memory.disco.hashes:
            self.host.memory.disco.hashes[cap_hash] = disco_infos
            self.host.memory.updateEntityData(client.jid, C.ENTITY_CAP_HASH, cap_hash, profile)


class XEP_0115_handler(XMPPHandler):
    implements(iwokkel.IDisco)

    def __init__(self, plugin_parent, profile):
        self.plugin_parent = plugin_parent
        self.host = plugin_parent.host
        self.profile = profile

    def connectionInitialized(self):
        self.xmlstream.addObserver(CAPABILITY_UPDATE, self.update)

    def getDiscoInfo(self, requestor, target, nodeIdentifier=''):
        return [disco.DiscoFeature(NS_ENTITY_CAPABILITY), disco.DiscoFeature(NS_CAPS_OPTIMIZE)]

    def getDiscoItems(self, requestor, target, nodeIdentifier=''):
        return []

    @defer.inlineCallbacks
    def update(self, presence):
        """
        Manage the capabilities of the entity

        Check if we know the version of this capatilities and get the capibilities if necessary
        """
        from_jid = jid.JID(presence['from'])
        c_elem = presence.elements(NS_ENTITY_CAPABILITY, 'c').next()
        try:
            c_ver = c_elem['ver']
            c_hash = c_elem['hash']
            c_node = c_elem['node']
        except KeyError:
            log.warning(_('Received invalid capabilities tag'))
            return

        if c_ver in self.host.memory.disco.hashes:
            # we already know the hash, we update the jid entity
            log.debug ("hash [%(hash)s] already in cache, updating entity [%(jid)s]" % {'hash': c_ver, 'jid': from_jid.full()})
            self.host.memory.updateEntityData(from_jid, C.ENTITY_CAP_HASH, c_ver, self.profile)
            return

        yield self.host.getDiscoInfos(from_jid, self.profile)
        if c_hash != 'sha-1':
            #unknown hash method
            log.warning(_('Unknown hash method for entity capabilities: [%(hash_method)s] (entity: %(jid)s, node: %(node)s)') % {'hash_method':c_hash, 'jid': from_jid, 'node': c_node})
        computed_hash = self.host.memory.getEntityDatum(from_jid, C.ENTITY_CAP_HASH, self.profile)
        if computed_hash != c_ver:
            log.warning(_('Computed hash differ from given hash:\ngiven: [%(given_hash)s]\ncomputed: [%(computed_hash)s]\n(entity: %(jid)s, node: %(node)s)') % {'given_hash':c_ver, 'computed_hash': computed_hash, 'jid': from_jid, 'node': c_node})

        # TODO: me must manage the full algorithm described at XEP-0115 #5.4 part 3
