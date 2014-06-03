# -*- coding: utf-8 -*-
# :Progetto:  PatchDB -- MySQL script execution context
# :Creato:    lun 02 giu 2014 09:21:14 CEST
# :Autore:    Lele Gaifax <lele@metapensiero.it>
# :Licenza:   GNU General Public License version 3 or later
#

from . import logger
from .sql import SqlContext


class MySQLContext(SqlContext):
    def makeConnection(self, host, db, username, password):
        import cymysql as dbapi
        import re

        self.host = host
        self.db = db
        self.username = username
        self.password = password
        logger.info(u'Connecting to %s/%s', self.host, self.db)
        self.connection = dbapi.connect(host=self.host,
                                        user=self.username,
                                        passwd=self.password,
                                        db=self.db,
                                        use_unicode=True)
        cursor = self.connection.cursor()
        cursor.execute("SELECT version()")
        v = cursor.fetchone()
        m = re.match('(\d+)\.(\d+)\.(\d+)', v[0])
        assert m, u"Could not determine mysql version"
        version = tuple([int(x) for x in m.group(1, 2)])

        self.assertions.update({
            'mysql': True,
            'mysql_6_x': (6,0) <= version < (7,0),
            'mysql_5_x': (5,0) <= version < (6,0),
            'mysql_4_x': (4,0) <= version < (5,0),
            })

    def setupContext(self):
        from cymysql.err import ProgrammingError
        from ..patch import MAX_PATCHID_LEN

        cursor = self.connection.cursor()
        try:
            cursor.execute("DESCRIBE patchdb")
        except ProgrammingError:
            logger.info(u'Creating patchdb table')
            cursor.execute("CREATE TABLE patchdb ("
                           " patchid VARCHAR(%d) NOT NULL PRIMARY KEY,"
                           " revision SMALLINT NOT NULL,"
                           " applied TIMESTAMP NOT NULL"
                           ")" % MAX_PATCHID_LEN)

    def classifyError(self, exc):
        msg = exc.errmsg
        if hasattr(msg, 'decode'):
            try:
                msg = msg.decode('utf-8')
            except UnicodeDecodeError:
                msg = msg.decode('latin1', 'ignore')
        code = exc.errno
        msg = u'[%d] %s' % (code, msg)
        # See http://dev.mysql.com/doc/refman/5.5/en/error-messages-server.html
        syntaxerror = code in (1064, 1149)
        nonexistingobj = code in (1051, 1091, 1146)
        return msg, syntaxerror, nonexistingobj
