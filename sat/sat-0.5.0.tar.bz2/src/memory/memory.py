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

import os.path
from ConfigParser import SafeConfigParser, NoOptionError, NoSectionError
from uuid import uuid4
from sat.core.log import getLogger
log = getLogger(__name__)
from twisted.internet import defer, reactor
from twisted.words.protocols.jabber import jid
from sat.core import exceptions
from sat.core.constants import Const as C
from sat.memory.sqlite import SqliteStorage
from sat.memory.persistent import PersistentDict
from sat.memory.params import Params
from sat.memory.disco import Discovery
from sat.memory.crypto import BlockCipher
from sat.tools import config as tools_config


class Sessions(object):
    """Sessions are data associated to key used for a temporary moment, with optional profile checking."""
    DEFAULT_TIMEOUT = 600

    def __init__(self, timeout=None):
        """
        @param timeout: nb of seconds before session destruction
        """
        self._sessions = dict()
        self.timeout = timeout or Sessions.DEFAULT_TIMEOUT

    def newSession(self, session_data=None, profile=None):
        """ Create a new session
        @param session_data: mutable data to use, default to a dict
        @param profile: if set, the session is owned by the profile,
                        and profileGet must be used instead of __getitem__
        @return: session_id, session_data
        """
        session_id = str(uuid4())
        timer = reactor.callLater(self.timeout, self._purgeSession, session_id)
        if session_data is None:
            session_data = {}
        self._sessions[session_id] = (timer, session_data) if profile is None else (timer, session_data, profile)
        return session_id, session_data

    def _purgeSession(self, session_id):
        del self._sessions[session_id]
        log.debug("Session [%s] purged" % session_id)

    def __len__(self):
        return len(self._sessions)

    def __contains__(self, session_id):
        return session_id in self._sessions

    def profileGet(self, session_id, profile):
        try:
            timer, session_data, profile_set = self._sessions[session_id]
        except ValueError:
            raise exceptions.InternalError("You need to use __getitem__ when profile is not set")
        if profile_set != profile:
            raise exceptions.InternalError("current profile differ from set profile !")
        timer.reset(self.timeout)
        return session_data

    def __getitem__(self, session_id):
        try:
            timer, session_data = self._sessions[session_id]
        except ValueError:
            raise exceptions.InternalError("You need to use profileGet instead of __getitem__ when profile is set")
        timer.reset(self.timeout)
        return session_data

    def __setitem__(self, key, value):
        raise NotImplementedError("You need do use newSession to create a session")

    def __delitem__(self, session_id):
        """ Cancel the timer, then actually delete the session data """
        try:
            timer = self._sessions[session_id][0]
            timer.cancel()
            self._purgeSession(session_id)
        except KeyError:
            log.debug("Session [%s] doesn't exists, timeout expired?" % session_id)

    def keys(self):
        return self._sessions.keys()

    def iterkeys(self):
        return self._sessions.iterkeys()


class ProfileSessions(Sessions):
    """ProfileSessions extends the Sessions class, but here the profile can be
    used as the key to retrieve data or delete a session (instead of session id).
    """

    def _profileGetAllIds(self, profile):
        """Return a list of the sessions ids that are associated to the given profile.

        @param profile: %(doc_profile)s
        @return: a list containing the sessions ids
        """
        ret = []
        for session_id in self._sessions:
            try:
                timer, session_data, profile_set = self._sessions[session_id]
            except ValueError:
                continue
            if profile == profile_set:
                ret.append(session_id)
        return ret

    def profileGetUnique(self, profile):
        """Return the data of the unique session that is associated to the given profile.

        @param profile: %(doc_profile)s
        @return:
            - mutable data (default: dict) of the unique session
            - None if no session is associated to the profile
            - raise an error if more than one session are found
        """
        ids = self._profileGetAllIds(profile)
        if len(ids) > 1:
            raise exceptions.InternalError('profileGetUnique has been used but more than one session has been found!')
        return self._sessions[ids[0]][1] if len(ids) == 1 else None

    def profileDelUnique(self, profile):
        """Delete the unique session that is associated to the given profile.

        @param profile: %(doc_profile)s
        @return: None, but raise an error if more than one session are found
        """
        ids = self._profileGetAllIds(profile)
        if len(ids) > 1:
            raise exceptions.InternalError('profileDelUnique has been used but more than one session has been found!')
        if len(ids) == 1:
            del self._sessions[ids[0]]


# XXX: tmp update code, will be removed in the future
# When you remove this, please add the default value for
# 'local_dir' in sat.core.constants.Const.DEFAULT_CONFIG
def fixLocalDir(silent=True):
    """Retro-compatibility with the previous local_dir default value.

    @param silent (boolean): toggle logging output (must be True when called from sat.sh)
    """
    user_config = SafeConfigParser()
    try:
        user_config.read(C.CONFIG_FILES)
    except:
        pass  # file is readable but its structure if wrong
    try:
        current_value = user_config.get('DEFAULT', 'local_dir')
    except (NoOptionError, NoSectionError):
        current_value = ''
    if current_value:
        return  # nothing to do
    old_default = '~/.sat'
    if os.path.isfile(os.path.expanduser(old_default) + '/' + C.SAVEFILE_DATABASE):
        if not silent:
            log.warning(_("A database has been found in the default local_dir for previous versions (< 0.5)"))
        tools_config.fixConfigOption('', 'local_dir', old_default, silent)


class Memory(object):
    """This class manage all persistent informations"""

    def __init__(self, host):
        log.info(_("Memory manager init"))
        self.initialized = defer.Deferred()
        self.host = host
        self._entities_cache = {} # XXX: keep presence/last resource/other data in cache
                                  #     /!\ an entity is not necessarily in roster
        self.subscriptions = {}
        self.auth_sessions = ProfileSessions()  # remember the authenticated profiles
        self.disco = Discovery(host)
        fixLocalDir(False)  # XXX: tmp update code, will be removed in the future
        self.config = self.parseMainConf()
        database_file = os.path.expanduser(os.path.join(self.getConfig('', 'local_dir'), C.SAVEFILE_DATABASE))
        self.storage = SqliteStorage(database_file, host.__version__)
        PersistentDict.storage = self.storage
        self.params = Params(host, self.storage)
        log.info(_("Loading default params template"))
        self.params.load_default_params()
        d = self.storage.initialized.addCallback(lambda ignore: self.load())
        self.memory_data = PersistentDict("memory")
        d.addCallback(lambda ignore: self.memory_data.load())
        d.chainDeferred(self.initialized)

    def parseMainConf(self):
        """look for main .ini configuration file, and parse it"""
        config = SafeConfigParser(defaults=C.DEFAULT_CONFIG)
        try:
            config.read(C.CONFIG_FILES)
        except:
            log.error(_("Can't read main config !"))
        return config

    def getConfig(self, section, name):
        """Get the main configuration option
        @param section: section of the config file (None or '' for DEFAULT)
        @param name: name of the option
        """
        return tools_config.getConfig(self.config, section, name, default='')

    def load_xml(self, filename):
        """Load parameters template from xml file

        @param filename (str): input file
        @return: bool: True in case of success
        """
        if not filename:
            return False
        filename = os.path.expanduser(filename)
        if os.path.exists(filename):
            try:
                self.params.load_xml(filename)
                log.debug(_("Parameters loaded from file: %s") % filename)
                return True
            except Exception as e:
                log.error(_("Can't load parameters from file: %s") % e)
        return False

    def load(self):
        """Load parameters and all memory things from db"""
        #parameters data
        return self.params.loadGenParams()

    def loadIndividualParams(self, profile):
        """Load individual parameters for a profile
        @param profile: %(doc_profile)s"""
        return self.params.loadIndParams(profile)

    def startProfileSession(self, profile):
        """"Iniatialise session for a profile
        @param profile: %(doc_profile)s"""
        log.info(_("[%s] Profile session started" % profile))
        self._entities_cache[profile] = {}

    def newAuthSession(self, key, profile):
        """Start a new session for the authenticated profile.

        The personal key is loaded encrypted from a PersistentDict before being decrypted.

        @param key: the key to decrypt the personal key
        @param profile: %(doc_profile)s
        @return: a deferred None value
        """
        def gotPersonalKey(personal_key):
            """Create the session for this profile and store the personal key"""
            self.auth_sessions.newSession({C.MEMORY_CRYPTO_KEY: personal_key}, profile)
            log.debug('auth session created for profile %s' % profile)

        d = PersistentDict(C.MEMORY_CRYPTO_NAMESPACE, profile).load()
        d.addCallback(lambda data: BlockCipher.decrypt(key, data[C.MEMORY_CRYPTO_KEY]))
        return d.addCallback(gotPersonalKey)

    def purgeProfileSession(self, profile):
        """Delete cache of data of profile
        @param profile: %(doc_profile)s"""
        log.info(_("[%s] Profile session purge" % profile))
        self.params.purgeProfile(profile)
        try:
            del self._entities_cache[profile]
        except KeyError:
            log.error(_("Trying to purge roster status cache for a profile not in memory: [%s]") % profile)

    def save_xml(self, filename):
        """Save parameters template to xml file

        @param filename (str): output file
        @return: bool: True in case of success
        """
        if not filename:
            return False
        #TODO: need to encrypt files (at least passwords !) and set permissions
        filename = os.path.expanduser(filename)
        try:
            self.params.save_xml(filename)
            log.debug(_("Parameters saved to file: %s") % filename)
            return True
        except Exception as e:
            log.error(_("Can't save parameters to file: %s") % e)
        return False

    def getProfilesList(self):
        return self.storage.getProfilesList()

    def getProfileName(self, profile_key, return_profile_keys=False):
        """Return name of profile from keyword
        @param profile_key: can be the profile name or a keywork (like @DEFAULT@)
        @return: profile name or None if it doesn't exist"""
        return self.params.getProfileName(profile_key, return_profile_keys)

    def asyncCreateProfile(self, name, password=''):
        """Create a new profile
        @param name: profile name
        @param password: profile password
        @return: Deferred
        """
        personal_key = BlockCipher.getRandomKey(base64=True)  # generated once for all and saved in a PersistentDict
        self.auth_sessions.newSession({C.MEMORY_CRYPTO_KEY: personal_key}, name)  # will be encrypted by setParam
        d = self.params.asyncCreateProfile(name)
        d.addCallback(lambda dummy: self.setParam(C.PROFILE_PASS_PATH[1], password, C.PROFILE_PASS_PATH[0], profile_key=name))
        return d

    def asyncDeleteProfile(self, name, force=False):
        """Delete an existing profile
        @param name: Name of the profile
        @param force: force the deletion even if the profile is connected.
        To be used for direct calls only (not through the bridge).
        @return: a Deferred instance
        """
        self.auth_sessions.profileDelUnique(name)
        return self.params.asyncDeleteProfile(name, force)

    def addToHistory(self, from_jid, to_jid, message, type_='chat', extra=None, timestamp=None, profile=C.PROF_KEY_NONE):
        assert profile != C.PROF_KEY_NONE
        if extra is None:
            extra = {}
        return self.storage.addToHistory(from_jid, to_jid, message, type_, extra, timestamp, profile)

    def getHistory(self, from_jid, to_jid, limit=0, between=True, profile=C.PROF_KEY_NONE):
        assert profile != C.PROF_KEY_NONE
        return self.storage.getHistory(jid.JID(from_jid), jid.JID(to_jid), limit, between, profile)

    def _getLastResource(self, jid_s, profile_key):
        jid_ = jid.JID(jid_s)
        return self.getLastResource(jid_, profile_key) or ""

    def getLastResource(self, entity_jid, profile_key):
        """Return the last resource used by an entity
        @param entity_jid: entity jid
        @param profile_key: %(doc_profile_key)s"""
        data = self.getEntityData(entity_jid.userhostJID(), [C.ENTITY_LAST_RESOURCE], profile_key)
        try:
            return data[C.ENTITY_LAST_RESOURCE]
        except KeyError:
            return None

    def _getPresenceStatuses(self, profile_key):
        ret = self.getPresenceStatuses(profile_key)
        return {entity.full():data for entity, data in ret.iteritems()}

    def getPresenceStatuses(self, profile_key):
        """Get all the presence status of a profile
        @param profile_key: %(doc_profile_key)s
        @return: presence data: key=entity JID, value=presence data for this entity
        """
        profile = self.getProfileName(profile_key)
        if not profile:
            raise exceptions.ProfileUnknownError(_('Trying to get entity data for a non-existant profile'))
        entities_presence = {}
        for entity in self._entities_cache[profile]:
            if "presence" in self._entities_cache[profile][entity]:
                entities_presence[entity] = self._entities_cache[profile][entity]["presence"]

        log.debug("Memory getPresenceStatus (%s)" % entities_presence)
        return entities_presence

    def setPresenceStatus(self, entity_jid, show, priority, statuses, profile_key):
        """Change the presence status of an entity
        @param entity_jid: jid.JID of the entity
        @param show: show status
        @param priotity: priotity
        @param statuses: dictionary of statuses
        @param profile_key: %(doc_profile_key)s
        """
        profile = self.getProfileName(profile_key)
        if not profile:
            raise exceptions.ProfileUnknownError(_('Trying to get entity data for a non-existant profile'))
        entity_data = self._getEntitiesData(entity_jid, profile)[entity_jid]
        resource = entity_jid.resource
        if resource:
            self.updateEntityData(entity_jid.userhostJID(), C.ENTITY_LAST_RESOURCE, resource, profile)
        entity_data.setdefault("presence", {})[resource or ''] = (show, priority, statuses)

    def _getEntitiesData(self, entity_jid, profile):
        """Get data dictionary for entities
        @param entity_jid: JID of the entity, or C.ENTITY_ALL for all entities)
        @param profile: %(doc_profile)s
        @return: entities_data (key=jid, value=entity_data)
        @raise: exceptions.ProfileNotInCacheError if profile is not in cache
        """
        if not profile in self._entities_cache:
            raise exceptions.ProfileNotInCacheError
        if entity_jid == C.ENTITY_ALL:
            entities_data = self._entities_cache[profile]
        else:
            entity_data = self._entities_cache[profile].setdefault(entity_jid, {})
            entities_data = {entity_jid: entity_data}
        return entities_data

    def _updateEntityResources(self, entity_jid, profile):
        """Add a known resource to bare entity_jid cache
        @param entity_jid: full entity_jid (with resource)
        @param profile: %(doc_profile)s
        """
        assert(entity_jid.resource)
        entity_data = self._getEntitiesData(entity_jid.userhostJID(), profile)[entity_jid.userhostJID()]
        resources = entity_data.setdefault('resources', set())
        resources.add(entity_jid.resource)

    def updateEntityData(self, entity_jid, key, value, profile_key):
        """Set a misc data for an entity
        @param entity_jid: JID of the entity, or C.ENTITY_ALL to update all entities)
        @param key: key to set (eg: "type")
        @param value: value for this key (eg: "chatroom")
        @param profile_key: %(doc_profile_key)s
        """
        profile = self.getProfileName(profile_key)
        if not profile:
            raise exceptions.ProfileUnknownError(_('Trying to get entity data for a non-existant profile'))
        entities_data = self._getEntitiesData(entity_jid, profile)
        if entity_jid.resource and entity_jid != C.ENTITY_ALL:
            self._updateEntityResources(entity_jid, profile)

        for jid_ in entities_data:
            entity_data = entities_data[jid_]
            if value == C.PROF_KEY_NONE and key in entity_data:
                del entity_data[key]
            else:
                entity_data[key] = value
            if isinstance(value, basestring):
                self.host.bridge.entityDataUpdated(jid_.full(), key, value, profile)

    def delEntityData(self, entity_jid, key, profile_key):
        """Delete data for an entity
        @param entity_jid: JID of the entity, or C.ENTITY_ALL to delete data from all entities)
        @param key: key to delete (eg: "type")
        @param profile_key: %(doc_profile_key)s
        """
        entities_data = self._getEntitiesData(entity_jid, profile_key)
        for entity_jid in entities_data:
            entity_data = entities_data[entity_jid]
            try:
                del entity_data[key]
            except KeyError:
                log.debug("Key [%s] doesn't exist for [%s] in entities_cache" % (key, entity_jid.full()))

    def getEntityData(self, entity_jid, keys_list, profile_key):
        """Get a list of cached values for entity

        @param entity_jid: JID of the entity
        @param keys_list (iterable): list of keys to get, empty list for everything
        @param profile_key: %(doc_profile_key)s
        @return: dict withs values for each key in keys_list.
                 if there is no value of a given key, resulting dict will
                 have nothing with that key nether
        @raise: exceptions.UnknownEntityError if entity is not in cache
        """
        profile = self.getProfileName(profile_key)
        if not profile:
            raise exceptions.ProfileUnknownError(_('Trying to get entity data for a non-existant profile'))
        entity_data = self._getEntitiesData(entity_jid, profile)[entity_jid]
        if not keys_list:
            return entity_data
        ret = {}
        for key in keys_list:
            if key in entity_data:
                ret[key] = entity_data[key]
        return ret

    def getEntityDatum(self, entity_jid, key, profile_key):
        """Get a datum from entity

        @param entity_jid: JID of the entity
        @param keys: key to get
        @param profile_key: %(doc_profile_key)s
        @return: requested value

        @raise: exceptions.UnknownEntityError if entity is not in cache
        @raise: KeyError if there is no value for this key and this entity
        """
        return self.getEntityData(entity_jid, (key,), profile_key)[key]

    def delEntityCache(self, entity_jid, delete_all_resources=True, profile_key=C.PROF_KEY_NONE):
        """Remove cached data for entity
        @param entity_jid: JID of the entity to delete
        @param delete_all_resources: if True also delete all known resources form cache
        @param profile_key: %(doc_profile_key)s
        """
        profile = self.getProfileName(profile_key)
        if not profile:
            raise exceptions.ProfileUnknownError(_('Trying to get entity data for a non-existant profile'))
        to_delete = set([entity_jid])

        if delete_all_resources:
            if entity_jid.resource:
                raise ValueError(_("Need a bare jid to delete all resources"))
            entity_data = self._getEntitiesData(entity_jid, profile)[entity_jid]
            resources = entity_data.setdefault('resources', set())
            to_delete.update([jid.JID("%s/%s" % (entity_jid.userhost(), resource)) for resource in resources])

        for entity in to_delete:
            try:
                del self._entities_cache[profile][entity]
            except KeyError:
                log.debug("Can't delete entity [%s]: not in cache" % entity.full())

    def encryptValue(self, value, profile):
        """Encrypt a value for the given profile. The personal key must be loaded
        already in the profile session, that should be the case if the profile is
        already authenticated.

        @param value (str): the value to encrypt
        @param profile (str): %(doc_profile)s
        @return: the deferred encrypted value
        """
        try:
            personal_key = self.host.memory.auth_sessions.profileGetUnique(profile)[C.MEMORY_CRYPTO_KEY]
        except TypeError:
            raise exceptions.InternalError(_('Trying to encrypt a value for %s while the personal key is undefined!') % profile)
        return BlockCipher.encrypt(personal_key, value)

    def decryptValue(self, value, profile):
        """Decrypt a value for the given profile. The personal key must be loaded
        already in the profile session, that should be the case if the profile is
        already authenticated.

        @param value (str): the value to decrypt
        @param profile (str): %(doc_profile)s
        @return: the deferred decrypted value
        """
        try:
            personal_key = self.host.memory.auth_sessions.profileGetUnique(profile)[C.MEMORY_CRYPTO_KEY]
        except TypeError:
            raise exceptions.InternalError(_('Trying to decrypt a value for %s while the personal key is undefined!') % profile)
        return BlockCipher.decrypt(personal_key, value)

    def encryptPersonalData(self, data_key, data_value, crypto_key, profile):
        """Re-encrypt a personal data (saved to a PersistentDict).

        @param data_key: key for the individual PersistentDict instance
        @param data_value: the value to be encrypted
        @param crypto_key: the key to encrypt the value
        @param profile: %(profile_doc)s
        @return: a deferred None value
        """

        def gotIndMemory(data):
            d = BlockCipher.encrypt(crypto_key, data_value)

            def cb(cipher):
                data[data_key] = cipher
                return data.force(data_key)

            return d.addCallback(cb)

        def done(dummy):
            log.debug(_('Personal data (%(ns)s, %(key)s) has been successfuly encrypted') %
                      {'ns': C.MEMORY_CRYPTO_NAMESPACE, 'key': data_key})

        d = PersistentDict(C.MEMORY_CRYPTO_NAMESPACE, profile).load()
        return d.addCallback(gotIndMemory).addCallback(done)

    def addWaitingSub(self, type_, entity_jid, profile_key):
        """Called when a subcription request is received"""
        profile = self.getProfileName(profile_key)
        assert profile
        if profile not in self.subscriptions:
            self.subscriptions[profile] = {}
        self.subscriptions[profile][entity_jid] = type_

    def delWaitingSub(self, entity_jid, profile_key):
        """Called when a subcription request is finished"""
        profile = self.getProfileName(profile_key)
        assert profile
        if profile in self.subscriptions and entity_jid in self.subscriptions[profile]:
            del self.subscriptions[profile][entity_jid]

    def getWaitingSub(self, profile_key):
        """Called to get a list of currently waiting subscription requests"""
        profile = self.getProfileName(profile_key)
        if not profile:
            log.error(_('Asking waiting subscriptions for a non-existant profile'))
            return {}
        if profile not in self.subscriptions:
            return {}

        return self.subscriptions[profile]

    def getStringParamA(self, name, category, attr="value", profile_key=C.PROF_KEY_NONE):
        return self.params.getStringParamA(name, category, attr, profile_key)

    def getParamA(self, name, category, attr="value", profile_key=C.PROF_KEY_NONE):
        return self.params.getParamA(name, category, attr, profile_key)

    def asyncGetParamA(self, name, category, attr="value", security_limit=C.NO_SECURITY_LIMIT, profile_key=C.PROF_KEY_NONE):
        return self.params.asyncGetParamA(name, category, attr, security_limit, profile_key)

    def asyncGetStringParamA(self, name, category, attr="value", security_limit=C.NO_SECURITY_LIMIT, profile_key=C.PROF_KEY_NONE):
        return self.params.asyncGetStringParamA(name, category, attr, security_limit, profile_key)

    def getParamsUI(self, security_limit=C.NO_SECURITY_LIMIT, app='', profile_key=C.PROF_KEY_NONE):
        return self.params.getParamsUI(security_limit, app, profile_key)

    def getParams(self, security_limit=C.NO_SECURITY_LIMIT, app='', profile_key=C.PROF_KEY_NONE):
        return self.params.getParams(security_limit, app, profile_key)

    def getParamsForCategory(self, category, security_limit=C.NO_SECURITY_LIMIT, app='', profile_key=C.PROF_KEY_NONE):
        return self.params.getParamsForCategory(category, security_limit, app, profile_key)

    def getParamsCategories(self):
        return self.params.getParamsCategories()

    def setParam(self, name, value, category, security_limit=C.NO_SECURITY_LIMIT, profile_key=C.PROF_KEY_NONE):
        return self.params.setParam(name, value, category, security_limit, profile_key)

    def updateParams(self, xml):
        return self.params.updateParams(xml)

    def paramsRegisterApp(self, xml, security_limit=C.NO_SECURITY_LIMIT, app=''):
        return self.params.paramsRegisterApp(xml, security_limit, app)

    def setDefault(self, name, category, callback, errback=None):
        return self.params.setDefault(name, category, callback, errback)
