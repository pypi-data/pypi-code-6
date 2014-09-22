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

import math
import os

from Bio import SeqIO
from collections import namedtuple

from biolite import diagnostics
from biolite import utils
from biolite import wrappers


def split_query(fasta, command, chunk_size=10000, workdir=''):
	"""
	Break a query file into chunks of roughly `chunk_size` nucleotides
	and return a path to a text file with `command` applied to each
	query fragment.
	"""

	workdir = os.path.abspath(workdir)
	utils.safe_mkdir(workdir)

	commands = os.path.join(workdir, 'commands.sh')
	chunk_id = 0
	chunk_file = None

	nbases = 0

	with open(commands, 'w') as f:
		for record in SeqIO.parse(open(fasta), 'fasta'):
			nbases += len(record.seq)
			if nbases > (chunk_id * chunk_size):
				chunk_id = nbases / chunk_size + 1
				chunk_file = open(
								os.path.join(workdir, '%d.fa' % chunk_id),
								'w')
				print >>f, command, '-query', '%d.fa' % chunk_id
			SeqIO.write(record, chunk_file, 'fasta')

	return commands


def evalue_hist(hits):
	"""
	Return a dict containing a histogram of e-value exponents for the
	given `hits`.
	"""

	hist = {}

	for hit in hits:
		i = int(math.log10(hit.evalue))
		hist[i] = hist.get(i, 0) + 1

	return hist


tabular_fields = (
	"qseqid", "qlen", "sseqid", "slen", "frames", "pident", "nident",
	"length", "mismatch", "gapopen", "qstart", "qend", "sstart", "send",
	"evalue", "bitscore", "stitle")
tabular_fields_str = ' '.join(tabular_fields)
TabularHit = namedtuple('TabularHit', tabular_fields)


def hits_tabular(filename, nlimit=1):
	"""
	Similar to `blast_top_hits` but uses BLAST custom tabular format as input.
	"""
	qseqid = None
	rank = 0
	# Loop over the blast records.
	for line in open(filename):
		hit = TabularHit(*line.rstrip().split('\t'))
		if (hit.qseqid != qseqid):
			qseqid = hit.qseqid
			rank = 0
		if rank < nlimit:
			yield hit
		rank += 1


def top_hits_tabular(filename):
	"""
	Similar to `hits_tabular`, but returns an dict keyed by query name
	with only one hit (the top hit) per query.
	"""
	hits = {}
	for hit in hits_tabular(filename, nlimit=1):
		hits[hit.qseqid] = hit
	return hits


def annotate(hits, fasta, annotated, expression={}):
	"""
	Iterates through the records in `fasta` and looks for a hit in a dict of
	BlastHit objects, `hits`.  For each record with a hit, the expression (if
	provided), hit title, and evalue are added to the ID. Records are written
	back out to `annotated`.
	"""
	with open(annotated, 'w') as f:
		for record in SeqIO.parse(open(fasta), 'fasta'):
			hit = hits.get(record.id)
			headers = [str(record.description).strip()]
			if 'blasthit' in headers[0]:
				utils.die(
					"found reserved word 'blasthit' in header:\n",
					headers[0])
			if record.id in expression:
				headers.append('expression:%.2f' % expression[record.id])
			if hit:
				headers.append('blasthit:%s|%s' % (hit.stitle, hit.evalue))
			utils.write_fasta(f, record.seq, *headers)


def annotate_split(hits, fasta, annotated, missed):
	"""
	Iterates through the records in `fasta` and looks for a hit in a dict of
	BlastHit objects, `hits`.  Write annotated hits to `annotated` and all
	records without a hit to `missed`.
	"""
	with open(annotated, 'w') as fannotated, open(missed, 'w') as fmissed:
		for record in SeqIO.parse(open(fasta), 'fasta'):
			hit = hits.get(record.id)
			if hit:
				if 'blasthit' in record.description:
					utils.die(
						"found reserved word 'blasthit' in header:\n",
						record.description)
				utils.write_fasta(
					fannotated, record.seq, record.description,
					'blasthit:%s|%s' % (hit.stitle, hit.evalue))
			else:
				utils.write_fasta(fmissed, record.seq, record.description)


def dustmasker(fasta, clean, dirty, max_lowc=0.8, min_region=0.1):
	"""
	Run dustmasker on `fasta` and filter out sequences with low
	complexity regions greater than fraction `max_lowc` or without a high
	complexity region greater than fraction `min_region`.
	"""

	dust = 'dust.fa'
	wrappers.Dustmasker(fasta, '-outfmt', 'fasta', '-out', dust)

	stats = {
		'bases': 0,
		'transcripts': 0,
		'lowc_bases': 0,
		'lowc_regions': 0,
		'lowc_transcripts': 0,
		'lowc_min_regions': 0}

	def count_upper_regions(seq):
		lengths = [0]
		for i in xrange(len(seq) - 1):
			if seq[i].isupper():
				lengths[-1] += 1
				if seq[i+1].islower():
					lengths.append(0)
		if seq[-1].isupper():
			lengths[-1] += 1
		return lengths

	with open(clean, 'w') as fclean, open(dirty, 'w') as fdirty:
		for record in SeqIO.parse(open(dust), 'fasta'):
			stats['transcripts'] += 1
			l = len(record.seq)
			stats['bases'] += l
			lowc_len = sum(1 for c in record.seq if c.islower())
			stats['lowc_bases'] += lowc_len

			if lowc_len:
				stats['lowc_regions'] += 1

			if float(lowc_len) / float(l) > max_lowc:
				stats['lowc_transcripts'] += 1
				utils.write_fasta(
							fdirty, record.seq, record.description, 'maxlowc')
			elif float(max(count_upper_regions(record.seq))) < min_region * l:
				stats['lowc_min_regions'] += 1
				utils.write_fasta(
							fdirty, record.seq, record.description, 'minregion')
			else:
				utils.write_fasta(fclean, record.seq, record.description)

	diagnostics.prefix.append('dustmasker')
	diagnostics.log_dict(stats)
	diagnostics.prefix.pop()

# vim: noexpandtab ts=4 sw=4
