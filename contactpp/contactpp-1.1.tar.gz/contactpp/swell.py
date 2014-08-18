
"""
Square well pseudopotential.
"""

import numpy as np
from scipy.optimize import brentq

class SquareWellPotential(object):
    """
    Object representing a Square well potential.

    Attributes
    ----------

    height : float
        Potential height (negative for a well).

    radius : float
        Potential radius
    """

    def __init__(self,height,radius):
        self.height = height
        self.radius = radius
        self._V = lambda r: np.where(abs(r)<=self.radius,
                self.height,0.)

    @property
    def V(self):
        return self._V


class _SquareWellBaseGenerator(object):
    """
    Base class for square well generators.
    """

    def __init__(self,a,c):
        self.a = a
        self.c = c # value or None
        self._check_inputs()
        
    def make_pseudopotential(self):
        if self.c is None:
            R = self._calc_V_R()
        else:
            R = self.c
        V = self._calc_V_from_R(R)
        return SquareWellPotential(V,R)


class TopHatGenerator(_SquareWellBaseGenerator):

    def _calc_gamma(self,R,V):
        return R*np.sqrt(V)

    def _check_inputs(self):
        if self.c is not None:
            if self.a >= self.c:
                raise ValueError("Cannot generate a top hat potential for \
scattering lengths a > c, where c is the top hat radius.")
        if self.a < 0.:
            raise ValueError("Scattering length a <= 0.")

    def _calc_a(self,R,V):
        g = self._calc_gamma(R,V)
        if g<1e-8:
            # Use Taylor expansion
            return R*((g**2)/3. - (g**4)*2./15. + (g**6)*17./315.)
        else:
            return R*(1.-np.tanh(g)/g)

    def _calc_reff(self,R,V):
        g = self._calc_gamma(R,V)
        return R* ( 1 + (3*np.tanh(g)-g*(3+g**2) )/(3*g*(g - np.tanh(g))**2))

    def _calc_V_from_R(self,R):
        f = lambda V: self._calc_a(R,V)-self.a
        xlow, xhigh = bracket_root(f, 0.) 
        return brentq(f,xlow,xhigh)

    def _calc_V_R(self):
        """
        Calculate V and R such that the potential has zero effective range.
        """
        def objective_func(R):
            V = self._calc_V_from_R(R)
            reff = self._calc_reff(R,V)
            return reff
        Rlow, Rhigh = bracket_root(
                objective_func,1.001*self.a,init_step=1e-3)
        R = brentq(objective_func,Rlow,Rhigh)
        return R


class SquareWellGenerator(_SquareWellBaseGenerator):

    def _calc_gamma(self,R,V):
        return R*np.sqrt(abs(V))

    def _check_inputs(self):
        if self.a > 0.:
            raise ValueError("Scattering length a >= 0.")

    def _calc_a(self,R,V):
        g = self._calc_gamma(R,V)
        if g < 1e-8:
            # Use Taylor expansion
            return -R*((g**2)/3. + (g**4)*2./15. +(g**6)*17./315.)
        else:
            return R*(1.-np.tan(g)/g)

    def _calc_V_from_R(self,R):
        f = lambda V: self._calc_a(R,V) - self.a
        # bracket a root between V = 0. and V corresponds to first divergence of a.
        xlow, xhigh = bracket_root(f,0.,direction=-1.,xmax=-np.pi**2/(4.*R**2)+1e-8)
        return brentq(f,xlow,xhigh)


def bracket_root(f,xstart,direction=1,xmax=None,init_step=0.1,step_ratio=1.3):
    """
    Bracket the first root of f beyond a certain point.

    Returns a tuple (xlow, xhigh) of points around a root of f. The 
    algorithm will only search x >= xstart if direction == 1, and only
    x <= xstart if direction == -1. Stop search if no root is found 
    between `xstart` and `xmax`.

    Arguments
    ---------

    f : scalar function f(x) -> y.
    xstart : float
        Will start looking for roots at `xstart`.
    direction : +1 or -1, optional.
        Direction in which to look for the root. If ``direction == +1``,
        search for ``x >= xstart``, else search for ``x <= xstart``.
        default: +1
    xmax : float, optional
        Only search for roots between ``xstart`` and ``xmax``. By default,
        ``direction*infty``
    init_step : float, optional
        Initial step size when searching. Reduce this if you think the 
        root is very close to ``xstart`` or if you think the algorithm
        is skipping over roots.
    step_ratio : float, optional
        How much the step size increases at each iteration. Increasing this
        increases the likelihood the algorithm will miss roots, at the cost
        of computational expense. It's unlikely you would ever want to set 
        this to less than 1.
        Default : 1.3
    """
    if xmax is None:
        xmax = direction*np.infty
    else:
        # Check that the sign of xmax is correct
        if np.sign(xmax-xstart) != direction:
            raise ValueError("Argument `xstart` has the wrong sign.")
    step = init_step
    xlow = xstart
    xhigh = xlow + direction*step
    flow = f(xlow)
    fhigh = f(xhigh)
    while flow*fhigh >= 0.:
        if fhigh == 0.:
            # Fallen exactly on a root. 
            xhigh = min(xmax,xhigh+init_step)
            break
        elif flow == 0.:
            # Starts exactly on a root.
            raise ValueError("xstart is a root.")
        step *= step_ratio
        xlow, xhigh = xhigh, xhigh + direction*step
        if xhigh >= xmax:
            xhigh = xmax
        flow = f(xlow)
        fhigh = f(xhigh)
        if xhigh == xmax and flow*fhigh >= 0.:
            raise RuntimeError(
                    "Failed to find a root between {} and {}.".format(
                        xlow,xhigh))
    return xlow,xhigh


def make_square_well_potential(scattering_length, radius):
    """
    Create a SquareWellPotential object. Can be either a top-hat
    potential (for positive scattering lengths) or a well 
    (for negative scattering lengths.
    
    Parameters
    ----------

    scattering_length : float
        Float indicating the scattering length.

    radius : float
        Radius of the potential.

    Returns
    -------

    SquareWellPotential
    """
    if radius is not None and radius <= 0.:
        raise ValueError("Well radius must be positive.")
    if scattering_length > 0.:
        gen = TopHatGenerator(scattering_length, radius)
    elif scattering_length < 0.:
        gen = SquareWellGenerator(scattering_length, radius)
    else:
        raise NotImplementedError("Not implemented for a = 0.")
    return gen.make_pseudopotential()


