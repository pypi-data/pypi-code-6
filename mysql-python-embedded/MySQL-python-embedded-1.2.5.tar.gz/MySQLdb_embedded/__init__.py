"""MySQLdb_embedded - A DB API v2.0 compatible interface to MySQL.

This package is a wrapper around _mysql_embedded, which mostly implements the
MySQL C API, and MySQL-python.

See the MySQL-python and MySQL documentation for more info.

"""

from MySQLdb_embedded.release import version_info as embedded_version_info

import _mysql_embedded

if embedded_version_info != _mysql_embedded.version_info:
    raise ImportError("this is MySQLdb_embedded version %s, but _mysql_embedded is version %r" %
                      (embedded_version_info, _mysql_embedded.version_info))

from MySQLdb import *
if version_info != embedded_version_info:
    raise ImportError("this is MySQLdb_embedded version %s, but _mysql is version %r" %
                      (embedded_version_info, _mysql.version_info))

from _mysql_embedded import *
from MySQLdb_embedded.connections import Connection
connect = Connect = Connection
