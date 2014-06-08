#
# This file is part of TensorToolbox.
#
# TensorToolbox is free software: you can redistribute it and/or modify
# it under the terms of the LGNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TensorToolbox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# LGNU Lesser General Public License for more details.
#
# You should have received a copy of the LGNU Lesser General Public License
# along with TensorToolbox.  If not, see <http://www.gnu.org/licenses/>.
#
# DTU UQ Library
# Copyright (C) 2014 The Technical University of Denmark
# Scientific Computing Section
# Department of Applied Mathematics and Computer Science
#
# Author: Daniele Bigoni
#

__all__ = ['RunUnitTests','RunTestTT','RunTestTensorWrapper','RunTestTTcross','RunTestQTT','RunTestSTT_0D', 'RunTestSTT_2D']

def RunTestTT(maxprocs=None):
    """ Runs the TestTT
    
    :params int maxprocs: If MPI support is enabled, defines how many processors to use.
    """
    import TestTT

def RunTestTensorWrapper(maxprocs=None):
    """ Runs the TestTensorWrapper
    
    :params int maxprocs: If MPI support is enabled, defines how many processors to use.
    """
    import TestTensorWrapper

def RunTestTTcross(maxprocs=None):
    """ Runs the TestTTcross
    
    :params int maxprocs: If MPI support is enabled, defines how many processors to use.
    """
    import TestTTcross

def RunTestQTT(maxprocs=None):
    """ Runs the TestQTT
    
    :params int maxprocs: If MPI support is enabled, defines how many processors to use.
    """
    import TestQTT

def RunTestSTT_0D(maxprocs=None):
    """ Runs the TestSTT_0D
    
    :params int maxprocs: If MPI support is enabled, defines how many processors to use.
    """
    import TestSTT_0D
    TestSTT_0D.run(maxprocs)

def RunTestSTT_2D(maxprocs=None):
    """ Runs the TestSTT_2D
    
    :params int maxprocs: If MPI support is enabled, defines how many processors to use.
    """
    import TestSTT_2D
    TestSTT_2D.run(maxprocs)

def RunUnitTests(maxprocs=None):
    """ Runs all the unit tests.
    
    :params int maxprocs: If MPI support is enabled, defines how many processors to use.
    """
    import TestTT
    import TestTensorWrapper
    import TestTTcross
    import TestQTT
    import TestSTT_0D
    TestSTT_0D.run(maxprocs)
    import TestSTT_2D
    TestSTT_2D.run(maxprocs)
