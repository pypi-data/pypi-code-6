# -*- coding: utf-8 -*-

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

import numpy as np

from numpy import linalg as la
from numpy import random

from scipy import stats

from mpi4py import MPI

from time import clock

from sobol_lib import i4_sobol_generate

class MultiDimDistribution():
    dists = []
    
    def __init__(self,dists):
        self.dists = dists;
    
    def rvs(self,size):
        samples = []
        for i in range(len(self.dists)):
            samples.append(self.dists[i].rvs(size))
        return np.asarray(samples).T

def Experiments(f,samples,params,paramUpdate,action):
    """
    Compute the Experiments f on the samples.
    The implementation uses MPI for parallel computations.
    INPUT:
        - f : experiment function handle. Signature: f( params )
        - samples : nd-array with the set of samples grouped by the first dimension
        - params: set of parameters to be passed to the experiment
        - action: post processing action
    OUTPUT:
        Array of computed values, ordered by the first dimension of the array.
    """
    
    def iterF(f,samples,params,paramUpdate,action):
        sols = []
        for i in xrange(0,samples.shape[0]):
            params = paramUpdate(params,samples[i])
            sol = f(params)
            print "Proc %d run %d/%d" % (myrank,i+1,len(samples))
            sols = action(sols,sol)
        return sols
    
    comm = MPI.COMM_WORLD
    nprocs = comm.Get_size()
    myrank = comm.Get_rank()
    
    if myrank == 0:
        # Split the input array
        splittedSamples = np.array_split(samples,nprocs)
        startTime = clock()
    else:
        splittedSamples = None
    
    samplesPart = comm.scatter(splittedSamples,root=0)
    
    splittedSolutions = iterF(f,samplesPart,params,paramUpdate,action)
    
    solutionsList = comm.gather(splittedSolutions)
    
    if myrank == 0:
        # Reassemble post processing data
        # To be fixed for MPI!!!!!! Use the proper action..
        solutions = [inner for outer in solutionsList for inner in outer]

        stopTime = clock()
        print "Elapsed Time: %f s" % (stopTime-startTime)
        
        return solutions

def MonteCarlo(dists,N,experiment,params,paramUpdate,postProc):
    """
    Run Monte Carlo Simulations
    """
    mdd = MultiDimDistribuion(dists);
    samples = mdd.rvs(N)
    return (samples,Experiments(experiment, samples, params, paramUpdate, postProc))

def QuasiMonteCarlo(dists,N,experiment,params,paramUpdate,postProc,skip=None):
    """
    Run Quasi Monte Carlo Simulations
    """
    # Generate uniformly distributed samples using Sobol sequence
    if skip == None:
        dim = len(dists)
        skip = int( np.random.uniform(2**np.ceil(np.log2(dim+1)), 2**(np.ceil(np.log2(dim+1))+1)) )
    unifSamples = i4_sobol_generate(len(dists),N,skip); 
    samples = np.zeros(unifSamples.T.shape);
    for i in range(0,len(dists)):
        samples[:,i] = dists[i].ppf(unifSamples[i,:])
    return (samples,Experiments(experiment, samples, params, paramUpdate, postProc), skip)

def lhc(N,d,dists=None):
    XX = np.zeros((N,d))
    for i in range(0,N):
        XX[i,:] = stats.uniform(loc=(i*1./N),scale=1./N).rvs(size=d)
    
    P = np.zeros((N,d),dtype=np.int)
    for i in range(0,d):
        P[:,i] = np.arange(0,N)
        random.shuffle(P[:,i])
    
    for i in range(0,d):
        XX[:,i] = XX[P[:,i],i]
    
    ''' Convert from uniform to dists '''
    udist = stats.uniform(0.,1.);
    if dists != None and len(dists) == d:
        for i in range(d):
            XX[:,i] = dists[i].ppf(udist.cdf(XX[:,i]))
    
    return XX

def LatinHyperCube(dists,N,experiment,params,paramUpdate,postProc):
    """
    Run Latin Hyper Cube Simulations
    """
    samples = lhc(N,len(dists),dists)
    return (samples,Experiments(experiment, samples, params, paramUpdate, postProc))
