"""
Coupling
--------

.. autoclass:: Coupling

"""


import abc
import math
import cmath
import numpy as np

from ..base import Base, JunctionLink, SubsystemFromLink, SubsystemToLink

class Coupling(Base):
    """
    Abstract base class for couplings.
    """
    
    SORT = 'Coupling'

    _DEPENDENCIES = ['subsystem_from', 'subsystem_to']

    junction = JunctionLink()
    """
    Junction this coupling is part of.
    """
    
    subsystem_from = SubsystemFromLink()
    """
    Type of subsystem origin for coupling
    """
    
    subsystem_to = SubsystemToLink()
    """
    Type of subsystem destination for coupling
    """
    
    size = None
    """
    Size of the coupling.
    """
    
    #def __init__(self, name, junction, subsystem_from, subsystem_to, **properties):
    def __init__(self, name, system, subsystem_to, **properties):
        """
        Constructor.
        
        :param name: Identifier
        :type name: string
        :param junction: junction
        :type junction: :class:`seapy.junctions.junction`
        :param subsystem_from: subsystem from
        :type subsystem_from: :class:`seapy.subsystems.Subsystem`
        :param subsystem_to: subsystem_to
        :type subsystem_to: :class:`seapy.subsystems.Subsystem`
        
        """
        super().__init__(name, system, **properties)
        #self.junction = junction
        #self.subsystem_from = subsystem_from
        #self.subsystem_to = subsystem_to
    

    def disable(self, subsystems=False):
        """
        Disable this coupling. Optionally disable dependent subsystems as well.
        
        :param subsystems: Disable subsystems
        :type subsystems: bool
        """
        self._enabled = False
        
        if subsystems:
            self.subsystem_from.disable()
            self.subsystem_to.disable()
    
    def enable(self, subsystems=False):
        """
        Enable this coupling. Optionally enable dependent subsystems as well.
        
        :param subsystems: Enable subsystems
        :type subsystems: bool
        """
        self._enabled = True
        
        if subsystems:
            self.subsystem_from.enable()
            self.subsystem_to.enable()


    @property
    @abc.abstractmethod
    def impedance_from(self):
        """Impedance of :attr:`subsystem_from` corrected for the type of coupling.
        
        :rtype: :class:`numpy.ndarray`
        """
        return
    
    @property
    @abc.abstractmethod
    def impedance_to(self):
        """Impedance of :attr:`subsystem_to` corrected for the type of coupling.
        
        :rtype: :class:`numpy.ndarray`
        """
        return
    
    
    @property
    def reciproce(self):
        """Reciproce or inverse coupling.
        
        :returns: Reciproce coupling if it exists, else None.
        
        """
        for coupling in self.junction.linked_couplings:
            if coupling.subsystem_from == self.subsystem_to and coupling.subsystem_to == self.subsystem_from:
                return coupling
            
    @property
    def clf(self):
        """Coupling loss factor `\\eta`.
        
        :rtype: :class:`numpy.ndarray`
        
        In case the CLF is not specified for the given coupling it is calculated using the SEA consistency relation.
        
        \\eta_{12} = \\eta_{21} \\frac{n_2}{n_1}
        
        """
        try:
            clf = self.reciproce.__class__.clf
        except AttributeError:
            raise ValueError("Cannot calculate CLF. Reciproce CLF has not been specified.")
        else:
            return clf * self.subsystem_to.modal_density / self.subsystem_from.modal_density
            
    @property
    def mobility_from(self):
        """Mobility of :attr:`subsystem_from` corrected for the type of coupling.
        
        :returns: Mobility :math:`Y`
        :rtype: :class:`numpy.ndarray`
        """
        return 1.0 / self.impedance_from
        
    @property
    def mobility_to(self):
        """Mobility of :attr:`subsystem_to` corrected for the type of coupling.
        
        :returns: Mobility :math:`Y`
        :rtype: :class:`numpy.ndarray`
        """
        return 1.0 / self.impedance_to
    
    @property
    def resistance_from(self):
        """Resistance of :attr:`subsystem_from` corrected for the type of coupling.
        
        :returns: Impedance :math:`Z`
        :rtype: :class:`numpy.ndarray`
        """
        return np.real(self.impedance_from)
    
    @property
    def resistance_to(self):
        """Resistance of :attr:`subsystem_to` corrected for the type of coupling.
        
        :returns: Impedance :math:`Z`
        :rtype: :class:`numpy.ndarray`
        """
        return np.real(self.impedance_to)
    
    
    @property
    def modal_coupling_factor(self):
        """Modal coupling factor of the coupling.
        
        :rtype: :class:`numpy.ndarray`
        
        .. math:: \\beta_{ij} = \\frac{ f * \\eta_{ij} } { \\overline{\\delta f_i} }
        
        See Lyon, above equation 12.1.4
        """
        return self.frequency.center * self.clf / self.subsystem_from.average_frequency_spacing
        
