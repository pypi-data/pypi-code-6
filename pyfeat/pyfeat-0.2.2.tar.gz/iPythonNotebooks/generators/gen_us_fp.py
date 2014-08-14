#!/usr/bin/env python
r"""
.. codeauthor:: Antonia Mey <antonia.mey@fu-berlin.de> Christoph Wehmeyer <christoph.wehmeyer@fu-berlin.de>
"""
import numpy as np
from potentials import FoldingPotential
from potentials import HarmonicRestraint
from integrators import BrownianIntegrator
from replica import USReplica
import os
import matplotlib.pyplot as plt



#================================
#Functions
#================================
def discretize( x, inner_edges ):
    r""" discretises a trajectory into Markov states
    Parameters
    ----------
    x : double
        position coordinate
    inner_edges : double array
        array of inner edges of the binning
    Returns
    -------
    returns the discrete state according to the binning
    
    """

    if x<inner_edges[0]:
        return 0
    if x>=inner_edges[-1]:
        return inner_edges.shape[0]
    for i in xrange( inner_edges.shape[0]-1 ):
        if ( inner_edges[i]<=x) and ( x< inner_edges[i+1] ):
            return i+1

#================================
#Main
#================================
if '__main__' == __name__:
    #checking if directories for writing exist
    directory=os.path.join("data","US_FP")
    if not os.path.exists(directory):
        os.makedirs(directory)
    #setting the simulation temperature
    kT = np.array( [1.1] )
    nsteps=1000
    
    fp = FoldingPotential(3.0)
    d=np.linspace(0,8,100)
    Z = fp.get_partition_function(kT,d)
    #exact probability distribution for comparison
    e_file = os.path.join(directory,"exact.dat")
    fh = open( e_file, 'w' )
    for c in  xrange(fp.bin_centers.shape[0]) :
        p=fp.prob_density( kT[0], fp.bin_centers[c])
        fh.write( "%4f %+.6e" % ( fp.bin_centers[c] , p ) )
        fh.write("\n")
    fh.close()
    
    integrator = BrownianIntegrator( fp, 0.01, 1.0/kT[0], 1.0, 1.0 )
    restraints_pos = np.linspace(0.1,6.5,20)
    n_therm_states = restraints_pos.shape[0]
    
    
    restraints = []
    for r0 in restraints_pos:
        restraints.append(HarmonicRestraint(r0,30.0))
    replica = USReplica(integrator, restraints)
    replica.run(nsteps)
    
    
    
    for r in xrange(restraints_pos.shape[0]):
        traj = np.array(replica.trajectory[r])
        n_traj_frames = traj.shape[0]
        r_file = os.path.join(directory,"replica"+str(r)+".dat")
        fh =open(r_file, 'w')
        for t in xrange( n_traj_frames ):
            fh.write( "%6d %6d %+.6e " % (discretize( traj[t,0], fp.inner_edges ) , traj[t,1] , traj[t,2]/kT[0]) )
            for j in xrange(restraints_pos.shape[0]):
                fh.write("%+.6e " % (traj[t,3+j]/kT[0]))
            fh.write("\n")
        fh.close()
        
    wham_f = os.path.join(directory,"us_wham.dat")
    fh = open(wham_f, 'w')
    for c in xrange( fp.bin_centers.shape[0] ):
        for i in xrange( n_therm_states ):
            fh.write( " %+.8e" % ( restraints[i].energy( fp.bin_centers[c] ) / kT[0] ) )
        fh.write( "\n" )
    fh.close()
