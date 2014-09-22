#!/usr/bin/env python
#
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
Assembles reads into transcripts, processes the assembly, and generates
assembly diagnostics. Read pairs are first filtered at a more stringent
mean quality threshold. Transcriptome assembly is generated with Trinity
assembler.
"""

import os
import shutil
from glob import glob
from agalma import config
from biolite import diagnostics
from biolite import report
from biolite import utils
from biolite import workflows
from biolite import wrappers
from biolite.pipeline import IlluminaPipeline

pipe = IlluminaPipeline('assemble', __doc__)

### ARGUMENTS ###

pipe.add_arg('--quality', '-q', type=int, metavar='MIN', default=33, help="""
	Filter out reads that have a mean quality < MIN.""")

pipe.add_arg('--nreads', '-n', type=int, metavar='N', default=0, help="""
	Number of high quality reads to assemble (0 means all).""")

pipe.add_arg('--min_length', '-l', type=int, metavar='L', default=300, help="""
	Only keep transcripts longer than L nucleotides.""")

pipe.add_arg('--ss', default=None, help="""
	Specify orientation of strand-specific reads: FR or RF for paired, F or R for
	single-end. See the Trinity documentation for more details.""")

### STAGES ###

pipe.add_data_sources("sanitize", "remove_rrna")

@pipe.stage
def prep_data(id, data, quality, nreads):
	"""Filter out low-quality reads and interleave into a single FASTA file"""

	if len(data[-1]) == 1:
		fasta = 'single.fa'
		wrappers.FilterIllumina(
			data[-1], [], "-f -a -b -q", quality, "-n", nreads,
			stdout=fasta)
		paired = False
	elif len(data[-1]) == 2:
		fasta = 'both.fa'
		wrappers.FilterIllumina(
			data[-1], [], "-f -s / -a -b -q", quality, "-n", nreads,
			stdout=fasta)
		paired = True
	else:
		utils.die("expected either 1 (SE) or 2 (PE) input FASTQ files")

	diagnostics.log_path(fasta)
	log_state('data')
	ingest('fasta', 'paired')


@pipe.stage
def trinity(id, fasta, min_length, paired, ss, outdir):
	"""Assemble the filtered reads with Trinity"""

	args = ["--min_contig_length", min_length]
	if paired:
		args.append("--run_as_paired")
	if ss:
		args += ["--SS_lib_type", ss]
	wrappers.Trinity(fasta, *args)
	assembly = os.path.join(outdir, id + ".Trinity.fa")
	shutil.copyfile("trinity_out_dir/Trinity.fasta", assembly)
	diagnostics.log_path(assembly)
	finish("assembly")


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
		self.lookup('filter', 'assemble.prep_data.filter_illumina')
		self.percent('filter', 'percent_kept', 'pairs_kept', 'pairs')
		if 'filter' in self.data:
			# Pull the quality treshold out of the command arguments.
			self.data.filter['quality'] = self.extract_arg(
								'assemble.prep_data.filter_illumina', '-q')
		# Generators
		self.generator(self.filter_table)

	def filter_table(self):
		if 'filter' in self.data:
			html = [self.header("Illumina Filtering")]
			html += self.summarize(report.filter_schema, 'filter')
			return html

# vim: noexpandtab ts=4 sw=4
