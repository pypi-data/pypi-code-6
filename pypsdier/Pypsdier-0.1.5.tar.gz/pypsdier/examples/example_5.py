# -*- coding: utf-8 -*-
# Pennicilyn Acilase synthesis with two phase enzyme
import pypsdier
from math import exp

################################################################################
# AUXILIAR DEFINITIONS OF REACTION AND ENZIMATIC CHARGE
################################################################################
def ReaccionPenG(Cs, E0, k, K, Ks, K1, K2):
  """
  ReaccionPenG(Cs, E0, params)
  Cs = PenG [mM], AFA [mM], 6-APA [mM]
  E0 [mM]
  params = k [1/s], K [mM], Ks [mM], K1 [mM], K2 [mM]
  """
  PenG, AFA, APA6 = Cs
  mcd = K+PenG+PenG*PenG/Ks+K*AFA/K1+K*APA6/K2+PenG*APA6/K2+K*AFA*APA6/(K1*K2)
  v_S = k*E0*PenG/mcd
  v = (-v_S, v_S, v_S )
  return v

def CatalystEnzymeConcentration(t, E0=0.200, alpha=0.327, k1=(1.686/3600.), k2=(0.25/3600.)):
  e1 = (1+alpha*k1/(k2-k1))*exp(-k1*t)
  e2 = (alpha*k1/(k2-k1))*exp(-k2*t)
  return E0*(e1+e2) 

################################################################################
# THE DICT params WILL CONTAIN ALL THE REQUIRED INFORMATION
# MUST PROVIDE A UNIQUE SEED FOR THE EXPERIMENT (WILL OVERWRITE FILE IF EXISTS)
# Names, InitialConditions, EffectiveDiffusionCoefficients MUST HAVE THE SAME NUMBER OF ELEMENTS
# Radiuses, RadiusesFrequencies MUST HAVE THE SAME NUMBER OF ELEMENTS
# ReactionParameters NEEDS TO BE COMPATIBLE WITH THE DEFINITION OF THE ReactionFunction
################################################################################
pde_params = {}
pde_params["SeedFile"] = "example_5.rde" # filename where the simulation will be stored
pde_params["SimulationTime"] = 10.*60 # [s], total time to be simulated 
pde_params["SavingTimeStep"] = 1. # [s], saves only one data per second
pde_params["CatalystVolume"]  = 0.200 # [mL], total volume of all catalyst particles in reactor
pde_params["BulkVolume"]  = 40.0  # [mL], bulk volume of the liquid phase
pde_params["Names"] = ('PenG', 'AFA', '6-APA')  # legend for the xls, reports and plots
pde_params["InitialConcentrations"] = (10.0, 0., 0.)   # [mM], initial concentration of substrates and products
pde_params["EffectiveDiffusionCoefficients"] = (5.30E-10, 7.33E-10, 5.89E-10)  # [m2/s], effective diffusion coefficient for substrates and products
pde_params["CatalystParticleRadius"] = (100.E-6,) # [m], list of possible catalyst particle radiuses
pde_params["CatalystParticleRadiusFrequency"] = (1.0,) # [], list of corresponding frequencies of catalyst particle radiuses
pde_params["ReactionFunction"] = ReaccionPenG # function defining the reaction 
pde_params["ReactionParameters"] = 41., 0.13, 821., 1.82, 48.  #[1/s] and [mM]*4  # [1/s], [mM/s], parameters to be used in the reaction function 
pde_params["CatalystEnzymeConcentration"] = CatalystEnzymeConcentration # [mM] can be a float, int or a function returning float or int. 

################################################################################
# SOLVE THE PDE AND SAVE THE RESULT INTO THE SEED
################################################################################
pypsdier.pde(pde_params)
pypsdier.ode(pde_params)
