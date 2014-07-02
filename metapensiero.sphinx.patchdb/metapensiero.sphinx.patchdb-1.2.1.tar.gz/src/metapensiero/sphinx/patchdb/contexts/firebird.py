# -*- coding: utf-8 -*-
# :Progetto:  PatchDB -- Firebird SQL script execution context
# :Creato:    sab 31 mag 2014 13:01:51 CEST
# :Autore:    Lele Gaifax <lele@metapensiero.it>
# :Licenza:   GNU General Public License version 3 or later
#

from . import logger
from .sql import SqlContext


class FirebirdContext(SqlContext):
    def makeConnection(self, dsn, username, hostname):
        import kinterbasdb as dbapi

        self.dsn = dsn
        self.username = username
        self.password = password
        logger.info(u'Connecting to %s', self.dsn)
        self.connection = dbapi.connect(dsn=self.dsn,
                                        user=self.username,
                                        password=self.password)
        self.assertions['firebird'] = True

    def setupContext(self):
        from ..patch import MAX_PATCHID_LEN

        cursor = self.connection.cursor()
        cursor.execute("SELECT rdb$relation_name"
                       " FROM rdb$relations"
                       " WHERE rdb$relation_name = 'PATCHDB'")
        result = cursor.fetchone()
        if not result:
            logger.info(u'Creating patchdb table')
            cursor.execute("CREATE TABLE patchdb ("
                           " patchid VARCHAR(%d) NOT NULL PRIMARY KEY,"
                           " revision SMALLINT NOT NULL,"
                           " applied TIMESTAMP NOT NULL"
                           ")" % MAX_PATCHID_LEN)
