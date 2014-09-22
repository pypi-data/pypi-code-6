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
Prepares raw paired-end Illumina data for assembly
"""

# This pipeline is a meta-pipeline that connects the following pipelines:
from agalma import sanitize
from agalma import insert_size
from agalma import remove_rrna

from biolite import diagnostics
from biolite.pipeline import IlluminaPipeline

pipe = IlluminaPipeline('preassemble', __doc__)

### sanitize ###

pipe.import_module(sanitize, start=1)

### insert_size ###

pipe.add_arg('--insert_quality', type=int, metavar='MIN', default=36, help="""
	Use reads with mean quality > MIN.""")

pipe.add_arg('--insert_nreads', type=int, metavar='N', default=100000, help="""
	Number of high quality reads to use.""")

@pipe.stage
def insert_connector(insert_quality, insert_nreads):
	"""[connector between "sanitize" and "insert_size"]"""
	return {'quality': insert_quality, 'nreads': insert_nreads}

pipe.import_module(insert_size, [], start=1)

### remove_rrna ###

pipe.add_arg('--rrna_quality', type=int, metavar='MIN', default=36, help="""
	Use reads with mean quality > MIN.""")

@pipe.stage
def rrna_connector(rrna_quality):
	"""[connector between "insert_size" and "remove_rrna"]"""
	return {'quality': rrna_quality}

pipe.import_module(remove_rrna, ['subsets', 'ss'], start=1)

if __name__ == "__main__":
	# Run the pipeline.
	pipe.run()
	# Push the local diagnostics to the global database.
	diagnostics.merge()

# vim: noexpandtab ts=4 sw=4
