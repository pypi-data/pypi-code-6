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
from sat.core.constants import Const as C
from sat.core import exceptions
from sat.core.log import getLogger
log = getLogger(__name__)
from sat.memory.crypto import BlockCipher, PasswordHasher
from sat.tools.config import fixConfigOption
from twisted.enterprise import adbapi
from twisted.internet import defer
from collections import OrderedDict
from time import time
import re
import os.path
import cPickle as pickle
import hashlib

CURRENT_DB_VERSION = 2

# XXX: DATABASE schemas are used in the following way:
#      - 'current' key is for the actual database schema, for a new base
#      - x(int) is for update needed between x-1 and x. All number are needed between y and z to do an update
#        e.g.: if CURRENT_DB_VERSION is 6, 'current' is the actuel DB, and to update from version 3, numbers 4, 5 and 6 are needed
#      a 'current' data dict can contains the keys:
#      - 'CREATE': it contains an Ordered dict with table to create as keys, and a len 2 tuple as value, where value[0] are the columns definitions and value[1] are the table constraints
#      - 'INSERT': it contains an Ordered dict with table where values have to be inserted, and many tuples containing values to insert in the order of the rows (#TODO: manage named columns)
#      an update data dict (the ones with a number) can contains the keys 'create', 'delete', 'cols create', 'cols delete', 'cols modify', 'insert' or 'specific'. See Updater.generateUpdateData for more infos. This method can be used to autogenerate update_data, to ease the work of the developers.

DATABASE_SCHEMAS = {
        "current": {'CREATE': OrderedDict((
                              ('profiles',        (("id INTEGER PRIMARY KEY ASC", "name TEXT"),
                                                   ("UNIQUE (name)",))),
                              ('message_types',   (("type TEXT PRIMARY KEY",),
                                                   tuple())),
                              ('history',         (("id INTEGER PRIMARY KEY ASC", "profile_id INTEGER", "source TEXT", "dest TEXT", "source_res TEXT", "dest_res TEXT", "timestamp DATETIME", "message TEXT", "type TEXT", "extra BLOB"),
                                                   ("FOREIGN KEY(profile_id) REFERENCES profiles(id) ON DELETE CASCADE", "FOREIGN KEY(type) REFERENCES message_types(type)"))),
                              ('param_gen',       (("category TEXT", "name TEXT", "value TEXT"),
                                                   ("PRIMARY KEY (category,name)",))),
                              ('param_ind',       (("category TEXT", "name TEXT", "profile_id INTEGER", "value TEXT"),
                                                   ("PRIMARY KEY (category,name,profile_id)", "FOREIGN KEY(profile_id) REFERENCES profiles(id) ON DELETE CASCADE"))),
                              ('private_gen',     (("namespace TEXT", "key TEXT", "value TEXT"),
                                                   ("PRIMARY KEY (namespace, key)",))),
                              ('private_ind',     (("namespace TEXT", "key TEXT", "profile_id INTEGER", "value TEXT"),
                                                   ("PRIMARY KEY (namespace, key, profile_id)", "FOREIGN KEY(profile_id) REFERENCES profiles(id) ON DELETE CASCADE"))),
                              ('private_gen_bin', (("namespace TEXT", "key TEXT", "value BLOB"),
                                                   ("PRIMARY KEY (namespace, key)",))),
                              ('private_ind_bin', (("namespace TEXT", "key TEXT", "profile_id INTEGER", "value BLOB"),
                                                   ("PRIMARY KEY (namespace, key, profile_id)", "FOREIGN KEY(profile_id) REFERENCES profiles(id) ON DELETE CASCADE")))
                              )),
                    'INSERT': OrderedDict((
                              ('message_types', (("'chat'",), ("'error'",), ("'groupchat'",), ("'headline'",), ("'normal'",))),
                              )),
                    },
        2:         {'specific': 'update2raw_v2'
                   },
        1:         {'cols create': {'history': ('extra BLOB',)}
                   },
        }


class SqliteStorage(object):
    """This class manage storage with Sqlite database"""

    def __init__(self, db_filename, sat_version):
        """Connect to the given database
        @param db_filename: full path to the Sqlite database"""
        self.initialized = defer.Deferred()  # triggered when memory is fully initialised and ready
        self.profiles = {}  # we keep cache for the profiles (key: profile name, value: profile id)

        log.info(_("Connecting database"))
        new_base = not os.path.exists(db_filename)  # do we have to create the database ?
        if new_base:  # the dir may not exist if it's not the XDG recommended one
            dir_ = os.path.dirname(db_filename)
            if not os.path.exists(dir_):
                os.makedirs(dir_, 0700)
        self.dbpool = adbapi.ConnectionPool("sqlite3", db_filename, check_same_thread=False)

        # init_defer is the initialisation deferred, initialisation is ok when all its callbacks have been done
        # XXX: foreign_keys activation doesn't seem to work, probably because of the multi-threading
        # All the requests that need to use this feature should be run with runInteraction instead,
        # so you can set the PRAGMA as it is done in self.deleteProfile
        init_defer = self.dbpool.runOperation("PRAGMA foreign_keys = ON").addErrback(lambda x: log.error(_("Can't activate foreign keys")))

        def getNewBaseSql():
            log.info(_("The database is new, creating the tables"))
            database_creation = ["PRAGMA user_version=%d" % CURRENT_DB_VERSION]
            database_creation.extend(Updater.createData2Raw(DATABASE_SCHEMAS['current']['CREATE']))
            database_creation.extend(Updater.insertData2Raw(DATABASE_SCHEMAS['current']['INSERT']))
            return database_creation

        def getUpdateSql():
            updater = Updater(self.dbpool, sat_version)
            return updater.checkUpdates()

        def commitStatements(statements):

            if statements is None:
                return defer.succeed(None)
            log.debug("===== COMMITING STATEMENTS =====\n%s\n============\n\n" % '\n'.join(statements))
            d = self.dbpool.runInteraction(self._updateDb, tuple(statements))
            return d

        init_defer.addCallback(lambda ignore: getNewBaseSql() if new_base else getUpdateSql())
        init_defer.addCallback(commitStatements)

        def fillProfileCache(ignore):
            d = self.dbpool.runQuery("SELECT name,id FROM profiles").addCallback(self._profilesCache)
            d.chainDeferred(self.initialized)

        init_defer.addCallback(fillProfileCache)

    def _updateDb(self, interaction, statements):
        for statement in statements:
            interaction.execute(statement)

    #Profiles
    def _profilesCache(self, profiles_result):
        """Fill the profiles cache
        @param profiles_result: result of the sql profiles query"""
        for profile in profiles_result:
            name, id_ = profile
            self.profiles[name] = id_

    def getProfilesList(self):
        """"Return list of all registered profiles"""
        return self.profiles.keys()

    def hasProfile(self, profile_name):
        """return True if profile_name exists
        @param profile_name: name of the profile to check"""
        return profile_name in self.profiles

    def createProfile(self, name):
        """Create a new profile
        @param name: name of the profile
        @return: deferred triggered once profile is actually created"""

        def getProfileId(ignore):
            return self.dbpool.runQuery("SELECT (id) FROM profiles WHERE name = ?", (name, ))

        def profile_created(profile_id):
            _id = profile_id[0][0]
            self.profiles[name] = _id  # we synchronise the cache

        d = self.dbpool.runQuery("INSERT INTO profiles(name) VALUES (?)", (name, ))
        d.addCallback(getProfileId)
        d.addCallback(profile_created)
        return d

    def deleteProfile(self, name):
        """Delete profile
        @param name: name of the profile
        @return: deferred triggered once profile is actually deleted"""
        def deletionError(failure):
            log.error(_("Can't delete profile [%s]") % name)
            return failure

        def delete(txn):
            del self.profiles[name]
            txn.execute("PRAGMA foreign_keys = ON")
            txn.execute("DELETE FROM profiles WHERE name = ?", (name,))
            return None

        d = self.dbpool.runInteraction(delete)
        d.addCallback(lambda ignore: log.info(_("Profile [%s] deleted") % name))
        d.addErrback(deletionError)
        return d

    #Params
    def loadGenParams(self, params_gen):
        """Load general parameters
        @param params_gen: dictionary to fill
        @return: deferred"""

        def fillParams(result):
            for param in result:
                category, name, value = param
                params_gen[(category, name)] = value
        log.debug(_("loading general parameters from database"))
        return self.dbpool.runQuery("SELECT category,name,value FROM param_gen").addCallback(fillParams)

    def loadIndParams(self, params_ind, profile):
        """Load individual parameters
        @param params_ind: dictionary to fill
        @param profile: a profile which *must* exist
        @return: deferred"""

        def fillParams(result):
            for param in result:
                category, name, value = param
                params_ind[(category, name)] = value
        log.debug(_("loading individual parameters from database"))
        d = self.dbpool.runQuery("SELECT category,name,value FROM param_ind WHERE profile_id=?", (self.profiles[profile], ))
        d.addCallback(fillParams)
        return d

    def getIndParam(self, category, name, profile):
        """Ask database for the value of one specific individual parameter
        @param category: category of the parameter
        @param name: name of the parameter
        @param profile: %(doc_profile)s
        @return: deferred"""
        d = self.dbpool.runQuery("SELECT value FROM param_ind WHERE category=? AND name=? AND profile_id=?", (category, name, self.profiles[profile]))
        d.addCallback(self.__getFirstResult)
        return d

    def setGenParam(self, category, name, value):
        """Save the general parameters in database
        @param category: category of the parameter
        @param name: name of the parameter
        @param value: value to set
        @return: deferred"""
        d = self.dbpool.runQuery("REPLACE INTO param_gen(category,name,value) VALUES (?,?,?)", (category, name, value))
        d.addErrback(lambda ignore: log.error(_("Can't set general parameter (%(category)s/%(name)s) in database" % {"category": category, "name": name})))
        return d

    def setIndParam(self, category, name, value, profile):
        """Save the individual parameters in database
        @param category: category of the parameter
        @param name: name of the parameter
        @param value: value to set
        @param profile: a profile which *must* exist
        @return: deferred"""
        d = self.dbpool.runQuery("REPLACE INTO param_ind(category,name,profile_id,value) VALUES (?,?,?,?)", (category, name, self.profiles[profile], value))
        d.addErrback(lambda ignore: log.error(_("Can't set individual parameter (%(category)s/%(name)s) for [%(profile)s] in database" % {"category": category, "name": name, "profile": profile})))
        return d

    #History
    def addToHistory(self, from_jid, to_jid, message, _type='chat', extra=None, timestamp=None, profile=None):
        """Store a new message in history
        @param from_jid: full source JID
        @param to_jid: full dest JID
        @param message: message
        @param _type: message type (see RFC 6121 §5.2.2)
        @param extra: dictionary (keys and values are unicode) of extra message data
        @param timestamp: timestamp in seconds since epoch, or None to use current time
        """
        assert(profile)
        if extra is None:
            extra = {}
        extra_ = pickle.dumps({k: v.encode('utf-8') for k, v in extra.items()}, 0).decode('utf-8')
        d = self.dbpool.runQuery("INSERT INTO history(source, source_res, dest, dest_res, timestamp, message, type, extra, profile_id) VALUES (?,?,?,?,?,?,?,?,?)",
                                 (from_jid.userhost(), from_jid.resource, to_jid.userhost(), to_jid.resource, timestamp or time(),
                                  message, _type, extra_, self.profiles[profile]))
        d.addErrback(lambda ignore: log.error(_("Can't save following message in history: from [%(from_jid)s] to [%(to_jid)s] ==> [%(message)s]" %
                                          {"from_jid": from_jid.full(), "to_jid": to_jid.full(), "message": message})))
        return d

    def getHistory(self, from_jid, to_jid, limit=0, between=True, profile=None):
        """Store a new message in history
        @param from_jid: source JID (full, or bare for catchall
        @param to_jid: dest JID (full, or bare for catchall
        @param size: maximum number of messages to get, or 0 for unlimited
        """
        assert(profile)

        def sqliteToList(query_result):
            query_result.reverse()
            result = []
            for row in query_result:
                timestamp, source, source_res, dest, dest_res, message, type_, extra_raw = row
                try:
                    extra = pickle.loads(str(extra_raw or ""))
                except EOFError:
                    extra = {}
                result.append((timestamp, "%s/%s" % (source, source_res) if source_res else source,
                                          "%s/%s" % (dest, dest_res) if dest_res else dest,
                                          message, type_, extra))
            return result

        query_parts = ["SELECT timestamp, source, source_res, dest, dest_res, message, type, extra FROM history WHERE profile_id=? AND"]
        values = [self.profiles[profile]]

        def test_jid(type_, _jid):
            values.append(_jid.userhost())
            if _jid.resource:
                values.append(_jid.resource)
                return '(%s=? AND %s_res=?)' % (type_, type_)
            return '%s=?' % (type_, )

        if between:
            query_parts.append("((%s AND %s) OR (%s AND %s))" % (test_jid('source', from_jid),
                                                             test_jid('dest', to_jid),
                                                             test_jid('source', to_jid),
                                                             test_jid('dest', from_jid)))
        else:
            query_parts.append("%s AND %s" % (test_jid('source', from_jid),
                                              test_jid('dest', to_jid)))

        query_parts.append("ORDER BY timestamp DESC")

        if limit:
            query_parts.append("LIMIT ?")
            values.append(limit)

        d = self.dbpool.runQuery(" ".join(query_parts), values)
        return d.addCallback(sqliteToList)

    #Private values
    def loadGenPrivates(self, private_gen, namespace):
        """Load general private values
        @param private_gen: dictionary to fill
        @param namespace: namespace of the values
        @return: deferred"""

        def fillPrivates(result):
            for private in result:
                key, value = private
                private_gen[key] = value
        log.debug(_("loading general private values [namespace: %s] from database") % (namespace, ))
        d = self.dbpool.runQuery("SELECT key,value FROM private_gen WHERE namespace=?", (namespace, )).addCallback(fillPrivates)
        return d.addErrback(lambda x: log.debug(_("No data present in database for namespace %s") % namespace))

    def loadIndPrivates(self, private_ind, namespace, profile):
        """Load individual private values
        @param privates_ind: dictionary to fill
        @param namespace: namespace of the values
        @param profile: a profile which *must* exist
        @return: deferred"""

        def fillPrivates(result):
            for private in result:
                key, value = private
                private_ind[key] = value
        log.debug(_("loading individual private values [namespace: %s] from database") % (namespace, ))
        d = self.dbpool.runQuery("SELECT key,value FROM private_ind WHERE namespace=? AND profile_id=?", (namespace, self.profiles[profile]))
        d.addCallback(fillPrivates)
        return d.addErrback(lambda x: log.debug(_("No data present in database for namespace %s") % namespace))

    def setGenPrivate(self, namespace, key, value):
        """Save the general private value in database
        @param category: category of the privateeter
        @param key: key of the private value
        @param value: value to set
        @return: deferred"""
        d = self.dbpool.runQuery("REPLACE INTO private_gen(namespace,key,value) VALUES (?,?,?)", (namespace, key, value))
        d.addErrback(lambda ignore: log.error(_("Can't set general private value (%(key)s) [namespace:%(namespace)s] in database" %
                     {"namespace": namespace, "key": key})))
        return d

    def setIndPrivate(self, namespace, key, value, profile):
        """Save the individual private value in database
        @param namespace: namespace of the value
        @param key: key of the private value
        @param value: value to set
        @param profile: a profile which *must* exist
        @return: deferred"""
        d = self.dbpool.runQuery("REPLACE INTO private_ind(namespace,key,profile_id,value) VALUES (?,?,?,?)", (namespace, key, self.profiles[profile], value))
        d.addErrback(lambda ignore: log.error(_("Can't set individual private value (%(key)s) [namespace: %(namespace)s] for [%(profile)s] in database" %
                     {"namespace": namespace, "key": key, "profile": profile})))
        return d

    def delGenPrivate(self, namespace, key):
        """Delete the general private value from database
        @param category: category of the privateeter
        @param key: key of the private value
        @return: deferred"""
        d = self.dbpool.runQuery("DELETE FROM private_gen WHERE namespace=? AND key=?", (namespace, key))
        d.addErrback(lambda ignore: log.error(_("Can't delete general private value (%(key)s) [namespace:%(namespace)s] in database" %
                     {"namespace": namespace, "key": key})))
        return d

    def delIndPrivate(self, namespace, key, profile):
        """Delete the individual private value from database
        @param namespace: namespace of the value
        @param key: key of the private value
        @param profile: a profile which *must* exist
        @return: deferred"""
        d = self.dbpool.runQuery("DELETE FROM private_ind WHERE namespace=? AND key=? AND profile=?)", (namespace, key, self.profiles[profile]))
        d.addErrback(lambda ignore: log.error(_("Can't delete individual private value (%(key)s) [namespace: %(namespace)s] for [%(profile)s] in database" %
                     {"namespace": namespace, "key": key, "profile": profile})))
        return d

    def loadGenPrivatesBinary(self, private_gen, namespace):
        """Load general private binary values
        @param private_gen: dictionary to fill
        @param namespace: namespace of the values
        @return: deferred"""

        def fillPrivates(result):
            for private in result:
                key, value = private
                private_gen[key] = pickle.loads(str(value))
        log.debug(_("loading general private binary values [namespace: %s] from database") % (namespace, ))
        d = self.dbpool.runQuery("SELECT key,value FROM private_gen_bin WHERE namespace=?", (namespace, )).addCallback(fillPrivates)
        return d.addErrback(lambda x: log.debug(_("No binary data present in database for namespace %s") % namespace))

    def loadIndPrivatesBinary(self, private_ind, namespace, profile):
        """Load individual private binary values
        @param privates_ind: dictionary to fill
        @param namespace: namespace of the values
        @param profile: a profile which *must* exist
        @return: deferred"""

        def fillPrivates(result):
            for private in result:
                key, value = private
                private_ind[key] = pickle.loads(str(value))
        log.debug(_("loading individual private binary values [namespace: %s] from database") % (namespace, ))
        d = self.dbpool.runQuery("SELECT key,value FROM private_ind_bin WHERE namespace=? AND profile_id=?", (namespace, self.profiles[profile]))
        d.addCallback(fillPrivates)
        return d.addErrback(lambda x: log.debug(_("No binary data present in database for namespace %s") % namespace))

    def setGenPrivateBinary(self, namespace, key, value):
        """Save the general private binary value in database
        @param category: category of the privateeter
        @param key: key of the private value
        @param value: value to set
        @return: deferred"""
        d = self.dbpool.runQuery("REPLACE INTO private_gen_bin(namespace,key,value) VALUES (?,?,?)", (namespace, key, pickle.dumps(value, 0)))
        d.addErrback(lambda ignore: log.error(_("Can't set general private binary value (%(key)s) [namespace:%(namespace)s] in database" %
                     {"namespace": namespace, "key": key})))
        return d

    def setIndPrivateBinary(self, namespace, key, value, profile):
        """Save the individual private binary value in database
        @param namespace: namespace of the value
        @param key: key of the private value
        @param value: value to set
        @param profile: a profile which *must* exist
        @return: deferred"""
        d = self.dbpool.runQuery("REPLACE INTO private_ind_bin(namespace,key,profile_id,value) VALUES (?,?,?,?)", (namespace, key, self.profiles[profile], pickle.dumps(value, 0)))
        d.addErrback(lambda ignore: log.error(_("Can't set individual binary private value (%(key)s) [namespace: %(namespace)s] for [%(profile)s] in database" %
                     {"namespace": namespace, "key": key, "profile": profile})))
        return d

    def delGenPrivateBinary(self, namespace, key):
        """Delete the general private binary value from database
        @param category: category of the privateeter
        @param key: key of the private value
        @return: deferred"""
        d = self.dbpool.runQuery("DELETE FROM private_gen_bin WHERE namespace=? AND key=?", (namespace, key))
        d.addErrback(lambda ignore: log.error(_("Can't delete general private binary value (%(key)s) [namespace:%(namespace)s] in database" %
                     {"namespace": namespace, "key": key})))
        return d

    def delIndPrivateBinary(self, namespace, key, profile):
        """Delete the individual private binary value from database
        @param namespace: namespace of the value
        @param key: key of the private value
        @param profile: a profile which *must* exist
        @return: deferred"""
        d = self.dbpool.runQuery("DELETE FROM private_ind_bin WHERE namespace=? AND key=? AND profile=?)", (namespace, key, self.profiles[profile]))
        d.addErrback(lambda ignore: log.error(_("Can't delete individual private binary value (%(key)s) [namespace: %(namespace)s] for [%(profile)s] in database" %
                     {"namespace": namespace, "key": key, "profile": profile})))
        return d
    ##Helper methods##

    def __getFirstResult(self, result):
        """Return the first result of a database query
        Useful when we are looking for one specific value"""
        return None if not result else result[0][0]


class Updater(object):
    stmnt_regex = re.compile(r"(?:[\w ]+(?:\([\w, ]+\))?)+")
    clean_regex = re.compile(r"^ +|(?<= ) +|(?<=,) +| +$")
    CREATE_SQL = "CREATE TABLE %s (%s)"
    INSERT_SQL = "INSERT INTO %s VALUES (%s)"
    DROP_SQL = "DROP TABLE %s"
    ALTER_SQL = "ALTER TABLE %s ADD COLUMN %s"
    RENAME_TABLE_SQL = "ALTER TABLE %s RENAME TO %s"

    CONSTRAINTS = ('PRIMARY', 'UNIQUE', 'CHECK', 'FOREIGN')
    TMP_TABLE = "tmp_sat_update"

    def __init__(self, dbpool, sat_version):
        self._sat_version = sat_version
        self.dbpool = dbpool

    def getLocalVersion(self):
        """ Get local database version
        @return: version (int)

        """
        return self.dbpool.runQuery("PRAGMA user_version").addCallback(lambda ret: int(ret[0][0]))

    def _setLocalVersion(self, version):
        """ Set local database version
        @param version: version (int)
        @return: deferred

        """
        return self.dbpool.runOperation("PRAGMA user_version=%d" % version)

    def getLocalSchema(self):
        """ return raw local schema
        @return: list of strings with CREATE sql statements for local database

        """
        d = self.dbpool.runQuery("select sql from sqlite_master where type = 'table'")
        d.addCallback(lambda result: [row[0] for row in result])
        return d

    @defer.inlineCallbacks
    def checkUpdates(self):
        """ Check if a database schema/content update is needed, according to DATABASE_SCHEMAS
        @return: deferred which fire a list of SQL update statements, or None if no update is needed

        """
        local_version = yield self.getLocalVersion()
        raw_local_sch = yield self.getLocalSchema()
        local_sch = self.rawStatements2data(raw_local_sch)
        current_sch = DATABASE_SCHEMAS['current']['CREATE']
        local_hash = self.statementHash(local_sch)
        current_hash = self.statementHash(current_sch)

        # Force the update if the schemas are unchanged but a specific update is needed
        force_update = local_hash == current_hash and local_version < CURRENT_DB_VERSION \
                        and 'specific' in DATABASE_SCHEMAS[CURRENT_DB_VERSION]

        if local_hash == current_hash and not force_update:
            if local_version != CURRENT_DB_VERSION:
                log.warning(_("Your local schema is up-to-date, but database versions mismatch, fixing it..."))
                yield self._setLocalVersion(CURRENT_DB_VERSION)
        else:
            # an update is needed

            if local_version == CURRENT_DB_VERSION:
                # Database mismatch and we have the latest version
                if self._sat_version.endswith('D'):
                    # we are in a development version
                    update_data = self.generateUpdateData(local_sch, current_sch, False)
                    log.warning(_("There is a schema mismatch, but as we are on a dev version, database will be updated"))
                    update_raw = yield self.update2raw(update_data, True)
                    defer.returnValue(update_raw)
                else:
                    log.error(_(u"schema version is up-to-date, but local schema differ from expected current schema"))
                    update_data = self.generateUpdateData(local_sch, current_sch, True)
                    update_raw = yield self.update2raw(update_data)
                    log.warning(_(u"Here are the commands that should fix the situation, use at your own risk (do a backup before modifying database), you can go to SàT's MUC room at sat@chat.jabberfr.org for help\n### SQL###\n%s\n### END SQL ###\n") % u'\n'.join("%s;" % statement for statement in update_raw))
                    raise exceptions.DatabaseError("Database mismatch")
            else:
                # Database is not up-to-date, we'll do the update
                if force_update:
                    log.info(_("Database content needs a specific processing, local database will be updated"))
                else:
                    log.info(_("Database schema has changed, local database will be updated"))
                update_raw = []
                for version in xrange(local_version + 1, CURRENT_DB_VERSION + 1):
                    try:
                        update_data = DATABASE_SCHEMAS[version]
                    except KeyError:
                        raise exceptions.InternalError("Missing update definition (version %d)" % version)
                    update_raw_step = yield self.update2raw(update_data)
                    update_raw.extend(update_raw_step)
                update_raw.append("PRAGMA user_version=%d" % CURRENT_DB_VERSION)
                defer.returnValue(update_raw)

    @staticmethod
    def createData2Raw(data):
        """ Generate SQL statements from statements data
        @param data: dictionary with table as key, and statements data in tuples as value
        @return: list of strings with raw statements

        """
        ret = []
        for table in data:
            defs, constraints = data[table]
            assert isinstance(defs, tuple)
            assert isinstance(constraints, tuple)
            ret.append(Updater.CREATE_SQL % (table, ', '.join(defs + constraints)))
        return ret

    @staticmethod
    def insertData2Raw(data):
        """ Generate SQL statements from statements data
        @param data: dictionary with table as key, and statements data in tuples as value
        @return: list of strings with raw statements

        """
        ret = []
        for table in data:
            values_tuple = data[table]
            assert isinstance(values_tuple, tuple)
            for values in values_tuple:
                assert isinstance(values, tuple)
                ret.append(Updater.INSERT_SQL % (table, ', '.join(values)))
        return ret

    def statementHash(self, data):
        """ Generate hash of template data
        useful to compare schemas

        @param data: dictionary of "CREATE" statement, with tables names as key,
                     and tuples of (col_defs, constraints) as values
        @return: hash as string
        """
        hash_ = hashlib.sha1()
        tables = data.keys()
        tables.sort()

        def stmnts2str(stmts):
            return ','.join([self.clean_regex.sub('',stmt) for stmt in sorted(stmts)])

        for table in tables:
            col_defs, col_constr = data[table]
            hash_.update("%s:%s:%s" % (table, stmnts2str(col_defs), stmnts2str(col_constr)))
        return hash_.digest()

    def rawStatements2data(self, raw_statements):
        """ separate "CREATE" statements into dictionary/tuples data
        @param raw_statements: list of CREATE statements as strings
        @return: dictionary with table names as key, and a (col_defs, constraints) tuple

        """
        schema_dict = {}
        for create_statement in raw_statements:
            if not create_statement.startswith("CREATE TABLE "):
                log.warning("Unexpected statement, ignoring it")
                continue
            _create_statement = create_statement[13:]
            table, raw_col_stats = _create_statement.split(' ',1)
            if raw_col_stats[0] != '(' or raw_col_stats[-1] != ')':
                log.warning("Unexpected statement structure, ignoring it")
                continue
            col_stats = [stmt.strip() for stmt in self.stmnt_regex.findall(raw_col_stats[1:-1])]
            col_defs = []
            constraints = []
            for col_stat in col_stats:
                name = col_stat.split(' ',1)[0]
                if name in self.CONSTRAINTS:
                    constraints.append(col_stat)
                else:
                    col_defs.append(col_stat)
            schema_dict[table] = (tuple(col_defs), tuple(constraints))
        return schema_dict

    def generateUpdateData(self, old_data, new_data, modify=False):
        """ Generate data for automatic update between two schema data
        @param old_data: data of the former schema (which must be updated)
        @param new_data: data of the current schema
        @param modify: if True, always use "cols modify" table, else try to ALTER tables
        @return: update data, a dictionary with:
                 - 'create': dictionary of tables to create
                 - 'delete': tuple of tables to delete
                 - 'cols create': dictionary of columns to create (table as key, tuple of columns to create as value)
                 - 'cols delete': dictionary of columns to delete (table as key, tuple of columns to delete as value)
                 - 'cols modify': dictionary of columns to modify (table as key, tuple of old columns to transfert as value). With this table, a new table will be created, and content from the old table will be transfered to it, only cols specified in the tuple will be transfered.

        """

        create_tables_data = {}
        create_cols_data = {}
        modify_cols_data = {}
        delete_cols_data = {}
        old_tables = set(old_data.keys())
        new_tables = set(new_data.keys())

        def getChanges(set_olds, set_news):
            to_create = set_news.difference(set_olds)
            to_delete = set_olds.difference(set_news)
            to_check = set_news.intersection(set_olds)
            return tuple(to_create), tuple(to_delete), tuple(to_check)

        tables_to_create, tables_to_delete, tables_to_check = getChanges(old_tables, new_tables)

        for table in tables_to_create:
            create_tables_data[table] = new_data[table]

        for table in tables_to_check:
            old_col_defs, old_constraints = old_data[table]
            new_col_defs, new_constraints = new_data[table]
            for obj in old_col_defs, old_constraints, new_col_defs, new_constraints:
                if not isinstance(obj, tuple):
                    raise exceptions.InternalError("Columns definitions must be tuples")
            defs_create, defs_delete, ignore = getChanges(set(old_col_defs), set(new_col_defs))
            constraints_create, constraints_delete, ignore = getChanges(set(old_constraints), set(new_constraints))
            created_col_names = set([name.split(' ',1)[0] for name in defs_create])
            deleted_col_names = set([name.split(' ',1)[0] for name in defs_delete])
            if (created_col_names.intersection(deleted_col_names or constraints_create or constraints_delete) or
                (modify and (defs_create or constraints_create or defs_delete or constraints_delete))):
                # we have modified columns, we need to transfer table
                # we determinate which columns are in both schema so we can transfer them
                old_names = set([name.split(' ',1)[0] for name in old_col_defs])
                new_names = set([name.split(' ',1)[0] for name in new_col_defs])
                modify_cols_data[table] = tuple(old_names.intersection(new_names));
            else:
                if defs_create:
                    create_cols_data[table] = (defs_create)
                if defs_delete or constraints_delete:
                    delete_cols_data[table] = (defs_delete)

        return {'create': create_tables_data,
                'delete': tables_to_delete,
                'cols create': create_cols_data,
                'cols delete': delete_cols_data,
                'cols modify': modify_cols_data
                }

    @defer.inlineCallbacks
    def update2raw(self, update, dev_version=False):
        """ Transform update data to raw SQLite statements
        @param upadte: update data as returned by generateUpdateData
        @param dev_version: if True, update will be done in dev mode: no deletion will be done, instead a message will be shown. This prevent accidental lost of data while working on the code/database.
        @return: list of string with SQL statements needed to update the base

        """
        ret = self.createData2Raw(update.get('create', {}))
        drop = []
        for table in update.get('delete', tuple()):
            drop.append(self.DROP_SQL % table)
        if dev_version:
            if drop:
                log.info("Dev version, SQL NOT EXECUTED:\n--\n%s\n--\n" % "\n".join(drop))
        else:
            ret.extend(drop)

        cols_create = update.get('cols create', {})
        for table in cols_create:
            for col_def in cols_create[table]:
                ret.append(self.ALTER_SQL % (table, col_def))

        cols_delete = update.get('cols delete', {})
        for table in cols_delete:
            log.info("Following columns in table [%s] are not needed anymore, but are kept for dev version: %s" % (table, ", ".join(cols_delete[table])))

        cols_modify = update.get('cols modify', {})
        for table in cols_modify:
            ret.append(self.RENAME_TABLE_SQL % (table, self.TMP_TABLE))
            main, extra = DATABASE_SCHEMAS['current']['CREATE'][table]
            ret.append(self.CREATE_SQL % (table, ', '.join(main + extra)))
            common_cols = ', '.join(cols_modify[table])
            ret.append("INSERT INTO %s (%s) SELECT %s FROM %s" % (table, common_cols, common_cols, self.TMP_TABLE))
            ret.append(self.DROP_SQL % self.TMP_TABLE)

        insert = update.get('insert', {})
        ret.extend(self.insertData2Raw(insert))

        specific = update.get('specific', None)
        if specific:
            cmds = yield getattr(self, specific)()
            ret.extend(cmds)
        defer.returnValue(ret)

    def update2raw_v2(self):
        """Update the database from v1 to v2 (add passwords encryptions):
            - the XMPP password value is re-used for the profile password (new parameter)
            - the profile password is stored hashed
            - the XMPP password is stored encrypted, with the profile password as key
            - as there are no other stored passwords yet, it is enough, otherwise we
              would need to encrypt the other passwords as it's done for XMPP password
        """
        xmpp_pass_path = ('Connection', 'Password')

        def encrypt_values(values):
            ret = []
            list_ = []

            def prepare_queries(result, xmpp_password):
                try:
                    id_ = result[0][0]
                except IndexError:
                    log.error("Profile of id %d is referenced in 'param_ind' but it doesn't exist!" % profile_id)
                    return defer.succeed(None)

                sat_password = xmpp_password
                d1 = PasswordHasher.hash(sat_password)
                personal_key = BlockCipher.getRandomKey(base64=True)
                d2 = BlockCipher.encrypt(sat_password, personal_key)
                d3 = BlockCipher.encrypt(personal_key, xmpp_password)

                def gotValues(res):
                    sat_cipher, personal_cipher, xmpp_cipher = res[0][1], res[1][1], res[2][1]
                    ret.append("INSERT INTO param_ind(category,name,profile_id,value) VALUES ('%s','%s',%s,'%s')" %
                               (C.PROFILE_PASS_PATH[0], C.PROFILE_PASS_PATH[1], id_, sat_cipher))

                    ret.append("INSERT INTO private_ind(namespace,key,profile_id,value) VALUES ('%s','%s',%s,'%s')" %
                               (C.MEMORY_CRYPTO_NAMESPACE, C.MEMORY_CRYPTO_KEY, id_, personal_cipher))

                    ret.append("REPLACE INTO param_ind(category,name,profile_id,value) VALUES ('%s','%s',%s,'%s')" %
                               (xmpp_pass_path[0], xmpp_pass_path[1], id_, xmpp_cipher))

                return defer.DeferredList([d1, d2, d3]).addCallback(gotValues)

            for profile_id, xmpp_password in values:
                d = self.dbpool.runQuery("SELECT id FROM profiles WHERE id=?", (profile_id,))
                d.addCallback(prepare_queries, xmpp_password)
                list_.append(d)

            d_list = defer.DeferredList(list_)
            d_list.addCallback(lambda dummy: ret)
            return d_list

        def updateLiberviaConf(values):
            try:
                profile_id = values[0][0]
            except IndexError:
                return  # no profile called "libervia"

            def cb(selected):
                try:
                    password = selected[0][0]
                except IndexError:
                    log.error("Libervia profile exists but no password is set! Update Libervia configuration will be skipped.")
                    return
                fixConfigOption('libervia', 'passphrase', password, False)
            d = self.dbpool.runQuery("SELECT value FROM param_ind WHERE category=? AND name=? AND profile_id=?", xmpp_pass_path + (profile_id,))
            return d.addCallback(cb)

        d = self.dbpool.runQuery("SELECT id FROM profiles WHERE name='libervia'")
        d.addCallback(updateLiberviaConf)
        d.addCallback(lambda dummy: self.dbpool.runQuery("SELECT profile_id,value FROM param_ind WHERE category=? AND name=?", xmpp_pass_path))
        d.addCallback(encrypt_values)
        return d
