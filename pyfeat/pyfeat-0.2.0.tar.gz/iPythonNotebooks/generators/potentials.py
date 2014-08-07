#!/usr/bin/env python
r"""
===================================
Module containing potential classes
===================================
.. codeauthor:: Antonia Mey <antonia.mey@fu-berlin.de> Christoph Wehmeyer <christoph.wehmeyer@fu-berlin.de>

"""
#================================
#Imports
#================================
import numpy as np
from scipy.integrate import quad
import math

#================================
#different potential classes
#================================
class SymetricDoubleWellPotential( object ):
    r"""class for a sysemtric double well potential
    """
    
    def __init__( self ):
        self.Z = []
        self.inner_edges = np.linspace(-1.8,1.8,20)
        self.n_bins = self.inner_edges.shape[0]+1
        self.bin_centers = np.zeros(self.n_bins)
        self.bin_centers[1:-1] = self.inner_edges[1:]-0.5*(self.inner_edges[1]-self.inner_edges[0])
        self.bin_centers[0] = -2.0
        self.bin_centers[-1] = 2.0
    def energy( self, x ):
        r""" calculates the energy of the potential at x
        Parameters
        ----------
        x : double
            position x 
        Returns
        -------
        energy : double
        """
        return x**4 - 4.5*x**2
    def gradient( self, x ):
        r""" calculates the gradient of the potential at x
        Parameters
        ----------
        x : double
            position x 
        Returns
        -------
        gradient : double
        """
        return 4.0*x**3 - 9.0*x
    def integ( self , x , kT ):
        r""" integrand for calculating Z 
        Parameters
        ----------
        x : double
            position in the potential
        kT : double
            temperature
        Returns
        -------
        exponential of -energy/kt over which shoudl be integrated
        """
        return np.exp( - self.energy( x )/kT )
    def get_partition_function ( self, kT ):
        for T in kT:
            self.Z.append(quad(self.integ, -50.0, 50.0, args=(T,))[0])
        self.Z = np.array(self.Z)
        return self.Z
        
        
class AssymetricDoubleWellPotential ( object ):
    r"""class for an assymetic double well potential
    """
    def __init__( self ):
        self.Z = []
        self.inner_edges = np.linspace(-0.4,4.2,20)
        self.n_bins = self.inner_edges.shape[0]+1
        self.bin_centers = np.zeros(self.n_bins)
        self.bin_centers[1:-1] = self.inner_edges[1:]-0.5*(self.inner_edges[1]-self.inner_edges[0])
        self.bin_centers[0] = -0.7
        self.bin_centers[-1] = 4.5

    def energy( self, x ):
        return 2*(x-2)-6*(x-2)**2 + (x-2)**4
    def gradient( self, x ):
        return 2*x -12*(x-2)+4*(x-2)**3
    def integ( self , x , kT ):
        return np.exp( - self.energy( x )/kT )
    def get_partition_function ( self, kT ):
        for T in kT:
            self.Z.append(quad(self.integ, -100.0, 100.0, args=(T,))[0])
        self.Z = np.array(self.Z)
        return self.Z
    
class HarmonicRestraint( object ):
    r"""class for harmonic restraints used in US
    """
    
    def __init__( self, r0, k ):
        self.r0 = r0
        self.k = k
    def energy( self, r_vector ):
        if (isinstance (r_vector, float)) or (r_vector.shape[0]==1):
            return 0.5 * self.k * ( r_vector - self.r0 )**2
        else:
            return 0.5 * self.k * ( np.linalg.norm( r_vector ) - self.r0 )**2
    def gradient( self, r_vector ):
        if (isinstance (r_vector, float)) or (r_vector.shape[0]==1):
            return self.k*(r_vector-self.r0)
        else:
            r = np.linalg.norm( r_vector )
            if r==0:
                return np.zeros(r_vector.shape[0])
            else:
                return self.k * ( r - self.r0 ) * r_vector / r

class FoldingPotential( object ):
    r"""Class for the folding potential
    """
    def __init__( self, rc, ndim=5 ):
        self.rc = rc
        self.ndim = ndim
        self.Z = []
        self.inner_edges = np.linspace(0.3,6,20)
        self.n_bins = self.inner_edges.shape[0]+1
        self.bin_centers = np.zeros(self.n_bins)
        self.bin_centers[1:-1] = self.inner_edges[1:]-0.5*(self.inner_edges[1]-self.inner_edges[0])
        self.bin_centers[0] = 0.1
        self.bin_centers[-1] = 6.5
    def energy( self, r_norm ):
        r = r_norm - self.rc
        rr = r * r
        if 0.0 > r:
            return -2.5 * rr
        return 0.5 * rr * r - rr
    def gradient( self, r_vector ):
        r_norm = np.linalg.norm( r_vector )
        r = r_norm - self.rc
        f = None
        if 0.0 > r:
            f = -5.0 * r
        else:
            f = ( 1.5 * r - 2.0 ) * r
        return f * r_vector / r_norm
    def get_probability_distribution ( self, kT , distances = None):
        r"""Function returning the proability distribution of the folding model
        Paramerers
        ----------
        kT : double 
            kT for which the probability distribution should be returned
        Retruns
        -------
        p : double array
            array containing the values of the probabiity density 
        distances : double array
            array containing distance bins at which the probabilities were evaluated
        """
        if distances == None :
            distances = np.linspace(0,7,100)
        Z = self.get_partition_function ( kT, distances )
        p = np.zeros( np.shape(distances) )
        i = 0
        for d in distances:
            p[i] = self.prob_density ( kT, d ) 
            i = i+1
        p = p/(Z/len(distances))
        p /= p.sum()
        return (p, distances)
        
    def get_Z ( self, kT, distances ):
        Z = 0.0
        for d in distances:
            Z+=self.prob_density(kT,d)
        return Z
        
    def get_partition_function ( self, kT_array, distances ):
        r""" Function that popoulates Z for all kT's desired
        Parameters
        ----------
        kT_array : double array
            array containing all the kT's for which Z should be calculated
        
        distances : double array
            distance array at which the potential will be evaluated
        """
        if self.Z != None:
            self.Z = []
        for T in kT_array:
            self.Z.append( self.get_Z( T, distances ) )
        self.Z = np.array(self.Z)/distances.shape[0]
    def prob_density( self, kT, distance ):
        r""" function that will return the probability density at a given distance 
        Parameters
        ----------
        kT : double
            kT value of interest
            
        distance : double
            distance of interest
        Returns
        -------
        p : double
            value of the probability density at provided distance 
        
        """
        e = self.energy(distance)
        area = self. get_hyper_sphere_surface_area(self.ndim,distance)
        p = math.exp(-e/kT)*area
        return p
        
    def get_hyper_surface( self, R, n ):
        r""" fuction that evaluates the volume of the n dimensional hypersphere surface with radius R
        Parameters
        ----------
        R : double
            radius
        n : int
            dimension
        Returns
        -------
        V : double
            Volume of the hypersphere surface of radius R and dimension n
        """
        S = hyper_sphere_surface_area(n, 1.0)
        V = S * pow(R, n) / n
        return (V)
    def get_hyper_sphere_surface_area(self, n, R):
        r""" function that evaluates the area of an n dimensional hypersphere at radius R
        Parameters
        ----------
        R : double
            radius
        n: double
            dimension
        Retruns
        -------
        S : double
            Area of the hypersphere surface
        """
        k=0
        if self.is_even(n): 
            k = n / 2
        else:
            k = (n - 1) / 2
        
        S = np.power(2, n - k) * pow(math.pi, k) * pow(R, n - 1) * n / self.double_factorial(n)
        return S
    def is_even(self,a):
        r"""
        Paramerters
        -----------
        a : int
            integer number
            
        Returns
        -------
        bool
            True: if number is even, False otherwise
        """
        if a%2==0:
            return True
        else:
            return False
    def double_factorial(self, n):
        r"""
        Parameters
        ----------
        n : int
            whole number
        """
        if (n > 200):
            raise RuntimeError("Can't compute doubleFactorial(n) for n>200")
        f = 1
        for i in range(n,1,-2):
            f *= i
        return f
