#!/usr/bin/env python
"""
=================================
module containing replica classes
=================================
.. codeauthor:: Antonia Mey <antonia.mey@fu-berlin.de>
"""
#================================
#Imports
#================================
import numpy as np
from potentials import FoldingPotential


class STReplica( object ):
    def __init__( self,Z, integrator, kT ):
        r""" Constructor function
        Parameters
        ----------
        
        Z : double array
            containing normalisation factors used for weighting different temperatures
        
        integrator : BrownianIntegrator object
            the actual simulation
        
        kT : double array
            array contianing the possible temperatures at which sampling occurs
        """
        self.Z = Z
        self.integrator = integrator
        self.kT = kT
        self.trajectory = []
    def run( self, nsteps=1 ):
        r""" function that runs the replica exchange simulation
        Parameters
        ----------
        nsteps : int
            number of steps the integrator should compute between exchanges
            Default=1
        """
        for i in xrange( nsteps ):
            self.trajectory.append(self.integrator.step())
    def change_temperature( self ):
        r"""Metropolis hastings steps that allows to change between two randomly chosen temperatures
        """
        r = np.random.randint( self.kT.shape[0] )
        beta_new = 1.0/self.kT[r]
        beta_old = self.integrator.beta
        beta_int = np.where( self.kT == 1.0/beta_old )
        deltaG = -np.log ( self.integrator.potential.Z[r] ) + np.log( self.integrator.potential.Z[beta_int] )
        enExp = -self.trajectory[-1][2]*(beta_new-beta_old)
        exponent = enExp + deltaG
        
        if ( exponent >= 0 ) or ( np.random.random()< np.exp(exponent) ):
            self.integrator.set_temperature(1.0/self.kT[r])
            self.integrator.set_t_index(r)
            #print "New temperature is: "+str(self.integrator.beta)
            
class PTReplica( object ):
    def __init__( self ):
        raise NotImplementedError, "Planned for a future release...."
    
class USReplica( object ):
    r""" class descriptor
    """
    def __init__( self,integrator, RS ):
        self.integrator = integrator
        self.RS = RS
        self.trajectory = []
        self.n_therm_states = len(RS)
        self.ndim=1
        if isinstance(self.integrator.potential, FoldingPotential):
            self.ndim=self.integrator.potential.ndim
        
    def run( self, nsteps ):
        count = 0
        for r in self.RS:
            r_traj = []
            self.integrator.set_position(np.ones(self.ndim)*r.r0/np.sqrt(self.ndim))
            self.integrator.t_index = count
            for i in xrange( nsteps ):
                int_return = self.integrator.step(r)
                bias = self.calculate_bias(self.integrator.x)
                r_traj.append(np.hstack((int_return,bias)))
                if i%nsteps==1000:
                    print 'steps '+ str(i)+'/'+str(nsteps) +'done.'
            count = count+1
            self.trajectory.append(r_traj)
    def calculate_bias( self, pos ):
        bias = np.zeros(self.n_therm_states)
        for b in xrange(self.n_therm_states):
            bias[b]=self.RS[b].energy(pos)
        return bias
        
