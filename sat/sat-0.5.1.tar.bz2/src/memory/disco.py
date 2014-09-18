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

from sat.core.i18n import _
from sat.core import exceptions
from sat.core.log import getLogger
log = getLogger(__name__)
from twisted.words.protocols.jabber import jid
from twisted.words.protocols.jabber.error import StanzaError
from twisted.internet import defer
from twisted.internet import reactor
from sat.core.constants import Const as C
from wokkel import disco
from base64 import b64encode
from hashlib import sha1


PRESENCE = '/presence'
NS_ENTITY_CAPABILITY = 'http://jabber.org/protocol/caps'
CAPABILITY_UPDATE = PRESENCE + '/c[@xmlns="' + NS_ENTITY_CAPABILITY + '"]'
TIMEOUT = 15

class HashGenerationError(Exception):
    pass


class ByteIdentity(object):
    """This class manage identity as bytes (needed for i;octet sort), it is used for the hash generation"""

    def __init__(self, identity, lang=None):
        assert isinstance(identity, disco.DiscoIdentity)
        self.category = identity.category.encode('utf-8')
        self.idType = identity.type.encode('utf-8')
        self.name = identity.name.encode('utf-8') if identity.name else ''
        self.lang = lang.encode('utf-8') if lang is not None else ''

    def __str__(self):
        return "%s/%s/%s/%s" % (self.category, self.idType, self.lang, self.name)


class Discovery(object):
    """ Manage capabilities of entities """

    def __init__(self, host):
        self.host = host
        self.hashes = {} # key: capability hash, value: disco features/identities
        # TODO: save hashes in databse, remove legacy hashes

    @defer.inlineCallbacks
    def hasFeature(self, feature, jid_=None, profile_key=C.PROF_KEY_NONE):
        """Tell if an entity has the required feature

        @param feature: feature namespace
        @param jid_: jid of the target, or None for profile's server
        @param profile_key: %(doc_profile_key)s
        @return: a Deferred which fire a boolean (True if feature is available)
        """
        disco_infos = yield self.getInfos(jid_, profile_key)
        defer.returnValue(feature in disco_infos.features)

    @defer.inlineCallbacks
    def checkFeature(self, feature, jid_=None, profile_key=C.PROF_KEY_NONE):
        """Like hasFeature, but raise an exception is feature is not Found

        @param feature: feature namespace
        @param jid_: jid of the target, or None for profile's server
        @param profile_key: %(doc_profile_key)s
        @return: None if feature is found

        @raise: exceptions.FeatureNotFound
        """
        disco_infos = yield self.getInfos(jid_, profile_key)
        if not feature in disco_infos.features:
            raise exceptions.FeatureNotFound
        defer.returnValue(feature in disco_infos)

    def getInfos(self, jid_=None, profile_key=C.PROF_KEY_NONE):
        """get disco infos from jid_, filling capability hash if needed

        @param jid_: jid of the target, or None for profile's server
        @param profile_key: %(doc_profile_key)s
        @return: a Deferred which fire disco.DiscoInfo
        """
        client = self.host.getClient(profile_key)
        if jid_ is None:
            jid_ = jid.JID(client.jid.host)
        try:
            cap_hash = self.host.memory.getEntityData(jid_, [C.ENTITY_CAP_HASH], client.profile)[C.ENTITY_CAP_HASH]
            disco_infos = self.hashes[cap_hash]
            return defer.succeed(disco_infos)
        except KeyError:
            # capability hash is not available, we'll compute one
            def infosCb(disco_infos):
                cap_hash = self.generateHash(disco_infos)
                self.hashes[cap_hash] = disco_infos
                self.host.memory.updateEntityData(jid_, C.ENTITY_CAP_HASH, cap_hash, client.profile)
                return disco_infos
            d = client.disco.requestInfo(jid_)
            d.addCallback(infosCb)
            return d

    @defer.inlineCallbacks
    def getItems(self, jid_=None, profile_key=C.PROF_KEY_NONE):
        """get disco items from jid_, cache them for our own server

        @param jid_: jid of the target, or None for profile's server
        @param profile_key: %(doc_profile_key)s
        @return: a Deferred which fire disco.DiscoItems
        """
        client = self.host.getClient(profile_key)
        if jid_ is None:
            jid_ = jid.JID(client.jid.host)
            # we cache items only for our own server
            try:
                items = self.host.memory.getEntityData(jid_, ["DISCO_ITEMS"], client.profile)["DISCO_ITEMS"]
                log.debug("[%s] disco items are in cache" % jid_.full())
            except KeyError:
                log.debug("Caching [%s] disco items" % jid_.full())
                items = yield client.disco.requestItems(jid_)
                self.host.memory.updateEntityData(jid_, "DISCO_ITEMS", items, client.profile)
        else:
            items = yield client.disco.requestItems(jid_)

        defer.returnValue(items)


    def _infosEb(self, failure, entity_jid):
        failure.trap(StanzaError)
        log.warning(_("Error while requesting [%(jid)s]: %(error)s") % {'jid': entity_jid.full(),
                                                                    'error': failure.getErrorMessage()})

    def findServiceEntities(self, category, type_, jid_=None, profile_key=C.PROF_KEY_NONE):
        """Return all available items of an entity which correspond to (category, type_)

        @param category: identity's category
        @param type_: identitiy's type
        @param jid_: the jid of the target server (None for profile's server)
        @param profile_key: %(doc_profile_key)s
        @return: a set of entities or None if no cached data were found
        """
        found_entities = set()

        def infosCb(infos, entity_jid):
            if (category, type_) in infos.identities:
                found_entities.add(entity_jid)

        def gotItems(items):
            defers_list = []
            for item in items:
                info_d = self.getInfos(item.entity, profile_key)
                info_d.addCallbacks(infosCb, self._infosEb, [item.entity], None, [item.entity])
                defers_list.append(info_d)
            return defer.DeferredList(defers_list)

        d = self.getItems(jid_, profile_key)
        d.addCallback(gotItems)
        d.addCallback(lambda dummy: found_entities)
        reactor.callLater(TIMEOUT, d.cancel) # FIXME: one bad service make a general timeout
        return d

    def findFeaturesSet(self, features, category=None, type_=None, jid_=None, profile_key=C.PROF_KEY_NONE):
        """Return entities (including jid_ and its items) offering features

        @param features: iterable of features which must be present
        @param category: if not None, accept only this category
        @param type_: if not None, accept only this type
        @param jid_: the jid of the target server (None for profile's server)
        @param profile_key: %(doc_profile_key)s
        @return: a set of found entities
        """
        client = self.host.getClient(profile_key)
        if jid_ is None:
            jid_ = jid.JID(client.jid.host)
        features = set(features)
        found_entities = set()

        def infosCb(infos, entity):
            if category is not None or type_ is not None:
                categories = set()
                types = set()
                for identity in infos.identities:
                    id_cat, id_type = identity
                    categories.add(id_cat)
                    types.add(id_type)
                if category is not None and category not in categories:
                    return
                if type_ is not None and type_ not in types:
                    return
            if features.issubset(infos.features):
                found_entities.add(entity)

        def gotItems(items):
            defer_list = []
            for entity in [jid_] + [item.entity for item in items]:
                infos_d = self.getInfos(entity, profile_key)
                infos_d.addCallbacks(infosCb, self._infosEb, [entity], None, [entity])
            defer_list.append(infos_d)
            return defer.DeferredList(defer_list)

        d = self.getItems(jid_, profile_key)
        d.addCallback(gotItems)
        d.addCallback(lambda dummy: found_entities)
        reactor.callLater(TIMEOUT, d.cancel) # FIXME: one bad service make a general timeout
        return d

    def generateHash(self, services):
        """ Generate a unique hash for given service

        hash algorithm is the one described in XEP-0115
        @param services: iterable of disco.DiscoIdentity/disco.DiscoFeature, as returned by discoHandler.info

        """
        s = []
        byte_identities = [ByteIdentity(service) for service in services if isinstance(service, disco.DiscoIdentity)]  # FIXME: lang must be managed here
        byte_identities.sort(key=lambda i: i.lang)
        byte_identities.sort(key=lambda i: i.idType)
        byte_identities.sort(key=lambda i: i.category)
        for identity in byte_identities:
            s.append(str(identity))
            s.append('<')
        byte_features = [service.encode('utf-8') for service in services if isinstance(service, disco.DiscoFeature)]
        byte_features.sort()  # XXX: the default sort has the same behaviour as the requested RFC 4790 i;octet sort
        for feature in byte_features:
            s.append(feature)
            s.append('<')
        #TODO: manage XEP-0128 data form here
        cap_hash = b64encode(sha1(''.join(s)).digest())
        log.debug(_('Capability hash generated: [%s]') % cap_hash)
        return cap_hash

    @defer.inlineCallbacks
    def _discoInfos(self, entity_jid_s, profile_key=C.PROF_KEY_NONE):
        """ Discovery method for the bridge
        @param entity_jid_s: entity we want to discover

        @return: list of tu"""
        entity = jid.JID(entity_jid_s)
        disco_infos = yield self.getInfos(entity, profile_key)
        defer.returnValue((disco_infos.features, [(cat, type_, name or '') for (cat, type_), name in disco_infos.identities.items()]))

    @defer.inlineCallbacks
    def _discoItems(self, entity_jid_s, profile_key=C.PROF_KEY_NONE):
        """ Discovery method for the bridge
        @param entity_jid_s: entity we want to discover

        @return: list of tu"""
        entity = jid.JID(entity_jid_s)
        disco_items = yield self.getItems(entity, profile_key)
        defer.returnValue([(item.entity.full(), item.nodeIdentifier or '', item.name or '') for item in disco_items])
