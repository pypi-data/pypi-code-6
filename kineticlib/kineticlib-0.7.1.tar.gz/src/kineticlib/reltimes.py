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
    return raw_rot_rel_time(T, idata, molecule.LJe, n, infcoll, model)


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
    if isinstance(partner, MoleculeSTS):
        return raw_rot_tel_time_def_molecule_partner(T, idata[1], idata[0], idata[9], idata[10],
                                                     molecule.Z_rot(T), partner.Z_rot(T),
                                                     molecule.rot_symmetry, partner.rot_symmetry, molecule.rot_const,
                                                     partner.rot_const, molecule.num_rot, partner.num_rot,
                                                     molecule.name, partner.name, n)
    else:
        return raw_rot_tel_time_def_atom_partner(T, idata[1], idata[0], idata[9], idata[10],
                                                 molecule.Z_rot(T), molecule.rot_symmetry, molecule.rot_const,
                                                 molecule.num_rot, n)


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
        the interaction model to be used, possible values:
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
        the interaction model to be used, possible values:
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


def raw_rot_rel_time(T: float, idata: np.ndarray, eps: float, n: float, infcoll: float,
                     model: str='IPL') -> float:
    """
    Calculates the rotational relaxation time using Parker's formula and :math:`\\Omega^{(2,2)}` integral,
    *raw* version

    Parameters
    ----------
    T : float
        the temperature of the mixture
    idata : 1-D array-like
        the array of interaction data
    eps : float
        the Lennard-Jones :math:`\\varepsilon_{cd}` parameter of the molecule, divided by Boltzmann's constant
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
    return 0.15625 * constants.pi * Zr_original(T, eps, infcoll) * constants.pi\
        / (n * omega(T, 2, 2, idata, model=model, nokt=False))  # 0.15625 is 5 / 32


def raw_rot_tel_time_def_molecule_partner(T: float, sigma: float, mass: float, vssc: float, vsso: float,
                                          Z_rot1: float, Z_rot2: float,
                                          molecule_rot_symmetry1: float, molecule_rot_symmetry2: float,
                                          molecule_rot_const1: float, molecule_rot_const2: float,
                                          molecule_num_rot1: int, molecule_num_rot2: int, molecule_name: str,
                                          partner_name: str, n: float) -> float:
    """ Calculates the rotational relaxation time using the definition (through the averaging of the squared
    rotational energy difference), *raw* version for the case when the partner is a molecule

    Parameters
    ----------
    T : float
        the temperature of the mixture
    sigma : float
        the collision diameter :math:`\\sigma_{cd}`
    mass : float
        the collision-reduced mass :math:`m_{cd}`
    vssc : float
        the elastic crosssection VSS potential :math:`C` parameter
    vsso : float
        the elastic crosssection VSS potential :math:`\\omega` parameter
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
    molecule_name : str
        the name of the relaxating molecule
    partner_name : str
        the name of the collision partner molecule
    n : float
        the numeric density of the mixtue

    Returns
    -------
    float
        Rotational relaxation time
    """

    if molecule_name == partner_name:
        return 0.5 / (n * cs.elastic_integral(T, 0, sigma, mass, vssc, vsso)
                      * (2 * cs.raw_dE_rot_sq(T, sigma, mass, vssc, vsso, Z_rot1, molecule_rot_symmetry1,
                                              molecule_rot_const1, molecule_num_rot1, False, False)
                         + 2 * cs.raw_dE_rot_c_dE_rot_d(T, sigma, mass, vssc, vsso, Z_rot1, Z_rot2,
                                                        molecule_rot_symmetry1, molecule_rot_symmetry2,
                                                        molecule_rot_const1, molecule_rot_const2,
                                                        molecule_num_rot1, molecule_num_rot2, False, False)))
    else:
        return 0.25 / (n * cs.elastic_integral(T, 0, sigma, mass, vssc, vsso)
                       * cs.raw_dE_rot_dE_rot_full(T, sigma, mass, vssc, vsso, Z_rot1, Z_rot2, molecule_rot_symmetry1,
                                                   molecule_rot_symmetry2, molecule_rot_const1, molecule_rot_const2,
                                                   molecule_num_rot1, molecule_num_rot2, False, False))
        
        
def raw_rot_tel_time_def_atom_partner(T: float, sigma: float, mass: float, vssc: float, vsso: float,
                                      Z_rot: float, molecule_rot_symmetry: float,
                                      molecule_rot_const: float, molecule_num_rot: int, n: float) -> float:
    """ Calculates the rotational relaxation time using the definition (through the averaging of the squared
    rotational energy difference), *raw* version for the case when the partner is an atom

    Parameters
    ----------
    T : float
        the temperature of the mixture
    sigma : float
        the collision diameter :math:`\\sigma_{cd}`
    mass : float
        the collision-reduced mass :math:`m_{cd}`
    vssc : float
        the elastic crosssection VSS potential :math:`C` parameter
    vsso : float
        the elastic crosssection VSS potential :math:`\\omega` parameter
    Z_rot : float
        the value of the rotational partition function of the molecule
    molecule_rot_symmetry : float
        should equal 2.0 if the molecule is homonuclear and 1.0 otherwise
    molecule_rot_const : float
        The quantity :math:`h ^ 2 / (8 \\pi ^ 2 I_{rot,c})`, where :math:`I_{rot,c}` is the moment of rotational
        inertia of the molecule
    molecule_num_rot : int
        the amount of rotational levels in the molecule
    n : float
        the numeric density of the mixtue

    Returns
    -------
    float
        Rotational relaxation time
    """
    return 0.25 / (n * cs.elastic_integral(T, 0, sigma, mass, vssc, vsso)
                   * cs.raw_dE_rot_sq(T, sigma, mass, vssc, vsso, Z_rot, molecule_rot_symmetry,
                                      molecule_rot_const, molecule_num_rot, False, False))