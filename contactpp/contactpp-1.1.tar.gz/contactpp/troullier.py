
import numpy as np
from numpy.polynomial.polynomial import Polynomial
from scipy.optimize import fminbound, brentq
from scipy.integrate import quad

def get_contact_u(E,delta):
    k = np.sqrt(E)
    return lambda r: np.sin(k*r+delta)

def get_contact_psi(E,delta):
    return lambda r: get_contact_u(E,delta)(r)/r

def get_delta(k,a):
    return np.arctan(-k*a)

class _TroullierPotential(object):
    """
    Object representing a scattering potential.

    Represents a scattering pseudopotential built using the 
    Troullier-Martins formalism. 

    Attributes
    ----------

    cutoff: float
    
    calibration_energy: float

    scattering_length: float

    coefficients: numpy array
        array of coefficients for the pseudopotential, 
        V(r) = sum(coefficients[i]*r^i) for r < cutoff.

    psi: function 
        psi(r) returns the value of the pseudowavefunction at the
        calibration energy at r.

    true_psi: function
        true_psi(r) returns the value of the contact wavefunction
        at the calibration at r.

    V: function
        V(r) returns the value of the pseudopotential at r.
    """
    def __init__(self, ppsi_polynomial, cutoff, calibration_energy, scattering_length):
        self.ppsi_polynomial = ppsi_polynomial
        self.cutoff = cutoff
        self.calibration_energy = calibration_energy
        self.scattering_length = scattering_length
        self._potential_polynomial = self._get_pp_poly()
        self._check_potential_polynomial()
        self._V = lambda r: np.where(abs(r)<=self.cutoff,
                self._potential_polynomial(r),0.)
        self._ppsi_inner = self._make_ppsi()
        self._true_psi = self._get_true_psi()
        self._ppsi = lambda r: np.where(abs(r)<=self.cutoff,
                self._ppsi_inner(r),self._true_psi(r))

    def _get_pp_poly(self):
        p = self.ppsi_polynomial
        dp = p.deriv(1)
        dp_o_r = p.deriv(1) / Polynomial([0.,1.])
        ddp = p.deriv(2)
        pp_poly = self.calibration_energy + 2*dp_o_r + (ddp + dp**2)
        return pp_poly
    
    def _check_potential_polynomial(self):
        Vcut = self._potential_polynomial(self.cutoff)
        if abs(Vcut)>1e-6:
            raise RuntimeError(
                    "Value of PP at cutoff is too large: {}".format(Vcut))

    def _make_ppsi(self):
        return lambda r: np.exp(self.ppsi_polynomial(r))

    @property
    def coefficients(self):
        return self._potential_polynomial.coef

    @property
    def V(self):
        return self._V

    @property
    def psi(self):
        """
        Pseudowavefunction at calibration energy.
        """
        return self._ppsi

    @property
    def true_psi(self):
        """
        True contact wavefunction at calibration energy.
        """
        return self._true_psi


class TroullierScatteringPotential(_TroullierPotential):
    __doc__ = _TroullierPotential.__doc__
    def _get_true_psi(self):
        k = np.sqrt(self.calibration_energy)
        delta = get_delta(k,self.scattering_length)
        return lambda r : np.sin(k*r+delta)/r

class TroullierBoundPotential(_TroullierPotential):
    __doc__ = _TroullierPotential.__doc__
    def _get_true_psi(self):
        k = np.sqrt(-self.calibration_energy)
        return lambda r : np.exp(-k*r)/r



class _TroullierGenerator(object):
    """
    Base class for all Troullier generators.
    """
    def __init__(self,a,k,c):
        assert k > 0.
        self.a = a
        self.k = float(k)
        self.delta = get_delta(self.k,self.a)
        self.c = c if c is not None else self.calc_c()
        self._check_c()
        self.norm_true = self.calc_norm_true()

    def psi(self,r):
        return self.ur(r)/r

    def _build_lmatrix(self):
        """ Build the LHS of the linear equations """
        m = np.zeros((4,4))
        c = self.c
        m[0,:] = np.array([ 1., c**2,  c**6,    c**8]) # p
        m[1,:] = np.array([ 0., 2*c, 6*c**5,  8*c**7]) # p'
        m[2,:] = np.array([ 0., 2., 30*c**4, 56*c**6]) # p''
        m[3,:] = np.array([ 0., 0.,120*c**3,336*c**5]) # p'''
        return m

    def _build_rvec(self,a4):
        """ RHS of linear equations. """
        c = self.c
        a8 = 0.
        p, dp = self._get_p_dp()
        ddp = -self.true_energy() -2./c*dp-dp**2
        dddp = 2./c**2*dp-2./c*ddp-2.*dp*ddp
        return np.array((p - a4*c**4 - a8*c**8,
                         dp - 4.*a4*c**3 - 8.*a8*c**7,
                         ddp - 12.*a4*c**2 - 56.*a8*c**6,
                         dddp - 24.*a4*c - 336*a8*c**5))

    def _solve_cont(self,a4):
        """
        Solve continuity equations for a particular a4.
        """
        lmatrix = self._build_lmatrix()
        rvec = self._build_rvec(a4)
        a0,a2,a6,a8 = np.linalg.solve(lmatrix,rvec)
        return a0,a2,a6,a8

    def _make_p(self,as_):
        """
        Exponential kernel of pseudo-wavefunction for coefficients as_
        """
        a0,a2,a4,a6,a8 = as_
        return Polynomial((a0,0.,a2,0.,a4,0.,a6,0.,a8))

    def _make_ppsi(self,as_):
        """
        Pseudo wavefunction for as_
        """
        return lambda r: np.exp(self._make_p(as_)(r))

    def _get_norm_diff(self,a4):
        """
        Get the difference in norm (over r = 0..c) between
        pseudo wavefunction made with a4 and true wavefunction.
        """
        a0,a2,a6,a8 = self._solve_cont(a4)
        as_ = (a0,a2,a4,a6,a8)
        ppsi = self._make_ppsi(as_)
        return quad(lambda r: ppsi(r)**2*r**2,0.,self.c)[0] - self.norm_true

    def _find_a4_bracket(self):
        dinc = 2.
        norm_a4p = self._get_norm_diff(0.1)
        norm_a4m = self._get_norm_diff(-0.1)
        xmax = 1e7
        if norm_a4p*norm_a4m < 0.:
            xl, xr = -0.1,0.1
        elif abs(norm_a4p) < abs(norm_a4m):
            # search on the positive side.
            xl = 0.1
            xr = dinc*xl
            if xr > xmax:
                raise RuntimeError("Max value exceeded when trying to bracket coefficient.")
            norml = norm_a4p
            normr = self._get_norm_diff(xr)
            while normr*norml > 0.:
                xl,xr = xr,xr*dinc
                norml, normr = normr, self._get_norm_diff(xr)
        else:
            # search on negative side
            # search on the positive side.
            xl = -0.1
            xr = dinc*xl
            if xr < -xmax:
                raise RuntimeError("Min value exceeded when trying to bracket coefficient.")
            norml = norm_a4p
            normr = self._get_norm_diff(xr)
            while normr*norml > 0.:
                xl,xr = xr,xr*dinc
                norml, normr = normr, self._get_norm_diff(xr)
        assert self._get_norm_diff(xl)*self._get_norm_diff(xr) < 0., \
                "xl: {}, xr: {}, norml: {}, normr: {}".format(xl,xr,self.get_norm_diff(xl),self.get_norm_diff(xr))
        return xl,xr

    def _solve_bracketed(self,a4l,a4h):
        a4 = brentq(self._get_norm_diff,a4l,a4h)
        a0,a2,a6,a8 = self._solve_cont(a4)
        return (a0,a2,a4,a6,a8)

    def _solve(self):
        """ 
        Return the coefficients for the PP.

        Returns (a0,a2,a4,a6,a8)
        """
        a4l, a4h = self._find_a4_bracket()
        return self._solve_bracketed(a4l,a4h)

    def make_pseudopotential(self):
        """
        Return a pseudopotential object.
        """
        as_ = self._solve()
        ppsi_polynomial = self._make_p(as_)
        ppot = self.potential_class(ppsi_polynomial,self.c,self.true_energy(),self.a)
        return ppot


class _TroullierScatteringGenerator(_TroullierGenerator):
    """
    Base class for the repulsive/attractive generators.
    """
    def ur(self,r):
        return np.sin(self.k*r+self.delta)

    def true_energy(self):
        return self.k**2

    def calc_norm_true(self):
        """
        Norm of the true wavefunction over r <= c
        """
        k = self.k
        d = self.delta
        c = self.c
        return 0.25/k * (-np.sin(2*(d+k*c)) + np.sin(2*d) + 2*k*c )

    def _get_p_dp(self):
        """ 
        First and second derivative of 'p' in terms of the true wavefunction
        """
        kca = self.k*self.c + self.delta
        p = np.log(np.sin(kca))-np.log(self.c)
        dp = self.k/np.tan(kca) - 1./self.c
        return p, dp


class TroullierRepulsiveGenerator(_TroullierScatteringGenerator):
    """
    Class to generate a Troullier pseudopotential for the 
    repulsive scattering branch of the Feschbach resonance.
    """
    def __init__(self,a,k,c=None):
        assert a > 0.
        self.potential_class = TroullierScatteringPotential
        super(TroullierRepulsiveGenerator,self).__init__(a,k,c)

    def _check_c(self):
        if self.c <= 0.:
            raise ValueError("Cutoff <= 0.")
        if self.psi(self.c) <= 0.:
            raise ValueError("Cutoff >= first node.")
        
    def calc_c(self):
        """
        Calculate the cutoff length.

        Set at the first antinode of the wavefunction.
        """
        cl = 1./self.k * (- self.delta)
        ch = 1./self.k * (np.pi - self.delta)
        c = fminbound(lambda r: -self.psi(r),cl,ch)
        return c


class TroullierAttractiveGenerator(_TroullierScatteringGenerator):
    """
    Class to generate a Troullier pseudopotential for the 
    attractive scattering branch of the Feschbach resonance.
    """
    def __init__(self,a,k,c):
        assert a < 0.
        try:
            float(c)
        except TypeError:
            raise TypeError("Invalid argument for c. Note that default \
                parameters cannot be used for the cutoff in the \
                attractive branch.")
        self.potential_class = TroullierScatteringPotential
        super(TroullierAttractiveGenerator,self).__init__(a,k,c)

    def _check_c(self):
        """
        Check that the cutoff is between 0 and the first node
        of the wavefunction.
        """
        if self.c <= 0.:
            raise ValueError("Cutoff <= 0.")
        first_node = (np.pi-self.delta)/self.k
        if self.c > first_node:
            raise ValueError(
                    "Cutoff >= first node. first node: {}".format(first_node))


class TroullierBoundGenerator(_TroullierGenerator):
    """
    Class to generate a Troullier pseudopotential for the 
    bound state of the Feschbach resonance.
    """
    def __init__(self,a,c):
        assert a > 0.
        k = 1./a
        try:
            float(c)
        except TypeError:
            raise TypeError("Invalid argument for c. Note that default \
                parameters cannot be used for the cutoff in the \
                attractive branch.")
        self.potential_class = TroullierBoundPotential
        super(TroullierBoundGenerator,self).__init__(a,k,c)

    def ur(self,r):
        return np.exp(-self.k*r)

    def true_energy(self):
        return -0.5*self.k**2

    def calc_norm_true(self):
        """ Norm of the true wavefunction over r <= c """
        k = self.k
        c = self.c
        return 0.5/k * (1.-np.exp(-2*c*k))

    def _check_c(self):
        if self.c <= 0.:
            raise ValueError("Cutoff <= 0.")
        first_node = (np.pi-self.delta)/self.k
        if self.c > first_node:
            raise ValueError(
                    "Cutoff >= first node. first node: {}".format(first_node))


    def _get_p_dp(self):
        p = -self.k*self.c - np.log(self.c)
        dp = -self.k-1./self.c
        return p, dp
                

branch_generator = {
        "repulsive" : TroullierRepulsiveGenerator,
        "attractive" : TroullierAttractiveGenerator,
        "bound" : TroullierBoundGenerator,
        }


def make_troullier_potential(branch, scattering_length, calibration_energy=None, cutoff=None):
    """
    Create a TroullierPotential object.

    Parameters
    ----------

    branch: {"repulsive", "scattering", "bound"}

    scattering_length: float
        Float indicating the scattering length. Must be positive 
        if branch is "repulsive" or "bound", and negative
        otherwise.

    calibration_energy: float
        Energy at which to calibrate the Troullier potential. The Fermi
        energy is normally a good choice. Must be larger than 0 if 
        branch is "repulsive" or "attractive". This parameter is
        ignored if branch is "bound". In that case, the 
        calibration energy is taken to be the true bound state
        energy -1/2a^2.

    cutoff: float
        Choice of cutoff radius. Compulsory if branch is
        "bound" or "attractive". If branch == "repulsive", this
        is chosen as the first antinode of the true wavefunction
        at the calibration energy by default, but can be overriden.

    Returns
    -------

    TroullierBoundPotential or TroullierScatteringPotential
    """
    if branch == "bound":
        pgen = branch_generator[branch](scattering_length,cutoff)
    else:
        k = np.sqrt(calibration_energy)
        try:
            pgen = branch_generator[branch](scattering_length,k,cutoff)
        except KeyError:
            raise ValueError("Wrong argument for 'branch'. Should be one of: {}".
                    repr(branch_generator.keys()))
    ppot = pgen.make_pseudopotential()
    return ppot

