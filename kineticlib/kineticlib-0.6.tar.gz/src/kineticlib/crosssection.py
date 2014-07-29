"""Contains various elastic and inelastic crosssections and generalized omega integrals
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
from scipy import integrate
from .particles import Molecule, MoleculeSTS
from . import probabilities as prob
from .errors import KineticlibError


def diss_integral_rigid_sphere(T: float, deg: int, idata: np.ndarray, molecule: Molecule, i: int,
                               center_of_mass: bool=True, vl_dependent: bool=True, nokt: bool=False) -> float:
    """Calculates the generalized dissociation omega integral either using the rigid sphere model or the rigid sphere
    model depending on the relative energy along the center-of-mass line

    Parameters
    ----------
    T : float
        the temperature of the mixture
    deg : int
        the degree of the omega integral
    idata : 1-D array-like
        the array of interaction data
    molecule : Molecule
        the molecule which dissociates
    i : int
        the vibrational level from which the molecule dissociates
    center_of_mass : bool, optional
        if True, the kinetic energy of the collision partners will be calculated along the center-of-mass line,
        if False, the total kinetic energy will be used, defaults to True
    vl_dependent : bool, optional
        if True, the dissociation crosssection takes into account the vibrational energy of the dissociating molecule,
        if False, the crosssection is independent of the vibrational energy, defaults to True
    nokt : bool, optional
        if True, the result will be multiplied by :math:`\\sqrt{(1 / kT)}`, defaults to True

    Returns
    -------
    float
        The generalized omega integral over the dissociation crosssection

    Raises
    ------
    KineticlibError
        if `deg > 1`
    """
    if nokt is False:
        multiplier = constants.pi * (idata[1] ** 2) * ((constants.k * T / (2 * constants.pi * idata[0])) ** 0.5)
    else:
        multiplier = constants.pi * (idata[1] ** 2) * ((0.5 / (constants.pi * idata[0])) ** 0.5)
    if vl_dependent is True:
        min_sq = (molecule.diss - molecule.vibr[i]) / (constants.k * T)
    else:
        min_sq = molecule.diss / (constants.k * T)
    if deg == 0:
        if center_of_mass is False:
            return 0.5 * multiplier * np.exp(-min_sq)
        else:
            return multiplier * 0.5 * (min_sq + 1.0) * np.exp(-min_sq)
    elif deg == 1:
        if center_of_mass is False:
            return 0.5 * multiplier * (min_sq + 2.0) * np.exp(-min_sq)
        else:
            return multiplier * 0.5 * ((min_sq ** 2) + 2.0 * min_sq + 1.0) * np.exp(-min_sq)  # re-check!
    else:
        raise KineticlibError('Cannot calculated generalized dissociation omega integral of degree ' + str(deg))


def elastic_integral(T: float, deg: int, idata: np.ndarray, rig_sphere: bool=False, nokt: bool=False) -> float:
    """Calculates the generalized elastic omega integral either using the rigid sphere model or the VSS model

    Parameters
    ----------
    T : float
        the temperature of the mixture
    deg : int
        the degree of the omega integral
    idata : 1-D array-like
        the array of interaction data
    molecule : Molecule
        the molecule which dissociates
    rig_sphere : bool, optional
        if True, the the rigid sphere model is used for the crosssection, if False, the VSS model is used, defaults to
        False
    nokt : bool, optional
        if True, the result will be multiplied by :math:`\\sqrt{(1 / kT)}`, defaults to True

    Returns
    -------
    float
        The generalized omega integral over the elastic crosssection
    """
    if rig_sphere is False:
        if nokt is False:
            multiplier = idata[9] * ((T * constants.k / (2.0 * constants.pi * idata[0])) ** 0.5) * (T ** (-idata[10]))
        else:
            multiplier = idata[9] * ((0.5 / (constants.pi * idata[0])) ** 0.5) * (T ** (-idata[10]))
        return 0.5 * gamma(2.0 - idata[10] + deg) * (constants.physical_constants['Angstrom star'][0] ** 2) * multiplier
    else:
        if nokt is False:
            multiplier = ((T * constants.k / (2.0 * constants.pi * idata[0])) ** 0.5)
        else:
            multiplier = ((0.5 / (constants.pi * idata[0])) ** 0.5)
        if deg == 0:
            return multiplier * 0.25 * constants.pi * (idata[1] ** 2)
        else:
            return 0.0


def elastic_crosssection(g: float, deg: int, vsso: float) -> float:
    """Calculates the velocity-dependent part of the generalized elastic omega integral for the VSS model

    Parameters
    ----------
    g : float
        the dimensionless relative velocity of the particles
    deg : int
        the degree of the omega integral
    vsso : float
        the omega parameter in the VSS model

    Returns
    -------
    float
        The velocity-dependent part of the generalized omega integral
    """
    return np.exp(-(g ** 2)) * (g ** (3 + 2 * (deg - vsso)))


def vt_integral(T: float, deg: int, idata: np.ndarray, molecule: MoleculeSTS, i: int, delta: int,
                nokt: bool=False) -> float:
    """Calculates the generalized VT omega integral using the FHO probability and VSS cross-section models
    for the following process: M(i) + P -> M(i + delta) + P

    Parameters
    ----------
    T : float
        the temperature of the mixture
    deg : int
        the degree of the omega integral
    idata : 1-D array-like
        the array of interaction data
    molecule : MoleculeSTS or Molecule
        the molecule which undergoes the VT transition
    i : int
        the vibrational level of the molecule
    delta : int
        the change in vibrational level of the molecule
    nokt : bool, optional
        if True, the result will be multiplied by :math:`\\sqrt{(1 / kT)}`, defaults to True

    Returns
    -------
    float
        The generalized omega integral over the VT crosssection

    Raises
    ------
    KineticlibError
        if `delta == 0`
    
    """
    if delta != 0:
        f = lambda g: prob.vt_prob_g_only(g, T, idata, molecule.vibr, i, delta, molecule.vibr_zero + molecule.diss) \
                      * elastic_crosssection(g, deg, idata[10])
        if delta == 1:
            mult = (i + 1)
        elif delta == -1:
            mult = i
        elif delta > 0:
            mult = prob.fact_div_fact(i, i + delta) / (factorial(delta) ** 2)
        else:
            mult = prob.fact_div_fact(i + delta, i) / (factorial(-delta) ** 2)
        if nokt is False:
            return mult * (constants.physical_constants['Angstrom star'][0] ** 2) * idata[9]\
                        * ((T * constants.k / (2.0 * constants.pi * idata[0])) ** 0.5) * (T ** (-idata[10]))\
                        * integrate.quad(f, 0, np.inf)[0]
        else:
            return mult * (constants.physical_constants['Angstrom star'][0] ** 2) * idata[9]\
                        * ((0.5 / (constants.pi * idata[0])) ** 0.5) * (T ** (-idata[10]))\
                        * integrate.quad(f, 0, np.inf)[0]
    else:
        raise KineticlibError('VT transition with no change in vibrational level specified')


def vv_integral(T: float, deg: int, idata: np.ndarray, molecule1: MoleculeSTS, molecule2: MoleculeSTS, i: int,
                k: int, i_delta: int, nokt=False) -> float:
    """Calculates the generalized VV omega integral using the FHO probability and VSS cross-section models
    for the following process: M1(i) + M2(k) -> M1(i + i_delta) + M2(k - i_delta)

    Parameters
    ----------
    T : float
        the temperature of the mixture
    deg : int
        the degree of the omega integral
    idata : 1-D array-like
        the array of interaction data
    molecule1 : MoleculeSTS or Molecule
        the first molecule which undergoes the VV transition
    molecule2 : MoleculeSTS or Molecule
        the second molecule which undergoes the VV transition
    i : int
        the vibrational level of molecule1
    k : int
        the vibrational level of molecule2
    i_delta : int
        the change in vibrational level of the first molecule
    nokt : bool, optional
        if True, the result will be multiplied by :math:`\\sqrt{(1 / kT)}`, defaults to True

    Returns
    -------
    float
        The generalized omega integral over the VV crosssection

    Raises
    ------
    KineticlibError
        if `i_delta == 0`
    
    """
    if i_delta != 0:
        f = lambda g: prob.vv_prob_g_only(g, T, idata, molecule1.vibr, molecule2.vibr, i, k, i_delta) \
                      * elastic_crosssection(g, deg, idata[10])
        if i_delta == 1:
            mult = (i + 1) * k
        elif i_delta == -1:
            mult = i * (k + 1)
        elif i_delta > 0:
            mult = prob.fact_div_fact(i, i + i_delta) * prob.fact_div_fact(k - i_delta, k) / (factorial(i_delta) ** 2)
        else:
            mult = prob.fact_div_fact(i + i_delta, i) * prob.fact_div_fact(k, k - i_delta) / (factorial(-i_delta) ** 2)
        if nokt is False:
            return mult * (constants.physical_constants['Angstrom star'][0] ** 2) * idata[9]\
                        * ((T * constants.k / (2.0 * constants.pi * idata[0])) ** 0.5) * (T ** (-idata[10]))\
                        * integrate.quad(f, 0, np.inf)[0]
        else:
            return mult * (constants.physical_constants['Angstrom star'][0] ** 2) * idata[9]\
                        * ((0.5 / (constants.pi * idata[0])) ** 0.5) * (T ** (-idata[10]))\
                        * integrate.quad(f, 0, np.inf)[0]
    else:
        raise KineticlibError('VV transition with no change in vibrational level specified')


def vv_collisions(T: float, T1_1: float, T1_2: float, idata: np.ndarray, molecule1: Molecule, molecule2: Molecule,
                  nokt: bool=False) -> np.ndarray:
    """Calculates the averaging :math:`\\left<F \\right>^{VV}_{cd}` over all one-quantum VV crosssections of the type
    M1(i) + M2(k) -> M1(i + i_delta) + M2(k - i_delta) (using the FHO probability and VSS crosssection)
    of the following quantities:
        0. :math:`\\left(\\Delta \\mathcal{E}^{vibr}_{c}\\right)^{2}`
        #. :math:`\\left(\\Delta \\mathcal{E}^{vibr}_{d}\\right)^{2}`
        #. :math:`\\Delta \\mathcal{E}^{vibr}_{c} \\mathcal{E}^{vibr}_{d}`
        #. :math:`\\Delta i \\Delta \\mathcal{E}^{vibr}_{c}`
        #. :math:`\\Delta i \\Delta \\mathcal{E}^{vibr}_{d}`
        #. :math:`\\Delta k \\Delta \\mathcal{E}^{vibr}_{c}`
        #. :math:`\\Delta k \\Delta \\mathcal{E}^{vibr}_{d}`
        #. :math:`\\Delta \\mathcal{E}^{vibr}_{c}`
        #. :math:`\\Delta \\mathcal{E}^{vibr}_{d}`
        #. :math:`\\left(\\Delta i \\right)^{2}`
        #. :math:`\\left(\\Delta k \\right)^{2}`
        #. :math:`\\Delta i \\Delta k`
        #. :math:`\\Delta i`

    Parameters
    ----------
    T : float
        the temperature of the mixture
    T1_1 : float
        the temperature of the first vibrational level of the first molecule
    T1_2 : float
        the temperature of the first vibrational level of the second molecule
    deg : int
        the degree of the omega integral
    idata : 1-D array-like
        the array of interaction data
    molecule1 : MoleculeSTS or Molecule
        the first molecule which undergoes the VV transition
    molecule2 : MoleculeSTS or Molecule
        the second molecule which undergoes the VV transition
    i : int
        the vibrational level of molecule1
    k : int
        the vibrational level of molecule2
    i_delta : int
        the change in vibrational level of the first molecule
    nokt : bool, optional
        if True, the result will be multiplied by :math:`\\sqrt{(1 / kT)}`, defaults to True

    Returns
    -------
    np.ndarray
        An array containing the averaged quantities listed above (in the same order)
    
    """
    result = np.zeros(12)
    Z = molecule1.Z_vibr(T, T1_1) * molecule2.Z_vibr(T, T1_2)

    a = np.arange(0, molecule1.num_vibr + 1)
    b = np.arange(0, molecule2.num_vibr + 1)

    vibr_energy = molecule1.vibr[a] / (constants.k * T)
    vibr_energy2 = molecule2.vibr_energy(b) / (constants.k * T)
    vibr_exp = molecule1.vibr_exp(a, T, T1_1)
    vibr_exp2 = molecule2.vibr_exp(b, T, T1_2)

    for k in range(molecule2.num_vibr):
        for i in range(molecule1.num_vibr):
            cs = vv_integral(T, 0, idata, molecule1, molecule2, i, k + 1, 1, nokt)
            result[0] += ((vibr_energy[i] - vibr_energy[i + 1]) ** 2) * vibr_exp[i] * vibr_exp2[k + 1] * cs
            result[1] += ((vibr_energy2[k + 1] - vibr_energy2[k]) ** 2) * vibr_exp[i] * vibr_exp2[k + 1] * cs
            result[2] += ((vibr_energy[i + 1] - vibr_energy[i]) * (vibr_energy2[k] - vibr_energy2[k + 1]))\
                * vibr_exp[i] * vibr_exp2[k + 1] * cs
            result[3] += (vibr_energy[i + 1] - vibr_energy[i]) * vibr_exp[i] * vibr_exp2[k + 1] * cs
            result[4] += (vibr_energy2[k] - vibr_energy2[k + 1]) * vibr_exp[i] * vibr_exp2[k + 1] * cs
            result[5] -= (vibr_energy[i + 1] - vibr_energy[i]) * vibr_exp[i] * vibr_exp2[k + 1] * cs
            result[6] -= (vibr_energy2[k] - vibr_energy2[k + 1]) * vibr_exp[i] * vibr_exp2[k + 1] * cs
            result[7] += (vibr_energy[i + 1] - vibr_energy[k + 1]) * vibr_exp[i] * vibr_exp2[k + 1] * cs
            result[8] += (vibr_energy2[k] - vibr_energy2[k + 1]) * vibr_exp[i] * vibr_exp2[k + 1] * cs
            result[9] += vibr_exp[i] * vibr_exp2[k + 1] * cs  # i, k -> i + 1, k - 1
            result[10] -= vibr_exp[i] * vibr_exp2[k + 1] * cs
            result[11] += vibr_exp[i] * vibr_exp2[k + 1] * cs

            cs = vv_integral(T, 0, idata, molecule1, molecule2, i + 1, k, -1, nokt)
            result[0] += ((vibr_energy[i] - vibr_energy[i + 1]) ** 2)\
                * vibr_exp[i + 1] * vibr_exp2[k] * cs  # <Ev_i^2>
            result[1] += ((vibr_energy2[k] - vibr_energy2[k + 1]) ** 2)\
                * vibr_exp[i + 1] * vibr_exp2[k] * cs  # <Ev_k^2>
            result[2] += ((vibr_energy[i] - vibr_energy[i + 1]) * (vibr_energy2[k + 1] - vibr_energy2[k]))\
                * vibr_exp[i + 1] * vibr_exp2[k] * cs  # <Ev_i Ev_k>
            result[3] -= (vibr_energy[i] - vibr_energy[i + 1]) * vibr_exp[i + 1] * vibr_exp2[k] * cs  # <i * Ev_i>
            result[4] -= (vibr_energy2[k + 1] - vibr_energy2[k]) * vibr_exp[i + 1] * vibr_exp2[k] * cs  # <i Ev_k>
            result[5] += (vibr_energy[i] - vibr_energy[i + 1]) * vibr_exp[i + 1] * vibr_exp2[k] * cs
            result[6] += (vibr_energy2[k + 1] - vibr_energy2[k]) * vibr_exp[i + 1] * vibr_exp2[k] * cs
            result[7] += (vibr_energy[i] - vibr_energy[i + 1]) * vibr_exp[i + 1] * vibr_exp2[k] * cs  # <Ev_i>
            result[8] += (vibr_energy2[k + 1] - vibr_energy2[k]) * vibr_exp[i + 1] * vibr_exp2[k] * cs  # <Ev_k>
            result[9] += vibr_exp[i + 1] * vibr_exp2[k] * cs  # <i ^ 2>
            result[10] -= vibr_exp[i + 1] * vibr_exp2[k] * cs  # <i k>
            result[11] -= vibr_exp[i + 1] * vibr_exp2[k] * cs  # <i>

    return result / Z


def dE_rot_sq(T: float, idata: np.ndarray, molecule: MoleculeSTS, full_integral: bool=True, nokt: bool=False) -> float:
    """Calculates either the partial averaging of the squared change in rotational energy
    :math:`\\left<\\left(\\Delta \\mathcal{E}^{rot}_{c}\\right)^{2}\\right>_{part}`
    or the full averaging of the same quantity :math:`\\left<\\left(\\Delta \\mathcal{E}^{rot}_{c}\\right)^{2}\\right>`

    Parameters
    ----------
    T : float
        the temperature of the mixture
    idata : 1-D array-like
        the array of interaction data
    molecule : MoleculeSTS or Molecule
        the molecule which undergoes the rotational energy transition
    full_integral : bool
        if True, the full averaging is calculated, if false, the partial averaging is calculated, defaults to True
    nokt : bool, optional
        if True and full_integral is True, the result will be multiplied by :math:`\\sqrt{(1 / kT)}`, defaults to True

    Returns
    -------
    float
        The calculated averaging
    """
    f = lambda j: (2 * molecule.rot_energy(j) * molecule.rot_energy(j + 1)
                   + molecule.rot_energy(j) ** 2
                   + molecule.rot_energy(j + 1) ** 2) * molecule.rot_exp(j, T)
    tmp = integrate.quad(f, 0, molecule.num_rot - 1)[0]
    f = lambda j: (2 * molecule.rot_energy(j) * molecule.rot_energy(j - 1)
                   + molecule.rot_energy(j) ** 2
                   + molecule.rot_energy(j - 1) ** 2) * molecule.rot_exp(j, T)
    tmp += integrate.quad(f, 1, molecule.num_rot)[0]
    if full_integral is False:
        return tmp * 0.5 / (molecule.Z_rot(T) * ((constants.k * T) ** 2) * molecule.num_rot)
    else:
        return tmp * 0.5 / (molecule.Z_rot(T) * ((constants.k * T) ** 2) * molecule.num_rot)\
               * elastic_integral(T, 0, idata, nokt=nokt)


def dE_rot_single(T: float, idata: np.ndarray, molecule: MoleculeSTS, full_integral: bool=True, nokt: bool=False) -> float:
    """Calculates either the partial averaging of the squared change in rotational energy
    :math`\\left<\\Delta \\mathcal{E}^{rot}_{c}\\right>_{part}`
    or the full averaging of the same quantity :math:`\\left<\\Delta \\mathcal{E}^{rot}_{c}\\right>`

    Parameters
    ----------
    T : float
        the temperature of the mixture
    idata : 1-D array-like
        the array of interaction data
    molecule : MoleculeSTS or Molecule
        the molecule which undergoes the rotational energy transition
    full_integral : bool
        if True, the full averaging is calculated, if false, the partial averaging is calculated, defaults to True
    nokt : bool, optional
        if True and full_integral is True, the result will be multiplied by :math:`\\sqrt{(1 / kT)}`, defaults to True

    Returns
    -------
    float
        The calculated averaging
    """
    f = lambda j: (molecule.rot_energy(j) - molecule.rot_energy(j + 1)) * molecule.rot_exp(j, T)
    tmp = integrate.quad(f, 0, molecule.num_rot - 1)[0]
    f = lambda j: (molecule.rot_energy(j) - molecule.rot_energy(j - 1)) * molecule.rot_exp(j, T)
    tmp += integrate.quad(f, 1, molecule.num_rot)[0]
    if full_integral is False:
        return tmp * 0.5 / (molecule.Z_rot(T) * constants.k * T * molecule.num_rot)
    else:
        return tmp * 0.5 / (molecule.Z_rot(T) * constants.k * T * molecule.num_rot) * elastic_integral(T, 0, idata,
                                                                                                       nokt=nokt)


def dE_rot_c_dE_rot_d(T: float, idata: np.ndarray, molecule1: MoleculeSTS, molecule2: MoleculeSTS,
                      full_integral: bool=True, nokt: bool=False) -> float:
    """Calculates either the partial averaging of the squared change in rotational energy
    :math:`\\left<\\Delta \\mathcal{E}^{rot}_{c}\\Delta \\mathcal{E}^{rot}_{d}\\right>_{part}`
    or the full averaging of the same quantity
    `\\left<\\Delta \\mathcal{E}^{rot}_{c}\\Delta \\mathcal{E}^{rot}_{d}\\right>`

    Parameters
    ----------
    T : float
        the temperature of the mixture
    idata : 1-D array-like
        the array of interaction data
    molecule1 : MoleculeSTS or Molecule
        the first molecule which undergoes the rotational energy transition
    molecule2 : MoleculeSTS or Molecule
        the second molecule which undergoes the rotational energy transition
    full_integral : bool
        if True, the full averaging is calculated, if false, the partial averaging is calculated, defaults to True
    nokt : bool, optional
        if True and full_integral is True, the result will be multiplied by :math:`\\sqrt{(1 / kT)}`, defaults to True

    Returns
    -------
    float
        The calculated averaging
    """
    return dE_rot_single(T, idata, molecule1, full_integral, nokt) * dE_rot_single(T, idata, molecule2, False)


def dE_rot_dE_rot_full(T: float, idata: np.ndarray, molecule1: MoleculeSTS, molecule2: MoleculeSTS,
                       full_integral: bool=True, nokt: bool=False) -> float:
    """Calculates either the partial averaging of the squared change in rotational energy
    :math:`\\left<\\Delta \\mathcal{E}^{rot}_{c}\\left(\\Delta \\mathcal{E}^{rot}_{c}
    + \\Delta \\mathcal{E}^{rot}_{d} \\right)\\right>_{part}`
    or the full averaging of the same quantity
    :math:`\\left<\\Delta \\mathcal{E}^{rot}_{c}\\left(\\Delta \\mathcal{E}^{rot}_{c}
    + \\Delta \\mathcal{E}^{rot}_{d} \\right)\\right>`

    Parameters
    ----------
    T : float
        the temperature of the mixture
    idata : 1-D array-like
        the array of interaction data
    molecule1 : MoleculeSTS or Molecule
        the first molecule which undergoes the rotational energy transition
    molecule2 : MoleculeSTS or Molecule
        the second molecule which undergoes the rotational energy transition
    full_integral : bool
        if True, the full averaging is calculated, if false, the partial averaging is calculated, defaults to True
    nokt : bool, optional
        if True and full_integral is True, the result will be multiplied by :math:`\\sqrt{(1 / kT)}`, defaults to True

    Returns
    -------
    float
        The calculated averaging
    """
    return dE_rot_sq(T, idata, molecule1, full_integral, nokt)\
           + dE_rot_single(T, idata, molecule1, full_integral, nokt) * dE_rot_single(T, idata, molecule2, False)