# BioLite - Tools for processing gene sequence data and automating workflows
# Copyright (c) 2012-2014 Brown University. All rights reserved.
#
# This file is part of BioLite.
#
# BioLite is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BioLite is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BioLite.  If not, see <http://www.gnu.org/licenses/>.

"""
Provides a collection of helper functions that coordinate multiple wrappers
from the :ref:`wrappers` to accomplish a unified goal or automate a common
analysis task.

Workflows are available for:

* Transcriptome statistics and assembly sweeps
* Contig parsing
* Blast result parsing
* Phylogenomic inference
* Interfacing with the NCBI Sequence Read Archive (SRA)
"""

import assembly
import blast
import phylogeny
import rrna
import sra
import transcriptome
