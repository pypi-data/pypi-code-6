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
Maps expression-only datasets to an assembly, estimates the read count for each
transcript in the assembly (at the gene and isoform level), and loads these
counts into the Agalma database.
"""

import os
from collections import namedtuple
from agalma import config
from agalma import database
from biolite import diagnostics
from biolite import report
from biolite import utils
from biolite import workflows
from biolite import wrappers
from biolite.pipeline import IlluminaPipeline

pipe = IlluminaPipeline('expression', __doc__)

Header = namedtuple(
	'Header',
	"gene isoform confidence genome_type molecule_type")

### ARGUMENTS ###

pipe.add_arg('load_id', metavar='LOAD_ID', help="""
	Load ID for the assembly to use as the reference, or a catalog ID to
	lookup the last load run for that catalog ID.""")

### STAGES ###

@pipe.stage
def find_assembly(id, load_id):
	"""Find assembly in the Agalma database and write to a FASTA file"""

	try:
		load_id = int(load_id)
	except ValueError:
		try:
			load_id = diagnostics.lookup_prev_run(load_id, None, 'load').run_id
		except AttributeError:
			utils.die("no previous loads found for id", load_id)


	assembly = os.path.abspath("assembly.fa")
	wrappers.Sqlite3(
		config.get_resource("agalma_database"),
		"""
			SELECT '>' || nucleotide_header || x'0A' || nucleotide_seq
			FROM sequences
			WHERE run_id=%d;
		""" % load_id,
		stdout=assembly)
	workflows.assembly.stats(assembly)

	diagnostics.log_exit('load_id', load_id)
	ingest('assembly')


@pipe.stage
def quantify(data, assembly, outdir):
	"""Build a table of the number of reads covering each transcript"""

	genes, isoforms = workflows.transcriptome.quantify(
									assembly, 'quantify', data[-1], outdir)
	finish('genes', 'isoforms')


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
		self.lookup("rsem", "expression.quantify.rsem-calculate-expression")
		self.lookup_attribute("expression.parse_expression", "types")
		# Generators
		self.generator(self.rsem_table)
		self.generator(self.types_table)

	def rsem_table(self):
		if self.check("rsem"):
			return self.summarize(report.rsem_schema, "rsem")

	def types_table(self):
		"""
		Table showing classification of genome and molecule types for the
		sequences.
		"""
		if self.check('types'):
			self.str2list('types')
			html = [
				self.header("Sequence Types"),
				'<table class="table table-striped table-condensed table-mini">',
				'<tr><td></td>']
			molecule_types = sorted(database.molecule_types)
			genome_types = sorted(database.genome_types)
			html += map('<td><b>{}</b></td>'.format, molecule_types)
			html.append('</tr>')
			for g in genome_types:
				html.append('</tr><td><b>{}</b></td>'.format(g))
				for m in molecule_types:
					t = database.genome_types[g] + database.molecule_types[m]
					html.append('<td>{:,g}</td>'.format(self.data.types.get(t, 0)))
				html.append('</tr>')
			html.append('</table>')
			return html

# vim: noexpandtab ts=4 sw=4
