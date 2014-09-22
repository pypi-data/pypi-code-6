# BioLite - Tools for processing gene sequence data and automating workflows
# Copyright (c) 2012-2014 Brown University. All rights reserved.
#
# This file is part of BioLite.
#
# BioLite is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BioLite is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BioLite.  If not, see <http://www.gnu.org/licenses/>.

"""
Provides an interface to the underlying SQLite database that stores the BioLite
**catalog**, **runs**, **diagnostics**, and **programs** tables.

.. _catalog-table:

catalog Table
-------------

::

%s

.. _runs-table:

runs Table
----------

::

%s

diagnostics Table
-----------------

::

%s

.. _programs-table:

programs Table
--------------

::

%s
"""

import os
import sqlite3
import textwrap

import config
import utils


# Interal data and helper functions.
_db = None


def _create_sql(name, schema, index):
	sql = [" CREATE TABLE %s (" % name]
	sql += ["   %s %s," % s for s in schema[:-1]]
	sql += ["   %s %s);" % schema[-1]]
	sql += [" CREATE INDEX {0}_{1} ON {0}({1});".format(name, i) for i in index]
	return '\n'.join(sql)


def _create_db():
	global _db
	_db.executescript(catalog_sql + runs_sql + diagnostics_sql + programs_sql)


# External data.
runs_schema = (
	('done', "INTEGER DEFAULT '0'"),
	('run_id', "INTEGER PRIMARY KEY AUTOINCREMENT"),
	('id', 'VARCHAR(256)'),
	('name', 'VARCHAR(32)'),
	('hostname', 'VARCHAR(32)'),
	('username', 'VARCHAR(32)'),
	('timestamp', 'DATETIME'),
	('hidden', "INTEGER DEFAULT '0'"))

runs_index = ('id', 'name', 'done', 'hidden')

runs_sql = _create_sql('runs', runs_schema, runs_index)

diagnostics_schema = (
	('id', 'VARCHAR(256)'),
	('run_id', 'INTEGER'),
	('entity', 'VARCHAR(128)'),
	('attribute', 'VARCHAR(32)'),
	('value', 'TEXT'),
	('timestamp', 'DATETIME'))
diagnostics_index = ('id', 'run_id', 'entity', 'attribute', 'timestamp')

diagnostics_sql = _create_sql('diagnostics', diagnostics_schema, diagnostics_index) + "CREATE UNIQUE INDEX entry ON diagnostics(run_id,entity,attribute);"

catalog_schema = (
	('id', 'VARCHAR(256) PRIMARY KEY NOT NULL'),
	('paths', 'TEXT'),
	('species', 'VARCHAR(256)'),
	('ncbi_id', 'INTEGER'),
	('itis_id', 'INTEGER'),
	('extraction_id', 'VARCHAR(256)'),
	('library_id', 'VARCHAR(256)'),
	('library_type', 'VARCHAR(256)'),
	('individual', 'VARCHAR(256)'),
	('treatment', 'VARCHAR(256)'),
	('sequencer', 'VARCHAR(256)'),
	('seq_center', 'VARCHAR(256)'),
	('note', 'TEXT'),
	('sample_prep', 'TEXT'),
	('timestamp', 'DATETIME'))

# Index all fields in the catalog, except id (already a key) and paths.
catalog_index = [column[0] for column in catalog_schema[2:]]
catalog_sql = _create_sql('catalog', catalog_schema, catalog_index)

programs_schema = (
	('binary', 'CHAR(32) PRIMARY KEY NOT NULL'),
	('name', 'VARCHAR(256)'),
	('version', 'TEXT'))

programs_index = ('name',)
programs_sql = _create_sql('programs', programs_schema, programs_index)

# Add the SQL schema for each table to the documentation.
__doc__ %= (catalog_sql, runs_sql, diagnostics_sql, programs_sql)


# Public functions. ###

def connect():
	"""
	Establish a gobal database connection.
	"""
	global _db
	if _db is None:
		path = config.get_resource('database')
		exists = os.path.isfile(path)
		if not exists:
			utils.safe_mkdir(os.path.dirname(path))
		_db = sqlite3.connect(path, timeout=60.0, isolation_level=None)
		if not exists:
			_create_db()


def disconnect():
	"""
	Close the global database connection, set it to None.
	"""
	global _db
	if _db is not None:
		_db.close()
	_db = None


def execute(*args, **kwargs):
	global _db
	if _db is None:
		connect()
	try:
		return _db.execute(*args, **kwargs)
	except sqlite3.InterfaceError as e:
		utils.die(
			"sqlite error:\n", e, '\n',
			"SQL:", textwrap.dedent(args[0]), '\n',
			"Values:", args[1], '\n')

