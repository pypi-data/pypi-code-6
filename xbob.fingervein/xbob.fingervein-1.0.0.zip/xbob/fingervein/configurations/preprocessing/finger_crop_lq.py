#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pedro Tome <Pedro.Tome@idiap.ch>

import xbob.fingervein

# Contour localization mask 
CONTOUR_MASK_HEIGHT = 4 # Height of the mask
CONTOUR_MASK_WIDTH = 40 # Width of the mask

HISTOGRAM_EQUALIZATION = False

PADDING_OFFSET = 5
PADDING_THRESHOLD = 0.2 #Threshold for padding black zones

GPU_ACCELERATION = False

# define the preprocessor
preprocessor = xbob.fingervein.preprocessing.FingerCrop(
	mask_h =CONTOUR_MASK_HEIGHT,
  	mask_w =CONTOUR_MASK_WIDTH,
	heq = HISTOGRAM_EQUALIZATION,
	padding_offset = PADDING_OFFSET,
	padding_threshold = PADDING_THRESHOLD,
	gpu = GPU_ACCELERATION
)

