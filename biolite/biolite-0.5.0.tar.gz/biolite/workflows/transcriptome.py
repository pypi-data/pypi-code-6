#!/usr/bin/env python
#
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

import os
import re

from Bio import SeqIO

from biolite import diagnostics
from biolite import utils
from biolite import wrappers


### Headers ###

standard_header = "agalma/gene:{}/isoform:{} len:{} confidence:{}"

trinity_header = re.compile(
	r"c(\d+)_g(\d+)_i(\d+) len=(\d+) path=\[([-: \d]+)\]$")


def unpack_header(header):
	"""
	Unpacks an Agalma header into a dictionary of key:val pairs.  For
	non-Agalma headers, returns a dictionary with only the key 'gene' with
	value header (first 255 characters). The 'gene' value can then be used
	as a key in the `sequences` table in the Agalma database.

	Example header:

	>agalma/gene:9919.0/isoform:1 len:160 confidence:0
	"""
	d = utils.AttributeDict()
	if header.startswith("agalma/gene:"):
		d = utils.AttributeDict()
		header, _, d.blast_hit = header[7:].partition("blasthit:")
		for token in header.replace('/', ' ').split(' '):
			key, _, val = token.partition(':')
			d[key] = val
	else:
		header, _, d.blast_hit = header.partition("blasthit:")
		d.gene = header.partition(' ')[0][:255]
	return d


def parse_headers(fasta_in, fasta_out):
	"""
	Parse `fasta_in` for Trinity-style headers, and convert them to Agalma's
	standardized header format. Otherwise, remove illegal characters ':' and '|'.
	"""

	with open(fasta_out, 'w') as f:
		for record in SeqIO.parse(fasta_in, 'fasta'):
			match = trinity_header.match(record.description)
			if not match is None:
				comp, gene, isoform, length, _ = match.groups()
				utils.write_fasta(
					f, record.seq,
					standard_header.format(
						"%s.%s" % (comp, gene), isoform, length, 0))
			else:
				utils.write_fasta(
					f, record.seq,
					record.description.replace(':', '_').replace('|', '_'))


### Expression ###

def quantify(assembly, name, reads, outdir):
	"""
	"""

	prefix = os.path.abspath(name)

	# Build text file that maps transcript IDs to gene IDs (e.g. locus name)
	gene_map = prefix + '.gene_map.txt'
	with open(gene_map, 'w') as f:
		for record in SeqIO.parse(assembly, 'fasta'):
			print >>f, unpack_header(record.id).gene + '\t' + record.id

	# Build the RSEM reference using the mapping
	wrappers.RsemReference(
					assembly, prefix, '--transcript-to-gene-map', gene_map)

	# Could do our own mapping in the future:
	# bowtie -p 2 -n 2 -l 25 -e 99999999 -m 200 ref -1 input1 -2 input2 -S out

	# Bowtie2 - RSEM doesn't support gapped alignments
	#   (https://groups.google.com/forum/#!topic/rsem-users/l9vzo4HGSeQ)
	# "--all --ignore-quals -N 1"

	temp = prefix + ".temp"
	name = os.path.join(outdir, name)
	wrappers.RsemExpression(
		reads, prefix, name, "--no-bam-output --temporary-folder", temp)

	genes = name + '.genes.results'
	isoforms = name + '.isoforms.results'

	diagnostics.log_path(genes, 'genes')
	diagnostics.log_path(isoforms, 'isoforms')

	return genes, isoforms


def fpkms(coverage_table):
	"""
	"""

	out = {}

	with open(coverage_table) as f:
		next(f) # burn the header line
		for line in f:
			fields = line.rstrip().split()
			out[fields[0]] = float(fields[6])

	return out

# vim: noexpandtab ts=4 sw=4
