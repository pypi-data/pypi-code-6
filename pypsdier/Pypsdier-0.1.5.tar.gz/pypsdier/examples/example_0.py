# -*- coding: utf-8 -*-
import pypsdier
from math import exp

"""
Description: This is a extremely basic example. We will have a unique fictional 
substract being consumed with a reaction modelled by Michaelis Menten equation. 
Values for the parameters have been handpicked for a quick simulation,
only for numerical reasons.
It has constant catalyst enzyme Concentration, and the enzymes are kept in
a unique catalyst of particle radii 100 [um].
"""
################################################################################
# AUXILIAR DEFINITIONS OF REACTION AND ENZIMATIC CHARGE
################################################################################
def MichaelisMenten(Cs, E0, k, K):
  """
  Definition for Michaelis Menten reaction with params k [1/s] and K [mM]
  """
  S, = Cs
  v_S = k*E0*S/(K+S)
  v = (-v_S,)
  return v

################################################################################
# THE DICT params WILL CONTAIN ALL THE REQUIRED INFORMATION
# MUST PROVIDE A UNIQUE SEED FOR THE EXPERIMENT (WILL OVERWRITE FILE IF EXISTS)
# Names, InitialConditions, EffectiveDiffusionCoefficients MUST HAVE THE SAME NUMBER OF ELEMENTS
# Radiuses, RadiusesFrequencies MUST HAVE THE SAME NUMBER OF ELEMENTS
# ReactionParameters NEEDS TO BE COMPATIBLE WITH THE DEFINITION OF THE ReactionFunction
################################################################################
params = {}
params["SeedFile"] = "example_0.rde" # filename where the simulation will be stored
params["SimulationTime"] = 30*60. # [s], total time to be simulated 
params["SavingTimeStep"] = 60. # [s], saves only one data per second
params["CatalystVolume"]  = 0.01 # [mL], total volume of all catalyst particles in reactor
params["BulkVolume"]  = 40.0  # [mL], bulk volume of the liquid phase
params["Names"] = ('Substrat',)  # legend for the xls, reports and plots
params["InitialConcentrations"] = (1.0,)   # [mM], initial concentration of substrates and products
params["EffectiveDiffusionCoefficients"] = (1.0E-9,)  # [m2/s], effective diffusion coefficient for substrates and products
params["CatalystParticleRadius"] = [100.E-6] # [m], list of possible catalyst particle radiuses
params["CatalystParticleRadiusFrequency"] = [1.0] # [], list of corresponding frequencies of catalyst particle radiuses
params["ReactionFunction"] = MichaelisMenten # function defining the reaction 
params["ReactionParameters"] = (41 , 0.13)   # [1/s], [mM/s], parameters to be used in the reaction function after Cs and E0 
params["CatalystEnzymeConcentration"] = 0.5 # [mM] can be a float, int or a function returning float or int. 

################################################################################
# SOLVE THE PDE AND SAVE THE RESULT INTO THE SEED
################################################################################
pypsdier.pde(params)
pypsdier.ode(params)
