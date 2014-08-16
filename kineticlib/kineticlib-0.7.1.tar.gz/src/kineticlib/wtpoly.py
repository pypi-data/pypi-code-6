"""Contains functions for working with Waldman-Trubenbacher polynomials
"""
__author__ = 'George Oblapenko'
__license__ = "GPL"
__maintainer__ = "George Oblapenko"
__email__ = "kunstmord@kunstmord.com"
__status__ = "Production"

from .particles import Molecule


def Y_poly_norm(T: float, T1: float, molecule: Molecule, F: float=0.0) -> float:
    """Calculates the square of the "norm" of the Waldman Trubenbacher polynomial of the following form:
    :math:`P_{ij} = -[\\varepsilon_{ij} / kT - i F]'`, where the :math:`i` is the vibrational level of the molecule,
    :math:`j` is the rotational level of the molecule, :math:`[A]' = A - <A>_{int}`, where :math:`<>_{int}`
    denotes averaging over the internal spectrum.
    The square of the "norm" is defined as: :math:`||P_{ij}|| = \\left<P_{ij}^{2} \\right>_{int}`

    Parameters
    ----------
    T : float
        the temperature of the mixture
    T1 : float
        the temperature of the first vibrational level of the molecule for which the polynomial is used
    molecule : Molecule
        the molecule for which the polynomial is used
    F : float
        the constant appearing in the expression for the polynomial, defaults to 0.0

    Returns
    -------
    float
        The square of the "norm" of the Waldman Trubenbacher polynomial
    """
    return molecule.avg_vibr_energy_sq(T, T1, False) + molecule.avg_rot_energy_sq(T, False)\
                                                     + molecule.avg_i_sq(T, T1) * (F ** 2)\
                                                     + 2 * molecule.avg_vibr_energy(T, T1, False)\
                                                         * molecule.avg_rot_energy(T, False)\
                                                     - 2 * molecule.avg_vibr_energy_i(T, T1, False) * F\
                                                     - 2 * molecule.avg_rot_energy(T, False) * molecule.avg_i(T, T1)\
                                                                                             * F\
                                                     - (Y_simple_avg(T, T1, molecule, F) ** 2)


def Y_simple_avg(T: float, T1: float, molecule: Molecule, F: float=0.0) -> float:
    """Calculates the averaging over the internal energy spectrum of the following expression:
    :math:`\\varepsilon_{ij} / kT - i F`

    Parameters
    ----------
    T : float
        the temperature of the mixture
    T1 : float
        the temperature of the first vibrational level of the molecule for which the polynomial is used
    molecule : Molecule
        the molecule for which the polynomial is used
    F : float
        the constant appearing in the expression for the polynomial, defaults to 0.0

    Returns
    -------
    float
        The averaging over the internal energy spectrum Waldman Trubenbacher polynomial
    """
    return molecule.avg_full_energy(T, T1, False) - molecule.avg_i(T, T1) * F