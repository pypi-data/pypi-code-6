"""Contains functions for calculating generalized affinities and equilibrium concentrations in binary mixtures"""
__author__ = 'George Oblapenko'
__license__ = "GPL"
__maintainer__ = "George Oblapenko"
__email__ = "kunstmord@kunstmord.com"
__status__ = "Production"

import numpy as np
from scipy import constants
from scipy.optimize import brentq
from .particles import Atom, Molecule


def Gamma_VT(molecule: Molecule, T: float, T1: float, delta: int=-1) -> float:
    """Calculates the generalized thermodynamic force :math:`\\Gamma^{VT}` for a VT transition:
    M(i) + P -> M(i+delta) + P

    Parameters
    ----------
    molecule : Molecule
        the molecule undergoing the transition
    T : float
        the temperature of the mixture
    T1 : float
        the temperature of the first vibrational level of the molecule M
    delta : int
        the change in vibrational level

    Returns
    -------
    float
        The generalized thermodynamic force for a VT transition

    """
    return raw_Gamma_VT(molecule.vibr[1], T, T1, delta)


def Gamma_VV(molecule1: Molecule, molecule2: Molecule, T: float, T1_1: float, T1_2: float,
             i_delta: int, k_delta: int) -> float:
    """Calculates the generalized thermodynamic force :math:`\\Gamma^{VV}` for a VV transition:
    M1(i) + M2(k) -> M1(i+i_delta) + M2(k+k_delta)

    Parameters
    ----------
    molecule1 : Molecule
        the molecule M1
    molecule2 : Molecule
        the molecule M2
    T : float
        the temperature of the mixture
    T1_1 : float
        the temperature of the first vibrational level of the molecule M1
    T1_2 : float
        the temperature of the first vibrational level of the molecule M2
    i_delta : int
        the change in vibrational level of molecule M1
    k_delta : int
        the change in vibrational level of molecule M2

    Returns
    -------
    float
        The generalized thermodynamic force for a VV transition

    """
    return raw_Gamma_VV(molecule1.vibr[1], molecule2.vibr[1], T, T1_1, T1_2, i_delta, k_delta)


def Gamma_22(molecule1: Molecule, molecule2: Molecule, molecule_new1: Molecule, molecule_new2: Molecule, T: float,
             T1_1: float, T1_2: float, T1_new1: float, T1_new2: float, n_molecule1: float, n_molecule2: float,
             n_molecule_new1: float, n_molecule_new2: float, i: int, k: int, i_new: int, k_new: int) -> float:
    """Calculates the generalized thermodynamic force :math:`\\Gamma^{2\leftrightarrows2}` for a bimolecular
    exchange reaction:
    M1(i) + M2(k) -> M3(i_new) + M4(k_new)

    Parameters
    ----------
    molecule1 : Molecule
        the molecule M1
    molecule2 : Molecule
        the molecule M2
    molecule_new1 : Molecule
        the molecule M3
    molecule_new2 : Molecule
        the molecule M4   
    T : float
        the temperature of the mixture
    T1_1 : float
        the temperature of the first vibrational level of the molecule M1
    T1_2 : float
        the temperature of the first vibrational level of the molecule M2
    T1_new1 : float
        the temperature of the first vibrational level of the molecule M3
    T1_new2 : float
        the temperature of the first vibrational level of the molecule M4
    n_molecule1 : float
        the numeric density of molecules of species M1
    n_molecule2 : float
        the numeric density of molecules of species M2
    n_molecule_new1 : float
        the numeric density of molecules of species M3
    n_molecule_new2 : float
        the numeric density of molecules of species M4
    i : int
        the vibrational level of molecule M1
    k : int
        the vibrational level of molecule M2
    i_new : int
        the vibrational level of molecule M1
    k_new : int
        the vibrational level of molecule M2

    Returns
    -------
    float
        The generalized thermodynamic force for a bimolecular chemical exchange reaction

    """
    return raw_Gamma_22(molecule1.vibr[1], molecule2.vibr[1], molecule_new1.vibr[1], molecule_new2.vibr[1],
                        molecule1.Z_vibr(T, T1_1), molecule2.Z_vibr(T, T1_2),
                        molecule_new1.Z_vibr(T, T1_new1), molecule_new2.Z_vibr(T, T1_new2),
                        molecule1.mass, molecule2.mass, molecule_new1.mass, molecule_new2.mass,
                        molecule1.form, molecule2.form, molecule_new1.form, molecule_new2.form,
                        T, T1_1, T1_2, T1_new1, T1_new2, n_molecule1, n_molecule2, n_molecule_new1, n_molecule_new2,
                        i, k, i_new, k_new)


def Gamma_diss(molecule: Molecule, atom1: Atom, atom2: Atom, T: float, T1: float, n_molecule: float, n_atom1: float,
               n_atom2: float, diss_level: int) -> float:
    """Calculates the generalized thermodynamic force :math:`\\Gamma^{diss}` for a dissociation reaction:
    AB(diss_level) + P -> A + B + P

    Parameters
    ----------
    molecule : Molecule
        the molecule which dissociates
    atom1 : Atom
        atom of the first atomic species which make up the molecule
    atom2 : Atom
        atom of the second atomic species which make up the molecule
    T : float
        the temperature of the mixture
    T1 : float
        the temperature of the first vibrational level of the molecule M
    n_molecule : float
        the numeric density of molecules of species M
    n_atom1 : float
        the numeric density of atoms of species atom1
    n_atom2 : float
        the numeric density of atoms of species atom2
    diss_level : int
        the vibrational level from which the molecule dissociates
        
    Returns
    -------
    float
        The generalized thermodynamic force for a dissociation reaction

    """
    return raw_Gamma_diss(molecule.vibr[1], molecule.Z_int(T, T1), molecule.mass,
                          atom1.mass, atom2.mass, molecule.diss, T, T1, n_molecule, n_atom1, n_atom2, diss_level)


def find_natom_diss_eq(molecule: Molecule, atom1: Atom, atom2: Atom, T: float, n: float, relative: bool=True) -> float:
    """Finds the numeric density of atoms in a binary mixture (A2, A) in vibrational equilibrium (a one-temperature
    distribution is used) at which chemical equilibrium occurs (:math:`\\Gamma^{diss} = 0`)

    Parameters
    ----------
    molecule : Molecule
        the molecule which dissociates
    atom1 : Atom
        atom of the first atomic species which make up the molecule
    atom2 : Atom
        atom of the second atomic species which make up the molecule
    T : float
        the temperature of the mixture
    n : float
        the total numeric density of the mixture
    relative : bool, optional
        if True, returns the relative numeric density of atoms, if False, returns the absolute numeric density of atoms,
        defaults to True

    Returns
    -------
    float
        Numeric density of atoms at which chemical equilibrium occurs in the mixture
    """
    return raw_find_natom_diss_eq(molecule.Z_int(T, T), molecule.mass, atom1.mass, atom2.mass,
                                  molecule.diss, T, n, relative)


def raw_Gamma_VT(vibr_one: float, T: float, T1: float, delta: int=-1) -> float:
    """Calculates the generalized thermodynamic force :math:`\\Gamma^{VT}` for a VT transition:
    M(i) + P -> M(i+delta) + P, *raw* version

    Parameters
    ----------
    vibr_one : float
        the dimensional energy of the first vibrational level of the molecule undergoing the transition
    T : float
        the temperature of the mixture
    T1 : float
        the temperature of the first vibrational level of the molecule M
    delta : int
        the change in vibrational level

    Returns
    -------
    float
        The generalized thermodynamic force for a VT transition

    """
    return 1.0 - np.exp((vibr_one * delta * (1.0 / T - 1.0 / T1)) / constants.k)


def raw_Gamma_VV(vibr_one1: float, vibr_one2: float, T: float, T1_1: float, T1_2: float,
                 i_delta: int, k_delta: int) -> float:
    """Calculates the generalized thermodynamic force :math:`\\Gamma^{VV}` for a VV transition:
    M1(i) + M2(k) -> M1(i+i_delta) + M2(k+k_delta), *raw* version

    Parameters
    ----------
    vibr_one1 : float
        the dimensional energy of the first vibrational level of the molecule M1
    vibr_one2 : float
        the dimensional energy of the first vibrational level of the molecule M2
    T : float
        the temperature of the mixture
    T1_1 : float
        the temperature of the first vibrational level of the molecule M1
    T1_2 : float
        the temperature of the first vibrational level of the molecule M2
    i_delta : int
        the change in vibrational level of molecule M1
    k_delta : int
        the change in vibrational level of molecule M2

    Returns
    -------
    float
        The generalized thermodynamic force for a VV transition

    """
    add = i_delta * vibr_one1 * (1.0 - T / T1_1) + k_delta * vibr_one2 * (1.0 - T / T1_2)
    return 1.0 - np.exp(add / (constants.k * T))


def raw_Gamma_22(vibr_one1: float, vibr_one2: float, vibr_one_new1: float, vibr_one_new2: float,
                 Z_int1: float, Z_int2: float, Z_int_new1: float, Z_int_new2: float,
                 mass1: float, mass2: float, mass_new1: float, mass_new2: float,
                 form1: float, form2: float, form_new1: float, form_new2: float,
                 T: float, T1_1: float, T1_2: float, T1_new1: float, T1_new2: float, n_molecule1: float,
                 n_molecule2: float,  n_molecule_new1: float, n_molecule_new2: float,
                 i: int, k: int, i_new: int, k_new: int) -> float:
    """Calculates the generalized thermodynamic force :math:`\\Gamma^{2\leftrightarrows2}` for a bimolecular
    exchange reaction:
    M1(i) + M2(k) -> M3(i_new) + M4(k_new), *raw* version

    Parameters
    ----------
    vibr_one1 : float
        the dimensional energy of the first vibrational level of the molecule M1
    vibr_one2 : float
        the dimensional energy of the first vibrational level of the molecule M2
    vibr_one_new1 : float
        the dimensional energy of the first vibrational level of the molecule M3
    vibr_one_new2 : float
        the dimensional energy of the first vibrational level of the molecule M4
    Z_int1 : float
        the value of the internal partition function of the molecule M1
    Z_int2 : float
        the value of the internal partition function of the molecule M2
    Z_int_new1 : float
        the value of the internal partition function of the molecule M3
    Z_int_new2 : float
        the value of the internal partition function of the molecule M4
    mass1 : float
        the mass of the molecule M1
    mass2 : float
        the mass of the molecule M2
    mass_new1 : float
        the mass of the molecule M3
    mass_new2 : float
        the mass of the molecule M4
    form1 : float
        the formation energy of the molecule M1
    form2 : float
        the formation energy of the molecule M2
    form_new1 : float
        the formation energy of the molecule M3
    form_new2 : float
        the formation energy of the molecule M4
    T : float
        the temperature of the mixture
    T1_1 : float
        the temperature of the first vibrational level of the molecule M1
    T1_2 : float
        the temperature of the first vibrational level of the molecule M2
    T1_new1 : float
        the temperature of the first vibrational level of the molecule M3
    T1_new2 : float
        the temperature of the first vibrational level of the molecule M4
    n_molecule1 : float
        the numeric density of molecules of species M1
    n_molecule2 : float
        the numeric density of molecules of species M2
    n_molecule_new1 : float
        the numeric density of molecules of species M3
    n_molecule_new2 : float
        the numeric density of molecules of species M4
    i : int
        the vibrational level of molecule M1
    k : int
        the vibrational level of molecule M2
    i_new : int
        the vibrational level of molecule M1
    k_new : int
        the vibrational level of molecule M2

    Returns
    -------
    float
        The generalized thermodynamic force for a bimolecular chemical exchange reaction

    """
    kT = constants.k * T
    add = Z_int1 * Z_int2 / (Z_int_new1 * Z_int_new2)
    add *= (n_molecule1 * n_molecule2) / (n_molecule_new1 * n_molecule_new2)
    add *= (mass1 * mass2 / (mass_new1 * mass_new2)) ** 1.5
    add *= np.exp(form_new1 / kT + form_new2 / kT - form1 / kT - form2 / kT)
    add *= np.exp(vibr_one1 * i * (1.0 / (constants.k * T1_1) - 1.0 / kT)
                  + vibr_one2 * k * (1.0 / (constants.k * T1_2) - 1.0 / kT)
                  - vibr_one_new1 * i_new * (1.0 / (constants.k * T1_new1) - 1.0 / kT)
                  - vibr_one_new2 * k_new * (1.0 / (constants.k * T1_new2) - 1.0 / kT))
    return 1.0 - add


def raw_Gamma_diss(vibr_one: float, Z_int: float, mass_molecule: float, mass_atom1: float, mass_atom2: float,
                   molecule_diss: float, T: float, T1: float, n_molecule: float, n_atom1: float,
                   n_atom2: float, diss_level: int) -> float:
    """Calculates the generalized thermodynamic force :math:`\\Gamma^{diss}` for a dissociation reaction:
    AB(diss_level) + P -> A + B + P, *raw* version

    Parameters
    ----------
    vibr_one : float
        the dimensional energy of the first vibrational level of the molecule which dissociates
    Z_int : float
        the value of the internal partition function of the molecule which dissociates
    mass_molecule : float
        the mass of the molecule which dissociates
    mass_atom1 : float
        the mass of the first atom product of dissociation
    mass_atom2 : float
        the mass of the second atom product of dissociation
    molecule_diss : float
        the dissociation energy of the molecule which dissociates
    T : float
        the temperature of the mixture
    T1 : float
        the temperature of the first vibrational level of the molecule M
    n_molecule : float
        the numeric density of molecules of species M
    n_atom1 : float
        the numeric density of atoms of species atom1
    n_atom2 : float
        the numeric density of atoms of species atom2
    diss_level : int
        the vibrational level from which the molecule dissociates

    Returns
    -------
    float
        The generalized thermodynamic force for a dissociation reaction

    """
    add = Z_int * (n_atom1 * n_atom2) * (constants.h ** 3)\
                                      * ((mass_molecule / (2.0 * mass_atom1 * mass_atom2 * constants.pi
                                                               * constants.k * T)) ** 1.5) / n_molecule
    add = add * np.exp(molecule_diss / (constants.k * T) + vibr_one * ((1.0 / T1 - 1.0 / T) / constants.k)
                       * diss_level)
    return 1.0 - add


def raw_find_natom_diss_eq(Z_int: float, mass_molecule: float, mass_atom1: float, mass_atom2: float,
                           molecule_diss: float,  T: float, n: float, relative: bool=True) -> float:
    """Finds the numeric density of atoms in a binary mixture (A2, A) in vibrational equilibrium (a one-temperature
    distribution is used) at which chemical equilibrium occurs (:math:`\\Gamma^{diss} = 0`), *raw* version

    Parameters
    ----------
    Z_int : float
        the value of the internal partition function of the molecule which dissociates
    mass_molecule : float
        the mass of the molecule which dissociates
    mass_atom1 : float
        the mass of the first atom product of dissociation
    mass_atom2 : float
        the mass of the second atom product of dissociation
    molecule_diss : float
        the dissociation energy of the molecule which dissociates
    T : float
        the temperature of the mixture
    n : float
        the total numeric density of the mixture
    relative : bool, optional
        if True, returns the relative numeric density of atoms, if False, returns the absolute numeric density of atoms,
        defaults to True

    Returns
    -------
    float
        Numeric density of atoms at which chemical equilibrium occurs in the mixture
    """
    xatom = brentq(Gamma_diss_binary_equilibrium_xatom, 0, 1, xtol=0.00001, maxiter=1000,
                   args=(Z_int, mass_molecule, mass_atom1, mass_atom2, molecule_diss, T, n))
    if relative is True:
        return xatom
    else:
        return n * xatom


def Gamma_diss_binary_equilibrium_xatom(x_atom: float, Z_int: float, mass_molecule: float,
                                        mass_atom1: float, mass_atom2: float, molecule_diss: float,
                                        T: float, n: float) -> float:
    """A helper function, which calculates Gamma_diss (multiplied by the numeric density of the molecules) for a binary
    mixture (A2, A) in vibrational equilibrium (a one-temperature distribution is used): 2A + A -> 3A

    Parameters
    ----------
    x_atom : float
        the relative numeric density of atoms
    Z_int : float
        the value of the internal partition function of the molecule which dissociates
    mass_molecule : float
        the mass of the molecule which dissociates
    mass_atom1 : float
        the mass of the first atom product of dissociation
    mass_atom2 : float
        the mass of the second atom product of dissociation
    molecule_diss : float
        the dissociation energy of the molecule which dissociates
    T : float
        the temperature of the mixture
    n : float
        the total numeric density of the mixture

    Returns
    -------
    float
        Gamma_diss multiplied by the numeric density of the molecules
    """
    n_atom = x_atom * n
    mult = Z_int * (n_atom ** 2) * (constants.h ** 3)\
                                 * ((mass_molecule / (2.0 * mass_atom1 * mass_atom2 * constants.pi
                                                               * constants.k * T)) ** 1.5)\
                                 * np.exp(molecule_diss / (constants.k * T))
    return (n - n_atom) - mult