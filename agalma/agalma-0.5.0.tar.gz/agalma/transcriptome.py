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
The entire transcriptome pipeline, through assembly.
"""

# This pipeline is a meta-pipeline that connects the following pipelines:
from agalma import preassemble
from agalma import assemble
from agalma import postassemble

from biolite import diagnostics
from biolite.pipeline import IlluminaPipeline

pipe = IlluminaPipeline('transcriptome', __doc__)

### preassemble ###

pipe.import_module(preassemble, start=1)

### assemble ###

pipe.add_arg(
	'--assemble_quality', type=int, metavar='MIN', default=33, help="""
		Filter out reads that have a mean quality < MIN before assembly.""")

pipe.add_arg(
	'--assemble_nreads', type=int, metavar='N', default=0, help="""
		Number of high quality reads to assemble (0 means all).""")

@pipe.stage
def assemble_connector(assemble_quality, assemble_nreads):
	"""[connector between "preassemble" and "assemble"]"""
	return {'quality': assemble_quality, 'nreads': assemble_nreads}

pipe.import_module(assemble, ['min_length', 'ss'], start=1)

### postassemble ###

@pipe.stage
def postassemble_connector(exemplars_fasta):
	"""[connector between "assemble" and "postassemble"]"""
	return {'rrna_exemplars': exemplars_fasta, 'external': False}

pipe.import_module(postassemble, [], start=1)

if __name__ == "__main__":
	# Run the pipeline.
	pipe.run()
	# Push the local diagnostics to the global database.
	diagnostics.merge()

# vim: noexpandtab ts=4 sw=4
