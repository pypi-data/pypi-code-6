"""Contains functions for loading interaction data for elastic collisions and the Arrhenius dissociation model
"""
__author__ = 'George Oblapenko'
__license__ = "GPL"
__maintainer__ = "George Oblapenko"
__email__ = "kunstmord@kunstmord.com"
__status__ = "Development"


import numpy as np
from csv import reader
from os.path import normcase, join, split
from scipy import constants
from .errors import KineticlibError
from .particles import Particle, MoleculeSTS


def load_elastic_parameters(partner1: Particle, partner2: Particle) -> np.ndarray:
    """Loads interaction parameters for two partners for use in various integrals (loads IPL and VSS
    potential parameters + calculates collision radius, Lennard-Jones :math:`\\varepsilon_{cd}`
    parameter and collision-reduced mass :math:`m_{cd}`)
    from the file interactions.csv
    The values are stored in the file as the following units:
    :math:`\\phi_{0}` - electron-volt, :math:`\\beta` - 1 / Angstrom; all other values are stored in SI units

    Parameters
    ----------
    partner1 : Particle (or any subclass)
        the first collision partner
    partner2 : Particle (or any subclass)
        the second collision partner

    Returns
    -------
    np.ndarray

        An array, which contains the following quantities:
            0. The collision-reduced mass :math:`m_{cd}`
            #. The collision diameter :math:`\\sigma_{cd}`
            #. The Lennard-Jones epsilon parameter :math:`\\varepsilon_{cd}`, divided by Boltzmann's constant
            #. The :math:`\\phi_{0}` parameter for the IPL potential, divided by Boltzmann's constant
            #. The :math:`\\beta` parameter for the IPL potential
            #. The :math:`C` parameter for the VSS model for the :math:`\\Omega^{(1,1)}` integral
            #. The :math:`\\omega` parameter for the VSS model for the :math:`\\Omega^{(1,1)}` integral
            #. The :math:`C` parameter for the VSS model for the :math:`\\Omega^{(2,2)}` integral
            #. The :math:`\\omega` parameter for the VSS model for the :math:`\\Omega^{(2,2)}` integral
            #. The :math:`C` parameter for the VSS model for the :math:`\\Omega_{tot}` integral
            #. The :math:`\\omega` parameter for the VSS model for the :math:`\\Omega_{tot}` integral
            #. The :math:`C` parameter for the VSS model for the deflection angle
            #. The :math:`\\omega` parameter for the VSS model for the deflection angle
            #. The :math:`\\beta` parameter for the ESA model
            #. The :math:`\\varepsilon_{0}` parameter for the ESA model
            #. The :math:`r_{e}` parameter for the ESA model

    Notes
    -----
    Deflection angle parameters are needed to calculate amount of collisions needed to establish rotational
    equilibrium using the VSS model
    """
    m = (partner1.mass * partner2.mass)/(partner1.mass + partner2.mass)
    sigma = (partner1.LJs + partner2.LJs) * 0.5
    eps = np.sqrt(partner1.LJe * partner2.LJe * ((partner1.LJs * partner2.LJs) ** 6)) / (sigma ** 6)
    this_dir, this_filename = split(__file__)
    csv_file_object = reader(open(join(this_dir, normcase('data/models/interactions.csv')), 'r'))
    next(csv_file_object)
    res = np.zeros(16)
    res[:3] = [m, sigma, eps]

    for row in csv_file_object:
        if (row[0] == partner1.name and row[1] == partner2.name) or\
                (row[1] == partner1.name and row[0] == partner2.name):
            rd = np.array(row[2:]).astype(np.float64)
            # res[3:] = [rd[0], rd[1], rd[2], rd[3], rd[4], rd[5], rd[6], rd[7], rd[8], rd[9]]
            res[3:] = rd[:]

    res[3] *= constants.physical_constants['electron volt'][0] / constants.k
    res[4] *= 1.0 / constants.physical_constants['Angstrom star'][0]
    res[14] *= constants.physical_constants['electron volt'][0] / 1000.0
    res[15] *= constants.physical_constants['Angstrom star'][0]
    return res


def load_dissociation_parameters(molecule: MoleculeSTS, partner: Particle) -> np.ndarray:
    """Loads dissociation model parameters for Arrhenius model for the reaction
    molecule + partner -> atom1 + atom2 + partner.
    The model for the equilibrium reaction rate coefficient is considered to be as follows:
    :math:`k_{diss} = A T^{n}`

    Parameters
    ----------
    molecule_name : MoleculeSTS
        the molecule which dissociates
    partner_name : Particle
        the collision partner

    Returns
    -------
    np.ndarray
        An array, which contains the following quantities:
        result[0] - Arrhenius model n parameter
        result[1] - Arrhenius model A parameter

    Raises
    ------
    KineticlibError
        if no dissociation data is found for these collision partners
    """
    molecule_name = molecule.name
    partner_name = partner.name
    this_dir, this_filename = split(__file__)
    csv_file_object = reader(open(join(this_dir, normcase('data/models/dissociation.csv')), 'r'))
    next(csv_file_object)
    found = False
    for row in csv_file_object:
        if row[0] == molecule_name and row[1] == partner_name:
            dat = [row[2], row[3]]
            res = np.array(dat).astype(np.float64)
            res[1] *= (10 ** 16) / constants.N_A
            return res
    if found is False:
        raise KineticlibError('No dissociation data found for the reaction partners '
                              + molecule_name + ', ' + partner_name)