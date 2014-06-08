#
# This file is part of mpi_map.
#
# mpi_map is free software: you can redistribute it and/or modify
# it under the terms of the LGNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# mpi_map is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# LGNU Lesser General Public License for more details.
#
# You should have received a copy of the LGNU Lesser General Public License
# along with mpi_map.  If not, see <http://www.gnu.org/licenses/>.
#
# DTU UQ Library
# Copyright (C) 2014 The Technical University of Denmark
# Scientific Computing Section
# Department of Applied Mathematics and Computer Science
#
# Author: Daniele Bigoni
#

__all__ = ['mpi_map', 'mpi_map_code']

import os
import sys
import marshal, types
import inspect
import itertools
try:
    from mpi4py import MPI
    MPI_SUPPORT = True
except ImportError:
    MPI_SUPPORT = False

def mpi_map(f, x, params, procs):
    """ This function applies the function ``f`` to the ``x`` inputs on ``procs`` processors.
    
    :param str f: a marshallable function
    :param list x: list of inputs to be passed (pickable)
    :param params: parameters to be passed to the function (pickable)
    :param int procs: number of processors to be used
    """
    
    f_code = marshal.dumps(f.func_code)
    return mpi_map_code(f_code, x, params, procs)

def mpi_map_code(func_code, x, params, procs):
    """ This function applies the function in ``func_code`` to the ``x`` inputs on ``procs`` processors.
    
    :param str func_code: String containing the marshalled version of the function
    :param list x: list of inputs to be passed (pickable)
    :param params: parameters to be passed to the function (pickable)
    :param int procs: number of processors to be used
    """
    
    if not MPI_SUPPORT:
        raise ImportError("MPI is not supported by this system. Install mpi4py or run iteratively.")
    import mpi_map        # Do I need this? Yes, to get the folder! See next line.
    path = os.path.dirname(inspect.getfile(mpi_map)) + "/"

    procs = min(procs,len(x))
    
    comm = MPI.COMM_SELF.Spawn(sys.executable,
                               args=[path + 'mpi_eval.py'],
                               maxprocs=procs)
    
    # Broadcast function and parameters
    comm.bcast((func_code, params), root=MPI.ROOT)
    
    # Split the input data
    ns = [len(x) // procs]*procs
    for i in xrange(len(x) % procs): ns[i] += 1
    for i in xrange(1,procs): ns[i] += ns[i-1]
    ns.insert(0,0)
    split_x = [ x[ns[i]:ns[i+1]] for i in xrange(0, procs) ]
    
    # Scatter the data
    comm.scatter(split_x, root=MPI.ROOT)
    
    # Gather the results
    fval = comm.gather(None,root=MPI.ROOT)
    
    comm.Disconnect()

    fval = list(itertools.chain(*fval))
    
    return fval
