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
The BioLite *catalog* table pairs metadata with the raw NGS data files
(identified by their absolute path on disk). It includes the following:

* A *unique ID* for referencing the data set. If the data is
  paired-end Illumina HiSeq data, the ID can be automatically generated using
  unique information in the Illumina header.
* *Paths* to the raw sequence data. For paired-end Illumina data, this
  is expected to be two FASTQ files (possibly compressed) containing the
  forward and reverse reads.
* *Notes* about the species, the sample preparation and origin, the species,
  IDs from NCBI and ITIS taxonomies, and the sequencing
  machine and center where the data were collected.

The catalog acts as a bridge between the BioLite diagnostics and a more
detailed laboratory information management system (LIMS) for tracking
provenance of sample preparation and data collection upstream of and during
sequencing.  It contains the minimal context needed to associate diagnostics
reports of downstream analyses with the raw sequence data, but without
replicating or reimplementing the full functionality of a LIMS.
"""

import os
import sys

from collections import namedtuple

import database
import utils

path_sep = ':'
fields = [column[0] for column in database.catalog_schema]
itis_url = 'http://www.itis.gov/servlet/SingleRpt/SingleRpt?search_topic=TSN&search_value='


CatalogRecord = namedtuple('CatalogRecord', fields)
"""
A named tuple for holding records from the :ref:`catalog-table`.
"""


# Use coloring if connected to a tty and the termcolor module is available.
def colored(string, color, **kwargs):
	return string
if sys.stdout.isatty():
	try:
		from termcolor import colored
	except ImportError:
		pass


def split_paths(paths):
	"""
	Splits a catalog path entry to return a list of paths.
	"""
	return paths.split(path_sep)


def insert(**kwargs):
	"""
	Insert or update a catalog entry, where keyword arguments specify the
	column/value pairs. If an entry for the given ID already exists, then
	the specified column/values pairs are used to update the entry. If the
	ID does not exist, a new entry is created with the specified values.
	"""
	# Validate the id.
	if 'id' not in kwargs:
		raise ValueError("'id' is a required field")
	elif ':' in kwargs['id']:
		utils.info("converting ':' to '-' in id '%s'" % kwargs['id'])
		kwargs['id'] = kwargs['id'].replace(':', '-')

	# Validate the rest of the input dict.
	if 'timestamp' in kwargs:
		utils.info("ignoring 'timestamp' field: it will be set automatically")
		kwargs.pop('timestamp')

	keys = filter(lambda k : k in kwargs and not kwargs[k] is None, fields)
	values = map(kwargs.get, keys)

	# Try an update first, to see if the id exists.
	stmt = "UPDATE catalog SET %s WHERE id=?;" % ', '.join(map('{}=?'.format, keys))
	cursor = database.execute(stmt, tuple(values + [kwargs['id']]))

	# If not, there will be no modification and the new record should be
	# inserted. The timestamp is only set on the initial insert.
	if not cursor.rowcount:
		stmt = "INSERT INTO catalog (timestamp,%s) VALUES (DATETIME('now'),%s);" % (
				','.join(keys), ','.join(['?'] * len(keys))) 
		database.execute(stmt, values)

	return kwargs['id']


def select(id):
	"""
	Returns a CatalogRecord object for the given catalog ID, or :keyword:None if
	the ID is not found in the catalog.
	"""
	row = database.execute("SELECT * FROM catalog WHERE id=?;", (id,)).fetchone()
	if row:
		return CatalogRecord(*row)
	else:
		return None


def select_all():
	"""
	Yields a list of CatalogRecord objects for all entries in the catalog,
	ordered with the default ordering that SQLite provides.
	"""
	for row in database.execute("SELECT * FROM catalog;"):
		yield CatalogRecord(*row)


def search(string):
	"""
	Yields a list of CatalogRecord objects for all entries in the catalog
	with an indexed column matching the given search `string`. The indexed
	columns are all the columns in the catalog except `paths`.
	"""
	stmt = "SELECT * FROM catalog WHERE id LIKE ? OR "
	stmt += ' OR '.join([field + " LIKE ?" for field in database.catalog_index])
	stmt += ';'
	values = (string,) * (len(database.catalog_index) + 1)
	for row in database.execute(stmt, values):
		yield CatalogRecord(*row)


def make_record(**kwargs):
	"""
	Returns a CatalogRecord object by mapping the provided keyword arguments
	to field names.
	"""
	values = list()
	for field in CatalogRecord._fields:
		values.append(kwargs.get(field, ''))
	return CatalogRecord(*values)


def print_record(*args):
	"""
	A human-readable printout of CatalogRecord `record`, using colors if the
	current tty supports it and the `termcolor` module is installed.
	"""
	for arg in args:
		if isinstance(arg, basestring):
			record = select(arg)
		else:
			record = arg
		print "%s [%s]" % (
			colored(record.id, 'blue', attrs=['bold']),
			record.timestamp)
		if record.paths:
			for path in split_paths(record.paths):
				line = [path]
				try:
					size = os.stat(path).st_size
					line.append('(%s)' % utils.human_readable_size(size/1024, 1))
				except OSError:
					utils.info("could not stat file '%s'" % path)
				print colored(' '.join(line), 'red')
		for field, value in zip(fields[2:-1], record[2:-1]):
			print "  %s: %s" % (colored(field, 'green'), value)

