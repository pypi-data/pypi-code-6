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
Assembles and identifies ribosomal RNA (rRNA) sequences, removes read pairs
that map to these rRNA sequences, and provides a variety of diagnostics about
rRNA. A single exemplar sequence is presented for each type of rRNA that is
found, but rRNA read pairs are excluded by mapping to a large set of rRNA
transcripts that are derived from multiple assemblies over a range of data
subset sizes.
"""

import os
from Bio import SeqIO
from collections import defaultdict
from itertools import chain
from agalma import config
from biolite import diagnostics
from biolite import report
from biolite import utils
from biolite import wrappers
from biolite import workflows
from biolite.pipeline import IlluminaPipeline

pipe = IlluminaPipeline('remove_rrna', __doc__)

### ARGUMENTS ###

pipe.add_arg('--quality', '-q', type=int, metavar='MIN', default=36, help="""
	Use reads with mean quality > MIN.""")

pipe.add_arg(
	'--subsets', type=int, metavar='N', nargs='+',
	default=[1000, 2500, 5000, 10000, 25000, 50000, 100000], help="""
		Progressive sizes of subassemblies for identifying rRNA.""")

pipe.add_arg('--ss', default=None, help="""
	Specify orientation of strand-specific reads: FR or RF for paired, F or R for
	single-end. See the Trinity documentation for more details.""")

### STAGES ###

pipe.add_data_sources("sanitize")

@pipe.stage
def assemble_subsets(id, data, subsets, quality, ss):
	"""Assemble subsets of increasing numbers of reads"""

	transcripts = os.path.abspath('subassembly.all.fa')
	utils.truncate_file(transcripts)

	for n in subsets:

		diagnostics.prefix.append(str(n))

		# Create a subset of n high-quality reads
		subset = ['subset.%d.fq' % i for i in xrange(len(data[-1]))]
		wrappers.FilterIllumina(data[-1], subset, '-q', quality, '-n', n)

		# Assemble the subset
		assembly = "subassembly.%d" % n
		args = ["--min_contig_length 500 --full_cleanup --output", assembly]
		if ss:
			args += ["--SS_lib_type", ss]
		wrappers.Trinity(subset, *args, return_ok=None)
		assembly += ".Trinity.fasta"

		# Loop through the subassembly, append the subset size to the locus so
		# that loci are unique across assemblies, and add them to the
		# concatenated subassemblies
		if os.path.exists(assembly):
			with open(transcripts, 'a') as f:
				for i, record in enumerate(SeqIO.parse(assembly, 'fasta')):
					utils.write_fasta(
						f, record.seq, "%d:%d" % (i, n))
		else:
			utils.info("warning: unable to assemble %d subset" % n)

		diagnostics.prefix.pop()

	if not os.path.getsize(transcripts):
		transcripts = None

	ingest('transcripts')


@pipe.stage
def blast_transcripts(transcripts):
	"""Blast transcripts against known rRNA database"""

	if transcripts is None:
		utils.info("no transcripts found... skipping")
		return {"blast_xml": None}

	# Build the blast database each time from the fasta. This occurs a little
	# bit of overhead, but ensure that it is up to date and also that it is
	# being created somewhere that the users has write access

	dbname = os.path.abspath('rrna')
	wrappers.MakeBlastDB(config.get_resource('rrna_fasta'), dbname, 'nucl')

	blast_xml = 'rrna.xml'
	wrappers.BlastN(
		transcripts, dbname, '-out', blast_xml, "-outfmt 5 -evalue 0.0001")

	ingest('blast_xml')


@pipe.stage
def find_exemplars(transcripts, blast_xml, outdir):
	"""Parse blast output for exemplar rRNA sequences"""

	if transcripts is None:
		utils.info("no transcripts found... skipping")
		return {"exemplars_fasta": None}

	# Create a dictionary of all rRNA sequences from the assembly.
	sequences = SeqIO.to_dict(SeqIO.parse(transcripts, 'fasta'))

	# Build a new dictionary of rRNA sequences, annotating with rRNA
	# type, and taking reverse complement when needed.
	genes = defaultdict(list)
	for hit in workflows.rrna.blast_xml_hits(blast_xml):
		record = sequences[hit.query]
		record.name = ''
		record.description = "blasthit:" + hit.title
		record.id = ':'.join((hit.gene, hit.query))
		if hit.orient == -1:
			record.seq = record.seq.reverse_complement()
		genes[hit.gene].append(record)

	# Exclude all but the longest sequence for each gene for each assembly
	for gene in genes:
		longest = {}
		for record in genes[gene]:
			n = int(record.id.rpartition(':')[2])
			previous = longest.get(n, None)
			if not previous or len(previous.seq) < len(record.seq):
				longest[n] = record

		# Replace the full list for the gene with the list that includes no
		# more than one sequence per assembly subset size
		genes[gene] = [longest[n] for n in sorted(longest)]

	SeqIO.write(chain(*genes.values()), open('rrna_longest.fa', 'w'), 'fasta')

	# Create a dictionary with a list of sequence lengths for each rRNA gene
	# in the reference set with key gene name and value list of lengths
	gene_lengths = defaultdict(list)
	for record in SeqIO.parse(config.get_resource('rrna_fasta'), 'fasta'):
		gene = record.id.partition('|')[0]
		gene_lengths[gene].append(len(record.seq))

	target_genes = sorted(map(str, gene_lengths))
	diagnostics.log('target_genes', target_genes)

	# Identify the single exemplar to retain for each gene
	exemplars = []
	for gene in target_genes:
		utils.info("selecting an exemplar for gene target", gene)

		# Check that the current target gene was found in the data
		if not gene in genes:
			utils.info(gene, "not found in the assembly, skipping")
			continue

		# Calculate a length limit based on the longest gene from the
		# reference set
		maxlen = max(gene_lengths[gene]) * 1.25
		utils.info("length limit set to", maxlen)

		exemplar = workflows.rrna.select_exemplar(genes[gene], maxlen)
		if exemplar:
			utils.info(exemplar.id, "selected for gene", gene)
			exemplars.append(exemplar)

	# Write exemplar rRNA sequences to a file
	if exemplars:
		exemplars_fasta = os.path.join(outdir, 'rrna_exemplars.fa')
		SeqIO.write(exemplars, open(exemplars_fasta, 'w'), 'fasta')
		diagnostics.log_path(exemplars_fasta)
	else:
		exemplars_fasta = None

	ingest('exemplars_fasta')


@pipe.stage
def exemplar_nt_summary(exemplars_fasta, outdir):
	"""Blast rRNA exemplars against rRNA subset of nt database"""

	if exemplars_fasta:
		nt_summary = os.path.join(outdir, 'rrna_nt_summary.txt')
		wrappers.BlastN(
					exemplars_fasta, config.get_resource('nt_rrna_blastdb'),
					'-out', nt_summary,
					"-outfmt '6 qseqid stitle evalue' -max_target_seqs 10")
		diagnostics.log_path(nt_summary)
	else:
		utils.info("no rRNA exemplars were found... skipping")


@pipe.stage
def map_reads(data, exemplars_fasta):
	"""Map reads against rRNA exemplars"""

	if exemplars_fasta:
		ids = ["rrna.ids.%d.txt" % i for i in (0,1)]
		db = os.path.abspath('rrna_exemplars')
		wrappers.Bowtie2Build(exemplars_fasta, db)
		coverage = {}
		for fastq, id in zip(data[-1], ids):
			wrappers.Bowtie2(
						fastq, db, "-k 1 --local --no-unal --no-head",
						pipe=r"awk -F'[/\t]' '{print $1,$4}'", stdout=id)
			for line in open(id):
				gene = line.split()[-1].partition(':')[0]
				coverage[gene] = coverage.get(gene, 0) + 1
		diagnostics.log("coverage", coverage)
	else:
		ids = None
		utils.info("no rRNA exemplars were found... skipping")

	ingest('ids')


@pipe.stage
def exclude_reads(data, ids, gzip, outdir):
	"""Exclude pairs where either read maps to an rRNA exemplar"""

	if ids:
		norrna = os.path.abspath('reads.norrna')
		norrna = ['%s.%d.fq' % (norrna, i) for i in (0,1)]
		if gzip:
			norrna = [f+'.gz' for f in norrna]
		wrappers.Exclude(ids, data[-1], norrna)
		data.append(norrna)
	else:
		utils.info("no rRNA exemplars were found... skipping")

	finish('data')


### RUN ###

if __name__ == "__main__":
	# Run the pipeline.
	pipe.run()
	# Push the local diagnostics to the global database.
	diagnostics.merge()

class Report(report.BaseReport):

	def init(self):
		self.name = pipe.name
		# Lookups
		self.lookup("exemplars", "remove_rrna.find_exemplars", "path")
		self.lookup("nt_summary", "remove_rrna.exemplar_nt_summary", "path")
		self.lookup_attribute("remove_rrna.map_reads", "coverage")
		self.lookup("exclude", "remove_rrna.exclude_reads.exclude")
		self.percent("exclude", "percent_kept", "pairs_kept", "pairs")
		# Generators
		self.generator(self.exclude_table)
		self.generator(self.coverage_table)

	def exclude_table(self):
		if self.check("exclude"):
			return self.summarize(report.exclude_schema, "exclude")

	def coverage_table(self):
		if self.check("coverage", "exclude"):
			self.str2list("coverage")
			headers = ("Gene", "Mapped Reads", "Percent")
			rows = []
			for gene in self.data.coverage:
				nreads = int(self.data.coverage[gene])
				# use 50 to convert # of read pairs to # of reads
				percent = 50.0 * nreads / int(self.data.exclude["pairs"])
				rows.append((
					gene,
					"{:,d}".format(nreads),
					"{:.1f}%".format(percent)))
			return self.table(rows, headers, 'lrr')

# vim: noexpandtab ts=4 sw=4
