"""
Pipe
----

.. autoclass:: seapy.components.component1dpipe.Component1DPipe

Subsystems
++++++++++

.. autoclass:: seapy.components.component1dpipe.SubsystemLong
.. autoclass:: seapy.components.component1dpipe.SubsystemBend
.. autoclass:: seapy.components.component1dpipe.SubsystemShear


Classes describing a one-dimensional beam.
"""
import numpy as np
from .componentstructural import ComponentStructural
from ..subsystems import SubsystemStructural


class SubsystemLong(SubsystemStructural):
    pass


class SubsystemBend(SubsystemStructural):
    pass

class SubsystemShear(SubsystemStructural):
    pass



class ComponentPipe(ComponentStructural):
    """
    One-dimensional beam component.
    """

    SUBSYSTEMS = {'Long': SubsystemLong, 
                   'Bend': SubsystemBend, 
                   'Shear': SubsystemShear}
    
    @property
    def radius_of_gyration(self):
        """
        Radius of gyration :math:`\\kappa` is given by dividing the thickness of the beam by :math:`\\sqrt{2}`.
        See Lyon, above eq. 8.1.10
        
        .. math:: \\kappa = \\frac{h}{\\sqrt{2}}
        
        """
        return self.height / 12
