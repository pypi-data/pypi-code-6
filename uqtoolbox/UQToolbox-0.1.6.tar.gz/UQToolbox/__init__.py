# -*- coding: utf-8 -*-

#!/usr/bin/env python

#
# This file is part of UQToolbox.
#
# UQToolbox is free software: you can redistribute it and/or modify
# it under the terms of the LGNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# UQToolbox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# LGNU Lesser General Public License for more details.
#
# You should have received a copy of the LGNU Lesser General Public License
# along with UQToolbox.  If not, see <http://www.gnu.org/licenses/>.
#
# DTU UQ Library
# Copyright (C) 2014 The Technical University of Denmark
# Scientific Computing Section
# Department of Applied Mathematics and Computer Science
#
# Author: Daniele Bigoni
#


"""

Created on Wed Jul 11 10:40:30 2012

@author: Daniele Bigoni (dabi@imm.dtu.dk)

UncertaintyQuantificationToolbox is the collection of tools for Uncertainty Quantification.

@copyright: 2012-2014 The Technical University of Denmark
"""

import aux
from aux import *
import unittests
from unittests import *

__all__ = []
__all__ += aux.__all__
__all__ += ["RandomSampling","ModelReduction","gPC","sobol_lib","CutANOVA","mcmc"]

__author__ = "Daniele Bigoni"
__copyright__ = """Copyright 2012-2014, The Technical University of Denmark"""
__credits__ = ["Daniele Bigoni"]
__maintainer__ = "Daniele Bigoni"
__email__ = "dabi@imm.dtu.dk"
__status__ = "Production"
