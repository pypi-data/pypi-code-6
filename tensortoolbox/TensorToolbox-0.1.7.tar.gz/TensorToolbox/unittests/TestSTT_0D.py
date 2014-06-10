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

import sys
import time as systime
import numpy as np
import numpy.linalg as npla
from SpectralToolbox import Spectral1D as S1D
import TensorToolbox as TT
import os.path
import pickle as pkl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# For this example see also the documentation of the class STT

def run(maxprocs):

    # Function definition.
    # For MPI purposes, that cannot be imported from the system path (like user defined functions
    # used by f) MUST be defined inside the following definition. Whatever can be imported from
    # the system path (like numpy), can be imported from inside it.
    def f(p,params):
        import numpy as np
        return 1./(np.sum(p) + 1.)

    params = None               # Parameters to be passed to function f. In this case None.
                                # They must be Pickable

    order = 10                  # Approximation order
    store_file = '0d.pkl'       # Storage file (used for storage and restarting purposes
    store_freq = 10             # Seconds between every storage
    surr_type = TT.PROJECTION   # Alternatives are: TT.PROJECTION, TT.LINEAR_INTERPOLATION
                                #                   and TT.LAGRANGE_INTERPOLATION

    d = 4                       # Number of dimensions (The analytical integrals work for d=4)
    orders = [order] * d        # orders of the approximation
    X = []                      # Approximation points
    for i in xrange(d):
        if surr_type == TT.PROJECTION:
            # For each dimension, define: the polynomial type, the type of points, the polynomial parameters and the span over which the points will be rescaled
            X.append( (S1D.JACOBI, S1D.GAUSSLOBATTO, (0.,0.), [0.,1.]) )
        else:
            # In the LINEAR_INTERPOLATION and LAGRANGE_INTERPOLATION case any list of points in the span will work (Include the endpoints!).
            X.append( np.linspace(0.,1.,40) )

    if os.path.isfile(store_file): # If file already exists, then restart the construction from
                                   # already computed values
        ff = open(store_file)
        STTapprox = pkl.load(ff)
        ff.close()

        STTapprox.set_f(f)
        STTapprox.stt_store_freq = store_freq
        STTapprox.build(maxprocs)

    else:                       # Otherwise start a new approximation
        STTapprox = TT.STT(f, X, params, range_dim=0, orders=orders, surrogateONOFF=True, surrogate_type=surr_type, stt_store_location=store_file, stt_store_overwrite=True, stt_store_freq=store_freq,maxprocs=maxprocs) # See documentation of STT


    def eval_point(STTapprox,x,params,plotting=False):
        # Evaluates a point x with the STT approximation and the analytical function
        # Compare times and error

        # Evaluate a point
        start_eval = systime.clock()
        val = STTapprox(x)      # Point evaluation in TT format
        end_eval = systime.clock()
        print "Evaluation time: " + str(end_eval-start_eval)

        start_eval = systime.clock()
        exact = f(x,params)
        end_eval = systime.clock()
        print "Exact evaluation time: " + str(end_eval-start_eval)

        print "Err: " + str(np.abs(val-exact))

    # Point evaluation
    x = np.array([0.2]*d)
    eval_point(STTapprox,x,params,plotting=True)
    
    if surr_type == TT.PROJECTION:
        # Computing the mean
        mean = STTapprox.integrate()
        if d == 4:
            exact = -272. * np.log(2)/3. + 27. * np.log(3) + 125. * np.log(5) / 6.
            print "Mean err: %e" % (np.abs(mean-exact))
        else:
            print "Mean: %e" % mean

        # Computing the variance
        var = (STTapprox**2).integrate() - mean**2. # Mind that in the expression STTapprox**2,
                                                    # 2 is an integer!
        if d == 4:
            exact = np.log(4722366482869645213696./(1861718135983154296875. * np.sqrt(5))) - mean**2.
            print "Var err: %e" % (np.abs(var-exact))
        else:
            print "Variance: %e" % var

if __name__ == "__main__":
    # Number of processors to be used, defined as an additional arguement 
    # $ python TestSTT_0D.py N
    # Mind that the program in this case will run slower than the non-parallel case
    # due to the overhead for the creation and deletion of threads.
    if len(sys.argv) == 2:
        maxprocs = int(sys.argv[1])
    else:
        maxprocs = None

    run(maxprocs)

