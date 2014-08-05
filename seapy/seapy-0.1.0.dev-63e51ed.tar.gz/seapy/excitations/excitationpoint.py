"""
Point excitation
================

"""

import numpy as np
from .excitation import Excitation
#from ..subsystems import SubsystemCavity, SubsystemStructural

class ExcitationPoint(Excitation):
    """
    Point excitation
    """

    radius = None
    """
    Radius :math`r` of the source.
    """
    
    @property
    def resistance(self):
        return np.real(self.impedance)
    
    @property
    def conductance(self):
        return 1.0 / self.resistance
 
 
class ExcitationPointForce(ExcitationPoint):
    """
    Point excitation by a force.
    """

    _force = None
    _velocity = None

    @property
    def force(self):
        """Sound force :math:`p`.
        """
        if self._force:
            return self._force
        elif self._velocity:
            return self.resistance * self.velocity 
        else:
            raise ValueError("Neither force nor velocity is specified.")
        
    @force.setter
    def force(self, x):
        self._force = x
        self._velocity = None
    
    @property
    def velocity(self):
        """Structural velocity :math:`u`.
        """
        if self._velocity:
            return self._velocity
        elif self._force:
            return self.force / self.resistance
        else:
            raise ValueError("Neither force nor velocity is specified.")
            
    @velocity.setter
    def velocity(self, x):
        self._velocity = x
        self._force = None
        
    @property
    def power(self):
        return self.force * self.conductance
    
    @property
    def impedance(self):
        return self.subsystem.impedance_point_force
    
    
    
class ExcitationPointMoment(ExcitationPoint):
    """
    Point excitation of a moment.
    """
    
    _moment = None
    _velocity = None

    @property
    def moment(self):
        """Sound moment :math:`p`.
        """
        if self._moment:
            return self._moment
        elif self._velocity:
            return self.resistance * self.velocity 
        else:
            raise ValueError("Neither moment nor angular velocity is specified.")
        
    @moment.setter
    def moment(self, x):
        self._moment = x
        self._velocity = None
    
    @property
    def velocity(self):
        """Angular velocity :math:`\\omega`.
        """
        if self._velocity:
            return self._velocity
        elif self._velocity:
            return self.moment / self.resistance
        else:
            raise ValueError("Neither moment nor angular velocity is specified.")
        
    @velocity.setter
    def velocity(self, x):
        self._velocity = x
        self._moment = None
        
    @property
    def power(self):
        return self.moment * self.conductance
    
    @property
    def impedance(self):
        return self.subsystem.impedance_point_moment
    
  
class ExcitationPointVolume(ExcitationPoint):
    """
    Point excitation by a volume flow.
    """
    
    _pressure = None
    _velocity = None

    @property
    def pressure(self):
        """Sound pressure :math:`p`.
        """
        if self._pressure:
            return self._pressure
        elif self._velocity:
            return self.resistance * self.velocity 
        else:
            raise ValueError("Neither pressure nor angular velocity is specified.")
        
    @pressure.setter
    def pressure(self, x):
        self._pressure = x
        self._velocity = None
    
    @property
    def velocity(self):
        """Volume velocity :math:`U`.
        """
        if self._velocity:
            return self._velocity
        elif self._pressure:
            return self.pressure / self.resistance
        else:
            raise ValueError("Neither pressure nor angular velocity is specified.")
            
    @velocity.setter
    def velocity(self, x):
        self._velocity = x
        self._pressure = None
        
    @property
    def power(self):
        return self.pressure * self.conductance
    
    @property
    def impedance(self):
        try:
            return self.subsystem.impedance_point_volume(self)
        except TypeError:
            return self.subsystem.impedance_point_volume
            
    
