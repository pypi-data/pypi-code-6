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
Loads assembled sequences and protein translations into Agalma's database.  If
the sequences were generated with Agalma, it stores the gene/isoform names, the
estimated expression and the BLAST annotation if present.  For non-Agalma
(external) sequences, the entire header line up to the first space is used as
the gene name and isoforms are not supported.
"""

import re
from Bio import SeqIO
from collections import defaultdict
from operator import itemgetter
from agalma import database
from biolite import diagnostics
from biolite import report
from biolite import utils
from biolite import workflows
from biolite.pipeline import Pipeline

pipe = Pipeline('load', __doc__)

### ARGUMENTS ###

pipe.add_arg("--previous", "-p", metavar="RUN_ID", default=None, help="""
	Use the assembly, translation and rrna from a previous run of postassemble.""")

pipe.add_path_arg("--assembly", default=None, help="""
	Path to nucleotide FASTA file for the assembly.""")

pipe.add_path_arg("--translation", default=None, help="""
	Path to protein FASTA file for the translated assembly.""")

pipe.add_path_arg("--rrna", default=None, help="""
	Path to nucleotide FASTA file for rRNA cleaned from the assembly..""")

### STAGES ##

@pipe.stage
def setup_paths(id, previous, assembly, translation, rrna):
	"""Determine the paths to the nucleotide and protein FASTA files"""

	if not (assembly and translation and rrna):
		pipelines = ("postassemble", "transcriptome")
		try:
			prev = diagnostics.lookup_prev_run(id, previous, *pipelines)
			values = diagnostics.lookup(prev.run_id, diagnostics.EXIT)
		except AttributeError:
			utils.die("no previous", '/'.join(pipelines), "runs found for id", id)
		try:
			if not assembly:
				assembly = diagnostics.str2list(values["assembly"])[-1]
			if not translation:
				translation = diagnostics.str2list(values["translation"])[-1]
			if not rrna:
				rrna = values["rrna"]
		except KeyError:
			utils.die(
				"couldn't find paths in previous run", prev.run_id)

	utils.info("assembly:", assembly)
	utils.info("translation:", translation)
	utils.info("ribosomal sequences:", rrna)

	ingest("assembly", "translation", "rrna")

@pipe.stage
def parse_fasta(id, _run_id, assembly, translation, rrna):
	"""Parse the FASTA records to populate the fields of the database"""

	fields = map(itemgetter(0), database.sequences_schema)
	seqs = defaultdict(utils.AttributeDict)

	# RE for validating nucleotides
	nuc_alphabet = re.compile(r"^[acgntACGNT]+$")
	# RE for validating amino acids
	aa_alphabet = re.compile(r"^[a-zA-Z\-]+$")

	for i, record in enumerate(SeqIO.parse(rrna, "fasta")):
		nucleotide_seq = str(record.seq)
		# Validate sequence.
		if not nuc_alphabet.match(nucleotide_seq):
			utils.info("skipping bad rrna sequence #%d" % (i+1))
			continue
		# Parse sequence header.
		header = workflows.transcriptome.unpack_header(record.description)
		header.isoform = 1
		header.genome_type = database.get_genome_type(header.blast_hit)
		header.molecule_type = database.get_molecule_type(header.blast_hit)
		# Store to sequences.
		seq = seqs[record.id]
		seq.update(header)
		seq.nucleotide_seq = nucleotide_seq
		seq.nucleotide_header = record.description

	for i, record in enumerate(SeqIO.parse(assembly, "fasta")):
		nucleotide_seq = str(record.seq)
		# Validate sequence.
		if not nuc_alphabet.match(nucleotide_seq):
			utils.info("skipping bad nucleotide sequence #%d" % (i+1))
			continue
		# Check for duplicate id.
		if record.id in seqs:
			utils.info("skipping repeat nucleotide id", record.id)
			continue
		# Parse sequence header.
		header = workflows.transcriptome.unpack_header(record.description)
		header.genome_type = database.genome_types["unknown"]
		header.molecule_type = database.molecule_types["unknown"]
		# Store to sequences.
		seq = seqs[record.id]
		seq.update(header)
		seq.nucleotide_seq = nucleotide_seq
		seq.nucleotide_header = record.description

	for i, record in enumerate(SeqIO.parse(translation, "fasta")):
		protein_seq = str(record.seq).rstrip('*')
		# Validate sequence.
		if not aa_alphabet.match(protein_seq):
			utils.info("skipping bad protein sequence #%d" % (i+1))
			continue
		# Check for duplicate id.
		if record.id in seqs and "protein_header" in seqs[record.id]:
			utils.info("skipping repeat protein id", record.id)
			continue
		# Parse sequence header.
		header = workflows.transcriptome.unpack_header(record.description)
		header.genome_type = database.get_genome_type(header.blast_hit)
		header.molecule_type = database.molecule_types["protein-coding"]
		# Store to sequences.
		seq = seqs[record.id]
		seq.update(header)
		seq.protein_seq = protein_seq
		seq.protein_header = record.description
		seq.translation_method = "ORF"

	rows = []
	types = {}
	for seq in seqs.itervalues():
		rows.append(tuple([None, _run_id, id] + map(seq.get, fields[3:])))
		# Record genome/molecule type
		t = seq.genome_type + seq.molecule_type
		types[t] = types.get(t, 0) + 1

	diagnostics.log("types", types)

	ingest("rows")


@pipe.stage
def commit(_run_id, rows):
	"""Commit sequences to the Agalma database"""

	if not rows:
		utils.info("skipping: no rows were populated")
		return

	database.execute("BEGIN")

	# Clear any previous/failed loads
	database.execute("DELETE FROM sequences WHERE run_id=?;", (_run_id,))

	sql = "INSERT INTO sequences VALUES (%s);" % (','.join(['?'] * len(rows[0])))
	database.executemany(sql, rows)

	database.execute("COMMIT")


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
		self.lookup_attribute('load.parse_fasta', 'types')
		# Generators
		self.generator(self.types_table)

	def types_table(self):
		"""
		Table showing classification of genome and molecule types for the
		loaded sequences.
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
					html.append('<td>{:,d}</td>'.format(self.data.types.get(t, 0)))
				html.append('</tr>')
			html.append('</table>')
			return html

# vim: noexpandtab ts=4 sw=4
