# Agalma - an automated phylogenomics workflow
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
Builds a species tree from a supermatrix.
"""

import os
import random
import sys
from Bio import AlignIO
from agalma import config
from biolite import diagnostics
from biolite import report
from biolite import utils
from biolite import wrappers
from biolite.pipeline import Pipeline

pipe = Pipeline('speciestree', __doc__)

### ARGUMENTS ###

pipe.add_path_arg(
	'alignment', nargs='?', metavar='FASTA',
	default=None, help="""
		An explicit path to a FASTA (.fa) file for the alignment.""")

pipe.add_arg('--previous', '-p', metavar='RUN_ID', default=None, help="""
	Use the alignment from a previous run of supermatrix.""")

pipe.add_arg('--seq_type', '-t', default='protein', help="""
	Type of alignments: either protein or nucleotide sequences.""")

pipe.add_arg('--model', '-m', default='PROTGAMMAWAG', help="""
	The substitution model of evolution for RAxML.""")

pipe.add_arg('--bootstrap', '-b', type=int, default=10, help="""
	Number of bootstrap replicates to run for RAxML.""")

pipe.add_arg('--raxml_flags', '-f', default='', help="""
	Extra parameters to pass to RAxML. Make sure the flags make sense: refer to
	the RAxML Manual for help.""")

pipe.add_arg('--mpi', metavar='MPIRUN', default='', help="""
	Run RAxML in MPI mode using the specified MPIRUN command.""")

pipe.add_arg('--hybrid', action='store_true', default=False, help="""
	Specify in addition to --mpi to Run RAxML in MPI-hybrid mode.""")

### STAGES ###

@pipe.stage
def init(id, seq_type, previous, alignment):
	"""Determine path to input alignment"""

	if seq_type == 'protein': key = 'protdir'
	elif seq_type == 'nucleotide': key = 'nucdir'
	else: utils.die("unknown sequence type", seq_type)

	alignment = diagnostics.lookup_prev_val(
								id, previous, alignment, key, 'supermatrix')

	if not alignment:
		utils.die("could not determine alignment directory")

	if os.path.isdir(alignment):
		alignment = os.path.join(alignment, 'supermatrix.fa')

	diagnostics.log_path(alignment)
	ingest('alignment')


@pipe.stage
def convert_format(alignment, outdir):
	"""Convert alignment from fasta to phylip format"""

	basename = os.path.splitext(os.path.basename(alignment))[0]
	phylip = os.path.abspath(basename + '.phy')
	# Convert to phylip-relaxed to allow taxon names longer than 10
	AlignIO.convert(alignment, 'fasta', phylip, 'phylip-relaxed')

	ingest('phylip')


@pipe.stage
def speciestree(
		phylip, seq_type, model, bootstrap, raxml_flags, mpi, hybrid, outdir):
	"""Build species tree with bootstraps"""

	prot_models = ('PROTCATWAG', 'PROTCATLG',
	               'PROTGAMMAWAG', 'PROTGAMMALG')
	nuc_models = ('GTRMIX', 'GTRCAT', 'GTRGAMMA')

	if seq_type == 'protein' and model not in prot_models:
		utils.die(
			"%s is not a valid model for %s sequences" % (model, seq_type))
	elif seq_type == 'nucleotide' and model not in nuc_models:
		utils.die(
			"%s is not a valid model for %s sequences" % (model, seq_type))

	if bootstrap > 0:
		# Configure raxml to run both bootstraps and ml
		seed = 12345
		raxml_flags = '-f a -N {0} -x {1} '.format(bootstrap, seed) + raxml_flags

	basename = os.path.splitext(os.path.basename(phylip))[0]
	seed = random.randint(0, sys.maxint)

	args = ['-n', basename, '-m', model, '-w', outdir, '-p', seed, raxml_flags]

	# Run RAxML
	if mpi:
		if hybrid:
			wrappers.RaxmlHybrid(mpi, phylip, *args)
		else:
			wrappers.RaxmlMpi(mpi, phylip, *args)
	else:
		wrappers.Raxml(phylip, *args)

	besttree = os.path.join(outdir, "RAxML_bestTree." + basename)
	bipartition = os.path.join(outdir, "RAxML_bipartitions." + basename)
	finish("besttree", "bipartition")


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
		self.lookup('outdir', diagnostics.INIT, 'outdir')
		# Generators
		self.generator(self.supermatrix_tree)

	def supermatrix_tree(self):
		"""
		Maximum-likelihood tree for the supermatrix.
		"""
		if self.check('outdir'):
			newick = os.path.join(
						self.data.outdir,
						'RAxML_bestTree.supermatrix')
			if os.path.exists(newick):
				self.add_js('jsphylosvg-min.js')
				self.add_js('raphael-min.js')
				return ["""
					<div id="run_{0}_canvas"></div>
					<textarea readOnly="true" id="run_{0}_newick_text">{1}</textarea>
					<script type="text/javascript">
					var run_{0}_newick="{1}";
					Smits.PhyloCanvas.Render.Style.text["font-style"]="italic";
					run_{0}_canvas = new Smits.PhyloCanvas(
						run_{0}_newick,
						"run_{0}_canvas",
						800, 800);
					</script>
					""".format(
						self.run_id,
						open(newick).readline().rstrip().replace('_',' '))]

# vim: noexpandtab ts=4 sw=4
