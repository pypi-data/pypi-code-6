#!/usr/bin/env python
r"""

=====================
Result data container
=====================

.. codeauthor:: Antonia Mey <antonia.mey@fu-berlin.de>, Christoph Wehmeyer <christoph.wehmeyer@fu-berlin.de>

"""

#================================
#Imports
#================================
import numpy as np
from potentials import FoldingPotential
from integrators import BrownianIntegrator
from replica import STReplica
import os

#================================
#Functions
#================================
def discretize( x, inner_edges ):
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
    N_EXCHANGES=10000
    #checking if directories for writing exist
    directory="data/ST_FP/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    kT = np.array([1.1,1.2,1.4, 1.6, 1.7])
    n_therm_states = len(kT)
    initial_x = 0.5
    initial_t = 0
    n_dim = 5
    
    #set the initial n_d vector
    pos = np.ones(n_dim)
    pos = pos*initial_x
    
    fp = FoldingPotential(3.0)
    d=np.linspace(0,8,100)
    Z = fp.get_partition_function(kT,d)
    integrator = BrownianIntegrator( fp, 0.01, 1.0/kT[initial_t], 1.0, 1.0 )
    integrator.set_t_index(initial_t)
    integrator.set_position(pos)
    replica = STReplica(Z, integrator, kT )
    for i in xrange(N_EXCHANGES):
        replica.run(100)
        replica.change_temperature()
    
    traj = np.array(replica.trajectory)
   

    n_traj_frames =  np.shape(replica.trajectory)[0] 
    fh = open( directory+"replica.dat", 'w' )
    for t in xrange( n_traj_frames ):
        #fh.write( "%6d %6d %+.6e" % ( markov_state( replica.trajectory[t][0], bin_edges ), replica.trajectory[t][1], replica.trajectory[t][2]/kT[replica.trajectory[t][1]] ) )
        
        fh.write( "%6d %6d %+.6e" % ( discretize( traj[t,0], fp.inner_edges ), traj[t,1], traj[t,2] / kT[traj[t,1]] ) )
        fh.write( "\n" )
    fh.close()
    
    np.savetxt(directory+"kT.dat", kT)

    #constructing wham file
    # -> themodynamic state
    # |
    # v markov state
    #we need a target temperature \beta_0
    target = 0
    fh = open( directory+"st_wham.dat", 'w' )
    for c in xrange( fp.bin_centers.shape[0] ):
        for i in xrange( n_therm_states ):
            fh.write( " %+.6e" % ( fp.energy( fp.bin_centers[c] ) * (1.0/kT[i]-1.0/kT[target] ) ) )
        fh.write( "\n" )
    fh.close()
    
    #exact probability distribution for comparison
    fh = open( directory+"exact.dat", 'w' )
    for c in  xrange(fp.bin_centers.shape[0]) :
        p=fp.prob_density( kT[target], fp.bin_centers[c])
        fh.write( "%4f %+.6e" % ( fp.bin_centers[c] , p ) )
        fh.write("\n")
    fh.close()
    
