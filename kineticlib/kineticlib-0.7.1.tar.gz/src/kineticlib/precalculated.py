"""Functions for calculations of heat capacities and other mixture properties
"""
__author__ = 'George Oblapenko'
__license__ = "GPL"
__maintainer__ = "George Oblapenko"
__email__ = "kunstmord@kunstmord.com"
__status__ = "Development"

from .particles import Molecule, Atom
from scipy import constants


def dUdT(T: float, mixture_components: list) -> float:
    """Calculates the partial derivative of the internal energy of the mixture per unit of mass :math:`U` with respect
    to the flow temperature :math:`T`

    Parameters
    ----------
    T : float
        the temperature of the mixture
    mixture_components : list
        a list of iterables of the following form:

            0. the ``Particle`` subclass (either ``Atom`` or ``Molecule``)
            #. the numeric density of the particle species
            #. optional - the temperature of the first vibrational level, if the particle is of the ``Molecule`` class

    Returns
    -------
    float
        The quantity :math:`\\partial U / \\partial T`
    """
    density = 0.0
    n = 0.0
    curr_dudt = 0.0
    for component in mixture_components:
        density += component[0].mass * component[1]
        n += component[1]
    propmass = density / n
    for component in mixture_components:
        if isinstance(component[0], Molecule):
            curr_dudt += (component[1] / density) * constants.k + \
                         (component[0].mass * component[1] / density) * component[0].E_vibr_dT(T, component[2])
    return curr_dudt + 1.5 * constants.k / propmass


def dUdT1(T: float, T1: float, molecule: Molecule, n_molecule: float, mixture_density: float) -> float:
    """Calculates the partial derivative of the internal energy of the mixture per unit of mass :math:`U` with respect
    to the temperature of the first vibrational level (of a molecular species :math:`c`) :math:`T_{1}^{c}`

    Parameters
    ----------
    T : float
        the temperature of the mixture
    T1 : float
        the temperature of the first vibrational level of the molecular species with respect to which the derivative
        is being calculated
    molecule : Molecule
        the molecule corresponding to the molecular species with respect to which the derivative is being calculated
    n_molecule : float
        the numeric density of the molecular species with respect to which the derivative is being calculated
    mixture_density : float
        the mass density of the mixture

    Returns
    -------
    float
        The quantity :math:`\\partial U / \\partial T_{1}^{c}`
    """
    return molecule.E_vibr_dT1(T, T1) * molecule.mass * n_molecule / mixture_density


def dUdn_atom(T: float, atom: Atom, mixture_density: float) -> float:
    """Calculates the partial derivative of the internal energy of the mixture per unit of mass :math:`U` with respect
    to the numeric density of an atomic species

    Parameters
    ----------
    T : float
        the temperature of the mixture
    atom : Atom
        the atom corresponding to the atomic species with respect to the numeric density of which the derivative
        is being calculated
    mixture_density : float
        the mass density of the mixture

    Returns
    -------
    float
        The quantity :math:`\\partial U / \\partial n_{c}`
    """
    return (1.5 * constants.k * T + atom.form) / mixture_density


def dUdn_molecule(T: float, T1: float, molecule: Molecule, mixture_density: float) -> float:
    """Calculates the partial derivative of the internal energy of the mixture per unit of mass :math:`U` with respect
    to the numeric density of an atomic species

    Parameters
    ----------
    T : float
        the temperature of the mixture
    T1 : float
        the temperature of the first vibrational level of the molecular species with respect to the numeric density of
        which the derivative is being calculated
    molecule : Molecule
        the molecule corresponding to the molecular species with respect to the numeric density of which the derivative
        is being calculated
    mixture_density : float
        the mass density of the mixture

    Returns
    -------
    float
        The quantity :math:`\\partial U / \\partial n_{c}`
    """
    return (1.5 * constants.k * T + molecule.avg_rot_energy(T, True)
            + molecule.avg_vibr_energy(T, T1, True)) / mixture_density