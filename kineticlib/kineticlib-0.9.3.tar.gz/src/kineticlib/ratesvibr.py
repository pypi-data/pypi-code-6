"""Contains functions for calculating VV- and VT- rates
"""
__author__ = 'George Oblapenko'
__license__ = "GPL"
__maintainer__ = "George Oblapenko"
__email__ = "kunstmord@kunstmord.com"
__status__ = "Production"


from .crosssection import raw_vv_integral_fho, raw_vt_integral_fho, raw_vt_integral_rigid_sphere_fho, raw_vv_integral_rigid_sphere_fho
from .particles import Molecule
import numpy as np


def vt_rate_fho(T: float, idata: np.ndarray, molecule: Molecule, i: int, delta: int, rig_sphere: bool=False) -> float:
    """Calculates the VT transition rate constant using the FHO probability and VSS or rigid sphere cross-section models
    for the following process: **M(i) + P -> M(i + delta) + P**

    Parameters
    ----------
    T : float
        the temperature of the mixture
    idata : 1-D array-like
        the array of interaction data
    molecule : Molecule or any subclass (MoleculeMultiT, MoleculeOneT)
        the molecule which undergoes the VT transition
    i : int
        the vibrational level of the molecule
    delta : int
        the change in vibrational level of the molecule
    rig_sphere : bool, optional
        if ``True``, the rigid sphere model is used for the crosssection, if ``False``, the VSS is model is used,
        defaults to ``False``

    Returns
    -------
    float
        The VT transition rate

    """
    if not rig_sphere:
        return raw_vt_rate_fho(T, idata[0], idata[4], idata[9], idata[10],
                           molecule.vibr[i], molecule.vibr[i + delta], molecule.vibr_zero, molecule.diss, i, delta)
    else:
        return raw_vt_rate_rigid_sphere_fho(T, idata[1], idata[0], idata[4], molecule.vibr[i], molecule.vibr[i + delta],
                                        molecule.vibr_zero, molecule.diss, i, delta)


def vv_rate_fho(T: float, idata: np.ndarray, molecule1: Molecule, molecule2: Molecule, i: int, k: int, i_delta: int,
                rig_sphere: bool=False) -> float:
    """Calculates the VV transition rate constant using the FHO probability and VSS or rigid sphere cross-section models
    for the following process: **M1(i) + M2(k) -> M1(i + i_delta) + M2(k - i_delta)**

    Parameters
    ----------
    T : float
        the temperature of the mixture
    idata : 1-D array-like
        the array of interaction data
    molecule1 : Molecule or any subclass (MoleculeMultiT, MoleculeOneT)
        the molecule M1
    molecule2 : Molecule or any subclass (MoleculeMultiT, MoleculeOneT)
        the molecule M2
    i : int
        the vibrational level of molecule M1
    k : int
        the vibrational level of molecule M2
    i_delta : int
        the change in vibrational level of molecule M1
    rig_sphere : bool, optional
        if ``True``, the rigid sphere model is used for the crosssection, if ``False``, the VSS is model is used,
        defaults to ``False``

    Returns
    -------
    float
        The VV transition rate

    """
    if not rig_sphere:
        return raw_vv_rate_fho(T, idata[0], idata[4], idata[9], idata[10],
                           molecule1.vibr[i], molecule1.vibr[i + i_delta],
                           molecule2.vibr[k], molecule2.vibr[k - i_delta], i, k, i_delta)
    else:
        return raw_vv_rate_rigid_sphere_fho(T, idata[1], idata[0], idata[4], molecule1.vibr[i], molecule1.vibr[i + i_delta],
                                        molecule2.vibr[k], molecule2.vibr[k - i_delta], i, k, i_delta)


def raw_vt_rate_fho(T: float, mass: float, beta: float, vssc: float, vsso: float,
                    ve_before: float, ve_after: float, molecule_vibr_zero: float,
                    molecule_diss: float, i: int, delta: int) -> float:
    """Calculates the VT transition rate constant using the FHO probability and VSS cross-section models
    for the following process: **M(i) + P -> M(i + delta) + P**, *raw version*

    Parameters
    ----------
    T : float
        the temperature of the mixture
    mass : float
        the collision-reduced mass :math:`m_{cd}`
    beta : float
        the IPL :math:`\\beta` parameter
    vssc : float
        the elastic crosssection VSS potential :math:`C` parameter
    vsso : float
        the elastic crosssection VSS potential :math:`\\omega` parameter
    ve_before : float
        the vibrational energy of the molecule before the transition
    ve_after : float
        the vibrational energy of the molecule after the transition
    molecule_vibr_zero : float
        the energy of the 0-th vibrational level (with no offset)
    molecule_diss : float
        the dissociation energy of the molecule which undergoes the transition (with no offset)
    i : int
        the vibrational level of the molecule
    delta : int
        the change in vibrational level of the molecule

    Returns
    -------
    float
        The VT transition rate

    """
    return 8.0 * raw_vt_integral_fho(T, 0, mass, beta, vssc, vsso, ve_before, ve_after,
                                     molecule_vibr_zero, molecule_diss, i, delta, False)


def raw_vt_rate_rigid_sphere_fho(T: float, sigma: float, mass: float, beta: float,
                                 ve_before: float, ve_after: float, molecule_vibr_zero: float,
                                 molecule_diss: float, i: int, delta: int) -> float:
    """Calculates the VT transition rate constant using the FHO probability and rigid sphere cross-section models
    for the following process: **M(i) + P -> M(i + delta) + P**, *raw version*

    Parameters
    ----------
    T : float
        the temperature of the mixture
    sigma : float
        the collision diameter :math:`\\sigma_{cd}`
    mass : float
        the collision-reduced mass :math:`m_{cd}`
    beta : float
        the IPL :math:`\\beta` parameter
    ve_before : float
        the vibrational energy of the molecule before the transition
    ve_after : float
        the vibrational energy of the molecule after the transition
    molecule_vibr_zero : float
        the energy of the 0-th vibrational level (with no offset)
    molecule_diss : float
        the dissociation energy of the molecule which undergoes the transition (with no offset)
    i : int
        the vibrational level of the molecule
    delta : int
        the change in vibrational level of the molecule

    Returns
    -------
    float
        The VT transition rate

    """
    return 8.0 * raw_vt_integral_rigid_sphere_fho(T, 0, sigma, mass, beta, ve_before, ve_after, molecule_vibr_zero,
                                                  molecule_diss, i, delta, False)


def raw_vv_rate_fho(T: float, mass: float, beta: float, vssc: float, vsso: float,
                    ve_before1: float, ve_after1: float, ve_before2: float, ve_after2: float,
                    i: int, k: int, i_delta: int) -> float:
    """Calculates the VV transition rate constant using the FHO probability and VSS cross-section models
    for the following process: **M1(i) + M2(k) -> M1(i + i_delta) + M2(k - i_delta)**, *raw version*

    Parameters
    ----------
    T : float
        the temperature of the mixture
    mass : float
        the collision-reduced mass :math:`m_{cd}`
    beta : float
        the IPL :math:`\\beta` parameter
    vssc : float
        the elastic crosssection VSS potential :math:`C` parameter
    vsso : float
        the elastic crosssection VSS potential :math:`\\omega` parameter
    ve_before1 : float
        the vibrational energy of the molecule M1 before the transition
    ve_after1 : float
        the vibrational energy of the molecule M1 after the transition
    ve_before2 : float
        the vibrational energy of the molecule M2 before the transition
    ve_after2 : float
        the vibrational energy of the molecule M2 after the transition
    i : int
        the vibrational level of molecule M1
    k : int
        the vibrational level of molecule M2
    i_delta : int
        the change in vibrational level of molecule M1

    Returns
    -------
    float
        The VV transition rate

    """
    return 8.0 * raw_vv_integral_fho(T, 0, mass, beta, vssc, vsso,
                                     ve_before1, ve_after1, ve_before2, ve_after2, i, k, i_delta, False)


def raw_vv_rate_rigid_sphere_fho(T: float, sigma: float, mass: float, beta: float, ve_before1: float,
                                 ve_after1: float, ve_before2: float, ve_after2: float, i: int, k: int,
                                 i_delta: int) -> float:
    """Calculates the VV transition rate constant using the FHO probability and rigid sphere cross-section models
    for the following process: **M1(i) + M2(k) -> M1(i + i_delta) + M2(k - i_delta)**, *raw version*

    Parameters
    ----------
    T : float
        the temperature of the mixture
    sigma : float
        the collision diameter :math:`\\sigma_{cd}`
    mass : float
        the collision-reduced mass :math:`m_{cd}`
    beta : float
        the IPL :math:`\\beta` parameter
    ve_before1 : float
        the vibrational energy of the molecule M1 before the transition
    ve_after1 : float
        the vibrational energy of the molecule M1 after the transition
    ve_before2 : float
        the vibrational energy of the molecule M2 before the transition
    ve_after2 : float
        the vibrational energy of the molecule M2 after the transition
    i : int
        the vibrational level of molecule M1
    k : int
        the vibrational level of molecule M2
    i_delta : int
        the change in vibrational level of molecule M1

    Returns
    -------
    float
        The VV transition rate

    """
    return 8.0 * raw_vv_integral_rigid_sphere_fho(T, 0, sigma, mass, beta, ve_before1, ve_after1,
                                                  ve_before2, ve_after2, i, k, i_delta, False)