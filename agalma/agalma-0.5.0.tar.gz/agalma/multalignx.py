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

Uses an all-by-all tblastx alignment of sequences within each cluster to trim
sequence ends not included in any HSP.

Creates multiple sequence alignments for each cluster of homologous sequences
using Macse, a translation aware aligner that accounts for frameshifts and stop
codons; see doi:10.1371/journal.pone.0022594

Cleans up alignments by removing sequences/clusters with too many frameshifts,
and then using Gblocks.
"""

import os
from Bio import SeqIO
from itertools import izip
from operator import attrgetter
from agalma import config
from agalma import database
from biolite import diagnostics
from biolite import report
from biolite import utils
from biolite import wrappers
from biolite.pipeline import Pipeline

pipe = Pipeline('multalignx', __doc__)

### ARGUMENTS ###

pipe.add_arg('--previous', '-p', metavar='RUN_ID', default=None, help="""
	Use the homologous sequences from a previous run of homologize,
	orthologize, or treeprune.""")

pipe.add_arg('--min_taxa', type=int, default=4, help="""
	Minimum number of taxa required to retain a cluster.""")

pipe.add_arg('--max_sequences', type=int, default=300, help="""
	Maximum number of sequences to allow in a cluster.""")

pipe.add_arg('--max_length', type=int, default=10000, help="""
    Maximum length for sequences in a cluster.""")

pipe.add_arg('--frameshift', '-f', type=int, default=-40, help="""
	Penalty for frameshift within the sequence.""")

pipe.add_arg('--stopcodon', '-s', type=int, default=-150, help="""
	Penalty for stop codon not at the end of the sequence.""")

pipe.add_arg('--frameshift_cutoff', type=float, default=0.1, help="""
	Remove sequences with more than this proportion of frameshifts.""")

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
def refine_clusters(_run_id, homology_id, min_taxa, max_sequences, max_length):
	"""
	Select a cluster for each homologize component that meets size, sequence
	length, and composition requirements
	"""
	cluster_dir = utils.safe_mkdir('clusters')
	clusters = database.refine_clusters(
					_run_id, homology_id, 'nucleotide',
					min_taxa, max_sequences, max_length, cluster_dir)
	ingest('clusters')


@pipe.stage
def trim_sequences(clusters):
	"""Compare homologs within a cluster by all-to-all BLAST and trim sequence ends not included in any HSP"""

	# Create an allvall tblastx command for each cluster
	commands = "trim.sh"
	with open(commands, 'w') as f:
		for cluster in clusters:
			print >>f, '{0} -dbtype nucl -in {1} && {2} -db {1} -query {1} -evalue 1e-6 -outfmt "6 qseqid sseqid qstart qend" -out {1}.tblastx.txt'.format(
				config.get_command('makeblastdb')[0], cluster.fasta[-1],
				config.get_command('tblastx')[0])

	# Run tblastx
	wrappers.Parallel(
		commands, "--joblog trim.log --resume-failed --halt 1")

	trim_dir = utils.safe_mkdir('trimmed_clusters')

	clusters_keep = []
	for cluster in clusters:
		report = cluster.fasta[-1] + '.tblastx.txt'
		if not os.path.exists(report):
			utils.info("dropping cluster '%s': no tblastx report" % cluster.name)
			continue
		# Trim sequences using blast report
		endpoints = {}
		for line in open(report):
			query, subject, qstart, qend = utils.multimap(
				(str, str, int, int), line.rstrip().split())
			# Skip self hits
			if query != subject:
				if query in endpoints:
					endpoints[query] = (
						min(endpoints[query][0], qstart, qend),
						max(endpoints[query][1], qstart, qend))
				else:
					endpoints[query] = (min(qstart, qend), max(qstart, qend))
		# Load original sequences into a dict
		trimmed_fasta = os.path.join(trim_dir, cluster.name + '.fa')
		with open(trimmed_fasta, 'w') as f:
			for record in SeqIO.parse(open(cluster.fasta[-1]), 'fasta'):
				# Trim to endpoints
				if record.id in endpoints:
					record.seq = record.seq[endpoints[record.id][0]:endpoints[record.id][1]]
				SeqIO.write(record, f, 'fasta')
		cluster.fasta.append(trimmed_fasta)
		clusters_keep.append(cluster)

	return {'clusters': clusters_keep}


@pipe.stage
def align_sequences(clusters, frameshift, stopcodon, outdir):
	"""Align nucleotide sequences within each component using MACSE"""

	utils.safe_mkdir(os.path.join(outdir, 'macse'))

	commands = "macse.sh"
	java = config.get_command('java')[0]
	macse = config.get_command('macse')[0]
	threads = int(config.get_resource('threads'))
	mem = 0.5 * utils.mem_to_mb(config.get_resource('memory')) / threads

	# Sort by descending size to improve load balancing in parallel MACSE
	with open(commands, 'w') as f:
		for cluster in sorted(clusters, key=attrgetter('weight'), reverse=True):
			basename = os.path.join(outdir, 'macse', cluster.name)
			fasta = cluster.fasta[-1]
			print >>f, java, '-Xmx%.0fM' % mem, '-jar', macse, \
				"-i %s -o %s -f %d -s %d &>%s.macse.log" % (
				fasta, basename, frameshift, stopcodon, fasta)
			cluster.fasta.append(basename + '_AA.fasta')
			cluster.fasta.append(basename + '_DNA.fasta')

	wrappers.Parallel(
		commands, "--joblog macse.log --resume-failed --halt 1")


@pipe.stage
def remove_frameshifts(clusters, frameshift_cutoff, min_taxa):
	"""Remove sequences with too many frameshifts"""

	clusters_keep = []
	nseqs = 0

	# Histograms of frameshifts
	hist_sequences = dict()
	hist_clusters = dict()

	# Count frameshifts across species
	fs_species = dict()
	aa_species = dict()

	clusters_keep = []

	workdir = 'remove_frameshifts'
	utils.safe_mkdir(workdir)

	for cluster in clusters:
		# Skip any clusters that didn't finish MACSE
		if not (os.path.exists(cluster.fasta[-2]) and os.path.exists(cluster.fasta[-1])):
			utils.info("dropping cluster %s: no MACSE output" % cluster.name)
			continue

		aa_keep = []
		dna_keep = []

		# Count frameshifts across cluster
		fs_cluster = 0
		aa_cluster = 0

		# Count frameshifts in each sequence, and filter out those with too many
		aa_records = list(SeqIO.parse(open(cluster.fasta[-2]), 'fasta'))
		dna_records = SeqIO.parse(open(cluster.fasta[-1]), 'fasta')

		# Truncate sequences after first stop codon
		stop_codons = []
		for aa_record in aa_records:
			stop = aa_record.seq.find('*')
			if stop >= 0:
				stop_codons.append(stop)

		if stop_codons:
			end = min(stop_codons)
			if end == 0:
				utils.info("stop codon at beginning of sequence: dropping cluster '%s'" % cluster.name)
				continue
			else:
				for aa_record in aa_records:
					aa_record.seq = aa_record.seq[:end]

		for aa_record, dna_record in izip(aa_records, dna_records):
			species = aa_record.id.partition('@')[0]

			fs = sum(1 for c in aa_record.seq if c == '!')
			fs_cluster += fs
			fs_species[species] = fs_species.get(species, 0) + fs

			aa = sum(1 for c in aa_record.seq if c != '-')
			aa_cluster += aa
			aa_species[species] = aa_species.get(species, 0) + aa

			if not aa:
				utils.info(
					"all gaps: dropping sequence '%s' in cluster '%s'" %(
					aa_record.description, cluster.name))
				continue

			percent = round(float(fs) / float(aa), 3)
			hist_sequences[percent] = hist_sequences.get(percent, 0) + 1

			if percent > frameshift_cutoff:
				utils.info(
					"too many frameshifts: dropping sequence '%s' in cluster '%s'" % (
					aa_record.description, cluster.name))
			else:
				aa_keep.append(aa_record)
				dna_keep.append(dna_record)

		percent = round(float(fs_cluster) / float(aa_cluster), 3)
		hist_clusters[percent] = hist_clusters.get(percent, 0) + 1

		# Clusters must have at least min_taxa to be meaningful gene trees
		if len(aa_keep) < min_taxa:
			utils.info("fewer than %d taxa: dropping cluster '%s'" % (
					min_taxa,
					cluster.name))
		else:
			basename = os.path.join(workdir, cluster.name)
			cluster = database.Cluster(
					cluster.name, len(aa_keep), cluster.weight, cluster.fasta)
			clusters_keep.append(cluster)
			nseqs += cluster.size
			cluster.fasta.append(basename + '_AA')
			with open(cluster.fasta[-1], 'w') as f:
				for record in aa_keep:
					print >>f, ">%s" % record.description
					print >>f, str(record.seq).replace('!', '-')
			cluster.fasta.append(basename + '_DNA')
			with open(cluster.fasta[-1], 'w') as f:
				for record in dna_keep:
					print >>f, ">%s" % record.description
					print >>f, str(record.seq).replace('!', '-')

	hist_species = {}
	for s in aa_species:
		hist_species[s] = float(fs_species[s]) / float(aa_species[s])

	diagnostics.log('hist_sequences', str(hist_sequences))
	diagnostics.log('hist_clusters', str(hist_clusters))
	diagnostics.log('hist_species', str(hist_species))
	diagnostics.log('nseqs', nseqs)

	return {'clusters': clusters_keep}


@pipe.stage
def cleanup_alignments(clusters, min_taxa, outdir):
	"""Clean up aligned sequences with Gblocks"""

	clusters_keep = []
	nseqs = 0

	protdir = os.path.join(outdir, 'gblocks-prot')
	nucdir = os.path.join(outdir, 'gblocks-nuc')

	utils.safe_mkdir(protdir)
	utils.safe_mkdir(nucdir)

	for cluster in clusters:

		aa_name = cluster.fasta[-2]
		dna_name = cluster.fasta[-1]

		# Set Gblocks parameters based on cluster size
		b1 = cluster.size/2 + 1
		b2 = max(b1, int(0.65*cluster.size))

		wrappers.Gblocks(aa_name, "-t=p -b1=%d -b2=%d -b3=10 -b4=5 -b5=a" % (b1,b2))
		wrappers.Gblocks(dna_name, "-t=d -b2=%f -b3=10 -b4=5 -b5=a" % (0.65*cluster.size))

		# Parse Gblocks output

		aa_keep = []
		dna_keep = []

		aa_records = SeqIO.parse(open(aa_name + '-gb'), 'fasta')
		dna_records = SeqIO.parse(open(dna_name + '-gb'), 'fasta')

		for aa_record, dna_record in izip(aa_records, dna_records):

			aa_gaps = sum(1 for c in aa_record.seq if c == '-')
			dna_gaps = sum(1 for c in dna_record.seq if c == '-')

			# Remove sequences that are all gaps
			if aa_gaps < len(aa_record.seq) and dna_gaps < len(dna_record.seq):
				aa_keep.append(aa_record)
				dna_keep.append(dna_record)
			else:
				utils.info(
					"dropping sequence '%s' in cluster '%s'" % (
					aa_record.description, cluster.name))

		# Clusters must have at least size min_taxa to be meaningful gene trees
		if len(aa_keep) < min_taxa:
			utils.info("dropping cluster '%s'" % cluster.name)
		else:
			cluster.fasta.append(os.path.join(protdir, cluster.name + '.fa'))
			SeqIO.write(aa_keep, open(cluster.fasta[-1], 'w'), 'fasta')
			cluster.fasta.append(os.path.join(nucdir, cluster.name + '.fa'))
			SeqIO.write(dna_keep, open(cluster.fasta[-1], 'w'), 'fasta')
			clusters_keep.append(cluster)
			nseqs += cluster.size

	diagnostics.log('nseqs', nseqs)

	finish('clusters', 'protdir', 'nucdir')


# Report. #
class Report(report.BaseReport):
	def init(self):
		self.name = pipe.name
		# Lookups
		self.hist_names = ('hist_sequences', 'hist_clusters', 'hist_species')
		for name in self.hist_names:
			self.lookup(name, 'multalignx.remove_frameshifts', attribute=name)
		# Generators
		self.generator(self.histograms)

	def histograms(self):
		out = []
		for name in self.hist_names:
			if name in self.data:
				hist = eval(self.data[name])
				title = "Distribution of Frameshifts (by %s)" % name.partition('_')[2]
				out.append(self.header(title))
				if len(hist) < 10 or name == 'hist_species':
					# Make a table instead of a plot.
					if name == 'hist_species':
						for k in hist:
							hist[k] *= 100.0
						headers = (
							name.partition('_')[2],
							'Frameshifts (% of AA Sequence)')
						rows = [(k.replace('_', ' '), '%.1f%%' % hist[k]) for k in hist]
					else:
						headers = ('Frameshifts (% of AA Sequence)', 'Frequency')
						rows = [('%g%%' % k, hist[k]) for k in sorted(hist)]
					out += self.table(rows, headers)
				else:
					imgname = "%d.frameshifts.%s.png" % (self.run_id, name)
					props = {
						'xlabel': "Frameshifts (% of AA Sequence)",
						'xticks': [0, len(hist)-1],
						'xticklabels': ['0%', '%.1f%%' % (100.0*max(hist))],
						'ylabel': "Frequency"}
					out.append(self.histogram_categorical(imgname, hist, props=props))
		return out

if __name__ == "__main__":
	# Run the pipeline.
	pipe.run()
	# Push the local diagnostics to the global database.
	diagnostics.merge()

# vim: noexpandtab ts=4 sw=4
