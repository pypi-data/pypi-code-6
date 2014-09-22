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
Cleans transcripts to remove ribosomal, mitochondrial, vector, and
low-complexity sequences.  Vector sequences could include untrimmed adapters or
plasmids (we sometimes find sequences in our data for the protein expression
vectors used to manufacture the sample preparation enzymes).  Raw reads are
mapped back to the transcripts to estimate coverage and assign TPKM values.
Finally, transcripts are annotated with blast hits against SwissProt.
"""

import numpy as np
import os
import shutil
from Bio import SeqIO
from agalma import config
from biolite import catalog
from biolite import diagnostics
from biolite import report
from biolite import utils
from biolite import workflows
from biolite import wrappers
from biolite.pipeline import IlluminaPipeline

pipe = IlluminaPipeline('postassemble', __doc__)

### ARGUMENTS ###

pipe.add_path_arg('--assembly', '-a', default=None, help="""
	A FASTA file of transcripts.  These can be generic assemblies, from agalma
	or otherwise.  The original read data need not be provided, but if it is,
	transcript expression will be estimated by mapping the reads back to the
	assembly. NOTE: the header cannot contain any spaces or the special
	characters ':' or '|'.""")

pipe.add_path_arg('--rrna_exemplars', '-r', default=None, help="""
	A FASTA file of rRNA exemplars found by the remove_rrna pipeline.""")

pipe.add_arg('--external', action='store_true', default=False, help="""
	The assembly is from an external source and should be loaded directly
    from the catalog, not from a previous run of the 'assemble' pipeline.""")

### STAGES ###

@pipe.stage
def setup_assembly(id, data, previous, external, assembly):
	"""Setup path to the assembly FASTA file"""

	if external:
		# First path in the catalog is the assembly for external dataset.
		try:
			assembly = data[-1][0]
		except IndexError:
			utils.die("missing catalog path for id", id)
		data = None
		ingest("data")
	elif not assembly:
		assembly = diagnostics.lookup_prev_val(
	 					id, previous, None, "assembly", "assemble")
		if not assembly:
			utils.die("could not determine assembly path")

	utils.info("assembly:", assembly)
	diagnostics.log_path(assembly)

	return {
		'assembly': [assembly],
		'name': utils.basename(assembly)}


@pipe.stage
def setup_rrna_exemplars(id, external, rrna_exemplars):
	"""Setup path to the rRNA exemplars FASTA file"""
	if not rrna_exemplars:
		try:
			rrna = diagnostics.lookup_prev_run(id, None, "remove_rrna")
			rrna_exemplars = diagnostics.lookup(rrna.run_id, "remove_rrna.find_exemplars").get("path")
			utils.info("rrna_exemplars:", rrna_exemplars)
			ingest('rrna_exemplars')
		except AttributeError:
			utils.info("no previous remove_rrna run found for id", id)


@pipe.stage
def parse_assembly_headers(assembly, name):
	"""Parse the assembly headers and convert them to Agalma's format"""
	parsed_path = os.path.abspath(name + ".parsed.fa")
	workflows.transcriptome.parse_headers(assembly[-1], parsed_path)
	diagnostics.log_path(parsed_path)
	assembly.append(parsed_path)


@pipe.stage
def dustmasker(assembly, name, outdir):
	"""Remove low complexity regions with DustMasker"""

	dust_path = os.path.join(outdir, name + '.dust.fa')
	clean_path = os.path.abspath(name + '.nodust.fa')
	workflows.blast.dustmasker(assembly[-1], clean_path, dust_path)
	diagnostics.log_path(dust_path)
	assembly.append(clean_path)


@pipe.stage
def clean_univec(assembly, name, outdir):
	"""Remove vector contaminants from assembled transcripts"""

	vector_path = os.path.join(outdir, name + '.vectors.fa')
	clean_path = os.path.abspath(name + '.novectors.fa')
	workdir = os.path.abspath('univec')

	# Blastn against univec, transferring sequences with or without a hit to
	# their own files This removes sequences that still have adapters, or that
	# are contaminated with plasmids (including the protein expression plasmids
	# used to manufacture sample prep enzymes).
	report = os.path.join(workdir, 'out.txt')
	command = "blastn -evalue 0.0001 -outfmt '6 %s' -db %s -max_target_seqs 20" % (
				workflows.blast.tabular_fields_str,
				config.get_resource('univec_blastdb'))
	commands = workflows.blast.split_query(assembly[-1], command, 100000, workdir)
	wrappers.Parallel(
		commands, "--joblog univec.log --resume-failed --halt 1",
		stdout=report, cwd=workdir)

	hits = workflows.blast.top_hits_tabular(os.path.join(workdir, report))
	utils.info("Total of %d matches against UniVec." % len(hits))

	workflows.blast.annotate_split(hits, assembly[-1], vector_path, clean_path)

	diagnostics.log_path(vector_path)
	assembly.append(clean_path)


@pipe.stage
def clean_rrna(assembly, name, rrna_exemplars, outdir):
	"""Remove rRNA from assembled transcripts"""

	rrna_path = os.path.join(outdir, name + '.rrna.fa')
	clean_path = os.path.abspath(name + '.norrna.fa')
	workdir = os.path.abspath('rrna')

	# Build database from the resource rRNAs and the exmplars.
	db_path = os.path.abspath('rrna.db')
	if rrna_exemplars:
		utils.info("adding rRNA exemplars to blast database")
		utils.cat_to_file(rrna_exemplars, db_path+'.fa', mode='w')
	utils.cat_to_file(config.get_resource('rrna_fasta'), db_path+'.fa')
	wrappers.MakeBlastDB(db_path+'.fa', db_path, 'nucl')

	# Blastn against rRNA, transferring sequences with or without a hit to
	# their own files.  Even when rRNA reads are removed prior to assembly,
	# some may make it through and be assembled from the full dataset
	# (including low frequency contaminant rRNAs).
	report = os.path.join(workdir, 'out.txt')
	command = "blastn -evalue 0.0001 -outfmt '6 %s' -db %s -max_target_seqs 20" % (
				workflows.blast.tabular_fields_str, db_path)
	commands = workflows.blast.split_query(assembly[-1], command, 100000, workdir)
	wrappers.Parallel(
		commands, "--joblog rrna.log --resume-failed --halt 1",
		stdout=report, cwd=workdir)

	hits = workflows.blast.top_hits_tabular(os.path.join(workdir, report))
	utils.info("Total of %d matches against ribosomal RNA." % len(hits))

	workflows.blast.annotate_split(hits, assembly[-1], rrna_path, clean_path)
	if rrna_exemplars:
		utils.info("appending rRNA exemplars to removed rRNA")
		utils.cat_to_file(rrna_exemplars, rrna_path)

	assembly.append(clean_path)
	diagnostics.log_exit('rrna', rrna_path)


@pipe.stage
def translate(assembly, name, outdir):
	"""Identify likely coding regions"""

	translation = [os.path.join(outdir, name + '.translated.fa')]
	wrappers.Transdecoder(assembly[-1])

	with open(translation[-1], 'w') as f:
		for record in SeqIO.parse(
				"best_candidates.eclipsed_orfs_removed.pep",
				"fasta"):
			header = record.description.strip().split()
			gene, _, frame = header[8].rpartition(':')
			if frame: frame = "frame:"+frame
			utils.write_fasta(
						f, record.seq, gene, frame, header[5], header[6])

	ingest('translation')


@pipe.stage
def swissprot(translation, name, outdir):
	"""Blastp translations against SwissProt"""

	report = os.path.join(outdir, name + '.translated.blastp.txt')
	workdir = os.path.abspath('swissprot')
	command = "blastp -evalue 1e-6 -outfmt '6 %s' -db %s" % (
				workflows.blast.tabular_fields_str,
				config.get_resource('swissprot_blastdb'))
	commands = workflows.blast.split_query(
									translation[-1], command, 100000, workdir)
	wrappers.Parallel(
		commands, "--joblog swissprot.log --resume-failed --halt 1",
		stdout=report, cwd=workdir)

	hits = workflows.blast.top_hits_tabular(report)

	diagnostics.log_path(report)
	diagnostics.log('hits', len(hits))

	ingest('hits')


@pipe.stage
def select_orfs(translation, name, hits, outdir):
	"""Select the open reading frame with the best evalue"""

	# Annotate hits
	translation.append(os.path.join(outdir, name + '.translated.annotated.fa'))
	workflows.blast.annotate(hits, translation[-2], translation[-1])
	# Choose annotation with the lowest evalue
	records = {}
	evalues = {}
	for record in SeqIO.parse(translation[-1], 'fasta'):
		if "blasthit:" in record.description:
			evalue = float(record.description.rpartition('|')[2])
		else:
			evalue = 1.0
		if (not record.id in records) or (evalue < evalues[record.id]):
			records[record.id] = record
			evalues[record.id] = evalue
	translation.append(os.path.join(outdir, name + '.translated.orfs.fa'))
	with open(translation[-1], 'w') as f:
		for record in records.itervalues():
			utils.write_fasta(f, record.seq, record.description)

	diagnostics.log_exit("translation", translation)


@pipe.stage
def coverage(data, assembly, name, outdir):
	"""Build a table of the number of reads covering each transcript"""

	diagnostics.prefix.append('stats')
	workflows.assembly.stats(assembly[-1])
	diagnostics.prefix.pop()

	if data:
		coverage_table = workflows.transcriptome.quantify(
							assembly[-1], 'coverage', data[-1], outdir)[1]
		diagnostics.log_path(coverage_table)
		fpkms = workflows.transcriptome.fpkms(coverage_table)
	else:
		utils.info('no data - skipping')
		coverage_table = None
		fpkms = {}

	ingest('coverage_table', 'fpkms')


@pipe.stage
def annotate(assembly, name, hits, fpkms, coverage_table, outdir):
	"""Annotate transcripts with top blast hit"""

	# Annotate hits
	annotated = os.path.join(outdir, name + '.annotated.fa')
	workflows.blast.annotate(hits, assembly[-1], annotated, fpkms)
	diagnostics.log_path(annotated)
	assembly.append(annotated)

	# Contig stats for only the hits
	diagnostics.prefix.append('stats')
	workflows.assembly.stats(annotated, keyword="blasthit:")
	diagnostics.prefix.pop()

	# Coverage table for only the hits
	if coverage_table:
		hits_table = coverage_table + '.blasthits'
		with open(hits_table, 'w') as f:
			for line in open(coverage_table):
				if line.partition('\t')[0] in hits:
					f.write(line)
		diagnostics.log_path(hits_table, 'coverage')

	finish('assembly')


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
		self.lookup_unpack(diagnostics.EXIT)
		self.lookup('stats', 'postassemble.coverage.stats')
		self.lookup('stats_annotated', 'postassemble.annotate.stats')
		self.lookup('coverage', 'postassemble.coverage', 'path')
		self.lookup('coverage_annotated', 'postassemble.annotate.coverage', 'path')
		self.lookup('annotated', 'postassemble.annotate', 'path')
		self.lookup('vectors', 'postassemble.clean_univec', 'path')
		# Generators
		self.generator(self.assembly_table)
		self.generator(self.contig_histogram)
		self.generator(self.coverage_plot)
		self.generator(self.assembly_files)

	def assembly_files(self):
		links = {}
		keys = ("annotated", "rrna", "vectors")
		names = ("Annotated Assembly", "Ribosomal RNA", "Vectors")
		styles = ("success", "warning", "warning")
		for key in keys:
			src = self.data.get(key)
			if src and os.path.exists(src):
				dst = '%d.%s' % (self.run_id, os.path.basename(src))
				shutil.copy(src, os.path.join(self.outdir, dst))
				links[key] = dst
		if links:
			html = [
				'<div class="well well-sm" style="text-align:center">',
				'<h4>Assembly Files</h4>',
			]
			for key, name, style in zip(keys, names, styles):
				if key in links:
					html.append('<a href="%s" class="btn btn-lg btn-%s">%s</a>' % (links[key], style, name))
			html.append('</div>')
			return html

	def assembly_table(self):
		if self.check('stats', 'stats_annotated'):
			stats = self.data.stats
			stats_annotated = self.data.stats_annotated
			headers = ('', '<b>All transcripts</b>', '<b>Transcripts with blastx hits</b>')
			rows = [
				('<b># Transcripts</b>', stats['count'], stats_annotated['count']),
				('<b>Mean Transcript Length</b>', stats['mean'], stats_annotated['mean']),
				('<b>N50 Transcript Length</b>', stats['n50'], stats_annotated['n50'])]
			return self.table(rows, headers, 'lll')

	def contig_histogram(self):
		if self.check('stats', 'stats_annotated'):
			try:
				hists = [
					np.loadtxt(open(self.data.stats['path'])),
					np.loadtxt(open(self.data.stats_annotated['path']))]
			except IOError:
				utils.info("could not open histogram for run", self.run_id)
				return
			except KeyError:
				utils.info("missing histogram entry for run", self.run_id)
				return
			imgname = '%d.assembly.histogram.svg' % self.run_id
			props = {
				'title': "Transcripts - Histogram of Lengths (Full Assembly)",
				'xlabel': "Transcript Length (bp)",
				'ylabel': "Frequency"}
			labels=["all transcripts", "transcripts with blastx hit"]
			return [self.histogram_overlay(
								imgname, hists, labels=labels, props=props)]

	def load_coverage(self, path):
		coverage = np.loadtxt(open(path), skiprows=1, usecols=[6])
		# Sort by coverage, descending.
		coverage = np.sort(coverage)[::-1]
		# Compute cumulative sum of coverage.
		return coverage.cumsum()

	def coverage_plot(self):
		if self.check('coverage', 'coverage_annotated'):
			try:
				coverage = [
					self.load_coverage(self.data.coverage),
					self.load_coverage(self.data.coverage_annotated)]
			except IOError:
				utils.info("could not open coverage table for run", self.run_id)
				return
			imgname = '%d.assembly.coverage.svg' % self.run_id
			props = {
				'title': "Read Coverage across Transcripts",
				'xlabel': "Transcripts, ordered from highest to lowest representation",
				'ylabel': "Cumulative mapped reads (FPKM)"}
			plots = (
				(np.arange(coverage[0].size), coverage[0], "all transcripts"),
				(np.arange(coverage[1].size), coverage[1], "transcripts with blastx hits"))
			return [self.multilineplot(imgname, plots, props)]

# vim: noexpandtab ts=4 sw=4
