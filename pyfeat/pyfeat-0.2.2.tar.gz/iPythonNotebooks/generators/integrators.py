#!/usr/bin/env python
r"""
====================================
Module containing integrator classes
====================================
.. codeauthor:: Antonia Mey <antonia.mey@fu-berlin.de> Christoph Wehmeyer <christoph.wehmeyer@fu-berlin.de>

"""
#================================
#Imports
#================================
import numpy as np


class BrownianIntegrator( object ):
    r"""
    class that does brownian dynamics integration
    """
    def __init__( self, potential, dt, beta=1.0, mass=1.0, damping=1.0 ):
        r""" constructor function
        
        Parameters
        ----------
        potential : FoldingPotential object
            object that contains all the information about the potential in which the particle svolves
            
        dt : double
            timestep of the integrator
            
        beta : double
            inverse temperature of the simulation Default = 1
        
        mass : double
            mass of the particle, Default = 1.0  
        damping : double
            damping constant, Default = 1.0
        
        """
        self.potential = potential
        # store parameters
        self.dt = dt
        self.beta = beta
        self.mass = mass
        self.damping = damping
        # compute coefficients
        self.coeff_A = dt / ( mass * damping )
        self.coeff_B = np.sqrt( 2.0 * dt / ( beta * mass * damping ) )
        self.x = None
        self.t_index = None #thermodynamic index
    def step( self, restraint = None ):
        r"""function that carries out a single integration step
        """
        gradient = self.potential.gradient( self.x )
        if None != restraint:
            gradient += restraint.gradient( self.x )
        self.x = self.x - self.coeff_A * gradient + self.coeff_B * np.random.normal( size=self.n_dim )
        pos = self.x[0]
        if self.n_dim > 1 :
            pos = np.linalg.norm(self.x)
        return np.array( [ pos , self.t_index, self.potential.energy( pos ) ] )
            
       
    def set_temperature( self, beta ):
        r"""function that sets a new inverse temperature
        Parameters
        ----------
        
        beta : double
            inverse temperature beta
        
        """
        self.beta = beta
        self.coeff_B = np.sqrt( 2.0 * self.dt / ( self.beta * self.mass * self.damping ) )
    def set_position( self, x ):
        r"""function that sets the current position of the integrator
        Parameters
        ----------
        x : double
            current position of the particle
        
        """
        self.x = x
        self.n_dim = x.shape[0]
    def set_t_index( self, t ):
        r"""function that sets the temperature index, should there be more than one
        
        Parameters
        ----------
        t : int
            temperature index in the temperature array
        
        """
        self.t_index = t
        
class MCIntegrator( object ):
    r""" Monte carlo integrator
    """
    def __init__( self ):
        raise NotImplementedError, "Planned for a future release...."
    
class MDIntegrator( object ):
    r""" MD integrator
    """
    def __init__( self ):
        raise NotImplementedError, "Planned for a future release...."
