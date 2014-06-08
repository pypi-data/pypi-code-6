#!/usr/bin/env python

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

__all__ = []

import marshal, types
try:
    from mpi4py import MPI
    MPI_SUPPORT = True
except ImportError:
    MPI_SUPPORT = False

if __name__ == "__main__":
    comm = MPI.Comm.Get_parent()

    # Get the broadcasted function and parameters
    (code_string,params) = comm.bcast(None, root=0)

    # De-marshal function
    code = marshal.loads(code_string)
    func = types.FunctionType(code, globals(), "f")

    # Get scattered data
    part_x = comm.scatter(None, root=0)

    # Evaluate
    fval = [ func(x,params) for x in part_x ]

    # Gather
    comm.gather(fval, root=0)

    comm.Disconnect()
