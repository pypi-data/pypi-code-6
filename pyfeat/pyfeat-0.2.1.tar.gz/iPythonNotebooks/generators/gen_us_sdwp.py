#!/usr/bin/env python
r"""
.. codeauthor:: Antonia Mey <antonia.mey@fu-berlin.de> Christoph Wehmeyer <christoph.wehmeyer@fu-berlin.de>
"""
import numpy as np
from potentials import SymetricDoubleWellPotential
from potentials import HarmonicRestraint
from integrators import BrownianIntegrator
from replica import USReplica
import os



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
    directory=os.path.join("data","US_SDW")
    if not os.path.exists(directory):
        os.makedirs(directory)
    #setting the simulation temperature
    kT = np.array( [1.0] )
    nsteps=1500
    
    dwp = SymetricDoubleWellPotential()
    Z = dwp.get_partition_function(kT)
    #exact probability distribution for comparison
    e_file = os.path.join(directory,"exact.dat")
    fh = open( e_file, 'w' )
    for c in xrange( dwp.bin_centers.shape[0] ):
        p=np.exp(-dwp.energy( dwp.bin_centers[c] )* 1.0/kT[0])
        fh.write( "%4f %+.6e" % ( dwp.bin_centers[c] , p ) )
        fh.write("\n")
    fh.close()
    
    integrator = BrownianIntegrator( dwp, 0.01, 1.0/kT[0], 1.0, 1.0 )
    restraints_pos = np.array([-1.7,-1.5,-1.3,-1.1,-0.9,-0.7,-0.55,-0.4,-0.25,-0.15,-0.05,0.0,0.05,0.15,0.25,0.4,0.55,0.7,0.9,1.1,1.3,1.5,1.7])
    restraint_k = np.array([20,10,15,15,15,20,20,20,30,40,40,50,40,40,30,20,20,20,15,15,15,10,20])
    #restraints_pos = np.linspace(-1.8,1.8,16)
    n_therm_states = restraints_pos.shape[0]
    
    
    restraints = []
    for i in xrange(restraints_pos.shape[0]):
        restraints.append(HarmonicRestraint(restraints_pos[i],restraint_k[i]))
    replica = USReplica(integrator, restraints)
    replica.run(nsteps)
    for r in xrange(restraints_pos.shape[0]):
        traj = np.array(replica.trajectory[r])
        n_traj_frames = traj.shape[0]
        r_file = os.path.join(directory,"replica"+str(r)+".dat")
        fh =open(r_file, 'w')
        for t in xrange( n_traj_frames ):
            fh.write( "%6d %6d %+.6e " % (discretize( traj[t,0], dwp.inner_edges ) , traj[t,1] , traj[t,2]/kT[0]) )
            for j in xrange(restraints_pos.shape[0]):
                fh.write("%+.6e " % (traj[t,3+j]/kT[0]))
            fh.write("\n")
        fh.close()
        
    wham_f = os.path.join(directory,"us_wham.dat")
    fh = open(wham_f, 'w')
    for c in xrange( dwp.bin_centers.shape[0] ):
        for i in xrange( n_therm_states ):
            fh.write( " %+.8e" % ( restraints[i].energy( dwp.bin_centers[c] ) / kT[0] ) )
        fh.write( "\n" )
    fh.close()