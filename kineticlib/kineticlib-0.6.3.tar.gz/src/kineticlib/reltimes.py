"""Contains functions for calculating relaxation times
"""
__author__ = 'George Oblapenko'
__license__ = "GPL"
__maintainer__ = "George Oblapenko"
__email__ = "kunstmord@kunstmord.com"
__status__ = "Production"

from .omegaint import omega
from scipy import constants
from scipy.special import gamma
from . import crosssection as cs
from .particles import Particle, MoleculeSTS
import numpy as np


def Zr_original(T: float, eps: float, infcoll: float) -> float:
    """
    Calculates the collision amount needed to reach rotational equilibrium for the hard sphere model, but has an
    additional addendum

    Parameters
    ----------
    T : float
        the temperature of the mixture
    eps : float
        the Lennard-Jones :math:`\\varepsilon_{cd}` parameter
    infcoll : float
        the :math:`\\zeta_{\\inf}` parameter

    Returns
    -------
    float
        Amount of collisions needed to reach rotational equilibrium
    """
    TTstar = eps / T
    F = 1 + 0.5 * (constants.pi ** 1.5) * (TTstar ** 0.5)\
        + (0.25 * (constants.pi ** 2) + 2) * TTstar + (constants.pi ** 1.5) * (TTstar ** 1.5)
    return infcoll / F


def Zr(T: float, idata: np.ndarray, mass: float, infcoll: float, model: str='VSS') -> float:
    """
    Calculates the collision amount needed to reach rotational equilibrium for different models

    Parameters
    ----------
    T : float
        the temperature of the mixture
    idata : 1-D array-like
        the array of interaction data
    infcoll : float
        the :math:`\\zeta_{\\inf}` parameter
    model : str
        the interaction model to be used to calculate the :math:`\\Omega^{(2,2)}` integral, possible values:
            * 'VSS' (Variable Soft Sphere model)
            * 'VHS' (Variable Hard Sphere model)
            * the Rigid Sphere model will be used otherwise

        defaults to 'VSS'

    Returns
    -------
    float
        Amount of collisions needed to reach rotational equilibrium
    """
    if model == 'VSS':
        alpha = idata[11] * (T ** idata[12])
        vssomega = idata[6]
    elif model == 'VHS':
        alpha = 1.0
        vssomega = idata[6]
    else:
        alpha = 1.0
        vssomega = 0.0

    TTstar = idata[2] / T
    div = (2.0 - vssomega) / (1.0 + alpha) + 0.5 * (constants.pi ** 1.5) * gamma(1.0 + alpha) * gamma(2.5 - vssomega)\
        * (TTstar ** 0.5) / (gamma(1.5 + alpha) * gamma(2.0 - vssomega)) + (2.0 + 0.25 * (constants.pi ** 2)) * TTstar
    return mass * infcoll / (2.0 * div * idata[0])


def rot_rel_time(T: float, idata: np.ndarray, molecule: MoleculeSTS, n: float, infcoll: float,
                 model: str='IPL') -> float:
    """
    Calculates the rotational relaxation time using Parker's formula and :math:`\\Omega^{(2,2)}` integral

    Parameters
    ----------
    T : float
        the temperature of the mixture
    idata : 1-D array-like
        the array of interaction data
    molecule : MoleculeSTS or Molecule
        the molecule for which the rotational relaxation time is being calculated
    n : float
        the numeric density of the mixtue
    infcoll : float
        the :math:`\\zeta_{\\inf}` parameter
    model : str
        the interaction model to be used to calculate the :math:`\\Omega^{(2,2)}` integral, possible values:
            * 'IPL' (Inverse Power Law potential)
            * 'LJ' (Lennard-Jones potential)
            * 'RS' (Rigid Sphere model)
            * 'VSS' (Variable Soft Sphere model)
            * 'Switch' (returns the result for the Lennard-Jones model when :math:`T / \\varepsilon_{cd} < 10`
              and for the IPL potential otherwise)

        defaults to 'IPL'

    Returns
    -------
    float
        Rotational relaxation time
    """
    return 0.15625 * constants.pi * Zr_original(T, molecule.LJe, infcoll) * constants.pi\
        / (n * omega(T, 2, 2, idata, model=model, nokt=False))  # 0.15625 is 5 / 32


def rot_tel_time_def(T: float, idata: np.ndarray, molecule: MoleculeSTS, partner: Particle, n: float) -> float:
    """ Calculates the rotational relaxation time using the definition (through the averaging of the squared
    rotational energy difference)

    Parameters
    ----------
    T : float
        the temperature of the mixture
    idata : 1-D array-like
        the array of interaction data
    molecule : MoleculeSTS or Molecule
        the molecule for which the rotational relaxation time is being calculated
    partner : Particle
        the collision partner
    n : float
        the numeric density of the mixtue

    Returns
    -------
    float
        Rotational relaxation time
    """
    if molecule.name == partner.name:
        return 0.5 / (n * cs.elastic_integral(T, 0, idata) * (2 * cs.dE_rot_sq(T, molecule)
                                                              + 2 * cs.dE_rot_c_dE_rot_d(T, molecule, molecule)))
    else:
        if isinstance(partner, MoleculeSTS):
            return 0.25 / (n * cs.elastic_integral(T, 0, idata) * cs.dE_rot_dE_rot_full(T, molecule, partner))
        else:
            return 0.25 / (n * cs.elastic_integral(T, 0, idata) * cs.dE_rot_sq(T, molecule))


def rot_rel_time_VSS(T: float, idata: np.ndarray, n: float, mass: float, infcoll: float, model: str='VSS') -> float:
    """ Calculates the rotational relaxation time using the VSS/VHS/HS models and Parker's formula.

    Parameters
    ----------
    T : float
        the temperature of the mixture
    idata : 1-D array-like
        the array of interaction data
    mass : float
        the mass of the molecule for which the rotational relaxation time is being calculated
    infcoll : float
        the :math:`\\zeta_{\\inf}` parameter
    model : str
        the interaction model to be used to calculate the :math:`\\Omega^{(2,2)}` integral, possible values:
            * 'VSS' (Variable Soft Sphere model)
            * 'VHS' (Variable Hard Sphere model)
            * the Rigid Sphere model will be used otherwise

        defaults to 'VSS'

    Returns
    -------
    float
        Rotational relaxation time
    """
    return Zr(T, idata, mass, infcoll, model) / ((idata[5] * n
                                                * ((8 * constants.k * T / (constants.pi * idata[0])) ** 0.5)
                                                * (T ** -idata[6]) * gamma(2 - idata[6]))
                                               * (constants.physical_constants['Angstrom star'][0] ** 2))


def millikan_white(T: float, idata: np.ndarray, molecule: MoleculeSTS, p: float) -> float:
    """ Calculates the VT relaxation time using the Millikan-White formula.

    Parameters
    ----------
    T : float
        the temperature of the mixture
    idata : 1-D array-like
        the array of interaction data
    molecule : MoleculeSTS or Molecule
        the molecule for which the VT relaxation time is being calculated
    p : float
        the pressure (in atmospheres)

    Returns
    -------
    float
        VT relaxation time
    """
    mu = idata[0] * 1000.0 * constants.N_A
    return (10.0 ** (0.0005 * (mu ** 0.5) * ((molecule.hvc / constants.k) ** (4.0 / 3.0))
                     * (T ** (-1.0 / 3.0) - 0.015 * (mu ** 0.25)) - 8.0)) / p
