"""Contains functions for calculating generalized affinities and equilibrium concentrations in a binary mixture"""
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
    """Calculates the generalized thermodynamic force Gamma_VT for a VT transition: M(i) + P -> M(i+delta) + P

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
    return 1.0 - np.exp((molecule.vibr_one() * delta * (1.0 / T - 1.0 / T1)) / constants.k)


def Gamma_VV(molecule1: Molecule, molecule2: Molecule, T: float, T1_1: float, T1_2: float,
             i_delta: int, k_delta: int) -> float:
    """Calculates the generalized thermodynamic force Gamma_VV for a VV transition:
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
    add = i_delta * molecule1.vibr_one() * (1.0 - T / T1_1) + k_delta * molecule2.vibr_one() * (1.0 - T / T1_2)
    return 1.0 - np.exp(add / (constants.k * T))


def Gamma_22(molecule1: Molecule, molecule2: Molecule, molecule_new1: Molecule, molecule_new2: Molecule, T: float,
             T1_1: float, T1_2: float, T1_new1: float, T1_new2: float, n_molecule1: float, n_molecule2: float,
             n_molecule_new1: float, n_molecule_new2: float, i: int, k: int, i_new: int, k_new: int) -> float:
    """

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
    kT = constants.k * T
    add = molecule1.Z_vibr(T, T1_1) * molecule1.Z_rot(T) * molecule2.Z_vibr(T, T1_2) * molecule2.Z_rot(T)
    add /= molecule_new1.Z_vibr(T, T1_new1) * molecule_new1.Z_rot(T)\
           * molecule_new2.Z_vibr(T, T1_new2) * molecule_new2.Z_rot(T)
    add *= (n_molecule1 * n_molecule2) / (n_molecule_new1 * n_molecule_new2)
    add *= (molecule1.mass * molecule2.mass / (molecule_new1.mass * molecule_new2.mass)) ** 1.5
    add *= np.exp(molecule_new1.form / kT + molecule_new2.form / kT - molecule1.form / kT - molecule2.form / kT)
    add *= np.exp(molecule1.vibr_one() * i * (1.0 / (constants.k * T1_1) - 1.0 / kT)
                  + molecule2.vibr_one() * k * (1.0 / (constants.k * T1_2) - 1.0 / kT)
                  - molecule_new1.vibr_one() * i_new * (1.0 / (constants.k * T1_new1) - 1.0 / kT)
                  - molecule_new2.vibr_one() * k_new * (1.0 / (constants.k * T1_new2) - 1.0 / kT))
    return 1.0 - add


def Gamma_diss(molecule: Molecule, atom1: Atom, atom2: Atom, T: float, T1: float, n_molecule: float, n_atom1: float,
               n_atom2: float, diss_level: int) -> float:
    """Calculates the generalized thermodynamic force Gamma_diss for a dissociation reaction:
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
    add = molecule.Z_vibr(T, T1) * molecule.Z_rot(T) * (n_atom1 * n_atom2) * (constants.h ** 3)\
                                 * ((molecule.mass / (2.0 * atom1.mass * atom2.mass * constants.pi
                                                      * constants.k * T)) ** 1.5) / n_molecule
    add = add * np.exp(molecule.diss / (constants.k * T) + molecule.vibr_one() * ((1.0 / T1 - 1.0 / T) / constants.k)
                       * diss_level)
    return 1.0 - add


def Gamma_diss_binary_equilibrium_xatom(x_atom: float, molecule: Molecule, atom1: Atom, atom2: Atom,
                                        T: float, n: float) -> float:
    """A helper function, which calculates Gamma_diss (multiplied by the numeric density of the molecules) for a binary
    mixture (A2, A) in vibrational equilibrium (a one-temperature distribution is used): 2A + A -> 3A

    Parameters
    ----------
    x_atom : float
        the relative numeric density of atoms
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
        
    Returns
    -------
    float
        Gamma_diss multiplied by the numeric density of the molecules
    """
    n_atom = x_atom * n
    mult = molecule.Z_vibr(T, T) * molecule.Z_rot(T) * (n_atom ** 2) * (constants.h ** 3)\
                                 * ((molecule.mass / (2.0 * atom1.mass * atom2.mass * constants.pi
                                                      * constants.k * T)) ** 1.5)\
                                 * np.exp(molecule.diss / (constants.k * T))
    return (n - n_atom) - mult


def find_natom_diss_eq(molecule: Molecule, atom1: Atom, atom2: Atom, T: float, n: float, relative: bool=True) -> float:
    """Finds the numeric density of atoms in a binary mixture (A2, A) in vibrational equilibrium (a one-temperature distribution is used)
    at which chemical equilibrium occurs (Gamma_diss = 0)

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
    if relative is True:
        return brentq(Gamma_diss_binary_equilibrium_xatom, 0, 1, xtol=0.00001, maxiter=1000, args=(molecule, atom1,
                                                                                                   atom2, T, n))
    else:
        return n * brentq(Gamma_diss_binary_equilibrium_xatom, 0, 1, xtol=0.00001, maxiter=1000, args=(molecule, atom1,
                                                                                                       atom2, T, n))