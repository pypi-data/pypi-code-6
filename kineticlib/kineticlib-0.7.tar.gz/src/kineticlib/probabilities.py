"""Contains functions for calculating VV and VT transition probabilities
"""
__author__ = 'George Oblapenko'
__license__ = "GPL"
__maintainer__ = "George Oblapenko"
__email__ = "kunstmord@kunstmord.com"
__status__ = "Development"

import numpy as np
from scipy import constants
from scipy.misc import factorial
from .particles import MoleculeSTS
from .errors import KineticlibError


def fact_div_fact(start: int, end: int) -> float:
    """
    Helper function, returns end! / start!, where start and end are integers

    Parameters
    ----------
    start : int
        the start of the sequence of numbers
    end : int
        the end of the sequence of numbers

    Returns
    -------
    float
        The product of all numbers in the range `[start + 1, end]`

    Raises
    ------
    KineticlibError
        if `start >= end` or `end < 0.0`
    """
    if end < 0.0 or start >= end:
        raise KineticlibError
    else:
        return np.prod(np.arange(start + 1.0, end + 1.0, 1.0))


def vel_avg_vt(g: float, ve_before: float, ve_after: float, m: float) -> float:
    """Helper function, returns the arithmetic mean of the relative velocity of particles before and after
    a VT transition (using the energy conservation law) M(i1) + P -> M(i2) + P

    Parameters
    ----------
    g : float
        the relative dimensional velocity of the particles before the collision
    ve_before : float
        the vibrational energy of the molecule before the transition
    ve_after : float
        the vibrational energy of the molecule after the transition
    m : float
        the collision-reduced mass :math:`m_{cd}`

    Returns
    -------
    float
        Arithmetic mean of before- and after- velocities for a VT transition

    Notes
    -----
    If the squared after-collision velocity is < 0, then the collision is impossible for such parameters and
    the function returns -1
    """
    gn_sq = (ve_before - ve_after) * (2.0 / m) + (g ** 2)
    if gn_sq < 0:
        return -1
    else:
        return 0.5 * (g + (gn_sq ** 0.5))


def vel_avg_vv(g: float, ve_before1: float, ve_before2: float, ve_after1: float,
               ve_after2: float, m: float) -> float:
    """Helper function, returns the arithmetic mean of the relative velocity of particles before and after
    a VV transition (using the energy conservation law) M1(i1) + M2(k1) -> M1(i2) + M2(k2)

    Parameters
    ----------
    g : float
        the relative dimensional velocity of the particles before the collision
    ve_before1 : float
        the vibrational energy of the molecule M1 before the transition
    ve_after1 : float
        the vibrational energy of the molecule M1 after the transition
    ve_before2 : float
        the vibrational energy of the molecule M2 before the transition
    ve_after2 : float
        the vibrational energy of the molecule M2 after the transition
    m : float
        the collision-reduced mass :math:`m_{cd}`

    Returns
    -------
    float
        Arithmetic mean of before- and after- velocities for a VT transition

    Notes
    -----
    If the squared after-collision velocity is < 0, then the collision is impossible for such parameters and
    the function returns -1
    """
    gn_sq = (ve_before1 - ve_after1 + ve_before2 - ve_after2) * (2.0 / m) + (g ** 2)
    if gn_sq < 0:
        return -1
    else:
        return 0.5 * (g + (gn_sq ** 0.5))


def vt_probability(g: float, T: float, idata: np.ndarray, molecule_vibr_array: np.ndarray, molecule_vibr_zero: float,
                   molecule_diss: float,i: int, delta: int) -> float:
    """Returns the probability of a VT transition using the FHO (Forced harmonic oscillator) model
     M(i) + P -> M(i + delta) + P

    Parameters
    ----------
    g : float
        the relative dimensionless velocity of the particles before the collision
    T : float
        the temperature of the mixture
    idata : 1-D array-like
        the array of interaction data
    molecule_vibr_array1 : 1-D array-like
        the array of vibrational energies of the molecule undergoing the VT transition
    molecule_vibr_zero : float
        the energy of the 0-th vibrational level
    molecule_diss : float
        the dissociation energy of the molecule which undergoes the transition
    i : int
        the vibrational level of the molecule
    delta : int
        the change in vibrational level of the molecule

    Returns
    -------
    float
        VT transition probability
    """
    svt = 0.5

    if delta > 0:
        s = delta * 1.0
        ns = fact_div_fact(i, i + delta)
    else:
        s = -delta * 1.0
        ns = fact_div_fact(i + delta, i)

    omega = np.absolute((molecule_vibr_array[i] - molecule_vibr_array[i + delta]) / delta) / constants.hbar
    if omega == 0.0:
        return 0.0
    g *= (2 * constants.k * T / idata[0]) ** 0.5  # convert to dimensional velocity
    vel = vel_avg_vt(g, molecule_vibr_array[i], molecule_vibr_array[i + delta], idata[0])

    if vel < 0.0:
        return 0.0
    phi = 2.0 * np.arctan(((2.0 * (molecule_diss + molecule_vibr_zero) / idata[0]) ** 0.5) / vel)

    eps = (np.cosh((1.0 + phi) * omega / (idata[4] * vel))
           / (np.sinh(2.0 * constants.pi * omega / (idata[4] * vel)))) ** 2
    eps *= 4.0 * svt * (constants.pi ** 2) * omega * idata[0] / ((idata[4] ** 2) * constants.h)
    prob = ns * (eps ** s) * np.exp(- 2.0 * (ns ** (1.0 / s)) * eps / (s + 1)) / (factorial(s) ** 2)
    return prob


def vt_prob_g_only(g: float, T: float, idata: np.ndarray, molecule_vibr_array: np.ndarray, i: int, delta: int,
                   depth: float) -> float:
    """Returns the velocity-dependent part of the probability of a VT transition using
    the FHO (Forced harmonic oscillator) model M(i) + P -> M(i + delta) + P

    Parameters
    ----------
    g : float
        the relative dimensionless velocity of the particles before the collision
    T : float
        the temperature of the mixture
    idata : 1-D array-like
        the array of interaction data
    vibr_spec : 1-D array-like
        the array of the vibrational energies of the molecule undergoing the VT transition
    i : int
        the vibrational level of the molecule
    delta : int
        the change in vibrational level of the molecule
    depth : float
        the potential well depth of the molecule

    Returns
    -------
    float
        Velocity-dependent part of the VT transition probability
    """
    svt = 0.5

    g *= (2 * constants.k * T / idata[0]) ** 0.5  # convert to dimensional velocity
    vel = vel_avg_vt(g, molecule_vibr_array[i], molecule_vibr_array[i + delta], idata[0])
    if vel < 0.0:
        return 0.0

    if delta == 1:
        omega = (molecule_vibr_array[i + 1] - molecule_vibr_array[i]) / constants.hbar
        phi = 2.0 * np.arctan(((2.0 * depth / idata[0]) ** 0.5) / vel)

        eps = (np.cosh((1.0 + phi) * omega / (idata[4] * vel))
               / (np.sinh(2.0 * constants.pi * omega / (idata[4] * vel)))) ** 2
        eps *= 4.0 * svt * (constants.pi ** 2) * omega * idata[0] / ((idata[4] ** 2) * constants.h)
        return eps * np.exp(-(i + 1) * eps)
    elif delta == -1:
        omega = (molecule_vibr_array[i] - molecule_vibr_array[i - 1]) / constants.hbar
        phi = 2.0 * np.arctan(((2.0 * depth / idata[0]) ** 0.5) / vel)

        eps = (np.cosh((1.0 + phi) * omega / (idata[4] * vel))
               / (np.sinh(2.0 * constants.pi * omega / (idata[4] * vel)))) ** 2
        eps *= 4.0 * svt * (constants.pi ** 2) * omega * idata[0] / ((idata[4] ** 2) * constants.h)
        return eps * np.exp(-i * eps)
    elif delta > 0:
        s = delta * 1.0
        omega = (molecule_vibr_array[i + delta] - molecule_vibr_array[i]) / (delta * constants.hbar)
        ns = fact_div_fact(i, i + delta)
        phi = 2.0 * np.arctan(((2.0 * depth / idata[0]) ** 0.5) / vel)
        eps = (np.cosh((1.0 + phi) * omega / (idata[4] * vel))
               / (np.sinh(2.0 * constants.pi * omega / (idata[4] * vel)))) ** 2
        eps *= 4.0 * svt * (constants.pi ** 2) * omega * idata[0] / ((idata[4] ** 2) * constants.h)
        return (eps ** s) * np.exp(- 2.0 * (ns ** (1.0 / s)) * eps / (s + 1))
    else:
        s = -delta * 1.0
        omega = (molecule_vibr_array[i + delta] - molecule_vibr_array[i]) / (delta * constants.hbar)
        ns = fact_div_fact(i + delta, i)
        phi = 2.0 * np.arctan(((2.0 * depth / idata[0]) ** 0.5) / vel)
        eps = (np.cosh((1.0 + phi) * omega / (idata[4] * vel))
               / (np.sinh(2.0 * constants.pi * omega / (idata[4] * vel)))) ** 2
        eps *= 4.0 * svt * (constants.pi ** 2) * omega * idata[0] / ((idata[4] ** 2) * constants.h)
        return (eps ** s) * np.exp(- 2.0 * (ns ** (1.0 / s)) * eps / (s + 1))


def vv_probability(g: float, T: float, idata: np.ndarray, molecule_vibr_array1: np.ndarray,
                   molecule_vibr_array2: np.ndarray, i: int,
                   k: int, i_delta: int) -> float:
    """Returns the probability of a VV transition using the FHO (Forced harmonic oscillator) model
     M1(i) + M2(k) -> M1(i + delta) + M2(k - i_delta)

    Parameters
    ----------
    g : float
        the relative dimensionless velocity of the particles before the collision
    T : float
        the temperature of the mixture
    idata : 1-D array-like
        the array of interaction data
    molecule_vibr_array1 : 1-D array-like
        the array of vibrational energies of the first molecule undergoing the VV transition
    molecule_vibr_array2 : 1-D array-like
        the array of vibrational energies of the second molecule undergoing the VV transition
    i : int
        the vibrational level of molecule1
    k : int
        the vibrational level of molecule2
    i_delta : int
        the change in vibrational level of the first molecule

    Returns
    -------
    float
        VV transition probability
    """
    svv = 0.04

    if i_delta > 0:
        s = i_delta * 1.0
        ns1 = fact_div_fact(i, i + i_delta)
        ns2 = fact_div_fact(k - i_delta, k)
    else:
        s = -i_delta * 1.0
        ns1 = fact_div_fact(i + i_delta, i)
        ns2 = fact_div_fact(k, k - i_delta)

    g *= (2.0 * constants.k * T / idata[0]) ** 0.5
    vel = vel_avg_vv(g, molecule_vibr_array1[i], molecule_vibr_array2[k], molecule_vibr_array1[i + i_delta],
                     molecule_vibr_array2[k - i_delta],
                     idata[0])

    if vel < 0:
        return 0.0
    omega1 = np.absolute((molecule_vibr_array1[i] -
                          molecule_vibr_array1[i + i_delta]) / i_delta) / constants.hbar

    omega2 = np.absolute((molecule_vibr_array2[k] -
                          molecule_vibr_array2[k - i_delta]) / i_delta) / constants.hbar

    if omega1 == 0.0 or omega2 == 0:
        return 0.0
    xi = 2 * np.abs(omega1 - omega2) / (idata[4] * vel)
    if xi < 1.0 ** (-4):
        rhoxi = 0.25 * svv * ((idata[4] * vel) ** 2) / (omega1 * omega2)
    else:
        rhoxi = svv * (np.abs(omega1 - omega2) ** 2) / (omega1 * omega2 * (np.sinh(xi) ** 2))

    return rhoxi * ns1 * ns2 * np.exp(-2.0 * rhoxi * ((ns1 * ns2) ** (1.0 / s)) / (s + 1)) / (factorial(s) ** 2)


def vv_prob_g_only(g: float, T: float, idata: np.ndarray, molecule_vibr_array1: np.ndarray,
                   molecule_vibr_array2: np.ndarray, i: int,
                   k: int, i_delta: int) -> float:
    """Returns the velocity-dependent part of the probability of a VV transition using the FHO
    (Forced harmonic oscillator) model M1(i) + M2(k) -> M1(i + delta) + M2(k - i_delta)

    Parameters
    ----------
    g : float
        the relative dimensionless velocity of the particles before the collision
    T : float
        the temperature of the mixture
    idata : 1-D array-like
        the array of interaction data
    molecule_vibr_array1 : 1-D array-like
        the array of vibrational energies of the first molecule undergoing the VV transition
    molecule_vibr_array2 : 1-D array-like
        the array of vibrational energies of the second molecule undergoing the VV transition
    i : int
        the vibrational level of molecule1
    k : int
        the vibrational level of molecule2
    i_delta : int
        the change in vibrational level of the first molecule

    Returns
    -------
    float
        Velocity-dependent part of the VV transition probability
    """
    svv = 0.04
    g *= (2.0 * constants.k * T / idata[0]) ** 0.5
    vel = vel_avg_vv(g, molecule_vibr_array1[i], molecule_vibr_array2[k], molecule_vibr_array1[i + i_delta], molecule_vibr_array2[k - i_delta], idata[0])
    if vel < 0:
        return 0.0

    if i_delta == 1:
        omega1 = (molecule_vibr_array1[i + 1] - molecule_vibr_array1[i]) / constants.hbar
        omega2 = (molecule_vibr_array2[k] - molecule_vibr_array2[k - 1]) / constants.hbar
        xi = 2.0 * np.abs(omega1 - omega2) / (idata[4] * vel)
        if xi < 1.0 ** (-10):
            rhoxi = 0.25 * svv * ((idata[4] * vel) ** 2) / (omega1 * omega2)
        else:
            rhoxi = svv * ((omega1 - omega2) ** 2) / (omega1 * omega2 * (np.sinh(xi) ** 2))

        return rhoxi * np.exp(-((i + 1) * k) * rhoxi)
    elif i_delta == -1:
        omega1 = (molecule_vibr_array1[i] - molecule_vibr_array1[i - 1]) / constants.hbar
        omega2 = (molecule_vibr_array2[k + 1] - molecule_vibr_array2[k]) / constants.hbar

        xi = 2.0 * np.abs(omega1 - omega2) / (idata[4] * vel)
        if xi < 1.0 ** (-10):
            rhoxi = 0.25 * svv * ((idata[4] * vel) ** 2) / (omega1 * omega2)
        else:
            rhoxi = svv * ((omega1 - omega2) ** 2) / (omega1 * omega2 * (np.sinh(xi) ** 2))

        return rhoxi * np.exp(-(i * (k + 1)) * rhoxi)
    elif i_delta > 0:
        s = i_delta * 1.0

        omega1 = (molecule_vibr_array1[i + i_delta] - molecule_vibr_array1[i]) / (i_delta * constants.hbar)
        omega2 = (molecule_vibr_array2[k] - molecule_vibr_array2[k - i_delta]) / (i_delta * constants.hbar)

        xi = 2.0 * np.abs(omega1 - omega2) / (idata[4] * vel)
        if xi < 1.0 ** (-10):
            rhoxi = 0.25 * svv * ((idata[4] * vel) ** 2) / (omega1 * omega2)
        else:
            rhoxi = svv * (np.abs(omega1 - omega2) ** 2) / (omega1 * omega2 * (np.sinh(xi) ** 2))

        return rhoxi * np.exp(-2.0 * ((fact_div_fact(i, i + i_delta) * fact_div_fact(k - i_delta, k)) ** (1.0 / s))
                     * rhoxi / (s + 1))
    else:
        s = -i_delta * 1.0

        omega1 = (molecule_vibr_array1[i + i_delta] - molecule_vibr_array1[i]) / (i_delta * constants.hbar)
        omega2 = (molecule_vibr_array2[k] - molecule_vibr_array2[k - i_delta]) / (i_delta * constants.hbar)

        xi = 2.0 * np.abs(omega1 - omega2) / (idata[4] * vel)
        if xi < 1.0 ** (-10):
            rhoxi = 0.25 * svv * ((idata[4] * vel) ** 2) / (omega1 * omega2)
        else:
            rhoxi = svv * (np.abs(omega1 - omega2) ** 2) / (omega1 * omega2 * (np.sinh(xi) ** 2))

        return rhoxi * np.exp(-2.0 * ((fact_div_fact(i + i_delta, i) * fact_div_fact(k, k - i_delta)) ** (1.0 / s))
                     * rhoxi / (s + 1))