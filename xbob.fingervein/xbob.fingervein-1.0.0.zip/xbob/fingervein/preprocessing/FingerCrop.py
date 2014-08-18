#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: # Pedro Tome <Pedro.Tome@idiap.ch>
# @date: Thu Mar 27 10:21:42 CEST 2014
#
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
from facereclib.preprocessing.Preprocessor import Preprocessor
from .. import utils
from PIL import Image

class FingerCrop (Preprocessor):
  """Fingervein mask based on the implementation:
      E.C. Lee, H.C. Lee and K.R. Park. Finger vein recognition using minutia-based alignment and 
      local binary pattern-based feature extraction. International Journal of Imaging Systems and 
      Technology. Vol. 19, No. 3, pp. 175-178, September 2009.
    """

  def __init__(
      self,
      mask_h = 4, # Height of the mask
      mask_w = 40, # Width of the mask
      heq = True,
      padding_offset = 5,     #Always the same
      padding_threshold = 0.2,  #0 for UTFVP database (high quality), 0.2 for VERA database (low quality)
      gpu = False,
      color_channel = 'gray',    # the color channel to extract from colored images, if colored images are in the database
      **kwargs                   # parameters to be written in the __str__ method
  ):
    """Parameters of the constructor of this preprocessor:

    color_channel
      In case of color images, which color channel should be used?

    mask_h
      Height of the cropped mask of a fingervein image

    mask_w
      Height of the cropped mask of a fingervein image
    
    """

    # call base class constructor
    Preprocessor.__init__(
        self,
        mask_h = mask_h,
        mask_w = mask_w,
        heq = heq,        
        padding_offset = padding_offset,    
        padding_threshold = padding_threshold,
        gpu = gpu,
        color_channel = color_channel,
        **kwargs
    )

    self.mask_h = mask_h
    self.mask_w = mask_w
    self.heq = heq
    self.padding_offset = padding_offset    
    self.padding_threshold = padding_threshold    
    self.gpu = gpu
    self.color_channel = color_channel
     
  def __leemask__(self, image):
    
    img_h,img_w = image.shape
        
    # Determine lower half starting point vertically
    if numpy.mod(img_h,2) == 0:
        half_img_h = img_h/2 + 1
    else:
        half_img_h = numpy.ceil(img_h/2)
    
    # Determine lower half starting point horizontally
    if numpy.mod(img_w,2) == 0:
        half_img_w = img_w/2 + 1
    else:
        half_img_w = numpy.ceil(img_w/2)

    # Construct mask for filtering    
    mask = numpy.zeros((self.mask_h,self.mask_w))
    mask[0:self.mask_h/2,:] = -1
    mask[self.mask_h/2:,:] = 1

    img_filt = utils.imfilter(image, mask, self.gpu, conv=True)
        
    # Upper part of filtred image
    img_filt_up = img_filt[0:half_img_h-1,:]
    y_up = img_filt_up.argmax(axis=0)
    
        # Lower part of filtred image
    img_filt_lo = img_filt[half_img_h-1:,:]
    y_lo = img_filt_lo.argmin(axis=0)
        
    img_filt = utils.imfilter(image, mask.T, self.gpu, conv=True)
        
        # Left part of filtered image
    img_filt_lf = img_filt[:,0:half_img_w]
    y_lf = img_filt_lf.argmax(axis=1)
    
        # Right part of filtred image
    img_filt_rg = img_filt[:,half_img_w:]
    y_rg = img_filt_rg.argmin(axis=1)
        
    finger_mask = numpy.ndarray(image.shape, numpy.bool)    
    finger_mask[:,:] = False
    
    for i in range(0,y_up.size):
        finger_mask[y_up[i]:y_lo[i]+img_filt_lo.shape[0]+1,i] = True
    
    # Left region
    for i in range(0,y_lf.size):
        finger_mask[i,0:y_lf[i]+1] = False
                
    # Right region has always the finger ending, crop the padding with the meadian
    finger_mask[:,numpy.median(y_rg)+img_filt_rg.shape[1]:] = False    
        
    # Extract y-position of finger edges
    edges = numpy.zeros((2,img_w))
    edges[0,:] = y_up
    edges[0,0:round(numpy.mean(y_lf))+1] = edges[0,round(numpy.mean(y_lf))+1] 
       
    
    edges[1,:] = numpy.round(y_lo + img_filt_lo.shape[0])    
    edges[1,0:round(numpy.mean(y_lf))+1] = edges[1,round(numpy.mean(y_lf))+1]    
    
    return (finger_mask, edges)
   
     
  def __leemaskMATLAB__(self, image):

    img_h,img_w = image.shape
        
    # Determine lower half starting point
    if numpy.mod(img_h,2) == 0:
        half_img_h = img_h/2 + 1
    else:
        half_img_h = numpy.ceil(img_h/2)
    
    # Construct mask for filtering    
    mask = numpy.zeros((self.mask_h,self.mask_w))
    mask[0:self.mask_h/2,:] = -1
    mask[self.mask_h/2:,:] = 1

    img_filt = utils.imfilter(image, mask, self.gpu, conv=True)
        
    # Upper part of filtred image
    img_filt_up = img_filt[0:numpy.floor(img_h/2),:]
    y_up = img_filt_up.argmax(axis=0)

    # Lower part of filtred image
    img_filt_lo = img_filt[half_img_h-1:,:]
    y_lo = img_filt_lo.argmin(axis=0)
    
    for i in range(0,y_up.size):
        img_filt[y_up[i]:y_lo[i]+img_filt_lo.shape[0],i]=1
    
    finger_mask = numpy.ndarray(image.shape, numpy.bool)    
    finger_mask[:,:] = False
    
    finger_mask[img_filt==1] = True
  
    # Extract y-position of finger edges
    edges = numpy.zeros((2,img_w))
    edges[0,:] = y_up
    edges[1,:] = numpy.round(y_lo + img_filt_lo.shape[0])    
    
    return (finger_mask, edges)
 

  def __huangnormalization__(self, image, mask, edges):

    img_h, img_w = image.shape

    bl = (edges[0,:] + edges[1,:])/2  # Finger base line
    x = numpy.arange(0,img_w)
    A = numpy.vstack([x, numpy.ones(len(x))]).T
    
    # Fit a straight line through the base line points
    w = numpy.linalg.lstsq(A,bl)[0] # obtaining the parameters
      
    angle = -1*math.atan(w[0])  # Rotation
    tr = img_h/2 - w[1]         # Translation
    scale = 1.0                 # Scale
    
    #Affine transformation parameters    
    sx=sy=scale
    cosine = math.cos(angle)
    sine = math.sin(angle)
    
    a = cosine/sx
    b = -sine/sy
    #b = sine/sx
    c = 0 #Translation in x
    
    d = sine/sx
    e = cosine/sy
    f = tr #Translation in y
    #d = -sine/sy
    #e = cosine/sy
    #f = 0 
    
    g = 0 
    h = 0  
    #h=tr    
    i = 1        
    
    T = numpy.matrix([[a,b,c],[d,e,f],[g,h,i]])
    Tinv = numpy.linalg.inv(T)
    Tinvtuple = (Tinv[0,0],Tinv[0,1], Tinv[0,2], Tinv[1,0],Tinv[1,1],Tinv[1,2])
    
    img=Image.fromarray(image)
    image_norm = img.transform(img.size, Image.AFFINE, Tinvtuple, resample=Image.BICUBIC)
    #image_norm = img.transform(img.size, Image.AFFINE, (a,b,c,d,e,f,g,h,i), resample=Image.BICUBIC)
    image_norm = numpy.array(image_norm)        

    finger_mask = numpy.zeros(mask.shape)
    finger_mask[mask == True] = 1 

    img_mask=Image.fromarray(finger_mask)
    mask_norm = img_mask.transform(img_mask.size, Image.AFFINE, Tinvtuple, resample=Image.BICUBIC)
    #mask_norm = img_mask.transform(img_mask.size, Image.AFFINE, (a,b,c,d,e,f,g,h,i), resample=Image.BICUBIC)
    mask_norm = numpy.array(mask_norm)  

    mask[:,:] = False
    mask[mask_norm==1] = True
    
    return (image_norm,mask)
    
  def __padding_finger__(self, image):
    
    image_new = bob.core.convert(image,numpy.float64,(0,1),(0,255))    
    
    img_h, img_w = image_new.shape
    
    padding_w = self.padding_threshold * numpy.ones((self.padding_offset, img_w))     
    # up and down    
    image_new = numpy.concatenate((padding_w,image_new),axis=0)
    image_new = numpy.concatenate((image_new,padding_w),axis=0)
        
    img_h, img_w = image_new.shape
    padding_h = self.padding_threshold * numpy.ones((img_h,self.padding_offset))        
    # left and right        
    image_new = numpy.concatenate((padding_h,image_new),axis=1)
    image_new = numpy.concatenate((image_new,padding_h),axis=1)
       
    return bob.core.convert(image_new,numpy.uint8,(0,255),(0,1))
    
  def crop_finger(self, image):
    
    #Padding array 
    image = self.__padding_finger__(image)
    
    if self.heq == True: 
        image_eq = bob.ip.histogram_equalization(image)
    else:
        image_eq = image    
        
    #finger_mask, finger_edges = self.__leemaskMATLAB__(image_eq)
    finger_mask, finger_edges = self.__leemask__(image_eq)
       
    image_norm,finger_mask_norm = self.__huangnormalization__(image_eq, finger_mask, finger_edges)        
    
    finger_mask2 = bob.core.convert(finger_mask,numpy.uint8,(0,255),(0,1))    
        
    return (image_norm, finger_mask_norm, finger_mask2)
    
      

  def __call__(self, image, annotations=None):
    """Reads the input image, extract the Lee mask of the fingervein, and writes the resulting image"""
    return self.crop_finger(image)

  def save_data(self, image, image_file):
    f = bob.io.HDF5File(image_file, 'w')
    f.set('image', image[0])
    f.set('finger_mask', image[1])
    f.set('mask', image[2])

  def read_data(self, image_file):
    f = bob.io.HDF5File(image_file, 'r')
    image = f.read('image')
    finger_mask = f.read('finger_mask') 
    return (image, finger_mask)
