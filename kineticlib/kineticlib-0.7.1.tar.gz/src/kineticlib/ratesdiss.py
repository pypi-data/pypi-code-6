"""Contains functions for calculating dissociation rates
"""
__author__ = 'George Oblapenko'
__license__ = "GPL"
__maintainer__ = "George Oblapenko"
__email__ = "kunstmord@kunstmord.com"
__status__ = "Production"

import numpy as np
from scipy import constants
from .crosssection import raw_diss_integral_rigid_sphere
from .particles import MoleculeSTS


def k_diss_eq(T: float, model_data: np.ndarray, diss_energy: float) -> float:
    """Calculates the equilibrium dissociation rate constant using the Arrhenius model

    Parameters
    ----------
    T : float
        the temperature of the mixture
    model_data : 1-D array-like
        dissociation model data
    diss_energy : float
        dissociation energy of the molecule which dissociates

    Returns
    -------
    float
        Equilibrium dissociation rate constant

    """
    return model_data[1] * (T ** model_data[0]) * np.exp(-diss_energy/(constants.k * T))


def diss_rate_treanor_marrone(T: float, model_data: np.ndarray, molecule: MoleculeSTS, i: int,
                              model: str='D6k') -> float:
    """Calculates the non-equilibrium rate constant using the Treanor-Marrone model

    Parameters
    ----------
    T : float
        the temperature of the mixture
    model_data : 1-D array-like
        dissociation model data
    molecule : MoleculeSTS or Molecule
        the molecule which dissociates
    i : int
        the vibrational level from which the molecule dissociates
    model : str
        the model for the `U` parameter to be used, possible values:
            * 'inf' - the U parameter in the non-equilbrium factor
              will be equal to :math:`\\infty`
            * 'D6k' - the U parameter in the non-equilbrium factor will be equal
              to :math:`D / 6k`, where :math:`D` is the dissociation energy of the molecule
            * if equal to '3T', the U parameter in the non-equilbrium factor will be equal to :math:`3T`

        defaults to 'D6k'

    Returns
    -------
    float
        Non-equilibrium dissociation rate constant

    """
    return raw_diss_rate_treanor_marrone(T, model_data, molecule.Z_diss(i, T, model), molecule.diss)


def diss_rate_rigid_sphere(T: float, idata: np.ndarray, molecule: MoleculeSTS, i: int,
                           center_of_mass: bool=True, vl_dependent: bool=True) -> float:
    """Calculates the non-equilibrium rate constant using the rigid-sphere crosssection

    Parameters
    ----------
    T : float
        the temperature of the mixture
    idata : 1-D array-like
        the array of interaction data
    molecule : MoleculeSTS or Molecule
        the molecule which dissociates
    i : int
        the vibrational level from which the molecule dissociates
    center_of_mass : bool, optional
        if True, the kinetic energy of the collision partners will be calculated along the center-of-mass line,
        if False, the total kinetic energy will be used, defaults to True
    vl_dependent : bool, optional
        if True, the dissociation crosssection takes into account the vibrational energy of the dissociating molecule,
        if False, the crosssection is independent of the vibrational energy, defaults to True

    Returns
    -------
    float
        Non-equilibrium dissociation rate constant
    """
    return raw_diss_rate_rigid_sphere(T, idata[1], idata[0], molecule.vibr[i], molecule.diss, center_of_mass,
                                      vl_dependent)


def raw_diss_rate_treanor_marrone(T: float, model_data: np.ndarray, Z_diss: float, molecule_diss: float) -> float:
    """Calculates the non-equilibrium rate constant using the Treanor-Marrone model

    Parameters
    ----------
    T : float
        the temperature of the mixture
    model_data : 1-D array-like
        dissociation model data
    Z_diss : float
        the value of the non-equilibrium factor
    molecule_diss : float
        the dissociation energy of the molecule

    Returns
    -------
    float
        Non-equilibrium dissociation rate constant

    """
    return Z_diss * k_diss_eq(T, model_data, molecule_diss)


def raw_diss_rate_rigid_sphere(T: float, sigma: float, mass: float, molecule_vibr: float, molecule_diss: float,
                               center_of_mass: bool=True, vl_dependent: bool=True) -> float:
    """Calculates the non-equilibrium rate constant using the rigid-sphere crosssection

    Parameters
    ----------
    T : float
        the temperature of the mixture
    sigma : float
        the collision diameter :math:`\\sigma_{cd}`
    mass : float
        the collision-reduced mass :math:`m_{cd}`
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

    Returns
    -------
    float
        Non-equilibrium dissociation rate constant
    """
    return 8.0 * raw_diss_integral_rigid_sphere(T, 0, sigma, mass, molecule_vibr, molecule_diss, center_of_mass,
                                                vl_dependent, False)