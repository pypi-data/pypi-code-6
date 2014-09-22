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
Identifies orthologous sequences across datasets. Takes assembly or group of
assemblies and prepares a set of comprehensive comparisons between them.
"""

import os
import numpy
from collections import namedtuple
from agalma import config
from agalma import database
import biolite.database
from biolite import diagnostics
from biolite import report
from biolite import utils
from biolite import wrappers
from biolite.pipeline import Pipeline

pipe = Pipeline('orthologize', __doc__)

SpeciesData = namedtuple('SpeciesData', "name ncbi_id itis_id catalog_id")

### ARGUMENTS ###

pipe.add_arg('load_ids', nargs='+', metavar='LOAD_IDS', help="""
	Specifies which datasets to analyze; A space delimited list of run_id's
	corresponding to the load runs that populated the database""")

### STAGES ###

@pipe.stage
def lookup_species(load_ids):
	"""Lookup the species data for each run"""

	species = {}

	# Given a run_id, returns a named tuple with the following elements:
	#
	# name		The species names
	# ncbi_id		The NCBI taxon id
	# itis_id		The ITIS taxon id
	# catalog_id	The agalma catalog id

	for load_id in load_ids:
		row = biolite.database.execute("""
			SELECT catalog.species, catalog.ncbi_id, catalog.itis_id, catalog.id
			FROM catalog, runs
			WHERE runs.run_id=? AND catalog.id=runs.id;""",
			(load_id,)).fetchone()
		if not row:
			utils.die("Couldn't find species data for run ID %s" % load_id)
		if row[0] is None:
			utils.die("Species name is empty for catalog ID '%s'" % row[3])
		species[load_id] = SpeciesData(*row)
		diagnostics.log(str(load_id), row)

	diagnostics.log("species", species)
	ingest('species')


@pipe.stage
def write_fasta(id, _run_id, load_ids, species, outdir):
	"""Write the fasta file; also, make a list of nodes in the output directory corresponding sequences."""

	db = utils.safe_mkdir('DB')

	nloads = 0
	nseqs = 0
	nbases = 0
	for load_id in load_ids:
		nloads += 1
		taxon = species[load_id].name.replace(' ', '_').replace(':', '_')
		with open(os.path.join(db, taxon+'.fa'), 'w') as f:
			for record in database.load_seqs(load_id, taxon, 'protein'):
				nseqs += 1
				nbases += len(record.seq)
				print >>f, '>%d' % record.id
				print >>f, record.seq

	if not nseqs:
		utils.die("no sequences were written to the FASTA file")

	diagnostics.log('nloads', nloads)
	diagnostics.log('nseqs', nseqs)
	diagnostics.log('nbases', nbases)


@pipe.stage
def compare():
	"""All-by-all comparison to identify orthologous groups with OMA"""

	wrappers.Oma()
	return {'groups': os.path.join('Output', 'OrthologousGroups.txt')}


@pipe.stage
def load_groups(_run_id, groups):
	"""Load groups from OMA into homology database"""

	hist = {}

	database.execute("BEGIN")
	database.execute("DELETE FROM homology WHERE run_id=?;", (_run_id,))
	group_id = 0
	for line in open(groups):
		if line.startswith('#'): continue
		group = [x.partition(':')[2] for x in line.rstrip().split()[1:]]
		if group:
			l = len(group)
			hist[l] = hist.get(l, 0) + 1
			for seq_id in group:
				database.execute("""
					INSERT INTO homology (run_id, component_id, sequence_id)
					VALUES (?,?,?);""",
					(_run_id, group_id, seq_id))
			group_id += 1
	database.execute("COMMIT")

	utils.info(
		"histogram of orthologous group sizes:\n",
		'\n '.join("%d\t:\t%d" % (k, hist[k]) for k in sorted(hist)))

	diagnostics.log('histogram', hist)


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
		self.lookup('load_ids', diagnostics.INIT, 'load_ids')
		self.str2list('load_ids')
		self.lookup('species', 'homologize.lookup_species')
		self.lookup('nseqs', 'homologize.write_fasta', 'nseqs')
		# Generators
		self.generator(self.species_table)
		self.generator(self.component_histogram)

	def species_table(self):
		"""
		Summary of all species processed.
		"""
		html = []
		if self.check('nseqs'):
			html.append("<p>Total sequences: %s</p>" % self.data.nseqs)
		if self.check('load_ids', 'species'):
			headers = ("Load ID", "Catalog ID", "Species", "NCBI ID", "ITIS ID")
			rows = []
			for load_id in self.data.load_ids:
				row = self.data.species.get(str(load_id), '()')
				row = diagnostics.str2list(row)
				if len(row) == 4:
					rows.append((load_id, row[3], row[0], row[1], row[2]))
				else:
					rows.append((load_id, '-', '-', '-', '-'))
			html += self.table(rows, headers)
		return html

	def component_histogram(self):
		"""
		Distribution of the number of nodes in each cluster.
		"""
		hist = {}
		sql = """
			SELECT component_id, COUNT(*)
			FROM homology
			WHERE run_id=?
			GROUP BY component_id;"""
		for id, count in database.execute(sql, (self.run_id,)):
			hist[count] = hist.get(count, 0) + 1
		if hist:
			hist = [(k,hist[k]) for k in sorted(hist.iterkeys())]
			imgname = "%d.component.hist.png" % self.run_id
			props = {
				'title': "Distribution of Cluster Sizes",
				'xlabel': "# Nodes in Cluster",
				'ylabel': "Frequency"}
			return [self.histogram_overlay(imgname, [numpy.array(hist)], props=props)]

