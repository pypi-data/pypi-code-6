#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pedro Tome <Pedro.Tome@idiap.ch>

# Copyright (C) 2014 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import bob
import numpy
import math
#from math import pi 
#from mumpy import sqrt
import scipy.signal
from facereclib.features.Extractor import Extractor
from .. import utils

class MaximumCurvature (Extractor):
  
  """MiuraMax feature extractor based on 
    N. Miura, A. Nagasaka, and T. Miyatake, Extraction of Finger-Vein Pattern Using Maximum Curvature Points in Image Profiles. 
    Proceedings on IAPR conference on machine vision applications, 9 (2005), pp. 347--350    
  """
  
  
  def __init__(
      self,
      sigma = 5, #Sigma used for determining derivatives
      gpu = False
  ):

    # call base class constructor
    Extractor.__init__(
        self,
        sigma = sigma,
        gpu = gpu
    )
    
    # block parameters
    self.sigma = sigma
    self.gpu = gpu
  
    
  def maximum_curvature(self, image, mask):    
    """Computes and returns the Maximum Curvature features for the given input fingervein image"""
   
    finger_mask = numpy.zeros(mask.shape)
    finger_mask[mask == True] = 1 
   
    winsize = numpy.ceil(4*self.sigma)
    
    x = numpy.arange(-winsize, winsize+1)
    y = numpy.arange(-winsize, winsize+1)
    X, Y = numpy.meshgrid(x, y)
        
    h = (1/(2*math.pi*self.sigma**2))*numpy.exp(-(X**2 + Y**2)/(2*self.sigma**2))
    hx = (-X/(self.sigma**2))*h
    hxx = ((X**2 - self.sigma**2)/(self.sigma**4))*h
    hy = hx.T
    hyy = hxx.T
    hxy = ((X*Y)/(self.sigma**4))*h
        
    # Do the actual filtering
        
    fx = utils.imfilter(image, hx, self.gpu, conv=False)
    fxx = utils.imfilter(image, hxx, self.gpu, conv=False)
    fy = utils.imfilter(image, hy, self.gpu, conv=False)
    fyy = utils.imfilter(image, hyy, self.gpu, conv=False)
    fxy = utils.imfilter(image, hxy, self.gpu, conv=False)
        
    f1  = 0.5*numpy.sqrt(2)*(fx + fy)   # \  #
    f2  = 0.5*numpy.sqrt(2)*(fx - fy)   # /  #
    f11 = 0.5*fxx + fxy + 0.5*fyy       # \\ #
    f22 = 0.5*fxx - fxy + 0.5*fyy       # // #
  
    img_h, img_w = image.shape  #Image height and width
 
    # Calculate curvatures
    k = numpy.zeros((img_h, img_w, 4))
    k[:,:,0] = (fxx/((1 + fx**2)**(3/2)))*finger_mask  # hor #
    k[:,:,1] = (fyy/((1 + fy**2)**(3/2)))*finger_mask  # ver #
    k[:,:,2] = (f11/((1 + f1**2)**(3/2)))*finger_mask  # \   #
    k[:,:,3] = (f22/((1 + f2**2)**(3/2)))*finger_mask  # /   #
        
    # Scores
    Vt = numpy.zeros(image.shape)
    Wr = 0
            
    # Horizontal direction
    bla = k[:,:,0] > 0
    for y in range(0,img_h):    
        for x in range(0,img_w):    
            if (bla[y,x]):
                Wr = Wr + 1
            if ( Wr > 0 and (x == (img_w-1) or not bla[y,x]) ):
                if (x == (img_w-1)):
                    # Reached edge of image
                    pos_end = x
                else:
                    pos_end = x - 1
                 
                pos_start = pos_end - Wr + 1 # Start pos of concave      
                if (pos_start == pos_end):
                    I=numpy.argmax(k[y,pos_start,0])
                else:                
                    I=numpy.argmax(k[y,pos_start:pos_end+1,0])
                
                pos_max = pos_start + I
                Scr = k[y,pos_max,0]*Wr
                Vt[y,pos_max] = Vt[y,pos_max] + Scr
                Wr = 0                     
                        

    # Vertical direction
    bla = k[:,:,1] > 0
    for x in range(0,img_w):    
        for y in range(0,img_h):    
            if (bla[y,x]):
                Wr = Wr + 1
            if ( Wr > 0 and (y == (img_h-1) or not bla[y,x]) ):
                if (y == (img_h-1)):
                    # Reached edge of image
                    pos_end = y
                else:
                    pos_end = y - 1        
                    
                pos_start = pos_end - Wr + 1 # Start pos of concave
                if (pos_start == pos_end):
                    I=numpy.argmax(k[pos_start,x,1])
                else:
                    I=numpy.argmax(k[pos_start:pos_end+1,x,1])
                
                pos_max = pos_start + I 
                Scr = k[pos_max,x,1]*Wr
                
                Vt[pos_max,x] = Vt[pos_max,x] + Scr
                Wr = 0
                                            
    # Direction: \ #
    bla = k[:,:,2] > 0
    for start in range(0,img_w+img_h-1):
        # Initial values
        if (start <= img_w-1):
            x = start
            y = 0
        else:
            x = 0
            y = start - img_w + 1
        done = False
        
        while (not done):
            if(bla[y,x]):
                Wr = Wr + 1
            
            if ( Wr > 0 and (y == img_h-1 or x == img_w-1 or not bla[y,x]) ):
                if (y == img_h-1 or x == img_w-1):
                    # Reached edge of image
                    pos_x_end = x
                    pos_y_end = y
                else:
                    pos_x_end = x - 1
                    pos_y_end = y - 1
            
                pos_x_start = pos_x_end - Wr + 1
                pos_y_start = pos_y_end - Wr + 1
                               
                if (pos_y_start == pos_y_end and pos_x_start == pos_x_end):
                    d = k[pos_y_start, pos_x_start, 2]
                elif (pos_y_start == pos_y_end):
                    d = numpy.diag(k[pos_y_start, pos_x_start:pos_x_end+1, 2])
                elif (pos_x_start == pos_x_end):
                    d = numpy.diag(k[pos_y_start:pos_y_end+1, pos_x_start, 2])
                else:
                    d = numpy.diag(k[pos_y_start:pos_y_end+1, pos_x_start:pos_x_end+1, 2])
                                
                I = numpy.argmax(d)                 
                
                pos_x_max = pos_x_start + I 
                pos_y_max = pos_y_start + I 
                
                Scr = k[pos_y_max,pos_x_max,2]*Wr
                                
                Vt[pos_y_max,pos_x_max] = Vt[pos_y_max,pos_x_max] + Scr
                Wr = 0
            
            if((x == img_w-1) or (y == img_h-1)):
                done = True
            else:
                x = x + 1
                y = y + 1
                                           
    # Direction: /
    bla = k[:,:,3] > 0
    for start in range(0,img_w+img_h-1):
        # Initial values
        if (start <= (img_w-1)):
            x = start
            y = img_h-1
        else:
            x = 0
            y = img_w+img_h-start-1
        done = False
        
        while (not done):
            if(bla[y,x]):
                Wr = Wr + 1
            if ( Wr > 0 and (y == 0 or x == img_w-1 or not bla[y,x]) ):
                if (y == 0 or x == img_w-1):
                    # Reached edge of image
                    pos_x_end = x
                    pos_y_end = y
                else:
                    pos_x_end = x - 1
                    pos_y_end = y + 1
                
                pos_x_start = pos_x_end - Wr + 1
                pos_y_start = pos_y_end + Wr - 1
                                
                if (pos_y_start == pos_y_end and pos_x_start == pos_x_end):
                    d = k[pos_y_end, pos_x_start, 3]
                elif (pos_y_start == pos_y_end):
                    d = numpy.diag(numpy.flipud(k[pos_y_end, pos_x_start:pos_x_end+1, 3]))
                elif (pos_x_start == pos_x_end):
                    d = numpy.diag(numpy.flipud(k[pos_y_end:pos_y_start+1, pos_x_start, 3]))
                else:
                    d = numpy.diag(numpy.flipud(k[pos_y_end:pos_y_start+1, pos_x_start:pos_x_end+1, 3]))
               
                I = numpy.argmax(d) 
                pos_x_max = pos_x_start + I 
                pos_y_max = pos_y_start - I 
                Scr = k[pos_y_max,pos_x_max,3]*Wr
                Vt[pos_y_max,pos_x_max] = Vt[pos_y_max,pos_x_max] + Scr
                Wr = 0
            
            if((x == img_w-1) or (y == 0)):
                done = True
            else:
                x = x + 1
                y = y - 1   

    ## Connection of vein centres
    Cd = numpy.zeros((img_h, img_w, 4))
    for x in range(2,img_w-3):
        for y in range(2,img_h-3):
            Cd[y,x,0] = min(numpy.amax(Vt[y,x+1:x+3]), numpy.amax(Vt[y,x-2:x]))   # Hor  #
            Cd[y,x,1] = min(numpy.amax(Vt[y+1:y+3,x]), numpy.amax(Vt[y-2:y,x]))   # Vert #
            Cd[y,x,2] = min(numpy.amax(Vt[y-2:y,x-2:x]), numpy.amax(Vt[y+1:y+3,x+1:x+3])) # \  #
            Cd[y,x,3] = min(numpy.amax(Vt[y+1:y+3,x-2:x]), numpy.amax(Vt[y-2:y,x+1:x+3])) # /  #
        
    #Veins
    img_veins = numpy.amax(Cd,axis=2)
    
    # Binarise the vein image
    md = numpy.median(img_veins[img_veins>0])
    img_veins_bin = img_veins > md

    return img_veins_bin.astype(numpy.float64)
       
  
  def __call__(self, image):    
    """Reads the input image, extract the features based on Maximum Curvature of the fingervein image, and writes the resulting template"""
    
    finger_image = image[0]    #Normalized image with or without histogram equalization
    finger_mask = image[1]   
    
    return self.maximum_curvature(finger_image, finger_mask)  
    

  def save_feature(self, feature, feature_file):
    f = bob.io.HDF5File(feature_file, 'w')
    f.set('feature', feature)
            
  def read_feature(self, feature_file):
    f = bob.io.HDF5File(feature_file, 'r')
    image = f.read('feature')
    return (image)

  
    
