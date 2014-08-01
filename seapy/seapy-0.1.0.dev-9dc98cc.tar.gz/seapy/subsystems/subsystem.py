"""
Subsystem
---------

.. autoclass:: seapy.subsystems.subsystem.Subsystem

"""


from ..base import Base, ComponentLink, LinkedList
import abc
import math
import cmath
import numpy as np

from weakref import WeakSet
import logging

from seapy.excitations import excitations_map   # Circular dependency!

class Subsystem(Base):
    """Abstract Base Class for subsystems."""

    SORT = 'Subsystem'

    _DEPENDENCIES = ['component']

    component = ComponentLink()
    """
    Component this subsystem uses.
    """
    
    linked_couplings_from = LinkedList()
    """ 
    Set of couplings in which the subsystem is in the From field.
    """
    
    linked_couplings_to = LinkedList()
    """
    Set of couplings in which the subsystem is in the To field.
    """
    
    linked_excitations = LinkedList()
    """
    Set of excitations this subsystem experiences.
    """


    #def __init__(self, name, component, **properties):
    def __init__(self, name, system, **properties):
        """Constructor.
        
        :param name: Identifier
        :type name: string
        :param component: Component
        :type component: :class:`SeaPy.components.Component`
        
        """
        super().__init__(name, system, **properties)
        #super().__init__(name, component.system, **properties)
        
        #self.component = component
        #"""
        #Component this subsystem uses.
        #"""
        
        
    def __del__(self):
        """Destructor. Destroy linked couplings. Remove references from components"""
        for coupling in self.linked_couplings_from:
            logging.info("Destructor %s: Deleting linked coupling %s", self.name, coupling)
            self.system.removeObject(coupling)
        for coupling in self.linked_couplings_to:
            logging.info("Destructor %s: Deleting linked coupling %s", self.name, coupling)
            self.system.removeObject(coupling)
        for excitation in self.linked_excitations:
            logging.info("Destructor %s: Deleting linked excitation %s", self.name, excitation)
            self.system.removeObject(excitation)
        try:
            self.component.__dict__['linked_subsystems'].remove(self.name)
        except ReferenceError:
            pass
        #self.system.subsystems.remove(self.name)
        super().__del__() # Inherit destructor from base class


    
    def disable(self, couplings=False):
        """
        Disable this subsystem. Optionally disable dependent couplings as well.
        
        :param couplings: Disable couplings
        :type couplings: bool
        """
        self._enabled = False
        
        if couplings:
            for coupling in self.linked_couplings:
                coupling.disable()
    
    def enable(self, couplings=False):
        """
        Enable this subsystem. Optionally enable dependent couplings as well.
        
        :param couplings: Enable couplings
        :type couplings: bool
        """
        self._enabled = True
        
        if couplings:
            for coupling in self.linked_couplings:
                coupling.enable()
    
    def addExcitation(self, name, model, **properties):
        """Add excitation to subsystem.

        """
        obj = excitations_map[model](name, self.system.getObject(self.name), **properties)
        self.system._objects.append(obj)
        obj = self.system.getObject(obj.name)
        #self.linked_excitations.add(obj)
        return obj
    
    modal_energy = None        
    """
    Modal energies of each frequency band.
    """
    
    #def _set_modal_overlap_factor(self, x):
        #self._modal_overlap_factor = x
    
    #def _get_modal_overlap_factor(self):
        #if not self._modal_overlap_factor:
            #return self.component.material.loss_factor
        #else:
            #self._modal_overlap_factor
    
    #_modal_overlap_factor = None
    #modal_overlap_factor = property(fget=_get_modal_overlap_factor, fset=_set_modal_overlap_factor)
    #"""
    #Modal overlap factor. Initial value is based on damping loss factor of subsystem.
    #After solving the system a first time, this value is updated to its results.
    #This value is iteratively updated.
    #"""
    
    
    @property
    @abc.abstractmethod
    def soundspeed_phase(self):
        """
        Phase velocity in a subsystem.
        """
        return
  
    @property
    @abc.abstractmethod                    
    def soundspeed_group(self):
        """
        Group velocity in a subsystem.
        """
        return
        
    @property
    @abc.abstractmethod
    def average_frequency_spacing(self):
        """"
        Average frequency spacing.
        """
        return
    
    @property            
    def modal_density(self):
        """
        Modal density.
       
        .. math:: n(\\omega) = \\frac{1}{2 \\pi \\overline{\\delta f}}
        
        See Lyon, eq. 8.1.6
        """
        try:
            return 1.0 / (2.0 * np.pi * self.average_frequency_spacing)
        except FloatingPointError:
            return np.zeros(self.frequency.amount)
    
    @property
    #@abc.abstractmethod
    def wavenumber(self):
        """
        Wave number.
        """
        raise NotImplementedError
    
    @property
    def impedance(self):
        """
        Impedance :math:`Z`
        """
        raise NotImplementedError
        
    
    @property
    def resistance(self):
        """
        Resistance :math:`R`, the real part of the impedance :math:`Z`.
        
        .. math:: R = \\Re{Z}
        """
        return np.real(self.impedance)
    
    @property
    def conductance(self):
        """
        Conductance :math:`G`.
        
        .. math:: G = \\frac{1}{R}
        """
        return 1.0 / self.resistance
    
    @property
    def mobility(self):
        """
        Mobility `Y`
        
        .. math:: Y = \\frac{1}{Z}
        """
        try:
            return 1.0 / self.impedance
        except FloatingPointError:
            return np.zeros(self.frequency.amount)
            
    @property
    def damping_term(self):
        """
        The damping term is the ratio of the modal half-power bandwidth to the average modal frequency spacing.
        
        .. math:: \\beta_{ii} = \\frac{f \\eta_{loss} }{\\overline{\\delta f}}
        
        See Lyon, above equation 12.1.4
        """
        try:
            return self.frequency.center * self.component.material.loss_factor / self.average_frequency_spacing
        except FloatingPointError:
            return np.zeros(self.frequency.amount)
        
    @property
    def modal_overlap_factor(self):
        """
        Modal overlap factor.
        
        .. math:: M = \\frac{ \\pi \\beta_{ii} }{2}
        
        See Lyon, above equation 12.1.4
        """
        return np.pi * self.damping_term / 2.0
    
    
    @property
    def power_input(self):
        """
        Total input power due to excitations.
        """
        power = np.zeros(self.frequency.amount)
        #print self.linked_excitations
        for excitation in self.linked_excitations:
            power = power + excitation.power
        return power    

    @property
    def energy(self):
        """
        Total energy :math:`E` in subsystem.
        
        .. math:: E = M(\\omega) n(\\omega)
        """
        return self.modal_energy * self.modal_density

    @property
    def dlf(self):
        """Damping loss factor of subsystem.
        
        By default this is the loss factor of the material of the component.
        
        """
        if self._dlf:
            return self._dlf
        else:
            return self.component.material.loss_factor
     
    @property
    def dlf(self, x):
        self._dlf = x
    
    @property
    def tlf(self):
        """Total loss factor.
        
        .. math:: \\eta_i = \\eta_{id} + \\sum_{j=1, j \\neq i}^{n} \\eta_{ij}
        
        See Craik, equation 3.18, page 60.
        
        """
        return sum(coupling.clf for coupling in self.couplings_from) + self.dlf
        
        
