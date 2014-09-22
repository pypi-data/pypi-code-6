# Agalma - Tools for processing gene sequence data and automating workflows
# Copyright (c) 2012-2014 Brown University. All rights reserved.
#
# This file is part of Agalma.
#
# Agalma is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Agalma is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Agalma.  If not, see <http://www.gnu.org/licenses/>.

"""
Provides an interface to the underlying SQLite database that stores the
Agalma **sequences** and **homology** tables.
"""

import os
import re
import sqlite3
import textwrap
from collections import defaultdict, namedtuple
from agalma import config
from biolite import catalog
from biolite import diagnostics
from biolite import utils

_db = None

# Performance tuning recommended by:
# http://stackoverflow.com/questions/784173
pragma = """
	PRAGMA main.page_size=65536;
	PRAGMA main.cache_size=4096;
	PRAGMA main.locking_mode=EXCLUSIVE;
	PRAGMA main.synchronous=NORMAL;
	PRAGMA main.journal_mode=WAL;
	PRAGMA main.temp_store=MEMORY;"""

def _create_sql(name, schema, index):
	sql = [" CREATE TABLE %s (" % name]
	sql += ["   %s %s," % s for s in schema[:-1]]
	sql += ["   %s %s);" % schema[-1]]
	sql += [" CREATE INDEX {0}_{1} ON {0}({1});".format(name, i) for i in index]
	return '\n'.join(sql)

sequences_schema = (
	('sequence_id', 'INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL'),
	('run_id', 'INTEGER'),			# Foreign key to runs table, refers to the run_id of the process that populates the database
	('catalog_id', 'VARCHAR(256)'),			# Foreign key to catalog.id, could be obtained through join with run table but including it here makes things more robust
	('gene', 'VARCHAR(256)'),			# Parsed from the header
	('isoform', 'INTEGER'),			# Parsed from the header
	('confidence', 'FLOAT'),			# Parsed from the header
	('expression', 'FLOAT'),			# Parsed from the header
	('nucleotide_seq', 'TEXT'),			# Nucleotide sequence from either exemplars or transcripts file (which is loaded will be up to the user)
	('nucleotide_quality', 'TEXT'),			# Quality string corresponding to nucleotide_seq, NULL for most assemblers (including oases)
	('protein_seq', 'TEXT'),			# Parsed from the prot4EST output, for now will be null for non-exemplars since they aren't translated.
	('translation_method', 'VARCHAR(256)'),			# A string with the program and method, eg "prot4EST SIMILARITY", only applies when protein_seq is not NULL
	('genome_type', 'CHAR(1)'),				# Nuclear, mitochondrial, plastid
	('molecule_type', 'CHAR(1)'),			# Protein coding, small/large ribosomal
	('blast_hit', 'TEXT'),			# The name, gi, and evalue of the top blastx hit, could be parsed from the nucleotide fasta header or the blastx report. Provides a human readable label.
	('nucleotide_header', 'TEXT'),	# The header in the nucleotide fasta from which the sequence was loaded
	('protein_header', 'TEXT'),	# The header in the protein fasta from which the sequence was loaded
	('note', 'TEXT')			# Useful for user specified information')
)

sequences_index = ('run_id', 'gene')
sequences_sql = _create_sql('sequences', sequences_schema, sequences_index)

homology_schema = (
	('run_id', 'INTEGER'),			# Foreign key to runs table, refers to the run_id of the process that assigned homology and populated this table
	('component_id', 'INTEGER'),	# The id assigned to the component during graph processing
	('sequence_id', 'INTEGER'),		# Foreign key to sequences table, identifies the sequence assigned to a particular component
)

homology_index = ('run_id', 'component_id')
homology_sql = _create_sql('homology', homology_schema, homology_index)

def _create_db():
	_db.executescript(sequences_sql + homology_sql)

def _connect():
	"""
	Establish a gobal database connection.
	"""
	global _db
	path = config.get_resource('agalma_database')
	exists = os.path.isfile(path)
	if not exists: utils.safe_mkdir(os.path.dirname(path))
	_db = sqlite3.connect(path, timeout=60.0, isolation_level=None)
	_db.executescript(pragma)
	if not exists: _create_db()

def disconnect():
	"""
	Close the global database connection, set it to None, and set the
	`execute` function to auto-reconnect.
	"""
	global _db
	if _db is not None: _db.close()
	_db = None

def execute(*args, **kwargs):
	"""
	Call through to sqlite3.execute; connects to database if not already
	connected.
	"""
	if _db is None: _connect()
	try:
		return _db.execute(*args, **kwargs)
	except sqlite3.InterfaceError as e:
		utils.die(
			"sqlite error:\n", e, '\n',
			"SQL:", textwrap.dedent(args[0]), '\n',
			"Values:", args[1:], '\n')
	except sqlite3.OperationalError as e:
		utils.die(
			"sqlite error:\n", e, '\n',
			"SQL:", textwrap.dedent(args[0]), '\n',
			"Values:", args[1:], '\n')

def executemany(*args, **kwargs):
	"""
	Call through to sqlite3.executemany; connects to database if not already
	connected.
	"""
	if _db is None: _connect()
	return _db.executemany(*args, **kwargs)

molecule_types = {
	"ribosomal-small": "S",
	"ribosomal-large": "L",
	"protein-coding": "P",
	"unknown": "-"}

re_ribosomal_small = re.compile(r"^small-\w+-rRNA")
re_ribosomal_large = re.compile(r"^large-\w+-rRNA")

def get_molecule_type(hit):
	"""
	Parse a BLAST hit to determine if the molecule type is small or large
	ribosomal.
	"""
	if re_ribosomal_small.match(hit):
		return molecule_types["ribosomal-small"]
	elif re_ribosomal_large.match(hit):
		return molecule_types["ribosomal-large"]
	else:
		return molecule_types["unknown"]


genome_types = {
	"mitochondrial": "M",
	"plastid": "P",
	"nuclear": "N",
	"unknown": "-"}

def get_genome_type(hit):
	"""
	Parse a BLAST hit to determine the genome type of the sequence, either
	mitochondrial, plastid, or nuclear.
	"""
	if hit:
		og = hit.find("OG=")
		if og >= 0:
			if hit[og+3:].startswith("Mitochondrion"):
				return genome_types["mitochondrial"]
			elif hit[og+3:].startswith("Plastid"):
				return genome_types["plastid"]
			else:
				return genome_types["unknown"]
		else:
			return genome_types["nuclear"]
	else:
		return genome_types["unknown"]


# List of domains to mask, should eventually be put in config file
domains_to_mask = [

'gnl|CDD|144943',
'gnl|CDD|201208',
'gnl|CDD|200957',
'gnl|CDD|197705',
'gnl|CDD|143167',
'gnl|CDD|200980',
'gnl|CDD|200936',
'gnl|CDD|144972',
'gnl|CDD|200951',
'gnl|CDD|206635',
'gnl|CDD|197520',
'gnl|CDD|143165',
'gnl|CDD|29261',
'gnl|CDD|200936',
'gnl|CDD|197603',
'gnl|CDD|201739',
'gnl|CDD|200931',
'gnl|CDD|200948',
'gnl|CDD|200998',
'gnl|CDD|201332',
'gnl|CDD|201372',
'gnl|CDD|201053',
'gnl|CDD|201004',
'gnl|CDD|201223',
'gnl|CDD|200988',
'gnl|CDD|200930',
'gnl|CDD|197585',
'gnl|CDD|197685',
'gnl|CDD|197533',
'gnl|CDD|28904',
'gnl|CDD|201276',
'gnl|CDD|28904',
'gnl|CDD|197562',
'gnl|CDD|28898',
'gnl|CDD|201143',
'gnl|CDD|197480'

]


"""
The domains to mask are specified via the PSSM-Id, but the list that we have
from previous analyses is of the "View PSSM" field. Can search for the "View
PSSM" field at

http://www.ncbi.nlm.nih.gov/Structure/cdd/cdd.shtml

Then get the PSSM-Id in the Statistics dropdown of the result page

"View PSSM"	"PSSM-Id"
pfam01535	144943
pfam00400	201208
pfam00047	200957
smart00407	197705
cd00099	143167
pfam00076	200980
pfam00023	200936
pfam01576	144972
pfam00041	200951
cd00031	206635
smart00112	197520
cd00096	143165
cd00204	29261
pfam00023	200936
smart00248	197603
pfam01344	201739
pfam00018	200931
pfam00038	200948
pfam00096	200998
pfam00595	201332
pfam00651	201372
pfam00169	201053
pfam00105	201004
pfam00435	201223
pfam00084	200988
pfam00017	200930
smart00225	197585
smart00367	197685
smart00135	197533
cd00020	28904
pfam00514	201276
cd00020	28904
smart00185	197562
cd00014	28898
pfam00307	201143
smart00033	197480

"""

SeqRecord = namedtuple('SeqRecord', "id header seq")

def load_seqs(load_id, taxon, seq_type, molecule_type=None, genome_type=None):
	"""
	Returns a list of SeqRecords from the sequences table for the given
	load_id.

	seq_type can have one of three values:

	masked_protein	Protein sequences are written, with promiscuous domains masked
	protein			Protein sequences are written, without any masking
	nucleotide		Nucleotide sequences are written, without any masking

	By default, all genome and molecule types are selected, but this can be
	restricted using the optional keyword args.
	"""

	if seq_type != "nucleotide" and seq_type != "protein":
		utils.die("invalid sequence type:", seq_type)

	where = ["run_id=?"]
	values = [load_id]

	if molecule_type:
		where.append(
			"AND (%s)" % ' OR '.join(["molecule_type=?"]*len(molecule_type)))
		values += map(molecule_types.get, molecule_type)

	if genome_type:
		where.append(
			"AND (%s)" % ' OR '.join(["genome_type=?"]*len(genome_type)))
		values += map(genome_types.get, genome_type)

	sql = """
		SELECT sequence_id, %s_seq, gene, max(expression)
		FROM sequences
		WHERE %s
		GROUP BY gene;""" % (seq_type, ' '.join(where))

	for row in execute(sql, values):
		sequence_id = row[0]
		sequence_string = row[1]
		# Trim any stop codons
		if seq_type == "protein" and sequence_string:
			stopcodon = sequence_string.find('*')
			if stopcodon >= 0:
				sequence_string = sequence_string[:stopcodon]
		# Skip empty sequences
		if sequence_string:
			# Format the sequence record and append it to the list
			header = "{0}@{1}".format(taxon.replace(' ', '_'), sequence_id)
			yield SeqRecord(sequence_id, header, sequence_string)


# Data struct for a cluster of homologous sequences
Cluster = namedtuple('Cluster', "name size weight fasta")

def refine_clusters(
	run_id, homology_id, seq_type, min_taxa, max_sequences, max_length, outdir):
	"""
	"""

	clusters = []
	components = defaultdict(list)
	taxa = {}
	nseqs = {
		'max_length': 0,
		'max_sequences': 0,
		'min_taxa': 0,
		'taxa_mean': 0 }

	# Load components from database
	sql = """
		SELECT homology.component_id, homology.sequence_id,
		       sequences.%s_seq, sequences.catalog_id
		  FROM homology, sequences
		 WHERE homology.sequence_id=sequences.sequence_id
		   AND homology.run_id=?;""" % seq_type

	for row in execute(sql, (homology_id,)):
		comp_id, seq_id, seq, id = row
		if seq is None:
			utils.die("empty sequence in record:", row)
		# Filter out sequences that are too long
		if len(seq) <= max_length:
			nseqs['max_length'] += 1
			if not id in taxa:
				# Lookup species names for catalog ids
				record = catalog.select(id)
				if not record or not record.species:
					utils.die("couldn't find species for catalog id '%s'" % id)
				taxa[id] = record.species.replace(' ', '_')
			components[comp_id].append(SeqRecord(taxa[id], seq_id, seq))

	# Loop over the components and write the fasta files
	for comp_id, records in components.iteritems():

		# Apply filter on cluster size
		size = len(records)

		if size <= max_sequences:

			nseqs['max_sequences'] += size

			# Count the number of times a taxon is repeated in the cluster
			# and calculate the cluster weight
			taxa_count = {}
			weight = 0

			for record in records:
				taxa_count[record.id] = taxa_count.get(record.id, 0) + 1
				weight += len(record.seq)

			# Weight is an approximation of how many comparisons need to be
			# performed in multiple alignment, for ordering the Macse
			# calls later
			weight = (weight / size) ** size

			# Compute the mean number of repetitions
			taxa_count = taxa_count.values()
			taxa_mean = sum(taxa_count) / float(len(taxa_count))

			# Require at least min_taxa, and that the mean reptitions is less
			# than 5.
			if len(taxa_count) >= min_taxa:
				nseqs['min_taxa'] += size
				if taxa_mean < 5:
					nseqs['taxa_mean'] += size
					name = 'homologs_{0}_{1}'.format(run_id, comp_id)
					fasta = os.path.join(outdir, name+'.fa')
					with open(fasta, 'w') as f:
						for record in records:
							print >>f, '>%s@%d\n%s' % record
					clusters.append(Cluster(name, size, weight, [fasta]))

	utils.info(
		"found the following taxa for homology id %d:\n" % homology_id,
		'\n '.join("%s (%s)" % (taxon, id) for id, taxon in taxa.iteritems()))

	diagnostics.log('taxa', str(taxa))
	diagnostics.log_entity('max_length.nseqs', nseqs['max_length'])
	diagnostics.log_entity('max_sequences.nseqs', nseqs['max_sequences'])
	diagnostics.log_entity('min_taxa.nseqs', nseqs['min_taxa'])
	diagnostics.log_entity('taxa_mean.nseqs', nseqs['taxa_mean'])

	if not clusters:
		utils.die("no clusters passed the filtering criteria")

	return clusters

# vim: noexpandtab ts=4 sw=4
