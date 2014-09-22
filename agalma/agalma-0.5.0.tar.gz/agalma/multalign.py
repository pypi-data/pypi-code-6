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
Applies sampling and length filters to each cluster of homologous sequences.

Creates multiple sequence alignments for each cluster of homologous sequences
using MAFFT using the E-INS-i algorithm; see doi: 10.1093/molbev/mst010.

Cleans up alignments using Gblocks.
"""

import os
from Bio import SeqIO
from operator import attrgetter
from agalma import config
from agalma import database
from biolite import diagnostics
from biolite import report
from biolite import utils
from biolite import wrappers
from biolite.pipeline import Pipeline

pipe = Pipeline('multalign', __doc__)

### ARGUMENTS ###

pipe.add_arg('--previous', '-p', metavar='RUN_ID', default=None, help="""
	Use the homologous sequences from a previous run of homologize,
	orthologize, or treeprune.""")

pipe.add_arg('--seq_type', default='protein', help="""
	Choose whether alignments are based on 'nucleotide' or 'protein'
	sequences.""")

pipe.add_arg('--min_taxa', type=int, default=4, help="""
	Minimum number of taxa required to retain a cluster.""")

pipe.add_arg('--max_sequences', type=int, default=300, help="""
	Maximum number of sequences to allow in a cluster.""")

pipe.add_arg('--max_length', type=int, default=10000, help="""
    Maximum length for sequences in a cluster.""")

### STAGES ###

@pipe.stage
def lookup_homology_id(id, previous):
	"""Lookup the run ID for the last homology/treeprune run with the current ID"""

	pipelines = ("homologize", "orthologize", "treeprune")
	try:
		prev = diagnostics.lookup_prev_run(id, previous, *pipelines)
		utils.info("using previous '%s' run id %s" % (prev.name, prev.run_id))
	except AttributeError:
		utils.die("no previous", '/'.join(pipelines), "runs found for id", id)

	return {'homology_id': int(prev.run_id)}


@pipe.stage
def refine_clusters(
	_run_id, homology_id, seq_type, min_taxa, max_sequences, max_length):
	"""
	Select a cluster for each homologize component that meets size, sequence
	length, and composition requirements
	"""
	cluster_dir = utils.safe_mkdir('clusters')
	clusters = database.refine_clusters(
					_run_id, homology_id, seq_type,
					min_taxa, max_sequences, max_length, cluster_dir)
	ingest('clusters')


@pipe.stage
def align_sequences(clusters, seq_type, outdir):
	"""Align sequences within each component"""

	align_dir = utils.safe_mkdir(os.path.join(outdir, 'alignments'))

	if seq_type == "nucleotide":
		type_flag = "--nuc"
	elif seq_type == "protein":
		type_flag = "--amino"
	else:
		utils.die("invalid sequence type:", seq_type)

	# Sort by descending size to improve load balancing
	commands = "mafft.sh"
	with open(commands, 'w') as f:
		for cluster in sorted(clusters, key=attrgetter('weight'), reverse=True):
			aligned = os.path.join(align_dir, cluster.name+'.fa')
			print >>f, "%s %s --thread %s --ep 0 --genafpair --maxiterate 10000 %s > %s" % (
				config.get_command("mafft")[0], type_flag,
				config.get_resource('threads'), cluster.fasta[-1], aligned)
			cluster.fasta.append(aligned)

	wrappers.Parallel(
		commands, "--joblog mafft.log --resume-failed --halt 1", threads=1)


@pipe.stage
def cleanup_alignments(clusters, seq_type, min_taxa, outdir):
	"""Clean up aligned sequences with Gblocks"""

	nseqs = 0

	clean_dir = os.path.join(outdir, 'clean_alignments')
	utils.safe_mkdir(clean_dir)

	for cluster in clusters:

		fasta = cluster.fasta[-1]

		# Set Gblocks parameters based on cluster size
		b2 = 0.65*cluster.size
		if seq_type == 'nucleotide':
			wrappers.Gblocks(fasta, "-t=d -b2=%f -b3=10 -b4=5 -b5=a" % b2)
		else:
			wrappers.Gblocks(fasta, "-t=p -b2=%f -b3=10 -b4=5 -b5=a" % b2)

		# Parse Gblocks output
		keep = []
		for record in SeqIO.parse(fasta+'-gb', 'fasta'):
			gaps = sum(1 for c in record.seq if c == '-')
			# Keep sequences that aren't entirely  gaps
			if gaps < len(record.seq):
				keep.append(record)
			else:
				utils.info(
					"dropping sequence '%s' in cluster '%s'" % (
					record.description, cluster.name))

		# Clusters must have at least size min_taxa to be meaningful gene trees
		if len(keep) < min_taxa:
			utils.info("dropping cluster '%s'" % cluster.name)
		else:
			cleaned = os.path.join(clean_dir, cluster.name + '.fa')
			SeqIO.write(keep, open(cleaned, 'w'), 'fasta')
			nseqs += cluster.size

	diagnostics.log('nseqs', nseqs)

	if seq_type == 'nucleotide':
		nucdir = clean_dir
		finish('nucdir')
	else:
		protdir = clean_dir
		finish('protdir')


### RUN ###

if __name__ == "__main__":
	# Run the pipeline.
	pipe.run()
	# Push the local diagnostics to the global database.
	diagnostics.merge()

### REPORT ###

class Report(report.BaseReport):
	def init(self):
		self.name = pipe.name
		# Lookups
		# Generators

# vim: noexpandtab ts=4 sw=4
