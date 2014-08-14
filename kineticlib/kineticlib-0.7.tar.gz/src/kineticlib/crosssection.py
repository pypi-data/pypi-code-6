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


def diss_integral_rigid_sphere(T: float, deg: int, idata: np.ndarray, molecule: MoleculeSTS, i: int,
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
        if True, the result will be multiplied by :math:`\\sqrt{(1 / kT)}`, defaults to False

    Returns
    -------
    float
        The generalized omega integral over the dissociation crosssection

    Raises
    ------
    KineticlibError
        if `deg > 1`
    """
    return raw_diss_integral_rigid_sphere(T, deg, idata, molecule.vibr[i], molecule.diss, center_of_mass,
                                          vl_dependent, nokt)


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
        if True, the result will be multiplied by :math:`\\sqrt{(1 / kT)}`, defaults to False

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
        return 0.5 * multiplier * constants.pi * gamma(0.5 * deg + 2.0) * (idata[1] ** 2)


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
        if True, the result will be multiplied by :math:`\\sqrt{(1 / kT)}`, defaults to False

    Returns
    -------
    float
        The generalized omega integral over the VT crosssection

    Raises
    ------
    KineticlibError
        if `delta == 0`
    
    """
    return raw_vt_integral(T, deg, idata, molecule.vibr, molecule.vibr_zero, molecule.diss, i, delta, nokt)


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
        if True, the result will be multiplied by :math:`\\sqrt{(1 / kT)}`, defaults to False

    Returns
    -------
    float
        The generalized omega integral over the VV crosssection

    Raises
    ------
    KineticlibError
        if `i_delta == 0`
    
    """
    return raw_vv_integral(T, deg, idata, molecule1.vibr, molecule2.vibr, i, k, i_delta, nokt)


def vv_collisions(T: float, T1_1: float, T1_2: float, idata: np.ndarray, molecule1: Molecule, molecule2: Molecule,
                  nokt: bool=False) -> np.ndarray:
    """Calculates the averaging :math:`\\left<F \\right>^{VV}_{cd}` over all one-quantum VV crosssections of the type
    M1(i) + M2(k) -> M1(i + i_delta) + M2(k - i_delta), (`i_delta = 1` or `i_delta = -1`) of the following quantities:

        0. :math:`\\left(\\Delta\\mathcal{E}_{c} \\right)^2`
        #. :math:`\\left(\\Delta\\mathcal{E}_{d} \\right)^2`
        #. :math:`\\Delta\\mathcal{E}_{c}\\Delta\\mathcal{E}_{d}`
        #. :math:`\\Delta i \\Delta\\mathcal{E}_{c}`
        #. :math:`\\Delta i \\Delta\\mathcal{E}_{d}`
        #. :math:`\\Delta k \\Delta\\mathcal{E}_{c}`
        #. :math:`\\Delta k \\Delta\\mathcal{E}_{d}`
        #. :math:`\\Delta\\mathcal{E}_{c}`
        #. :math:`\\Delta\\mathcal{E}_{d}`
        #. :math:`\\left(\\Delta i \\right)^{2}`
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
        if True, the result will be multiplied by :math:`\\sqrt{(1 / kT)}`, defaults to False

    Returns
    -------
    np.ndarray
        An array containing the averaged quantities listed above (in the same order)
    
    """
    a = np.arange(0, molecule1.num_vibr_levels(T, T1_1, True) + 1)
    b = np.arange(0, molecule2.num_vibr_levels(T, T1_2, True) + 1)
    vibr_exp = molecule1.vibr_exp(a, T, T1_1)
    vibr_exp2 = molecule2.vibr_exp(b, T, T1_2)
    return raw_vv_collisions(T, idata, molecule1.Z_vibr(T, T1_1), molecule2.Z_vibr(T, T1_2),
                             molecule1.vibr, molecule2.vibr, vibr_exp, vibr_exp2,
                             molecule1.num_vibr, molecule2.num_vibr, nokt)


def dE_rot_sq(T: float, idata: np.ndarray, molecule: MoleculeSTS, full_integral: bool=True, nokt: bool=False) -> float:
    """Calculates either the partial averaging of the squared change in rotational energy
    over all one-quantum rotational transitions
    :math:`\\left<\\left(\\Delta \\mathcal{E}^{rot}_{c}\\right)^{2}\\right>_{part}`
    or the full averaging of the same quantity :math:`\\left<\\left(\\Delta \\mathcal{E}^{rot}_{c}\\right)^{2}\\right>`,
    considering all one-quantum transitions to be equiprobable

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
        if True and full_integral is True, the result will be multiplied by :math:`\\sqrt{(1 / kT)}`, defaults to False

    Returns
    -------
    float
        The calculated averaging
    """
    return raw_dE_rot_sq(T, idata, molecule.Z_rot(T), molecule.rot_symmetry, molecule.rot_const, molecule.num_rot,
                         full_integral, nokt)


def dE_rot_single(T: float, idata: np.ndarray, molecule: MoleculeSTS, full_integral: bool=True,
                  nokt: bool=False) -> float:
    """Calculates either the partial averaging of the squared change in rotational energy
    over all one-quantum rotational transitions
    :math:`\\left<\\Delta \\mathcal{E}^{rot}_{c}\\right>_{part}`
    or the full averaging of the same quantity :math:`\\left<\\Delta \\mathcal{E}^{rot}_{c}\\right>`,
    considering all one-quantum transitions to be equiprobable

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
        if True and full_integral is True, the result will be multiplied by :math:`\\sqrt{(1 / kT)}`, defaults to False

    Returns
    -------
    float
        The calculated averaging
    """
    return raw_dE_rot_single(T, idata, molecule.Z_rot(T), molecule.rot_symmetry, molecule.rot_const, molecule.num_rot,
                             full_integral, nokt)


def dE_rot_c_dE_rot_d(T: float, idata: np.ndarray, molecule1: MoleculeSTS, molecule2: MoleculeSTS,
                      full_integral: bool=True, nokt: bool=False) -> float:
    """Calculates either the partial averaging of the squared change in rotational energy
    over all one-quantum rotational transitions
    :math:`\\left<\\Delta \\mathcal{E}^{rot}_{c}\\Delta \\mathcal{E}^{rot}_{d}\\right>_{part}`
    or the full averaging of the same quantity
    :math:`\\left<\\Delta \\mathcal{E}^{rot}_{c}\\Delta \\mathcal{E}^{rot}_{d}\\right>`,
    considering all one-quantum transitions to be equiprobable

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
        if True and full_integral is True, the result will be multiplied by :math:`\\sqrt{(1 / kT)}`, defaults to False

    Returns
    -------
    float
        The calculated averaging
    """
    return raw_dE_rot_c_dE_rot_d(T, idata, molecule1.Z_rot(T), molecule2.Z_rot(T), molecule1.rot_symmetry,
                                 molecule2.rot_symmetry, molecule1.rot_const, molecule2.rot_const, molecule1.num_rot,
                                 molecule2.num_rot, full_integral, nokt)


def dE_rot_dE_rot_full(T: float, idata: np.ndarray, molecule1: MoleculeSTS, molecule2: MoleculeSTS,
                       full_integral: bool=True, nokt: bool=False) -> float:
    """Calculates either the partial averaging of the squared change in rotational energy
    over all one-quantum rotational transitions
    :math:`\\left<\\Delta \\mathcal{E}^{rot}_{c}\\left(\\Delta \\mathcal{E}^{rot}_{c}
    + \\Delta \\mathcal{E}^{rot}_{d} \\right)\\right>_{part}`
    or the full averaging of the same quantity
    :math:`\\left<\\Delta \\mathcal{E}^{rot}_{c}\\left(\\Delta \\mathcal{E}^{rot}_{c}
    + \\Delta \\mathcal{E}^{rot}_{d} \\right)\\right>`,
    considering all one-quantum transitions to be equiprobable

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
        if True and full_integral is True, the result will be multiplied by :math:`\\sqrt{(1 / kT)}`, defaults to False

    Returns
    -------
    float
        The calculated averaging
    """
    return raw_dE_rot_dE_rot_full(T, idata, molecule1.Z_rot(T), molecule2.Z_rot(T), molecule1.rot_symmetry,
                                  molecule2.rot_symmetry, molecule1.rot_const, molecule2.rot_const, molecule1.num_rot,
                                  molecule2.num_rot, full_integral, nokt)


def raw_diss_integral_rigid_sphere(T: float, deg: int, idata: np.ndarray, molecule_vibr: float,
                                   molecule_diss: float, center_of_mass: bool=True, vl_dependent: bool=True,
                                   nokt: bool=False) -> float:
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
    molecule_vibr : float
        the dimensional vibrational energy of the level from which the molecule dissociates
    molecule_diss : float
        the dissociation energy of the molecule which dissociates
    center_of_mass : bool, optional
        if True, the kinetic energy of the collision partners will be calculated along the center-of-mass line,
        if False, the total kinetic energy will be used, defaults to True
    vl_dependent : bool, optional
        if True, the dissociation crosssection takes into account the vibrational energy of the dissociating molecule,
        if False, the crosssection is independent of the vibrational energy, defaults to True
    nokt : bool, optional
        if True, the result will be multiplied by :math:`\\sqrt{(1 / kT)}`, defaults to False

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
        min_sq = (molecule_diss - molecule_vibr) / (constants.k * T)
    else:
        min_sq = molecule_diss / (constants.k * T)
    if deg == 0:
        if center_of_mass is False:
            return 0.5 * multiplier * np.exp(-min_sq)
        else:
            return multiplier * 0.5 * (min_sq + 1.0) * np.exp(-min_sq)
    elif deg == 1:
        if center_of_mass is False:
            return 0.5 * multiplier * (min_sq + 2.0) * np.exp(-min_sq)
        else:
            return multiplier * 0.5 * ((min_sq ** 2) + 2.0 * min_sq + 1.0) * np.exp(-min_sq)
    else:
        raise KineticlibError('Cannot calculated generalized dissociation omega integral of degree ' + str(deg))


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


def raw_vt_integral(T: float, deg: int, idata: np.ndarray, molecule_vibr_array: np.ndarray, molecule_vibr_zero: float,
                    molecule_diss: float, i: int, delta: int,
                    nokt: bool=False) -> float:
    """Calculates the generalized VT omega integral using the FHO probability and VSS cross-section models
    for the following process: M(i) + P -> M(i + delta) + P, *raw* version

    Parameters
    ----------
    T : float
        the temperature of the mixture
    deg : int
        the degree of the omega integral
    idata : 1-D array-like
        the array of interaction data
    molecule_vibr_array : 1-D array-like
        the array of vibrational energies of the molecule undergoing the VT transition
    molecule_vibr_zero : float
        the energy of the 0-th vibrational level
    molecule_diss : float
        the dissociation energy of the molecule which undergoes the transition
    i : int
        the vibrational level of the molecule
    delta : int
        the change in vibrational level of the molecule
    nokt : bool, optional
        if True, the result will be multiplied by :math:`\\sqrt{(1 / kT)}`, defaults to False

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
        f = lambda g: prob.vt_prob_g_only(g, T, idata, molecule_vibr_array, i, delta,
                                          molecule_vibr_zero + molecule_diss) * elastic_crosssection(g, deg, idata[10])
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


def raw_vv_integral(T: float, deg: int, idata: np.ndarray, molecule_vibr_array1: np.ndarray,
                    molecule_vibr_array2: np.ndarray, i: int, k: int, i_delta: int, nokt=False) -> float:
    """Calculates the generalized VV omega integral using the FHO probability and VSS cross-section models
    for the following process: M1(i) + M2(k) -> M1(i + i_delta) + M2(k - i_delta), *raw* version

    Parameters
    ----------
    T : float
        the temperature of the mixture
    deg : int
        the degree of the omega integral
    idata : 1-D array-like
        the array of interaction data
    molecule_vibr_array1 : 1-D array-like
        the array of vibrational energies of the molecule M1
    molecule_vibr_array2 : 1-D array-like
        the array of vibrational energies of the molecule M2
    i : int
        the vibrational level of molecule1
    k : int
        the vibrational level of molecule2
    i_delta : int
        the change in vibrational level of the first molecule
    nokt : bool, optional
        if True, the result will be multiplied by :math:`\\sqrt{(1 / kT)}`, defaults to False

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
        f = lambda g: prob.vv_prob_g_only(g, T, idata, molecule_vibr_array1, molecule_vibr_array2, i, k, i_delta) \
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


def raw_vv_collisions(T: float, idata: np.ndarray, Z_vibr1: float, Z_vibr2: float,
                      molecule_vibr_array1: np.ndarray, molecule_vibr_array2: np.ndarray,
                      molecule_vibr_exp_array1: np.ndarray, molecule_vibr_exp_array2: np.ndarray,
                      molecule_num_vibr1: int, molecule_num_vibr2: int,
                      nokt: bool=False) -> np.ndarray:
    """Calculates the averaging :math:`\\left<F \\right>^{VV}_{cd}` over all one-quantum VV crosssections of the type
    M1(i) + M2(k) -> M1(i + i_delta) + M2(k - i_delta), (`i_delta = 1` or `i_delta = -1`) of the following quantities:

        0. :math:`\\left(\\Delta\\mathcal{E}_{c} \\right)^2`
        #. :math:`\\left(\\Delta\\mathcal{E}_{d} \\right)^2`
        #. :math:`\\Delta\\mathcal{E}_{c}\\Delta\\mathcal{E}_{d}`
        #. :math:`\\Delta i \\Delta\\mathcal{E}_{c}`
        #. :math:`\\Delta i \\Delta\\mathcal{E}_{d}`
        #. :math:`\\Delta k \\Delta\\mathcal{E}_{c}`
        #. :math:`\\Delta k \\Delta\\mathcal{E}_{d}`
        #. :math:`\\Delta\\mathcal{E}_{c}`
        #. :math:`\\Delta\\mathcal{E}_{d}`
        #. :math:`\\left(\\Delta i \\right)^{2}`
        #. :math:`\\Delta i \\Delta k`
        #. :math:`\\Delta i`

    *raw* version

    Parameters
    ----------
    T : float
        the temperature of the mixture
    deg : int
        the degree of the omega integral
    idata : 1-D array-like
        the array of interaction data
    Z_vibr1 : float
        the value of the vibrational partition function of the molecule M1
    Z_vibr2 : float
        the value of the vibrational partition function of the molecule M2
    molecule_vibr_array1 : 1-D array-like
        the array of vibrational energies of the molecule M1
    molecule_vibr_array2 : 1-D array-like
        the array of vibrational energies of the molecule M2
    molecule_vibr_exp_array1 : 1-D array-like
        the array of vibrational exponents of the molecule M1
    molecule_vibr_exp_array2 : 1-D array-like
        the array of vibrational exponents of the molecule M2
    molecule_num_vibr1 : int
        the number of vibrational levels of molecule M1
    molecule_num_vibr2 : int
        the number of vibrational levels of molecule M2
    i : int
        the vibrational level of molecule1
    k : int
        the vibrational level of molecule2
    i_delta : int
        the change in vibrational level of the first molecule
    nokt : bool, optional
        if True, the result will be multiplied by :math:`\\sqrt{(1 / kT)}`, defaults to False

    Returns
    -------
    np.ndarray
        An array containing the averaged quantities listed above (in the same order)

    """
    result = np.zeros(12)
    Z = Z_vibr1 * Z_vibr2

    for k in range(molecule_num_vibr2):
        for i in range(molecule_num_vibr1):
            cs = raw_vv_integral(T, 0, idata, molecule_vibr_array1, molecule_vibr_exp_array2, i, k + 1, 1, nokt)
            result[0] += ((molecule_vibr_array1[i] -
                           molecule_vibr_array1[i + 1]) ** 2) * molecule_vibr_exp_array1[i]\
                                                              * molecule_vibr_exp_array2[k + 1] * cs
            result[1] += ((molecule_vibr_array2[k + 1] -
                           molecule_vibr_array2[k]) ** 2) * molecule_vibr_exp_array1[i] \
                                                          * molecule_vibr_exp_array2[k + 1] * cs
            result[2] += ((molecule_vibr_array1[i + 1] - molecule_vibr_array1[i])
                          * (molecule_vibr_array2[k] - molecule_vibr_array2[k + 1])) * molecule_vibr_exp_array1[i]\
                                                                                     * molecule_vibr_exp_array2[k + 1]\
                                                                                     * cs
            result[3] += (molecule_vibr_array1[i + 1] - molecule_vibr_array1[i]) * molecule_vibr_exp_array1[i]\
                                                                                 * molecule_vibr_exp_array2[k + 1] * cs
            result[4] += (molecule_vibr_array2[k] -
                          molecule_vibr_array2[k + 1]) * molecule_vibr_exp_array1[i] \
                                                       * molecule_vibr_exp_array2[k + 1] * cs
            result[5] -= (molecule_vibr_array1[i + 1] -
                          molecule_vibr_array1[i]) * molecule_vibr_exp_array1[i] \
                                                   * molecule_vibr_exp_array2[k + 1] * cs
            result[6] -= (molecule_vibr_array2[k] -
                          molecule_vibr_array2[k + 1]) * molecule_vibr_exp_array1[i] \
                                                       * molecule_vibr_exp_array2[k + 1] * cs
            result[7] += (molecule_vibr_array1[i + 1] -
                          molecule_vibr_array1[i]) * molecule_vibr_exp_array1[i] \
                                                       * molecule_vibr_exp_array2[k + 1] * cs
            result[8] += (molecule_vibr_array2[k] -
                          molecule_vibr_array2[k + 1]) * molecule_vibr_exp_array1[i] \
                                                       * molecule_vibr_exp_array2[k + 1] * cs
            result[9] += molecule_vibr_exp_array1[i] * molecule_vibr_exp_array2[k + 1] * cs
            result[10] -= molecule_vibr_exp_array1[i] * molecule_vibr_exp_array2[k + 1] * cs
            result[11] += molecule_vibr_exp_array1[i] * molecule_vibr_exp_array2[k + 1] * cs

            cs = raw_vv_integral(T, 0, idata, molecule_vibr_array1, molecule_vibr_array2, i + 1, k, -1, nokt)
            result[0] += ((molecule_vibr_array1[i] - molecule_vibr_array1[i + 1]) ** 2)\
                * molecule_vibr_exp_array1[i + 1] * molecule_vibr_exp_array2[k] * cs
            result[1] += ((molecule_vibr_array2[k] - molecule_vibr_array2[k + 1]) ** 2)\
                * molecule_vibr_exp_array1[i + 1] * molecule_vibr_exp_array2[k] * cs
            result[2] += ((molecule_vibr_array1[i] - molecule_vibr_array1[i + 1])
                          * (molecule_vibr_array2[k + 1] -
                             molecule_vibr_array2[k]))\
                          * molecule_vibr_exp_array1[i + 1] * molecule_vibr_exp_array2[k] * cs
            result[3] -= (molecule_vibr_array1[i] -
                          molecule_vibr_array1[i + 1]) * molecule_vibr_exp_array1[i + 1] \
                                                       * molecule_vibr_exp_array2[k] * cs
            result[4] -= (molecule_vibr_array2[k + 1] -
                          molecule_vibr_array2[k]) * molecule_vibr_exp_array1[i + 1] \
                                                   * molecule_vibr_exp_array2[k] * cs
            result[5] += (molecule_vibr_array1[i] -
                          molecule_vibr_array1[i + 1]) * molecule_vibr_exp_array1[i + 1] \
                                                       * molecule_vibr_exp_array2[k] * cs
            result[6] += (molecule_vibr_array2[k + 1] -
                          molecule_vibr_array2[k]) * molecule_vibr_exp_array1[i + 1] \
                                                   * molecule_vibr_exp_array2[k] * cs
            result[7] += (molecule_vibr_array1[i] -
                          molecule_vibr_array1[i + 1]) * molecule_vibr_exp_array1[i + 1] \
                                                       * molecule_vibr_exp_array2[k] * cs
            result[8] += (molecule_vibr_array2[k + 1] -
                          molecule_vibr_array2[k]) * molecule_vibr_exp_array1[i + 1] \
                                                   * molecule_vibr_exp_array2[k] * cs
            result[9] += molecule_vibr_exp_array1[i + 1] * molecule_vibr_exp_array2[k] * cs
            result[10] -= molecule_vibr_exp_array1[i + 1] * molecule_vibr_exp_array2[k] * cs
            result[11] -= molecule_vibr_exp_array1[i + 1] * molecule_vibr_exp_array2[k] * cs

    return result / Z


def raw_dE_rot_sq(T: float, idata: np.ndarray, Z_rot: float, molecule_rot_symmetry: float, molecule_rot_const: float,
                  molecule_num_rot: int, full_integral: bool=True, nokt: bool=False) -> float:
    """Calculates either the partial averaging of the squared change in rotational energy
    over all one-quantum rotational transitions
    :math:`\\left<\\left(\\Delta \\mathcal{E}^{rot}_{c}\\right)^{2}\\right>_{part}`
    or the full averaging of the same quantity :math:`\\left<\\left(\\Delta \\mathcal{E}^{rot}_{c}\\right)^{2}\\right>`,
    considering all one-quantum transitions to be equiprobable, *raw* version

    Parameters
    ----------
    T : float
        the temperature of the mixture
    idata : 1-D array-like
        the array of interaction data
    Z_rot : float
        the value of the rotational partition function of the molecule
    molecule_rot_symmetry : float
        should equal 2.0 if the molecule is homonuclear and 1.0 otherwise
    molecule_rot_const : float
        The quantity :math:`h ^ 2 / (8 \\pi ^ 2 I_{rot,c})`, where :math:`I_{rot,c}` is the moment of rotational
        inertia of the molecule
    molecule_num_rot : int
        the amount of rotational levels in the molecule
    full_integral : bool
        if True, the full averaging is calculated, if false, the partial averaging is calculated, defaults to True
    nokt : bool, optional
        if True and full_integral is True, the result will be multiplied by :math:`\\sqrt{(1 / kT)}`, defaults to False

    Returns
    -------
    float
        The calculated averaging
    """
    f = lambda j: (2 * j * (j + 1) * molecule_rot_const * (j + 1) * (j + 2) * molecule_rot_const
                   + (j * (j + 1) * molecule_rot_const) ** 2
                   + ((j + 1) * (j + 2) * molecule_rot_const) ** 2)\
                  * ((2.0 * j + 1.0) / molecule_rot_symmetry)\
                  * np.exp(-j * (j + 1) * molecule_rot_const / (constants.k * T))
    tmp = integrate.quad(f, 0, molecule_num_rot - 1)[0]
    f = lambda j: (2 * j * (j + 1) * molecule_rot_const * (j - 1) * j * molecule_rot_const
                   + (j * (j + 1) * molecule_rot_const) ** 2
                   + ((j - 1) * j * molecule_rot_const) ** 2)\
                  * ((2.0 * j + 1.0) / molecule_rot_symmetry)\
                  * np.exp(-j * (j + 1) * molecule_rot_const / (constants.k * T))
    tmp += integrate.quad(f, 1, molecule_num_rot)[0]
    if full_integral is False:
        return tmp * 0.5 / (Z_rot * ((constants.k * T) ** 2) * molecule_num_rot)
    else:
        return tmp * 0.5 / (Z_rot * ((constants.k * T) ** 2) * molecule_num_rot)\
                   * elastic_integral(T, 0, idata, nokt=nokt)


def raw_dE_rot_single(T: float, idata: np.ndarray, Z_rot: float, molecule_rot_symmetry: float,
                      molecule_rot_const: float, molecule_num_rot: int, full_integral: bool=True,
                      nokt: bool=False) -> float:
    """Calculates either the partial averaging of the squared change in rotational energy
    over all one-quantum rotational transitions
    :math:`\\left<\\Delta \\mathcal{E}^{rot}_{c}\\right>_{part}`
    or the full averaging of the same quantity :math:`\\left<\\Delta \\mathcal{E}^{rot}_{c}\\right>`,
    considering all one-quantum transitions to be equiprobable, *raw* version

    Parameters
    ----------
    T : float
        the temperature of the mixture
    idata : 1-D array-like
        the array of interaction data
    Z_rot : float
        the value of the rotational partition function of the molecule
    molecule_rot_symmetry : float
        should equal 2.0 if the molecule is homonuclear and 1.0 otherwise
    molecule_rot_const : float
        The quantity :math:`h ^ 2 / (8 \\pi ^ 2 I_{rot,c})`, where :math:`I_{rot,c}` is the moment of rotational
        inertia of the molecule
    molecule_num_rot : int
        the amount of rotational levels in the molecule
    full_integral : bool
        if True, the full averaging is calculated, if false, the partial averaging is calculated, defaults to True
    nokt : bool, optional
        if True and full_integral is True, the result will be multiplied by :math:`\\sqrt{(1 / kT)}`, defaults to False

    Returns
    -------
    float
        The calculated averaging
    """
    f = lambda j: (j * (j + 1) * molecule_rot_const - (j + 1) * (j + 2) * molecule_rot_const)\
                  * ((2.0 * j + 1.0) / molecule_rot_symmetry)\
                  * np.exp(-j * (j + 1) * molecule_rot_const / (constants.k * T))
    tmp = integrate.quad(f, 0, molecule_num_rot - 1)[0]
    f = lambda j: (j * (j + 1) * molecule_rot_const - (j - 1) * j * molecule_rot_const)\
                  * ((2.0 * j + 1.0) / molecule_rot_symmetry)\
                  * np.exp(-j * (j + 1) * molecule_rot_const / (constants.k * T))
    tmp += integrate.quad(f, 1, molecule_num_rot)[0]
    if full_integral is False:
        return tmp * 0.5 / (Z_rot * constants.k * T * molecule_num_rot)
    else:
        return tmp * 0.5 / (Z_rot * constants.k * T * molecule_num_rot) * elastic_integral(T, 0, idata, nokt=nokt)


def raw_dE_rot_c_dE_rot_d(T: float, idata: np.ndarray, Z_rot1: float, Z_rot2: float, molecule_rot_symmetry1: float,
                          molecule_rot_symmetry2: float, molecule_rot_const1: float, molecule_rot_const2: float,
                          molecule_num_rot1: int, molecule_num_rot2: int, full_integral: bool=True,
                          nokt: bool=False) -> float:
    """Calculates either the partial averaging of the squared change in rotational energy
    over all one-quantum rotational transitions
    :math:`\\left<\\Delta \\mathcal{E}^{rot}_{c}\\Delta \\mathcal{E}^{rot}_{d}\\right>_{part}`
    or the full averaging of the same quantity
    :math:`\\left<\\Delta \\mathcal{E}^{rot}_{c}\\Delta \\mathcal{E}^{rot}_{d}\\right>`,
    considering all one-quantum transitions to be equiprobable, *raw* version

    Parameters
    ----------
    T : float
        the temperature of the mixture
    idata : 1-D array-like
        the array of interaction data
    Z_rot1 : float
        the value of the rotational partition function of the first molecule
    Z_rot2 : float
        the value of the rotational partition function of the second molecule
    molecule_rot_symmetry1 : float
        should equal 2.0 if the first molecule is homonuclear and 1.0 otherwise
    molecule_rot_symmetry2 : float
        should equal 2.0 if the second molecule is homonuclear and 1.0 otherwise
    molecule_rot_const1 : float
        The quantity :math:`h ^ 2 / (8 \\pi ^ 2 I_{rot,c})`, where :math:`I_{rot,c}` is the moment of rotational
        inertia of the first molecule
    molecule_rot_const2 : float
        The quantity :math:`h ^ 2 / (8 \\pi ^ 2 I_{rot,c})`, where :math:`I_{rot,c}` is the moment of rotational
        inertia of the second molecule
    molecule_num_rot1 : int
        the amount of rotational levels in the first molecule
    molecule_num_rot2 : int
        the amount of rotational levels in the second molecule
    full_integral : bool
        if True, the full averaging is calculated, if false, the partial averaging is calculated, defaults to True
    nokt : bool, optional
        if True and full_integral is True, the result will be multiplied by :math:`\\sqrt{(1 / kT)}`, defaults to False

    Returns
    -------
    float
        The calculated averaging
    """
    return raw_dE_rot_single(T, idata, Z_rot1, molecule_rot_symmetry1, molecule_rot_const1, molecule_num_rot1,
                             full_integral, nokt) * raw_dE_rot_single(T, idata, Z_rot2, molecule_rot_symmetry2,
                                                                      molecule_rot_const2, molecule_num_rot2, False,
                                                                      False)


def raw_dE_rot_dE_rot_full(T: float, idata: np.ndarray, Z_rot1: float, Z_rot2: float, molecule_rot_symmetry1: float,
                           molecule_rot_symmetry2: float, molecule_rot_const1: float, molecule_rot_const2: float,
                           molecule_num_rot1: int, molecule_num_rot2: int, full_integral: bool=True,
                           nokt: bool=False) -> float:
    """Calculates either the partial averaging of the squared change in rotational energy
    over all one-quantum rotational transitions
    :math:`\\left<\\Delta \\mathcal{E}^{rot}_{c}\\left(\\Delta \\mathcal{E}^{rot}_{c}
    + \\Delta \\mathcal{E}^{rot}_{d} \\right)\\right>_{part}`
    or the full averaging of the same quantity
    :math:`\\left<\\Delta \\mathcal{E}^{rot}_{c}\\left(\\Delta \\mathcal{E}^{rot}_{c}
    + \\Delta \\mathcal{E}^{rot}_{d} \\right)\\right>`,
    considering all one-quantum transitions to be equiprobable, *raw* version

    Parameters
    ----------
    T : float
        the temperature of the mixture
    idata : 1-D array-like
        the array of interaction data
    Z_rot1 : float
        the value of the rotational partition function of the first molecule
    Z_rot2 : float
        the value of the rotational partition function of the second molecule
    molecule_rot_symmetry1 : float
        should equal 2.0 if the first molecule is homonuclear and 1.0 otherwise
    molecule_rot_symmetry2 : float
        should equal 2.0 if the second molecule is homonuclear and 1.0 otherwise
    molecule_rot_const1 : float
        The quantity :math:`h ^ 2 / (8 \\pi ^ 2 I_{rot,c})`, where :math:`I_{rot,c}` is the moment of rotational
        inertia of the first molecule
    molecule_rot_const2 : float
        The quantity :math:`h ^ 2 / (8 \\pi ^ 2 I_{rot,c})`, where :math:`I_{rot,c}` is the moment of rotational
        inertia of the second molecule
    molecule_num_rot1 : int
        the amount of rotational levels in the first molecule
    molecule_num_rot2 : int
        the amount of rotational levels in the second molecule
    full_integral : bool
        if True, the full averaging is calculated, if false, the partial averaging is calculated, defaults to True
    nokt : bool, optional
        if True and full_integral is True, the result will be multiplied by :math:`\\sqrt{(1 / kT)}`, defaults to False

    Returns
    -------
    float
        The calculated averaging
    """
    return raw_dE_rot_sq(T, idata, Z_rot1, molecule_rot_symmetry1, molecule_rot_const1, molecule_num_rot1,
                         full_integral, nokt) + raw_dE_rot_single(T, idata, Z_rot1, molecule_rot_symmetry1,
                                                                  molecule_rot_const1, molecule_num_rot1, full_integral,
                                                                  nokt) \
                                                * raw_dE_rot_single(T, idata, Z_rot2, molecule_rot_symmetry2,
                                                                    molecule_rot_const2, molecule_num_rot2, False,
                                                                    False)