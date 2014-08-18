
"""
A set of routines to find the eigenvalues and eigenfunctions
of the Schrodinger equation.

Taken from scikit-quantum.
"""

import numpy as np
from scipy.integrate import ode
from scipy.special import sph_jnyn


class IntegratorBase(object):
    """
    Base class to integrate the Schrodinger equation.

    Override get_gphi to define an integrator in a different
    geometry.
    """
    def __init__(self,V,mass=1.,integrator="vode",*integrator_args,**integrator_kwargs):
        self.V = V
        self.mass = mass
        self.integrator = ode(self._get_dphi)
        self.integrator.set_integrator(integrator,*integrator_args,**integrator_kwargs)

    def _get_ksq(self,x,E):
        return 2*self.mass*(E - self.V(x))

    def integrate_at_E(self,E,xs,psi_start, dpsi_start):
        """
        Integrate the Schrodinger equation at energy E.

        This routine integrates the Schrodinger equation
        by the shooting method.

        Parameters
        ----------

        E : float
            Energy at which the integration is performed. If this is
            not an eigenvalue and the potential V(inf) > E, (that is, if
            the particle is bound in the potential, the 
            integration will diverge.

        xs : iterable
            A value of the wavefunction and its gradient are returned
            for every x.

        psi_start : float
            Value of the wavefunction at ``xs[0]``.

        dpsi_start : float
            Value of the gradient of the wavefunction at ``xs[0]``.

        Returns
        -------

        psis : numpy array
            The wavefunction at each ``xs``.

        dpsis : numpy array
            The gradient of the wavefunction at each ``xs``.
        """
        xstart = xs[0]
        self.integrator.set_initial_value(
                (psi_start,dpsi_start),xstart)
        self.integrator.set_f_params(E)
        psis, dpsis = [psi_start], [dpsi_start]
        for x in xs[1:]:
            self.integrator.integrate(x)
            psis.append(self.integrator.y[0])
            dpsis.append(self.integrator.y[1])
        return np.array(psis), np.array(dpsis)

    def solve_last_val(self,Elow, Ehigh, xstart, xend, 
            psi_start, dpsi_start, psi_last,npts=500):
        """
        Solve the Schrodinger equation for a specific boundary condition.

        This routine integrates the Schrodinger equation from given
        initial conditions and varies E until a particular boundary
        condition holds at the other end.

        Parameters
        ----------

        Elow, Ehigh : float
            Search for energies between these values.

        xstart,xend : float
            Integrate from xstart to xend.

        psi_start : float
            Value of the wavefunction at `xstart`.

        dpsi_start : float
            Value of the gradient of the wavefunction at `xend`.

        psi_end : float
            Value of the wavefunction at xend. The energy is varied 
            until this boundary condition is achieved.

        npts : int
            Number of points to use in the integration. Increasing
            the number of points may increase the accuracy of the 
            solution if a low-quality integrator is used.

        Returns
        -------

        float:
            Energy at which the boundary conditions are satisfied.

        Raises
        ------

        ValueError
            If there is no solution in the range [ Elow, Ehigh ].
        """
        xs = np.linspace(xstart,xend,npts)
        f = lambda E: self.integrate_at_E(E,xs, psi_start, dpsi_start)[0][-1] - psi_last
        return brentq(f,Elow,Ehigh)


class Integrator1D(IntegratorBase):
    """
    Integrate the one-dimensional Schrodinger equation.

    This class defines methods to integrate the Schrodinger equation::

           1 d^2
       [ - - ---- + V(x) ]  psi(x) = E*psi(x)
           2 dx^2 

    Note that this also solves the radial component of the 
    Schrodinger equation for centrally symmetric fields v(r),
    with ``psi(x) = r u(r)`` and ``V(x) = l(l+1)/r^2 + v(r)``.

    Parameters
    ----------

    V : function
        Function defining the potential: V(x) -> x.

    integrator : string, optional
        valid integrator as recognized by the ``scipy.ode`` module.
        "vode" by default.

    *integrator_args, **integrator_kwargs : optional
        passed to the ``ode.set_integrator`` method.
    """
    def _get_dphi(self,x,(phi1,phi2),E):
        return [ phi2, -self._get_ksq(x,E)*phi1 ]
 

class ShootScattering(Integrator1D):
    """
    Calculate the scattering properties of a potential.
    """
    def get_phase_shift(self,E,r,npts=500):
        logder = self.get_logder(E,r,npts)
        return self.get_phase_shift_from_logder(logder,E,r)

    def get_phase_shift_from_logder(self,logder,E,r):
        k = np.sqrt(2*self.mass*E)
        kr = k*r
        jl, jlp, yl, ylp = sph_jnyn(0,kr)
        iyl = 1j*yl
        iylp = 1j*ylp
        sl = -(jl-iyl)/(jl+iyl) * (logder-kr*(jlp-iylp)/(jl-iyl))/(logder-kr*(jlp+iylp)/(jl+iyl))
        return np.angle(sl)/2.

    def get_logder(self,E,r,npts=500):
        rs = np.linspace(0.,r,npts)
        psis, dpsis = self.integrate_at_E(E,rs,0.,1.)
        return r*dpsis[-1]/psis[-1] - 1.

        
