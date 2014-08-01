"""
This module contains a class to describe physical junctions between :mod:`Sea.model.components`.
"""
import math
import cmath
import numpy as np

import warnings # Handling of warnings
import abc      # Abstract base classes
import logging  # Add logging functionality
from weakref import WeakSet, WeakKeyDictionary

import warnings
import itertools

import collections


from ..base import Base, LinkedList

from seapy.couplings import couplings_map

coupling_options = {        
        ('Point', 'Component1DBeam', 'Component1DBeam') : 'Coupling1DStructural',
        ('Line', 'Component1DBeam', 'Component1DBeam') : 'Coupling1DStructural',
        ('Surface', 'Component1DBeam', 'Component1DBeam') : 'Coupling1DStructural',
        ('Point', 'Component2DPlate', 'Component2DPlate') : 'Coupling1DStructural',
        ('Line', 'Component2DPlate', 'Component2DPlate') : 'CouplingLineStructural',
        ('Surface', 'Component2DPlate', 'Component2DPlate') : 'CouplingSurfaceStructural',
        
        ('Surface', 'Component2DPlate', 'Component3DAcoustical') : 'CouplingSurfacePlateAcoustical',
        ('Surface', 'Component3DAcoustical', 'Component2DPlate') : 'CouplingSurfaceAcousticalPlate',
        ('Surface', 'Component3DAcoustical', 'Component3DAcoustical') : 'CouplingSurfaceAcoustical',
    }
"""Map of couplings.

The keys are tuples of the form `(shape, component_sort_a, component_sort_b)`.

"""

junction_shapes = ['Point', 'Line', 'Surface']
"""Possible junction shapes.
"""

junction_mounts = ['corner', 'length']
"""Possible junction mounts.
"""

class Junction(Base):
    """Class for junctions between components."""
    #__metaclass__ = abc.ABCMeta
    
    SORT = 'Connection'
    
    _DEPENDENCIES = []
    
    @property
    def shape(self):
        """Shape of the junction.
        
        .. seealso:: :attr:`seapy.junctions.junction_shapes`
        """
        return self._shape
    
    @shape.setter
    def shape(self, x):
        if x in junction_shapes:
            self._shape = x
        else:
            raise ValueError("Invalid shape.")
        
    #_components = WeakKeyDictionary()
    """
    Dictionary containing how components are connected/mounted.
    
    The keys are the names of the components and the values are names of the mount types.
    
    When a component is removed from :attr:`components` it is removed from this dictionary as well.
    """
    
    
    linked_couplings = LinkedList()
    """
    All couplings.
    """
    
    
    def __init__(self, name, system, shape, **properties):
        """Constructor.
        
        :param name: Identifier
        :type name: string
        :param system: System
        :type system: :class:`SeaPy.system.System`
        """
        self._components = WeakSet()
        
        super().__init__(name, system, **properties)


        
        
        #self._components = WeakKeyDictionary()
        """
        Set of components that are connected through this junction. 
        
        Every list item is (or should be ?!) a tuple (component, mount) where mount is a string 
        describing whether the component is mounted at an edge or far from the edge, 
        and component is a weak reference to the component.
        
        Convert to a custom many-to-many link! 
        """
        
        self.shape = shape  
    
    @property
    def components(self):
        """
        Components that are part of this junction.
        """
        yield from self._components

    @components.setter
    def components(self, items):
        if isinstance(items, collections.abc.Iterable):
            objects = (self.system._getRealObject(obj) for obj in items)
            self._components.clear()
            self._components.update(objects)
        else:
            raise ValueError("Components can only be set with an iterable.")
    
    @property
    def subsystems(self):
        """Subsystems in this junction that are used.
        
        """
        yield from set( subsystem for subsystem in (coupling.subsystem_from, coupling.subsystem_to) for coupling in self.linked_couplings)
    
    @property
    def subsystems_available(self):
        """All available subsystems in this junction.
        
        :returns: iterator
        """
        yield from itertools.chain(*(component.linked_subsystems for component in self.components))
      

    
    def addComponent(self, component):
        """Add component to junction.
        """
        component = self.system._getRealObject(component)
        self._components.add(component)
        return self
        
    def removeComponent(self, component):
        """
        Remove component from junction.
        
        :param component: Component to be removed.
        
        """
        obj = self.system.getObject(component)
        self._components.remove(obj)
        
        #for item in self.components.filter(name=component.name):
            #self._removeMount()
            #self.components.remove(item)
        #for item in self.components:
            #if item.name == component.name:
                #self.components.remove(item)
                
    #def addComponent(self, component, mount):
        #"""
        #Add component to junction. Updates couplings automatically.
        
        #:param component: Component
        #:param mount: how component is mounted
        
        #"""
        #component = self.system.getObject(component)
        #if component not in self.components:
            #self._components.add(component)
            #self.setMount(component, mount)
            #self._updateCouplings()
        #else:
            #warnings.warn('Component is already part of junction. Not adding again.')

    #@property
    #def mounts(self):
        #"""
        #Dictionary describing how components are mounted/connected.
        
        #:rtype: dict
        #"""
        #yield from self._components.items()
        ##return self._mount.copy()#[(c, m) for c, m in self._mount.items()]
        
    #def get_mount(self, component):
        #"""
        #Retrieve how the component is mounted/connected.
        #"""
        #try:
            #return self._mount[component.name]
        #except KeyError:
            #warnings.warn('Component does not exist.')
            
    #def setMount(self, component, mount):
        #"""
        #Set how a component is mounted/connected.
        
        #:param component: Component. Type or name.
        #:param mount: Type of mounting.
        #:type mount: :func:`str()`
        
        #:returns: None
        #"""
        #component = self.system.getObject(component)
        #if component in self.components:
            #if mount in junction.mounts:
                #self._mount[component] = mount
            #else:
                #warnings.warn('Mount type does not exist.')
        #else:
            #warnings.warn('Component does not exist.')        
      
    
    #def _removeMount(self, component):
        #"""Remove mount."""
        #del self._mount[component]
    
 
    def disable(self, couplings=False):
        """
        Disable this junction. Optionally disable junctions' couplings.
        
        :param couplings: Disable couplings
        :type couplings: bool
        """
        self._enabled = False
        
        if couplings:
            for coupling in self.couplings:
                coupling.disable()
        
    def enable(self, couplings=False):
        """
        Enable this junction. Optionally enable junctions' couplings.
        
        :param couplings: Enable couplings
        :type couplings: bool
        """
        self._enabled = True
        
        if couplings:
            for coupling in self.couplings:
                coupling.enable()

    
    def addCouplingManual(self, name, model, subsystem_from, subsystem_to, **properties):
        """
        Add a coupling to the junction, specifying manually which `model` to use for the coupling.
        
        :param name: Name of coupling.
        :param model: Model or type of coupling. See :attr:`seapy.couplings.couplings_map`.
        :param properties: Other properties. Note that `subsystem_from` and `subsystem_to` are required.
        
        """
        properties['subsystem_from'] = subsystem_from
        properties['subsystem_to'] = subsystem_to
        
        obj = self.system.addCoupling(name, model, **properties)
        
        #obj = self.system._addObject(name, objects_map['couplings'][model] , **properties)
        return obj
        
    def addCoupling(self, subsystem_from, subsystem_to, name=None, **properties):
        """
        Add coupling to junction.
        
        :param subsystem_from: Subsystem from
        :param subsystem_to: Subsystem to
        """
        model = coupling_options[(self.shape, subsystem_from.component.__class__.__name__, subsystem_to.component.__class__.__name__)]
        
        if not name:
            name = subsystem_from.name + '_' + subsystem_to.name
        
        obj = self.addCouplingManual(name, model, subsystem_from, subsystem_to)
        return obj
        #coupling = couplings_map[model](name, self.system.getObject(self.name), sub_from, sub_to)

        #self.system._objects.append(coupling)
        
        #print( self.system.couplings())
        
        #coupling = self.system.getObject(coupling.name)
        
    def removeCoupling(self, coupling):
        """
        Remove coupling from junction.
        """
        self.system.removeObject(coupling)
    
    
    def _removeCouplings(self):
        """
        Remove all couplings from junction.
        """
        for coupling in self.linked_couplings:
            self._removeCoupling(coupling)
        
    
    def _updateCouplings(self):
        """
        Add all possible couplings to the junction.
        """
        self._removeCouplings()     # This is not so elegant. Instead try to apply only the changes, since this might delete user-added values 
        
        for i in self.subsystems_available:
            print(i)
        for sub_a, sub_b in itertools.combinations(self.subsystems_available, 2):
            print(sub_a, sub_b)
            self.addCoupling(sub_a, sub_b)
            self.addCoupling(sub_b, sub_a)
    
    def updateCouplings(self):
        """
        Update couplings. 
        
        .. attention:: List of couplings should already be kept up to date. Is it neccessary to expose this function?
        """
        self._updateCouplings()
    
    
    @property
    def impedance(self):
        """Total impedance at the coupling.
        
        :rtype: :class:`numpy.ndarray`
        """
        imp = np.zeros(len(self.omega))
        for subsystem in self.subsystems.items():
            print(subsystem.impedance)
            imp = imp + subsystem.impedance
        return impedance
    
    #def get_coupling(self, subsystem_from, subsystem_to):
        #"""Return the coupling between subsystems for calculations.
        #"""
        #return
    
    
    #@property
    #def routes(self):
        #"""
        #Create a list.
        #"""
        #return [(couplings.subsystem_from, coupling.subsystem_to) for coupling in couplings]
    
