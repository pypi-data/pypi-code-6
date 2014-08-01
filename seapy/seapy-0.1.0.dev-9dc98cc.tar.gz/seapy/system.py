"""
System
======

The System class is the main class and contains methods for solving the SEA model.

.. autoclass:: seapy.system.System

.. autoclass:: seapy.system.Frequency
.. autoclass:: seapy.system.Band

"""

import math
import cmath
import numpy as np

import warnings
import logging
from weakref import WeakSet
import weakref

from .base import Spectrum
from seapy.objects_map import objects_map

class System(object):
    """
    The System class contains methods for solving the model.
    """
    
    SORT = 'System'
    
    reference_pressure = 2.0e-5
    """Reference pressure :math:`p_{0}`.
    """
    
    reference_velocity = 5.0e-8
    """Reference velocity :math:`v_{0}`.
    """
    
    reference_power = 1.0e-12
    """Reference power :math:`P_{0}`.
    """
    
    solved = False
    """
    Switch indicating whether the system (modal energies) were solved or not.
    """
    
    @property
    def objects(self):
        """All objects in the system.
        
        :returns: Generator of objects.
        :rtype: :class:`types.GeneratorType`
        """
        yield from (self.getObject(obj.name) for obj in self._objects)
        
    @property
    def components(self):
        """All components in the system.
        
        :returns: Generator of components.
        :rtype: :class:`python.types.GeneratorType`
        """
        yield from (obj for obj in self.objects if obj.SORT=='Component')

    @property
    def subsystems(self):
        """All subsystems in the system.
        
        :returns: Generator of subsystems.
        :rtype: :class:`python.types.GeneratorType`
        """
        yield from (obj for obj in self.objects if obj.SORT=='Subsystem')
    
    @property
    def junctions(self):
        """All junctions in the system.
        
        :returns: Generator of junctions.
        :rtype: :class:`python.types.GeneratorType`
        """
        yield from (obj for obj in self.objects if obj.SORT=='Junction')
    
    @property
    def couplings(self):
        """All couplings in the system.
        
        :returns: Generator of couplings.
        :rtype: :class:`python.types.GeneratorType`
        """
        yield from (obj for obj in self.objects if obj.SORT=='Coupling')
    
    @property
    def materials(self):
        """All materials in the system.
        
        :returns: Generator of materials.
        :rtype: :class:`python.types.GeneratorType`
        """
        yield from (obj for obj in self.objects if obj.SORT=='Material')
    
    @property
    def excitations(self):
        """All excitations in the system.
        
        :returns: Generator of excitations.
        :rtype: :class:`python.types.GeneratorType`
        """
        yield from (obj for obj in self.objects if obj.SORT=='Excitation')

    
    def __init__(self):
        """Constructor.
        """
        self.frequency = Frequency(weakref.proxy(self))
        """
        Frequency object
        """
                        
        self._objects = list()
        """Private set of objects this SEA model consists of.
        """
    
    def __del__(self):
        
        for obj in self.objects:
            self.removeObject(obj.name)

    def _getRealObject(self, name):
        """
        Get real object by name.
        
        :param name: Name of `object`.
        
        :returns: Real `object`.
        """
        name = name if isinstance(name, str) else name.name
        for obj in self._objects:
            if name == obj.name:
                return obj
        else:
            raise ValueError("Unknown name. Cannot get object.")
        
    def getObject(self, name):
        """
        Get object by name.
        
        :param name: Name of `object`.
        
        :returns: Proxy to `object`.
        
        """
        name = name if isinstance(name, str) else name.name
        for obj in self._objects:
            if name == obj.name:
                return weakref.proxy(obj) 
        else:
            raise ValueError("Unknown name. Cannot get object.")
        
    
    def removeObject(self, name):
        """
        Delete object from SEA model.
        
        :param name: Name of `object`.
        
        :returns: Proxy to `object`.
        
        """
        for obj in self._objects:
            if name == obj.name:
                self._objects.remove(obj)
    
    def _addObject(self, name, model, **properties):
        """Add object to SEA model.
        
        :param name: Name of `object`.
        :param model: Model or type of `object`.
        :param properties: Other properties specific to `object`.
        
        """
        #if name not in self._objects:
        obj = model(name, weakref.proxy(self), **properties)   # Add hidden hard reference
        self._objects.append(obj)
        return self.getObject(obj.name)  
        
    def addComponent(self, name, model, **properties):
        """Add component to SEA model.
        
        :param name: Name of component.
        :param model: Model or type of component. See :attr:`seapy.components.components_map`.
        :param properties: Other properties specific to the component.
        
        """
        obj = self._addObject(name, objects_map['component'][model] , **properties)
        obj._addSubsystems()
        return obj
       
    def addJunction(self, name, model, **properties):
        """Add junction to SEA model."""
        obj = self._addObject(name, objects_map['junction'][model], **properties)
        obj._updateCouplings()
        return obj
    
    def addMaterial(self, name, model, **properties):
        """Add material to SEA model."""
        obj = self._addObject(name, objects_map['material'][model], **properties)
        return obj
    
    def addCoupling(self, name, model, **properties):
        """Add material to SEA model."""
        obj = self._addObject(name, objects_map['coupling'][model], **properties)
        return obj
    
    
    
    def createMatrix(self, subsystems, f):
        """Create loss factor matrix for given frequency band.
        
        :param subsystems: is a list of subsystems. Reason to give the list as argument instead of using self.subsystems is that that list might change during execution.
        :type subsystems: list
        :param f: is the index of the center frequency of the frequency band
        :type f: int
        :rtype: :class:`numpy.ndarray`
        
        """
        logging.info("Creating matrix for centerfrequency {}".format(self.frequency.center[f]))
        
        LF = np.zeros((len(subsystems), len(subsystems)), dtype=float)
        j = 0
        for subsystem_j in subsystems: # Row j 
            i = 0
            for subsystem_i in subsystems:       # Column i
                loss_factor = 0.0
                if i==j:
                    #print 'i = j'
                    ## Total loss factor: sum of damping loss factor + loss factors for power transported from i elsewhere
                    loss_factor = subsystem_i.component.material.loss_factor[f] # Damping loss factor
                    for coupling in subsystem_i.linked_couplings_from: # + all CLFs 'from' i elsewhere
                        if coupling.available:
                            loss_factor = loss_factor + coupling.clf[f] 
                
                else:
                    ####Take the coupling loss factor from subsystem i to subsystem j. Negative
                    x = list(set(subsystem_i.linked_couplings_from).intersection(set(subsystem_j.linked_couplings_to)))

                    ##if not x:
                    ## Use the relation consistency relationship?
                    ##pass
                    ##print 'error. No coupling?'
                    if len(x)==1:
                        coupling = x[0]
                        #loss_factor = - coupling.clf[f]
                    del x        
                LF[j,i] = loss_factor * subsystem_i.modal_density[f]
                i+=1
            j+=1
        logging.info('Matrix created.')
        
        logging.info(LF)
        return LF

    def clearResults(self):
        """Clear the results. Reset modal energies. Set :attr:`solved` to False.
        
        :rtype: None
        """
        logging.info('Clearing results...')
        
        for subsystem in self.subsystems:
            del subsystem.modal_energy
    
        self.solved = False
    
        logging.info('Cleared results.')
     
    def solveSystem(self):  # Put the actual solving in a separate thread?
        """Solve modal powers.
        
        :rtype: :func:`bool`
        
        This method solves the modal energies for every subsystem.
        The method :meth:`createMatrix` is called for every frequency band to construct a matrix of :term:`loss factors` and :term:`modal densities`.
        
        """
        logging.info('Solving system...')
        

        subsystems = self.subsystems(available=True)
        print(self.frequency)
        for f in range(0, self.frequency.amount, 1): # For every frequency band
            if self.frequency.enabled[f]:               # If it is enabled
                LF = self.createMatrix(subsystems, f)   # Create a loss factor matrix.
                
                input_power = np.zeros(len(subsystems))     # Create input power vector
                #print input_power    
                i=0
                for subsystem in subsystems:
                    input_power[i] = subsystem.input_power[f] / self.frequency.angular[f]   # Retrieve the power for the right frequency
                    i=i+1
                
                try:
                    modal_energy = np.linalg.solve(LF, input_power)    # Left division results in the modal energies.
                except np.linalg.linalg.LinAlgError as e:   # If there is an error solving the matrix, then quit right away.
                    warnings.warn( repr(e) )
                    return False
                # Save each modal energy to its respective Subsystem nameect
                
                
                
                i = 0
                for subsystem in subsystems:
                    subsystem.modal_energy[f] = modal_energy[i]
                    i=i+1
                    
                del modal_energy, input_power, LF
                
        self.solved = True  
        logging.info('System solved.')
        return True
    
    


class Band(object):
    """Frequency band class."""
    
    def __init__(self, lower=0.0, center=0.0,  upper=0.0, enabled=False):
        
        self.lower = lower
        self.center = center
        self.upper = upper
        self.enabled = enabled
    
    @property
    def bandwidth(self):
        return self.upper - self.lower
    
    @property
    def angular(self):
        return 2.0 * np.pi * self.center
   
   
class Frequency(object):
    """New-style spectrum class."""
    
    def __init__(self, system):
        self.system = system
        self._bands = list()
    
    
    def _spectrum(name):
        """Property to access the frequency bands as/using arrays."""

        @property
        def prop(self):
            return np.array([getattr(band, name) for band in self._bands])
        
        @prop.setter
        def prop(self, x):
            if len(x) == len(self._bands):
                """
                When the given array has the same amount of items as there are 
                frequency bands, we will fit them one on one.
                """
                for new, band in zip(x, self._bands):
                    setattr(band, name, new)
            else:
                """
                If not, we will delete the old frequency bands, and create new ones."""
                self._bands = list()
                for i in x:
                    band = Band()
                    setattr(band, name, i)
                    self._bands.append(band) # Use self.addBand() instead!!
        return prop
    
    lower = _spectrum('lower')
    center = _spectrum('center')
    upper = _spectrum('upper')
    enabled = _spectrum('enabled')
    
    @property
    def bandwidth(self):
        return np.array([band.bandwidth for band in self._bands])
        
    @property
    def angular(self):
        return np.array([band.angular for band in self._bands])
    
    @property
    def amount(self):
        return len(self._bands)
    
    @property
    def spectra(self):
        """Generator to obtain all spectra in use in the SEA model."""
        for obj in self.system.objects:
            for cls in obj.__class__.__mro__:
                for key, value in cls.__dict__.items():
                    if isinstance(value, Spectrum):
                        yield (obj, key)
    
    def appendBand(self, **kwargs):
        """
        Append frequency band.
        """
        self.addBand(len(self._bands), **kwargs)
    
    def addBand(self, pos, **kwargs):
        """
        Add frequency band.
        
        
        Inform all spectra of the change!!
        """
        
        self._bands.insert(pos, Band(**kwargs))  # Create a new frequency band
        
        default = 0.0 # default value of array cells
        
        for obj, attr in self.iterspectra():    # Add a band to all spectra
            setattr(obj, attr, np.insert(getattr(obj, attr), pos, default))
            
    
    def removeBand(self, pos):
        """
        Remove frequency band.
        
        Inform all spectra of the change!!
        """
        self._bands.pop(pos) # Remove the frequency band
        
        for obj, attr in self.iterspectra():     # Remove a band from all spectra
            setattr(obj, attr, np.delete(getattr(obj, attr), pos))
            
            
        
    #@property
    #def upper(self):
        #return np.array([band.upper for band in self._bands])
    
    #@property
    #def lower(self):
        #return np.array([band.lower for band in self._bands])
    
    #@property
    #def center(self):
        #return np.array([band.center for band in self._bands])
    
    #@center.setter
    #def center(self, x):
        #if len(x) == len(self.bands):
            #for new, band in zip(x, self.bands):
                #band.center = new
        ##else:
            #"""Add the required amount of bands."""

    #@property
    #def enabled(self):
        #return np.array([band.enabled for band in self._bands])
    

    
#class Frequency(object):
    #"""
    #Abstract base class for handling different frequency settings.
    #"""
    
    #def __init__(self, system):
        #self._system = system
    
    #def _set_band(self, x, sort):
        #for i in ['_lower', '_center', '_upper']:
            #if len(getattr(self, i)) != len(x):
                #setattr(self, i, np.zeros(len(x)))
        #if len(getattr(self, '_enabled')) != len(x):        
                #setattr(self, '_enabled', np.zeros(len(x), dtype=bool))
        #setattr(self, sort, np.array(x))
    

    
    #def _get_center(self):
        #return self._center
    
    #def _set_center(self, x):
        #self._set_band(x, '_center')
    
    #_center = np.array([0.0])
    #center = property(fget=_get_center, fset=_set_center)
    #"""
    #Center frequencies of frequency bands.
    #"""
    
    
    #def _get_upper(self):
        #return self._upper
    
    #def _set_upper(self, x):
        #self._set_band(x, '_upper')
    
    #_upper = np.array([0.0])
    #upper = property(fget=_get_upper, fset=_set_upper)
    #"""
    #Upper limit frequencies of frequency bands.
    #"""
    
    #def _set_lower(self, x):
        #self._set_band(x, '_lower')
    
    #def _get_lower(self):
        #return self._lower
    
    #_lower = np.array([0.0])
    #lower = property(fget=_get_lower, fset=_set_lower)
    #"""
    #Lower limit frequencies of frequency bands.
    #"""
    
    #def _set_enabled(self, x):
        #self._set_band(x, '_enabled')
    
    #def _get_enabled(self):
        #return self._enabled
    
    #_enabled = np.array([False]) 
    #enabled = property(fget=_get_upper, fset=_set_upper)
    #"""
    #Enabled frequency bands.
    
    #Modal powers will not be solved for disabled frequency bands.
    #"""
    
    #@property
    #def bandwidth(self):
        #"""Bandwidth of frequency bands,
        
        #:rtype: :class:`numpy.ndarray`
        #"""
        #return self.upper - self.lower

    #@property
    #def angular(self):
        #"""Angular frequency
        
        #:rtype: :class:`numpy.ndarray`
        #"""
        #return self.center * 2.0 * np.pi 
    
    
    
    #@property
    #def amount(self):
        #"""Amount of frequency bands
        
        #:rtype: :func:`int`
        #"""
        #try:
            #return len(self.center)
        #except TypeError:
            #return 0
