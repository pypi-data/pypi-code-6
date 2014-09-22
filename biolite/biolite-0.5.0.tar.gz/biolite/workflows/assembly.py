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
from Bio import SeqIO
from biolite import diagnostics


def stats(fasta, hist=None, keyword=None):
	"""
	Parses the assembled contigs in `fasta` and writes a histogram of
	contig length to the text file `hist`.

	Writes the total contig count, mean length, and N50 length to
	the diagnostics.
	"""
	count = 0
	mean = 0.0
	n50 = 0

	if hist:
		hist_path = hist
	else:
		hist_path = os.path.abspath(os.path.splitext(fasta)[0] + '.hist')

	# Parse the fasta file to construct a histogram, stored as a dictionary
	# {contig_length: frequency}, and to calculate total contig count and
	# mean length.
	hist = {}
	total_length = 0
	lengths = list()
	for record in SeqIO.parse(fasta, 'fasta'):
		if keyword and not (keyword in record.description):
			continue
		count += 1
		length = len(record.seq)
		lengths.append(length)
		hist[length] = hist.get(length, 0) + 1

	lengths.sort()
	total_length = sum(lengths)

	if count:
		mean = total_length / float(count)

	# Find the n50 value
	cum_length = 0
	for length in lengths:
		cum_length += length
		if cum_length >= (total_length / 2):
			n50 = length
			break

	# Loop through the histogram to dump it to a text file.
	with open(hist_path, 'w') as f:
		for key in sorted(hist.keys()): print >>f, key, hist[key]

	diagnostics.log('count', count)
	diagnostics.log('mean', mean)
	diagnostics.log('n50', n50)
	diagnostics.log_path(hist_path)


def max_contig(fasta):
	"""
	Parse the `fasta` file and return a SeqRecord for the contig with the
	longest length.
	"""
	max_len = 0
	max_record = None
	for record in SeqIO.parse(open(fasta), 'fasta'):
		if len(record.seq) > max_len:
			max_len = len(record.seq)
			max_record = record
	return max_record


def length(fasta):
	"""
	Sum up the length of all contigs in the given `fasta` file.
	"""
	length = 0
	for record in SeqIO.parse(open(fasta), 'fasta'):
		length += len(record.seq)
	return length

