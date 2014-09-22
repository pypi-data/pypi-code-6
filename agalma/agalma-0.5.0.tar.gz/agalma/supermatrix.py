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
Concatenates alignments of orhologous sequences to create a supermatrix.
It also creates a supermatrix with a given proportion of gene occupancy.
"""

import glob
import numpy as np
import os
import shutil
from itertools import izip

from biolite import diagnostics
from biolite import report
from biolite import utils
from biolite import workflows

from biolite.pipeline import Pipeline

pipe = Pipeline('supermatrix', __doc__)

### ARGUMENTS ###

pipe.add_path_arg('align_dir', nargs='?', metavar='DIR', default=None, help="""
	An explicit path to a directory containing a FASTA (.fa) file for
	each alignment.""")

pipe.add_arg('--previous', '-p', metavar='RUN_ID', default=None, help="""
	Use the alignments from a previous run of multalign or multalignx.""")

pipe.add_arg('--seq_type', '-t', default='protein', help="""
	Type of alignments: either protein or nucleotide sequences.""")

pipe.add_arg('--proportion', type=float, default=None, help="""
	If specified, creates a supermatrix with gene occupancy equal to
	proportion in [0-1].""")

### STAGES ###

@pipe.stage
def setup_path(id, seq_type, align_dir, previous):
	"""Determine the path of the input alignments"""

	if seq_type == 'protein': key = 'protdir'
	elif seq_type == 'nucleotide': key = 'nucdir'
	else: utils.die("unknown sequence type", seq_type)

	align_dir = diagnostics.lookup_prev_val(
					id, previous, align_dir, key, 'multalign', 'multalignx')

	if not align_dir:
		utils.die("could not determine alignment directory")

	ingest('align_dir')


@pipe.stage
def supermatrix(seq_type, align_dir, proportion, outdir):
	"""Concatenate multiple nucleotide alignments together into a supermatrix"""

	clusters = glob.glob(os.path.join(align_dir, '*.fa'))

	if seq_type == 'nucleotide':
		nucdir = os.path.join(outdir, 'supermatrix-nuc')
		utils.safe_mkdir(nucdir)
		workflows.phylogeny.supermatrix(clusters, nucdir, 'DNA', proportion)
		finish('nucdir')
	elif seq_type == 'protein':
		protdir = os.path.join(outdir, 'supermatrix-prot')
		utils.safe_mkdir(protdir)
		workflows.phylogeny.supermatrix(clusters, protdir, 'WAG', proportion)
		finish('protdir')
	else:
		utils.die("unknown sequence type", seq_type)


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
		self.basename = "%d.supermatrix" % self.run_id
		# Lookups
		self.lookup_attribute(diagnostics.INIT, 'seq_type')
		self.lookup_attribute(diagnostics.INIT, 'proportion')
		self.lookup_unpack('supermatrix.supermatrix')
		# Generators
		self.generator(self.load_supermatrix)
		self.generator(self.copy_files)
		self.generator(self.occupancy_table)
		self.generator(self.occupancy_plot)
		self.generator(self.cum_occupancy_plot)
		self.generator(self.taxon_genes_table)

	def load_supermatrix(self):
		"""
		"""
		if self.check('occupancy'):
			self.data.occupancy = np.loadtxt(
									self.data.occupancy, skiprows=1
									).transpose()
		if self.check('cum_occupancy'):
			self.data.cum_occupancy = np.loadtxt(self.data.cum_occupancy)

	def copy_files(self):
		# Copy supermatrix and partition to report.
		html = []
		if self.check('fasta'):
			shutil.copy(
				self.data.fasta,
				os.path.join(self.outdir, self.basename + '.fa'))
			html.append('[<a href="{0}.fa">FASTA</a>]')
		if self.check('partition'):
			shutil.copy(
				self.data.partition,
				os.path.join(self.outdir, self.basename + '.partition.txt'))
			html.append('[<a href="{0}.partition.txt">partition</a>]')
		if html:
			return [
				'<p>Files: ',
				' '.join(html).format(self.basename),
				'</p>']

	def occupancy_table(self):
		if self.check('seq_type', 'proportion', 'cum_occupancy', 'cell_occupancy', 'nsites'):
			if self.data.proportion == 'None':
				self.data.proportion = 1.0
			rows = [
				('Sequence type', self.data.seq_type),
				('Target gene occupancy', '%.1f%%' % (100*float(self.data.proportion))),
				('Actual gene occupancy', '%.1f%%' % (100*self.data.cum_occupancy[-1])),
				('Unambiguous cells', '%.1f%%' % (100*float(self.data.cell_occupancy))),
				('Number of genes', '{:,d}'.format(len(self.data.cum_occupancy))),
				('Number of sites', '{:,d}'.format(int(self.data.nsites)))]
			return self.table(rows, style='lr')

	def occupancy_plot(self):
		"""
		Image of the gene occupancy in the supermatrix, ordered by most
		complete taxa, then most complete gene. Black indicates the gene is
		present, white that it is absent.
		"""
		if self.check('occupancy', 'cum_occupancy'):

			# Convert 1.0 to black, 0.0 to white
			occupancy = (-1.0 * self.data.occupancy) + 1.0
			if occupancy.ndim == 1:
				occupancy = np.array([occupancy])

			# Plot matrix as grayscale image.
			return [self.imageplot(
				self.basename + '.png',
				occupancy,
				{
					'title': 'Gene Occupancy',
					'xlabel': 'Genes',
					'xticks': [],
					'ylabel': 'Taxa',
					'yticks': [],
					'figsize': (9, 3)
				})]

	def cum_occupancy_plot(self):
		"""
		Plot of gene occupancies for cumulatively larger subsets of genes in
		the supermatrix, ordered by most complete gene.
		"""
		if self.check('cum_occupancy'):
			# Cumulative occupancy
			return [self.lineplot(
				self.basename + '.cumalitve.png',
				self.data.cum_occupancy,
				{
					'title': 'Cumulative Gene Occupancy',
					'xlabel': 'Genes',
					'ylabel': 'Occupancy',
					'ylim': [0.0, 1.0],
					'figsize': (9, 3)
				})]

	def taxon_genes_table(self):
		"""
		Number and percent of genes per taxon in supermatrix
		"""
		if self.check('taxa', 'occupancy'):
			self.str2list('taxa')
			taxa_occupancy = np.sum(self.data.occupancy, axis=1)
			perc = 100.0 / self.data.occupancy.shape[1]
			rows = []
			for taxon, ngenes in izip(self.data.taxa, taxa_occupancy):
				rows.append(
					(taxon, '%.0f' % ngenes, '%.1f%%' % (ngenes*perc)))
			headers = ("Species", "Number of genes", "Percent")
			return self.table(rows, headers, 'lrr')

# vim: noexpandtab ts=4 sw=4
