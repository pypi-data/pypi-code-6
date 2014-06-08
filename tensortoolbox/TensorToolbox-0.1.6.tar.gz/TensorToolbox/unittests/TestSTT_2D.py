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

def run(maxprocs):

    def f(p,params):
        import numpy as np
        XX = params['XX']
        YY = params['YY']
        return np.sin(np.pi *(XX+YY)) * 1./( (1. + np.sin(2*np.pi*(XX+YY))) * np.sum(p) + 1.)

    x = np.linspace(0,1,11)
    y = np.linspace(0,1,11)
    XX,YY = np.meshgrid(x,y)
    params = {'XX': XX, 'YY': YY}

    d = 8
    ord = 10
    store_file = '2d.pkl'
    store_freq = 20

    orders = [10] * d
    X = [x, y]
    for i in xrange(d):
        X.append( (S1D.JACOBI, S1D.GAUSSLOBATTO, (0.,0.), [0.,1.]) )

    if os.path.isfile(store_file):
        ff = open(store_file)
        STTapprox = pkl.load(ff)
        ff.close()

        STTapprox.set_f(f)
        STTapprox.stt_store_freq = store_freq
        STTapprox.build(maxprocs)
    else:
        STTapprox = TT.STT(f, X, params, range_dim=2, orders=orders, surrogateONOFF=True, surrogate_type=TT.PROJECTION, stt_store_location=store_file, stt_store_overwrite=True, stt_store_freq=store_freq,maxprocs=maxprocs)

    def eval_point(STTapprox,x,params,plotting=False):
        XX = params['XX']
        YY = params['YY']

        # Evaluate a point
        start_eval = systime.clock()
        val = STTapprox(x)
        end_eval = systime.clock()
        print "Evaluation time: " + str(end_eval-start_eval)

        start_eval = systime.clock()
        exact = f(x,params)
        end_eval = systime.clock()
        print "Exact evaluation time: " + str(end_eval-start_eval)

        print "L2err: " + str(npla.norm( (val-exact).flatten(),2 ))

        if plotting:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            surf = ax.plot_surface(XX,YY,val)
            plt.title("Surrogate")
            plt.show(block=False)

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            surf = ax.plot_surface(XX,YY,exact)
            plt.title("Exact")
            plt.show(block=False)

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            surf = ax.plot_surface(XX,YY,np.abs(exact-val))
            plt.title("Error")
            plt.show(block=False)

    eval_point(STTapprox,np.array([0.2]*d),params,plotting=False)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        maxprocs = int(sys.argv[1])
    else:
        maxprocs = None

    run(maxprocs)

