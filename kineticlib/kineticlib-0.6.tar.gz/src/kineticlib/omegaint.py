"""Contains formulas for elastic omega integrals for various cross-section parameters, plus a function which
loads interaction parameters
"""
__author__ = 'George Oblapenko'
__license__ = "GPL"
__maintainer__ = "George Oblapenko"
__email__ = "kunstmord@kunstmord.com"
__status__ = "Development"


import numpy as np
from scipy import constants
from scipy.special import gamma
from scipy.misc import factorial
from .errors import KineticlibError


def rigid_sphere_omega(T: float, l: int, r: int, m: float, sigma: float, nokt: bool=False) -> float:
    """Returns the :math:`\\Omega^{(l,r)}`-integral for a rigid sphere potential for any `l > 0`  and `r > 0`

    Parameters
    ----------
    T : float
        the temperature of the mixture
    l : int
        the l degree of the integral
    r : int
        the r degree of the integral
    m : float
        the collision-reduced mass :math:`m_{cd}`
    sigma : float
        the collision diameter :math:`\\sigma_{cd}`
    nokt : bool, optional
        if True and full_integral is True, the result will be multiplied by :math:`\\sqrt{(1 / kT)}`, defaults to True

    Returns
    -------
    float
        The calculated rigid sphere omega integral
    """
    if nokt is False:
        mult = (T * constants.k / (2.0 * constants.pi * m)) ** 0.5
    else:
        mult = (1.0 / (2.0 * constants.pi * m)) ** 0.5

    return 0.5 * mult * constants.pi * factorial(r + 1) * (1.0 - 0.5 * (1.0 + (-1) ** l) / (l + 1)) * (sigma ** 2)


def omega_dimless_LJ(T: float, l: int, eps: float) -> float:
    """Returns the dimensionless :math:`\\Omega^{(l,l)}`-integral for the Lennard Jones potential (for `l=1` and `l=2`)

    Parameters
    ----------
    T : float
        the temperature of the mixture
    l : int
        the l degree of the integral
    eps : float
        the Lennard-Jones :math:`\\varepsilon_{cd}` parameter

    Returns
    -------
    float
        The dimensionless calculated Lennard-Jones omega integral

    Raises
    ------
    KineticlibError
        if `l` not in `{1,2}`
    """
    if l == 1:
        tmp = np.log(T / eps) + 1.4
        f = [-0.16845, -0.02258, 0.19779, 0.64373, -0.09267, 0.00711]
    elif l == 2:  # l = 2
        tmp = np.log(T / eps) + 1.5
        f = [-0.40811, -0.05086, 0.3401, 0.70375, -0.10699, 0.00763]
    else:
        raise KineticlibError('Cannot calculate the Omega^{(' + str(l) + ',' + str(l)
                              + ')} integral using the Lennard-Jones potentail')
    return 1.0 / (f[0] + f[1] / (tmp ** 2) + f[2] / tmp + f[3] * tmp
                + f[4] * (tmp ** 2) + f[5] * (tmp ** 3))


def omega_dimless_IPL(T: float, l: int, sigma: float, eps: float, phizero: float, beta: float) -> float:
    """Returns the dimensionless :math:`\\Omega^{(l,l)}`-integral for the IPL potential (for `l=1` and `l=2`)

    Parameters
    ----------
    T : float
        the temperature of the mixture
    l : int
        the l degree of the integral
    sigma : float
        the collision diameter :math:`\\sigma_{cd}`
    eps : float
        the Lennard-Jones :math:`\\varepsilon_{cd}` parameter
    phizero : float
        the IPL :math:`\\phi_{0}` parameter
    beta : float
        the IPL :math:`\\beta` parameter

    Returns
    -------
    float
        The dimensionless calculated IPL omega integral

    Raises
    ------
    KineticlibError
        if `l` not in `{1,2}`
    """
    Tstar = T / eps
    vstar = phizero / eps
    rstar = 1.0 / (beta * sigma)
    Abig = np.zeros(3)
    if l == 1:
        a = np.array([[-267.0, 201.57, 174.672, 54.305],
                      [26700, -19226.5, -27693.8, -10860.9],
                      [-8.9, 6.3201, 10.227, 5.4304]])
        a[2, :] = a[2, :] * 100000
        coeff = 0.89
        pows = np.array([2, 4, 6])
        TT = Tstar
    elif l == 2:  # l == 2
        a = np.array([[-33.0838, 20.0862, 72.1059, 68.5001],
                      [101.571, -56.4472, -286.393, -315.4531],
                      [-87.7036, 46.313, 227.146, 363.1807]])
        coeff = 1.04
        pows = np.array([2, 3, 4])
        TT = np.log(vstar / 10)
    else:
        raise KineticlibError('Cannot calculate the Omega^{(' + str(l) + ',' + str(l)
                              + ')} integral using the IPL potentail')
    Abig[:] = a[:, 0] + (a[:, 1] + a[:, 2] / np.log(vstar / 10) + a[:, 3] / ((np.log(vstar / 10)) ** 2)) /\
              ((rstar * np.log(vstar / 10)) ** 2)
    return (coeff + Abig[0] / (TT ** pows[0]) + Abig[1] / (TT ** pows[1]) + Abig[2] / (TT ** pows[2])) *\
           ((rstar * np.log(vstar / Tstar)) ** 2)


def omega_vss(T: float, l: int, m: float, vssc: float, vsso: float, nokt: bool=False) -> float:
    """Returns the dimensionless :math:`\\Omega^{(l,l)}`-integral for the VSS potential (for `l=1` and `l=2`)

    Parameters
    ----------
    T : float
        the temperature of the mixture
    l : int
        the l degree of the integral
    m : float
        the collision-reduced mass :math:`m_{cd}`
    vssc : float
        the VSS potential :math:`C` parameter
    vsso : float
        the VSS potential :math:`\\omega` parameter
    nokt : bool, optional
        if True and full_integral is True, the result will be multiplied by :math:`\\sqrt{(1 / kT)}`, defaults to True

    Returns
    -------
    float
        The dimensionless calculated VSS omega integral

    Raises
    ------
    KineticlibError
        if `l` not in `{1,2}`
    """
    if nokt is False:
        multiplier = vssc * ((T * constants.k / (2 * constants.pi * m)) ** 0.5) * (T ** (-vsso))
    else:
        multiplier = vssc * ((1 / (2 * constants.pi * m)) ** 0.5) * (T ** (-vsso))
    if l == 1:
        integral = 0.5 * gamma(3 - vsso)
        return multiplier * integral * (constants.physical_constants['Angstrom star'][0] ** 2)
    elif l == 2:
        integral = 0.5 * gamma(4 - vsso)
        return multiplier * integral * (constants.physical_constants['Angstrom star'][0] ** 2)
    else:
        raise KineticlibError('Cannot calculate the Omega^{(' + str(l) + ',' + str(l)
                              + ')} integral using the VSS potentail')


def omega(T: float, l: int, r: int, idata: np.ndarray, model: str='IPL', dimensional: bool=True,
          nokt: bool=False) -> float:
    """Returns the :math:`\\Omega^{(l,r)}`-integral for a specified potential

    Parameters
    ----------
    T : float
        the temperature of the mixture
    l : int
        the l degree of the integral
    r : int
        the r degree of the integral
    idata : 1-D array-like
        the array of interaction data
    model : str
        the interaction model to be used, possible values:
            * 'IPL' (Inverse Power Law potential)
            * 'LJ' (Lennard-Jones potential)
            * 'RS' (Rigid Sphere model)
            * 'VSS' (Variable Soft Sphere model)
            * 'Switch' (returns the result for the Lennard-Jones model when :math:`T / \\varepsilon_{cd} < 10`
              and for the IPL potential otherwise)

        defaults to 'IPL'
    dimensional : bool
        if True, then the dimensional :math:`\\Omega^{(l,r)}`-integral is returned, otherwise,
        the dimensionless :math:`\\Omega^{(l,r)}`-integral is returned (dimensional integral divided by the same
        integral for the Rigid Sphere model)
    nokt : bool, optional
        if True and full_integral is True, the result will be multiplied by :math:`\\sqrt{(1 / kT)}`, defaults to True

    Returns
    -------
    float
        The :math:`\\Omega^{(l,r)}`-integral calculated using the selected potential

    Raises
    ------
    KineticlibError
        For the 'VSS', 'LJ', 'IPL' and 'Switch' models: if `l!=r` or `l` not in `{1,2}`
    """
    m = idata[0]
    sigma = idata[1]
    eps = idata[2]
    phizero = idata[3]
    beta = idata[4]
    vssc_11 = idata[5]
    vsso_11 = idata[6]
    vssc_22 = idata[7]
    vsso_22 = idata[8]

    if model == 'LJ' and l == r and (l == 1 or l == 2):
            if dimensional is True:
                return omega_dimless_LJ(T, l, eps) * rigid_sphere_omega(T, l, l, m, sigma, nokt)
            else:
                return omega_dimless_LJ(T, l, eps)
    elif model == 'RS':
        if dimensional is True:
            return rigid_sphere_omega(T, l, r, m, sigma, nokt)
        else:
            return 1.0
    elif model == 'Switch' and l == r and (l == 1 or l == 2):  # eps/kT > 10
        if T / eps > 10:
            om_dimless = omega_dimless_IPL(T, l, sigma, eps, phizero, beta)
        else:
            om_dimless = omega_dimless_LJ(T, l, eps)
        if dimensional is True:
            return om_dimless * rigid_sphere_omega(T, l, r, m, sigma)
        else:
            return om_dimless
    elif model == 'IPL' and l == r and (l == 1 or l == 2):
        if dimensional is True:
            return omega_dimless_IPL(T, l, sigma, eps, phizero, beta) * rigid_sphere_omega(T, l, r, m, sigma, nokt)
        else:
            return omega_dimless_IPL(T, l, sigma, eps, phizero, beta)
    elif model == 'VSS' and l == r and (l == 1 or l == 2):
        if l == 1:
            if dimensional is True:
                return omega_vss(T, l, m, vssc_11, vsso_11, nokt)
            else:
                return omega_vss(T, l, m, vssc_11, vsso_11, nokt) / rigid_sphere_omega(T, l, r, m, sigma, nokt)
        elif l == 2:
            if dimensional is True:
                return omega_vss(T, l, m, vssc_22, vsso_22, nokt)
            else:
                return omega_vss(T, l, m, vssc_22, vsso_22, nokt) / rigid_sphere_omega(T, l, r, m, sigma, nokt)
    else:
        raise KineticlibError('Cannot calculate the Omega^{(' + str(l) + ',' + str(r)
                              + ')} integral using the' + model +'potentail')