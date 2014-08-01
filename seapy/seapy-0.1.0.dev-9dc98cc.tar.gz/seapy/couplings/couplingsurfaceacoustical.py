"""
Acoustical surface coupling
---------------------------

"""


import numpy as np
from .coupling import Coupling
from .couplingsurfaceplateacoustical import CouplingSurfacePlateAcoustical
    
class CouplingSurfaceAcoustical(Coupling):
    """
    Coupling for cavity3D to cavity transmission.
    """
    

    @property
    def _coupling_plate(self):
        """Coupling between plate and room.        
        """
        for coupling in self.junction.couplings:
            if isinstance(coupling.subsystem_from, CouplingSurfacePlateAcoustical) and coupling.subsystem_from==self.subsystem_to:
                return coupling
        else:
            raise ValueError("No coupling between plate and room present.")
        
    density = None
    """Density of the wall between the rooms.
    
    .. note:: This attribute might in the future be replaced by a reference to the component representing the wall.
    
    """

    @property
    def impedance_from(self):
        """
        Choses the right impedance of subsystem_from.
        Applies boundary conditions correction as well.
        """
        return self.subsystem_from.impedance

    @property
    def impedance_to(self):
        """
        Choses the right impedance of subsystem_from.
        Applies boundary conditions correction as well.
        """     
        return self.subsystem_to.impedance
    
    
    @property
    def tau(self):
        """
        Non-resonant transmission coefficient by Leppington et al (1987).
        
        .. math:: \\tau = \\left( \\frac{\\rho_0 c_0}{\\pi f \\rho_s \\left(1-f^2/f_c^2 \\right)} \\right)^2  \\left(  \\ln{\\left[ \\frac{2 \\pi f \\sqrt{S}}{c_0} \\right]}  + 0.160 + U(l_x,l_y) + \\frac{1}{4 \\mu^6} \\left[(2\\mu^2-1)(\\mu^2+1)^2\\ln{\\left(\\mu^2-1\\right)} + (2\\mu^2+1)(\\mu^2-1)^2 \\ln{\\left(\\mu^2+1\\right)} - 4\\mu^2 - 8\\mu^6 \\ln{\\mu}  \\right] \\right)
        
        See Craik, equation 4.22, page 101.
        
        .. note:: The shape function :math:`U(l_x,l_y)` is assumed to be zero.
        
        """
        U = 0.0
        
        fc = self._coupling_plate.critical_frequency
        rho_s = self._coupling_plate.subsystem_from.component.material.density
        
        f = self.frequency.center
        mu2 = fc/c # mu^2
        rho_0 = self.subsystem_from.component.material.density
        c_0 = self.subsystem_from.soundspeed_group

        
        A = ( rho_0 * c_0 / (np.pi*f*rho_s*(1.0-mu2**2.0)) )**2.0
        
        B1 = np.log(2.0*np.pi*f*np.sqrt(S)/c_0)
        B2 = 0.160 + U
        B3 = 1.0 / (4.0*mu2**3.0)
        
        C1 = (2.0*mu2-1)*(mu2+1.0)**2.0*np.log(mu2-1)
        C2 = (2.0*mu2+1)*(mu2-1.0)**2.0*np.log(mu2+1)
        C3 = -4.0*mu2 - 8.0*mu**3.0*np.log(np.sqrt(mu))
        
        return A * (B1 + B2 + B3*(C1 + C2 + C3))
    
    
    @property
    def clf(self):
        """
        Coupling loss factor for transmission from a 3D cavity to a 3D cavity.
        
        .. math:: \\eta_{12} = \\frac{c S \\tau_{12}}{8 \\pi f V}
        
        See Craik, equation 4.20, page 100.
        
        """
        return self.subsystem_from.soundspeed_group * self.area / (8.0 * np.pi * self.frequency.center * self.subsystem_from.volume) * self.tau
