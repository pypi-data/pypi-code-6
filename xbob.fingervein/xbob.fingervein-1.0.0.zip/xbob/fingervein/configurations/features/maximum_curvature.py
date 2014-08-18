#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pedro Tome <Pedro.Tome@idiap.ch>

import xbob.fingervein

# Parameters 
SIGMA_DERIVATES = 5 #Sigma used for determining derivatives

GPU_ACCELERATION = False

#Define feature extractor
feature_extractor = xbob.fingervein.features.MaximumCurvature(
	sigma = SIGMA_DERIVATES,
	gpu = GPU_ACCELERATION
	
)

