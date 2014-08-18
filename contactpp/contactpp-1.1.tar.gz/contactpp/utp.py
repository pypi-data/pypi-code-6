
import numpy as np
from scipy.optimize import fmin
from numpy.polynomial.polynomial import Polynomial

from troullier import make_troullier_potential
from solve import ShootScattering

class UTPPotential(object):
    """
    Object representing a scattering potential.
    """
    def __init__(self,potential_polynomial,cutoff,scattering_length):
        self._potential_polynomial = potential_polynomial
        self.cutoff = cutoff
        self._V = lambda r: np.where(abs(r)<=self.cutoff,
                self._potential_polynomial(r/self.cutoff),0.)

    @property
    def V(self):
        return self._V

    @property
    def coefficients(self):
        return self._potential_polynomial.coef


class UTPGenerator(object):

    def __init__(self,a,kf,c=None,init_coeffs=None,
            integrator="vode",npoints=1000,nks=10,objective_function="rms",dos=None,
            verbose=True):
        self.a = a
        self.kf = float(kf)
        self.Ef = self.kf**2
        self.c = c
        if self.a < 0.:
            if self.c is None:
                raise ValueError("Cutoff cannot be undefined if the \
                branch is 'attractive'.")
        if init_coeffs is not None:
            if c is None:
                raise ValueError(
                        "If initial coefficients are specified, the cutoff\
                        must also be specified explicitly.")
            self.init_coeffs = init_coeffs
        else:
            self.init_coeffs, self.c = \
                    self._get_init_coeffs_from_troullier()
        self.integrator = integrator
        self.npoints = npoints
        self.objective_function = objective_function
        if self.objective_function not in ("rms", "max") : 
            raise ValueError(
                    "objective_function argument should be either 'rms'\
                    or 'max'.")
        if self.objective_function == "max" and dos is not None:
            raise ValueError(
                    "Cannot specify DOS when objective function is 'max'. "\
                    "Specifying a DOS is only valid when the objective "\
                    "function is 'rms'.")
        if self.objective_function == "rms" :
            self.dos = dos if dos is not None else lambda k: k**2
        self.OBJECTIVE_FUNCTIONS = {
                "rms" : self._calc_rms_error,
                "max" : self._calc_max_error
        }
        self.ks = np.linspace(0.,kf,nks)
        self.verbose = bool(verbose)

    def _get_init_coeffs_from_troullier(self):
        Ef = self.kf**2
        calibration_energy = 0.6*Ef
        troullier_pp = make_troullier_potential(
                "repulsive" if self.a > 0 else "attractive",
                self.a,calibration_energy,self.c)
        assert(troullier_pp.coefficients[1] == 
                troullier_pp.coefficients[3] == 0.)
        troullier_coeffs = troullier_pp.coefficients
        # convert from polynomial in r to polynomial in r/rc
        troullier_poly = Polynomial(
                [ coeff*troullier_pp.cutoff**icoeff 
                    for icoeff, coeff in enumerate(troullier_coeffs) ])
        # factor out (1-r/r_c)^2
        init_poly = troullier_poly / (Polynomial([1.,-1.])**2)
        init_poly_coeffs = init_poly.coef
        init_coeffs = np.zeros((len(init_poly_coeffs)-2,))
        init_coeffs[0] = init_poly_coeffs[1] # v1
        init_coeffs[1] = init_poly_coeffs[2] # v2
        init_coeffs[2:] = init_poly_coeffs[4:]
        return init_coeffs,troullier_pp.cutoff

    def _calc_tandelta(self,V,k):
        s = ShootScattering(V,integrator=self.integrator,mass=0.5)
        E = k**2
        delta = s.get_phase_shift(E,1.1*self.c,npts=self.npoints)
        return float(np.tan(delta))

    def _calc_true_tandelta(self,k):
        return -k*self.a

    def _calc_tandelta_error(self,V):
        tandeltas = np.array([ self._calc_tandelta(V,k) for k in self.ks ])
        true_tandeltas = np.array([ self._calc_true_tandelta(k)
            for k in self.ks ])
        return true_tandeltas - tandeltas

    def _calc_rms_error(self,V):
        """
        Objective function.

        RMS error over all k values, weighted by a density of states.
        """
        tandelta_errors = self._calc_tandelta_error(V)
        return np.sqrt(sum(
            (tandelta_errors)**2 * self.dos(self.ks)))/len(self.ks)

    def _calc_max_error(self,V):
        """
        Objective function.

        Maximal (L-infinity norm) error over all k-values.
        """
        tandelta_errors = self._calc_tandelta_error(V)
        return max(abs(tandelta_errors))

    def _coeffs2poly(self,coeffs):
        poly_coeffs = np.zeros((len(self.init_coeffs)+2,))
        poly_coeffs[0] = 0.5*coeffs[0] # v1
        poly_coeffs[1] = coeffs[0] # v1
        poly_coeffs[2] = coeffs[1]  # v2
        poly_coeffs[3] = 2*coeffs[1]-coeffs[0]
        poly_coeffs[4:] = coeffs[2:]
        p = Polynomial(poly_coeffs)*Polynomial([1,-1])**2
        assert abs(p.coef[3]) < 1e-10
        assert abs(p.coef[1]) < 1e-10
        assert abs(p(1.))<1e-10
        return p

    def _make_pseudo(self,coeffs):
        p = self._coeffs2poly(coeffs)
        return lambda r: np.where(r<self.c,p(r/self.c),0.)

    def _make_objective_func(self):
        f = self.OBJECTIVE_FUNCTIONS[self.objective_function]
        def objective(coeffs):
            V = self._make_pseudo(coeffs)
            error = f(V)
            return error
        return objective

    def _make_callback_func(self):
        self.niter = 0
        if self.verbose:
            def callback(coeffs):
                if (self.niter % 10 == 0):
                    V = self._make_pseudo(coeffs)
                    error = self.OBJECTIVE_FUNCTIONS[self.objective_function](V)
                    print "# iterations: {:<4d} | {} error: {}".format(
                            self.niter,self.objective_function, error)
                self.niter += 1
        else:
            callback = None
        return callback

    def _run_optimizer(self):
        new_coeffs = fmin(self._make_objective_func(),
                self.init_coeffs,
                callback=self._make_callback_func(),
                disp=self.verbose)
        return new_coeffs

    def make_pseudopotential(self):
        new_coeffs = self._run_optimizer()
        p = self._coeffs2poly(new_coeffs)
        return UTPPotential(p,self.c,self.a)


def make_utp_potential(scattering_length, fermi_energy, cutoff=None, 
        init_coeffs=None,integrator="vode",npoints=1000,nks=10,objective_function="rms",
        dos=None,verbose=True):
    """
    Create a UTPPotential object.

    Parameters
    ----------

    scattering_length : float
        Scattering length. If positive, the pseudopotential is built for
        the repulsive branch. If negative, it is built for the attractive 
        branch. Note that UTP potentials do not exist for the bound state.
        
    fermi_energy : float
        The UTP constructor will minimize the errors in phase shifts over 
        the range ``k = 0`` to ``kf``, where ``kf = sqrt(Ef)`` is the 
        Fermi wavevector.

    cutoff : float
        Choice of cutoff radius. Compulsory for negative scattering lengths.
        If the branch is "repulsive", the cutoff is chosen as the first 
        antinode of the true wavefunction at ``3/5 * fermi_energy``. 
        Specifying the cutoff explicitly will override this.

    init_coeffs : iterable, optional
        Initial coefficients for the optimizer. If not specified, a Troullier
        pseudopotential is constructed and those coefficients are used.
        If specified, the coefficients will be interpreted as:
        ``[ v1, v2, v4, v5 ... v11 ]``, with the potential defined as,
        ``V(x)/Ef = (1-x^2) * (v1*(0.5+x) + v2*x^2 + (2v2-v1)*x^3 + v4*x^4 + 
        sum_{i=5}^13 v_i x^i`` where ``x = r/cutoff``.

    integrator : string, optional
        Which integrator to use when computing the phase shift. See the 
        documentation for ``scipy.integrate.ode`` for details. If the cutoff
        chosen is very small, it might be worthwhile changing this to 
        ``"dopri5"``. ``"vode"`` by default.

    npoints : int, optional
        Number of points to use in the integration. If the cutoff chosen
        is small, convergence of the results with respect to ``npoints`` 
        should be checked. 1000 by default.

    nks : int, optional
        Number of k-points to use when integrating the error in phase shifts.
        Increasing this may lead to somewhat better results. 10 by default.

    objective_function : string, optional
        Type of objective function to minimize: either "rms" to minimize 
        ``int_0^kF { [delta_PP(k) - delta_true(k)]^2 dos(k) dk``, where dos
        is another optional argument, or "max" to minimize 
        ``max(|delta_PP(k) - delta_true(k)|)``. "rms" by default.

    dos : function, dos(k) -> density of states, optional
        When using the RMS objective function, this argument sets the cost function 
        that is optimized when constructing the potential. The objective function is:
        ``int_0^kF { [delta_PP(k) - delta_true(k)]^2 dos(k) dk``. 
        By default, ``dos(k) = lambda k: k**2``. Must accept a numpy array (of k-values)
        as input. If the objective_function is not RMS, specifying this argument raises
        a ValueError.

    verbose : boolean, optional
        Display convergence information. True by default.
    """
    pgen = UTPGenerator(scattering_length,np.sqrt(fermi_energy),
            cutoff,init_coeffs,integrator,npoints,nks,objective_function,
            dos,verbose)
    return pgen.make_pseudopotential()
