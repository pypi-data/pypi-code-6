#!/usr/bin/env python
#coding=utf-8

# Part of the PsychoPy library
# Copyright (C) 2014 Jonathan Peirce
# Distributed under the terms of the GNU General Public License (GPL).

"""This demo shows you how to use a CRS BitsSharp device with PsychoPy

As of version 1.81.00 PsychoPy can make use of the Bits# in any of its rendering
modes provided that your graphics card supports OpenGL framebuffer objects.

You don't need to worry about setting the high- and low-bit pixels. Just draw as
normal and PsychoPy will do the conversions for you
"""

from psychopy import visual, core, event
from psychopy.hardware import crs

def _oneTest(LUT):
    global win, bits, stim
    win.setGammaTable(LUT)
    stim.draw()
    win.flip()
    pixels = 
    
def correct(screen=1, maxiterations = 1000, errCorrFactor = 0.03 # amount of correction done for each iteration
    videoLinesToUse = 1, # defines the video lines to use. Counted from the top.
    videoLineOffset = 0, #  horizontal start position
    buffsize = maxiterations,
    ditherIterations = 100, #number of repeats (successful) to check for dithering
    ):
    global win, bits, stim #NB these are just global to this file!
    
    win = visual.Window(screen=1, screen = screen, fullscr=True, useFBO=True)
    bits = crs.BitsSharp(win, mode='status')
    stim = visual.ImageStim(win)
    #create standard options
    LUTs = {}
    LUTs['intel'] = repmat(linspace(.05,.95,256),1,3)
    LUTs['logical'] = repmat(linspace(0,1,256),1,3)
    #mac mini with ATI HD 6630M
    LUTs['mac mini'] = repmat(linspace(0,1,256),1,3)
    LUTs['mac mini'][:55] += 0.5**13
    LUTs['mac mini'][191:] -= 0.5**13
    
    for currentLUT in 
    win.setGammaTable(currentLUT)
    
   