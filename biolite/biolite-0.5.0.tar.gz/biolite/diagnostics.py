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
Diagnostics usually come in the form of plots or summary statistics.
They can serve many purposes, such as:

* diagnosing problems in sample preparation and optimizing future preparations;
* providing feedback on the sequencing itself, e.g. on read quality;
* implementing 'sanity checks' at intermediate steps of analysis;
* finding optimal parameters by comparing previous runs;
* recording computational and storage demands, and predicting future demands.

The *diagnostics* database table archives summary statistics that can be
accessed across multiple stages of a pipeline, from different pipelines, and in
HTML reports.

A diagnostics record looks like:

::

    catalog_id | run_id | entity | attribute | value | timestamp

The `entity` field acts as a namespace to prevent attribute collisions, since
the same attribute name can arise multiple times within a pipeline run.

When running a BioLite pipeline, the default entity is the pipeline name plus
the stage name, so that values can be traced to the pipeline and stage during
which they were entered. Entries in the diagnostics table can include paths to
derivative files, which can be summaries of intermediate files that are used to
generate reports or intermediate data files that serve as input to other stages
and pipelines.

Initializing
------------

Before logging to diagnostics, your script must initialize this module with a
BioLite catalog ID and a name for the run using the `init` method. This will
return a new run ID from the :ref:`runs-table`. Optionally, you can pass an
existing run ID to `init` to continue a previous run.

Diagnostics are automatically initialized by the Pipeline and IlluminaPipeline
classes in the :ref:`pipeline-module`.

Logging a record
----------------

Use the `log` function described below.

Detailed system utilization statistics, including memory high-water marks and
compute wall-time are recorded automatically (by the wrapper base class) for
any wrapper that your pipeline calls, and for the overall pipeline itself.

Provenance
----------

Because every wrapper call is automatically logged, the diagnostics table holds
a complete non-executable history of the analysis, which complements the
original scripts that were used to run the analysis. In combination, the
diagnostics table and original scripts provide provenance for all analyses.

"""

import ast
import datetime
import getpass
import os
import re
import resource
import socket
import sys
import time
from collections import defaultdict, OrderedDict, namedtuple
from biolite import config
from biolite import database
from biolite import utils

# Internal data.
_id = None
_run_id = None
_diag_file = sys.stderr
_prog_file = sys.stderr
_diag_cache = defaultdict(dict)
_prog_cache = dict()

# Used by parse_program_output: compile once when this module loads.
_parse_pattern = re.compile(r"^\[biolite\.?(\w*)\]\s+(\S+)=(\S+)")
OutputPattern = namedtuple('OutputPattern', "re entity attr")

# External data.
prefix = []
INIT = '__init__'
EXIT = '__exit__'
RUSAGE = '__rusage__'
INSERT_SIZE = 'insert_size.estimate_insert.bowtie2'
run_fields = [column[0] for column in database.runs_schema]
diagnostic_fields = [column[0] for column in database.diagnostics_schema]
Run = namedtuple('Run', run_fields)


### Helper functions. ###

def _escape(s):
	return s.replace('\t','\\t').replace('\n','\\n')


def _unescape(s):
	return s.replace('\\t','\t').replace('\\n','\n')


def timestamp():
	"""
	Returns the current time in ISO 8601 format, e.g.
	:samp:`YYYY-MM-DDTHH:MM:SS[.mmmmmm][+HH:MM]`.
	"""
	return datetime.datetime.now().isoformat()


def str2list(data):
	"""
	Converts a diagnostics string with key `name` in `self.data` into a
	list, by parsing it as a typical Python list representation
	:samp:`[item1, item2, ... ]`.
	"""
	return ast.literal_eval(data)


def get_run_id():
	"""Returns the `run_id` (as a string)"""
	return _run_id


def get_entity():
	"""
	Returns the current `entity` as a dot-delimited string.
	"""
	return '.'.join(prefix)


### Initialization. ###

def init(id, name, run_id=None, workdir=os.getcwd()):
	"""
	By default, appends to a file `diagnostics.txt` in the current working
	directory, but you can override this with the `workdir` argument.

	You must specify a catalog `id` and a `name` for the run. If no `run_id`
	is specified, an auto-incremented run ID will be allocated by inserting
	a new row into the :ref:`runs-table`.

	Returns the `run_id` (as a string).
	"""
	global _id, _diag_file, _prog_file, _run_id

	_id = id

	if run_id is None:
		cursor = database.execute("""
			INSERT INTO runs (id,name,hostname,username,timestamp)
			VALUES(?,?,?,?,?);""",
			(_id, name, socket.gethostname(), getpass.getuser(), timestamp()))
		_run_id = str(cursor.lastrowid)

		# For new runs, the scratch directory is set to:
		# <workdir>/<name>-<run_id>
		workdir = os.path.join(workdir, '%s-%s' % (name, _run_id))
		utils.safe_mkdir(workdir)
		os.chdir(workdir)

	else:
		_run_id = str(run_id)

	_diag_file = open(os.path.join(workdir, 'diagnostics.txt'), 'a')
	_prog_file = open(os.path.join(workdir, 'programs.txt'), 'a')

	return _run_id


def check_init():
	"""
	Aborts if the biolite.diagnostics.init() has not been called yet.
	"""
	if _run_id == None:
		utils.die("diagonistics have not been initialized")


### Cache functions. ###

def merge():
	"""
	Merges the diagnostics and program caches into the SQLite database.
	"""
	database.execute("BEGIN")

	for entity in _diag_cache:
		for attribute, values in _diag_cache[entity].iteritems():
			database.execute("""
				REPLACE INTO diagnostics
					(id,run_id,entity,attribute,value,timestamp)
				VALUES(?,?,?,?,?,?);""",
				(_id, _run_id, entity, attribute, values[0], values[1]))

	for binary, values in _prog_cache.iteritems():
		database.execute("""
			REPLACE INTO programs (binary,name,version)
			VALUES (?,?,?);""", (binary, values[0], values[1]))

	database.execute("UPDATE runs SET done=? WHERE run_id=?", (1, _run_id))

	database.execute("COMMIT")


def merge_cwd(run_id):
	"""
	Merges the 'diagnostics.txt' and 'programs.txt' in the current working
	directory (cwd) into the diagnostics database.
	"""
	global _run_id, _diag_cache, _prog_cache
	_run_id_save = _run_id
	_run_id = str(run_id)
	with open('diagnostics.txt', 'r') as f:
		for line in f:
			# fields
			# id,run_id,entity,attribute,value,timestamp
			row = map(_unescape, line.rstrip('\n').split('\t', 5))
			if row[1] == _run_id:
				_diag_cache[row[2]][row[3]] = (row[4], row[5])
	with open('programs.txt', 'r') as f:
		for line in f:
			# fields
			# binary_hash,name,version
			row = map(_unescape, line.rstrip('\n').split('\t', 2))
			_prog_cache[row[0]] = (row[1], row[2])
	merge()
	_run_id = _run_id_save


def load_cache():
	"""
	Similar to a merge, but loads the local diagnostics file into an
	in-memory cache instead of the SQLite database.

	Uses the filename specified with `name`, or the file `diagnostics.txt` in
	the current working directory (default).
	"""
	global _diag_file, _diag_cache, _prog_file, _prog_cache

	# Close local diagnostics file so we can reopen in read mode.
	check_init()
	name = _diag_file.name
	_diag_file.close()

	with open(name, 'r') as f:
		for line in f:
			# fields
			# id,run_id,entity,attribute,value,timestamp
			row = map(_unescape, line.rstrip('\n').split('\t', 5))
			if row[1] == _run_id:
				_diag_cache[row[2]][row[3]] = (row[4], row[5])

	# Reopen local diagnostics file in append mode.
	_diag_file = open(name, 'a')

	# Do the same for the programs file.
	name = _prog_file.name
	_prog_file.close()

	with open(name, 'r') as f:
		for line in f:
			# fields
			# binary_hash,name,version
			row = map(_unescape, line.rstrip('\n').split('\t', 2))
			_prog_cache[row[0]] = (row[1], row[2])

	_prog_file = open(name, 'a')


### Logging functions. ###

def log(attribute, value):
	"""
	Log an `attribute`/`value` pair in the diagnostics using the currently set
	`entity`. The pair is written to the local diagnostics text file and also
	into the local in-memory cache.
	"""
	global _id, _run_id, _diag_file, _diag_cache

	ts = timestamp()
	attribute = str(attribute)
	value = str(value)
	entity = get_entity()

	if _run_id is None:
		if entity:
			entity = "[biolite:diagnostics:%s]" % entity
		else:
			entity = "[biolite:diagnostics]"
		row = map(_escape, (entity, attribute, value, ts))
	else:
		# Escape tab and newline.
		row = map(_escape, (_id, _run_id, entity, attribute, value, ts))

	print >> _diag_file, '\t'.join(row)
	_diag_file.flush()

	# Create a cached copy locally, in case the pipeline wants to lookup a
	# value before the merge to the global database happens.
	_diag_cache[entity][attribute] = (value, ts)


def log_entity(attribute, value):
	"""
	Log an `attribute`/`value` pair in the diagnostics, where the `attribute`
	can contain an `entity` that is separated from the attribute name by dots.
	Example:

	    log_entity('a.b.x', 1)

	would store the attribute/value pair (x,1) in an entity 'a.b' appended to
	the current `entity`.
	"""
	entity = attribute.split('.')
	for e in entity[:-1]: prefix.append(e)
	log(entity[-1], value)
	for _ in entity[:-1]: prefix.pop()


def log_exit(attribute, value):
	"""
	Log an `attribute`/`value` pair in the diagnostics in the special EXIT
	entity that is used to pass values between pipelines.
	"""
	global prefix
	prefix_save = prefix
	prefix = [EXIT]
	log(attribute, value)
	prefix = prefix_save


def log_path(path, log_prefix=None):
	"""
	Logs a `path` by writing these attributes at the current `entity`, with
	an optional prefix for this entry:
	1) the full `path` string
	2) the full `path` string, converted to an absolute path by os.path.abspath()
	3) the `size` of the file/directory at the path (according to `os.stat`)
	4) the `access time` of the file/directory at the path (according to `os.stat`)
	5) the `modify time` of the file/directory at the path (according to `os.stat`)
	6) the `permissions` of the file/directory at the path (according to `os.stat`)
	"""
	if log_prefix is not None:
		prefix.append(log_prefix)

	log('path', path)
	log('abspath', os.path.abspath(path))

	stat = os.stat(path)
	log('size', stat.st_size)
	log('atime', datetime.datetime.fromtimestamp(stat.st_atime).isoformat())
	log('mtime', datetime.datetime.fromtimestamp(stat.st_mtime).isoformat())
	log('mode', oct(stat.st_mode))

	if log_prefix is not None:
		prefix.pop()


def log_dict(d, prefix=None, filter=False):
	"""
	Log a dictionary `d` by calling `log` for each key/value pair.
	"""
	if prefix is None:
		prefix = ''
	else:
		prefix += '.'
	for key, val in d.iteritems():
		if filter and not val:
			continue
		log(prefix + key, val)


def log_rusage(log_prefix=RUSAGE):
	"""
	Log the current resource usage with a timestamp. Returns a `dict` with
	the fields:

	* timestamp
	* systime (ru_stime)
	* usertime (ru_utime)
	* maxrss (ru_maxrss)
	"""
	self = resource.getrusage(resource.RUSAGE_SELF)
	children = resource.getrusage(resource.RUSAGE_CHILDREN)

	rusage = {
		'timestamp': time.time(),
		'systime': self.ru_stime + children.ru_stime,
		'usertime': self.ru_utime + children.ru_utime,
		'maxrss': self.ru_maxrss + children.ru_maxrss}

	if config.uname == 'Darwin':
		rusage['maxrss'] /= 1024

	if log_prefix is not None:
		prefix.append(log_prefix)

	log_dict(rusage)

	if log_prefix is not None:
		prefix.pop()

	return rusage


def log_program_version(name, version, path):
	"""
	Enter the version string and a hash of the binary file at `path` into the
	programs table.
	"""
	if os.path.exists(path):
		binary_hash = utils.md5sum(path)
		# Store new hashes in the programs cache/file.
		if binary_hash not in _prog_cache:
			if _run_id is None:
				entity = "[biolite:program]"
				row = map(_escape, (entity, binary_hash, name, version))
			else:
				# Escape tab and newline.
				row = map(_escape, (binary_hash, name, version))
			print >> _prog_file, '\t'.join(row)
			_prog_file.flush()
			_prog_cache[binary_hash] = (name, version)
		return binary_hash
	else:
		return None


def log_program_output(filename, patterns=None):
	"""
	Read backwards through a program's output to find any [biolite] markers,
	then log their key=value pairs in the diagnostics.

	A marker can specify an entity suffix with the form [biolite.suffix].

	[biolite.profile] markers are handled specially, since mem= and vmem=
	entries need to be accumulated. These are inserted into a program's output
	on Linux systems by the preloaded memusage.so library.

	You can optionally include a list of additional patterns, specified as
	OutputPattern tuples with:

	  (regular expression string, entity, attribute)

	and the first line of program output matching the pattern will be logged
	to that entity and attribute name. The value will be the subexpressions
	matched by the regular expression, either a single value if there is one
	subexpression, or a string of the tuple if there are more.
	"""
	profile = dict()
	lines = list()

	with open(filename, 'r') as f:
		for line in utils.readlines_reverse(f):
			match = _parse_pattern.match(line)
			if match:
				entity, attr, val = match.groups()
				# Stop after encountering a previous timestamp.
				if attr == 'timestamp':
					break
				# Accumulate memory profile values.
				if entity == 'profile' and (attr == 'mem' or attr == 'vmem'):
					profile[attr] = max(profile.get(attr, 0), int(val))
				else:
					if entity:
						prefix.append(entity)
					log(attr, val)
					if entity:
						prefix.pop()
			elif patterns:
				lines.append(line)

	prefix.append('profile')
	log_dict(profile)
	prefix.pop()

	while lines and patterns:
		line = lines.pop(0)
		for i, pattern in enumerate(patterns):
			match = re.match(pattern.re, line)
			if match:
				if pattern.entity:
					prefix.append(pattern.entity)
				m = match.groups()
				if len(m) == 1:
					log(pattern.attr, m[0])
				else:
					log(pattern.attr, m)
				if pattern.entity:
					prefix.pop()
				patterns.pop(i)
				break


### Lookup functions. ###

def lookup(run_id, entity):
	"""
	Returns a dictionary of `attribute`/`value` pairs for the given `run_id` and
	`entity` in the SQLite database.

	Returns an empty dictionary if no records are found.
	"""
	stmt = """
		SELECT attribute, value
		FROM diagnostics
		WHERE run_id=? AND entity=?
		ORDER BY timestamp;"""
	return dict(database.execute(stmt, (run_id, entity)))


def local_lookup(entity):
	"""
	Similar to `lookup`, but queries the in-memory cache instead of the SQLite
	database. This can provide lookups when the local diagnostics text file
	has not yet been merged into the SQLite database (for instance, after
	restarting a pipeline that never completed, and hence never reached a
	diagnostics merge).

	Returns an empty dictionary if no records are found.
	"""
	d = _diag_cache.get(entity, dict())

	# Return a new dict with only the value field (not the timestamp).
	return dict([(k, v[0]) for k, v in d.iteritems()])


def lookup_like(run_id, entity):
	"""
	Similar to `lookup`, but allows for wildcards in the entity name (either
	the SQL '%' wildcard or the more standard UNIX '*' wildcard).

	Returns a dictinoary of dictionaries keyed on [`entity`][`attribute`].
	"""
	stmt = """
		SELECT entity, attribute, value
		FROM diagnostics
		WHERE run_id=? AND entity LIKE ?
		ORDER BY timestamp;"""
	values = OrderedDict()
	for row in database.execute(stmt, (run_id, entity.replace('*', '%'))):
		try:
			values[row[0]][row[1]] = row[2]
		except KeyError:
			values[row[0]] = dict([(row[1], row[2])])
	return values


def lookup_by_id(id, entity):
	if id is None:
		global _id
		id = _id
	stmt = """
		SELECT attribute, value
		FROM runs JOIN diagnostics ON runs.run_id=diagnostics.run_id
		WHERE runs.id=? AND runs.hidden=0 AND entity=?
		ORDER BY runs.run_id;"""
	return dict(database.execute(stmt, (id, entity)))


def lookup_attribute(run_id, attribute):
	"""
	Returns each value for the given `attribute` found in all entities for
	the given `run_id`, as an iterator of (entity, value) tuples.
	"""
	stmt = """
		SELECT entity, value
		FROM diagnostics
		WHERE run_id=? AND attribute=?
		ORDER BY timestamp;"""
	return database.execute(stmt, (run_id, attribute))


def lookup_entities(run_id):
	stmt = "SELECT entity FROM diagnostics WHERE run_id=?;"
	return frozenset(row[0] for row in database.execute(stmt, (run_id,)))


def lookup_pipelines(run_id):
	stmt = "SELECT DISTINCT entity FROM diagnostics WHERE run_id=?;"
	rows = database.execute(stmt, (run_id,))
	return frozenset(
			row[0].partition('.')[0] for row in rows
			if not row[0].startswith('__'))


def lookup_run(run_id):
	stmt = "SELECT * FROM runs WHERE run_id=?;"
	row = database.execute(stmt, (run_id,)).fetchone()
	if not row:
		utils.info("no run found for run id '%s'" % run_id)
		return None
	return Run(*row)


def lookup_runs(id=None, name=None, order='ASC', hidden=True):
	where = []
	args = []
	if id is not None:
		where.append("id=?")
		args.append(id)
	if name is not None:
		where.append("name=?")
		args.append(name)
	if not hidden:
		where.append("hidden=0")
	if where: where = 'WHERE ' + ' AND '.join(where)
	else: where = ''
	stmt = "SELECT * FROM runs %s ORDER BY run_id %s;" % (where, order)
	for row in database.execute(stmt, args):
		yield Run(*row)


def lookup_prev_run(id, previous, *args):
	"""
	Lookup either the specific `previous` run, or if `previous` is None,
    the latest run of a pipeline with a name in the `args` list.

	Will only return a run that is finished and not hidden.

	Returns None if no run can be found.
	"""
	if previous:
		return lookup_run(previous)
	elif len(args):
		where = []
		for name in args:
			where.append('name="%s"' % name)
		stmt = """
			SELECT *
			FROM runs
			WHERE id=? AND done=1 AND hidden=0 AND (%s)
			ORDER BY run_id
			DESC LIMIT 1;""" % (' OR '.join(where))
		row = database.execute(stmt, (id,)).fetchone()
		if row:
			return Run(*row)


def lookup_prev_val(id, previous, value, key, *args, **kwargs):
	"""
	Determine a value based on the following order:

	* use the specified `value` if it is not None
	* lookup the `previous` run ID if it is not None, and select `key` in the
	  exit diagnostics
	* lookup the latest run of a pipeline in `*args` and select `key` from
	  the exit diagnostics

	Will only search runs that are finished and not hidden.

	Returns None if no value can be determined.
	"""
	if not value is None and not value is []:
		return value
	elif previous:
		return lookup_prev_run(id, previous).get(key)
	elif len(args):
		where = []
		for name in args:
			where.append('name="%s"' % name)
		stmt = """
			SELECT name, run_id
			FROM runs
			WHERE id=? AND done=1 AND hidden=0 AND (%s)
			ORDER BY run_id
			DESC LIMIT 1;""" % (' OR '.join(where))
		row = database.execute(stmt, (id,)).fetchone()
		if row:
			utils.info("using previous '%s' run id %d" % row)
			return lookup(row[1], EXIT).get(key)


def lookup_insert_size():
	"""
	For tools that need insert sizes, use available estimates from the
	diagnostics database, or resort to the default values in the BioLite
	configuration file.

	Returns a Struct with the fields `mean`, `stddev` and `max`.
	"""
	global INSERT_SIZE
	# Try the diagnostics cache, if the estimate is from an earlier stage
	# of the current pipeline.
	size = utils.Struct(
			mean=float(local_lookup(INSERT_SIZE).get('mean', 0)),
			stddev=float(local_lookup(INSERT_SIZE).get('stddev', 0)),
			max=0.0)
	if not size.mean:
		# Search the global diagnostics database (passing None to lookup_by_id
		# will use the currently initialized id in diagnostics.
		values = lookup_by_id(None, INSERT_SIZE)
		size.mean = float(values.get('mean', 0))
		size.stddev = float(values.get('stddev', 0))
	if not size.mean:
		size.mean = int(config.get_resource('max_insert_size'))
		size.stddev = int(config.get_resource('mean_insert_size'))
	if not size.max:
		size.max = size.mean + \
					size.stddev * int(config.get_resource('max_insert_stddev'))
	return size


def dump(run_id):
	stmt = """
		SELECT entity, attribute, value, timestamp
		FROM diagnostics
		WHERE run_id=?
		ORDER BY timestamp;"""
	for row in database.execute(stmt, (run_id,)):
		print '|'.join([str(x) for x in row])


def dump_commands(run_id):
	stmt = """
		SELECT value
		FROM diagnostics
		WHERE run_id=? AND attribute='command' ORDER BY timestamp DESC"""
	for row in database.execute(stmt, (run_id,)):
		print row[0]


def dump_by_id(id):
	stmt = "SELECT * FROM diagnostics WHERE id=? ORDER BY timestamp;"
	for row in database.execute(stmt, (id,)):
		print '|'.join([str(x) for x in row[1:]])


def dump_all():
	stmt = "SELECT * FROM diagnostics ORDER BY timestamp;"
	for row in database.execute(stmt):
		print '|'.join([str(x) for x in row])


def hide_run(*args):
	stmt = "UPDATE runs SET hidden=? WHERE run_id=?;"
	database.execute('BEGIN')
	for run_id in args:
		database.execute(stmt, (1, run_id))
	database.execute('COMMIT')


def unhide_run(*args):
	stmt = "UPDATE runs SET hidden=? WHERE run_id=?;"
	database.execute('BEGIN')
	for run_id in args:
		database.execute(stmt, (0, run_id))
	database.execute('COMMIT')


def dump_programs():
	sep = '=' * 80
	for row in database.execute("SELECT * FROM programs;"):
		print "%s|%s\n%s\n%s\n" % (row[0], row[1], sep, row[2])

# vim: noexpandtab ts=4 sw=4
