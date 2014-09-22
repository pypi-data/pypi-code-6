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

from Bio.Blast import NCBIXML
from collections import namedtuple, OrderedDict

from biolite import utils

rRNAhit = namedtuple('rRNAhit', "query gene orient title")

def blast_xml_hits(filename):
	"""
	Reads an XML formatted BLAST report and saves one top hit per transcript.
	The rRNA hits are tuples with the following fields:
	  (query gene orient title)
	"""
	for entry in NCBIXML.parse(open(filename)):
		if entry.alignments:
			query = entry.query
			alignment = entry.alignments[0]
			orient = 0

			# Loop over the hsp's to get the orientation
			for hsp in alignment.hsps:
				# Check if the orient is the same by comparing
				# orientation of query and subject.
				if (hsp.query_start < hsp.query_end) == \
				   (hsp.sbjct_start < hsp.sbjct_end):
					orient |= 1
				# Or different.
				else:
					orient |= 2

			# Set orient to 0 of it is a mix between hsps (=3),
			# otherwise use the consistent value (1 or -1).
			orient = -1 if orient == 2 else orient % 3

			# Extract gene name from the hit definition.
			# Example definition:
			#  large-nuclear-rRNA|gi|166407160|gb|EU272576.1| Nanomia bijuga
			#  voucher Yale Peabody Museum No. 35043 28S large subunit ribosomal
			#  RNA gene, partial sequence
			gene = alignment.hit_def.partition('|')[0]

			yield rRNAhit(query, gene, orient, alignment.hit_def)


def select_exemplar(sequences, maxlen):
	"""
	"""
	# Use list comprehension to get a list of sequence lengths from the
	# list of sequence records stored in the dictionary; use this to find
	# the length of the longest sequence and compare it to length_limit
	if max(len(record.seq) for record in sequences) <= maxlen:
		utils.info("no sequences exceed length_limit, selecting longest")
		exemplar = sequences[0]
		for record in sequences[1:]:
			if len(record.seq) > len(exemplar.seq):
				exemplar = record
		return exemplar

	# If there is a sequence that exceeds length_limit, then use either the
	# sequence that has the first local maximum or that precedes the
	# first sequence to exceed length_limit
	utils.info("one or more sequences exceeds length limit")
	for i in range(len(sequences)-1):
		if len(sequences[i].seq) > len(sequences[i+1].seq):
			utils.info("selected the first local maximim")
			return sequences[i]
		elif len(sequences[i+1].seq) > maxlen:
			utils.info("selecting the sequence just below the length limit")
			return sequences[i]

	return None

# vim: noexpandtab ts=4 sw=4
