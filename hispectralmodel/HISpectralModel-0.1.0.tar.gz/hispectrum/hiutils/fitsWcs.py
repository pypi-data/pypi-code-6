#!/usr/bin/env python

# Name:                         fitsWcs
#
# Author: Ian Stewart
#
# TODO:
#
#    vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
#    Copyright (C) 2014  Ian M Stewart
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    For the GNU General Public License, see <http://www.gnu.org/licenses/>.
#    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# History (date, change author):
#
#	2014-05-14	IMS/AIfA
#.......................................................................
# * Copied to this release version.
# - Deleted test harness.
#
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

"""
Defines some classes to store World Coordinate System (WCS) information. The WCS concept was developed with FITS files in view but it has wider applicability: in fact to any situation in which one has an array of numbers of any dimensionality (the elements of the array are denoted in the WCS formalism as 'pixels') and wishes to encode a mapping of pixel number to some other coordinate system (known as the 'world coordinates').

The fundamental references for WCS are

	I: "Representations of world coordinates in FITS", Greisen, E.W. & Calabretta, M.R. (2002), Astronomy & Astrophysics, 395, 1061-1075.  

	Also a supplement to Paper I entitled Concatenation of FITS World Coordinate Systems by Steve Allen and Doug Mink.
	
	II: "Representations of celestial coordinates in FITS", Calabretta. M.R., & Greisen, E.W., (2002), Astronomy & Astrophysics, 395, 1077-1122.  
	
	III: "Representations of spectral coordinates in FITS", Greisen, E.W., Calabretta, M.R. Valdes, F.G., & Allen, S.L., (2006), Astronomy & Astrophysics, 446, 747-771. 

A quick glance at these will show that WCS can get a lot more complicated than I have presented here. But since I have myself never had occasion to use anything much more complicated than a simple linear mapping, and since this software is intended primarily for my own purposes, I have not attempted to write a really comprehensive interface. In any case there are packages which already exist which cover all the bases.
"""

_module_name = 'fitsWcs'

import numpy as nu

import local_exceptions as ex

#.......................................................................
# Exception classes:

class UnsupportedExtensionType(Exception):
  def __init__(self, extensionType):
    self.extensionType = extensionType
  def __str__(self):
    return 'Extension type %s is not supported.' % (self.extensionType)

class MismatchedExtensionType(Exception):
  def __init__(self, fileExtensionType, instanceExtensionType):
    self.fileExtensionType = fileExtensionType
    self.instanceExtensionType = instanceExtensionType
  def __str__(self):
    return 'Your WCS has extension type %s but the file you are writing to has type %s.'\
      % (self.fileExtensionType, self.instanceExtensionType)

class ComboSurprise(Exception):
  def __init__(self, axisI, comboI):
    self.axisI = axisI
    self.comboI = comboI
  def __str__(self):
    return 'In new combo, found axis %d which already has combo number %d.' % (self.axisI, self.comboI)

class MismatchedCombos(Exception):
  def __init__(self, comboI, comboJ):
    self.comboI = comboI
    self.comboJ = comboJ
  def __str__(self):
    return 'Expected combo %d but found %d.' % (self.comboI, self.comboJ)

class UnwantedCombo(Exception):
  def __init__(self, i, j, comboI):
    self.i = i
    self.j = j
    self.comboI = comboI
  def __str__(self):
    return 'No CD kwd found at axis pair (%d,%d) but axis %d was found labelled with combo number %d.' % (self.i, self.j, self.j, self.comboI)

class AxisIsInJoint(Exception):
  def __init__(self, axisNum):
    self.axisNum = axisNum
  def __str__(self):
    return 'Axis %d is part of a joint-transform group of axes and can not be returned via this method.' % (self.axisNum)

class AxisIsNotInJoint(Exception):
  def __init__(self, axisNum):
    self.axisNum = axisNum
  def __str__(self):
    return 'Axis %d is NOT part of a joint-transform group of axes and can not be returned via this method.' % (self.axisNum)

class AxisNotFound(Exception):
  def __init__(self, axisNum):
    self.axisNum = axisNum
  def __str__(self):
    return 'Axis %d was not found in the WCS.' % (self.axisNum)

#.......................................................................
class _WCS:
  _validExtensionTypes = ['IMAGE','BINTABLE',None]
  _ctypeKwdRoots = {'IMAGE':'CTYPE', 'BINTABLE':'TCTYP'}
  _cdKwdRoots    = {'IMAGE':'CD',    'BINTABLE':'TCD'}
  _kwdRoots = {'IMAGE':[   'CRPIX','CRVAL','CUNIT','CDELT']\
             , 'BINTABLE':['TCRPX','TCRVL','TCUNI','TCDLT']}

  def __init__(self, extensionType):
    self.extensionType = extensionType

#.......................................................................
class WCSAxis(_WCS):
  """
The primary superclass which contains most of the necessary information to define a WCS axis.
  """
  _attrNames = ['refInPixels', 'refInWorld', 'worldUnit', 'pixelDeltaWorld'] # order needs to match _WCS._kwdRoots.

  def __init__(self, ctype, refInPixels, refInWorld, worldUnit='', axisNumber=None, extensionType=None):
    """Note that the WCS convention is that the centre of the first pixel is located at 1.0 on the axis of pixel values. Thus when calling WCS routines from languages (almost all of them except Fortran!) in which the first element of any array has index zero, one must add 1 to the pixel index to get the WCS pixel coordinate value."""
    _WCS.__init__(self, extensionType)
    self.ctype         = ctype
    self.refInPixels   = refInPixels
    self.refInWorld    = refInWorld
    self.worldUnit     = worldUnit
    self.axisNumber    = axisNumber # image axis number for arrays, but column number for binary tables. If it is 'None' this is a flag to the addAxis method of FitsHeaderWCS, or the constructor of WcsAxisCombo, to assign the first free axis number.

  def compileListOfKwds(self):#, extensionType):
    if self.axisNumber==None:
      raise ex.NotYetImplemented()

    listOfKwds = []

    ctypeKwdRoot = self._ctypeKwdRoots[self.extensionType] # inherits from
    kwdRoots     = self._kwdRoots[     self.extensionType] # _WCS.

    # Write CTYPE and 'ordinary' keywords:
    #
    aI = self.axisNumber

    ctypeKwd = '%s%d' % (ctypeKwdRoot, aI) # axisNumber starts at 1.
    listOfKwds.append({'name':ctypeKwd,'value':self.ctype})

    for k in range(len(kwdRoots)-1): # '-1' because we don't want to assume CDELT at this stage.
      kwdName = '%s%d' % (kwdRoots[k], aI)
      attrName = self._attrNames[k]
      listOfKwds.append({'name':kwdName,'value':self.__dict__[attrName]})

    return listOfKwds

  def _getStrCore(self, spaces=''):
    returnedStr = spaces+'  Extension type: %s\n' % (self.extensionType)
    if self.extensionType==None:
      returnedStr += spaces+'    Axis number = %d\n' % (self.axisNumber)
      returnedStr += spaces+'   Mapping type = %s\n' % (self.ctype)
      returnedStr += spaces+'Reference pixel = %f\n' % (self.refInPixels)
      returnedStr += spaces+'Reference world = %f\n' % (self.refInWorld)
      returnedStr += spaces+'     World unit = %s\n' % (self.worldUnit)
    else:
      returnedStr += spaces+'Axis number = %d\n' % (self.axisNumber)
      listOfKwds = self.compileListOfKwds()
      for kwd in listOfKwds:
        returnedStr += spaces+'     %s = %s\n' % (kwd['name'], kwd['value'])

    return returnedStr

  def __str__(self, spaces=''):
    returnedStr = spaces+'<WCSAxis object.\n'
    returnedStr += self._getStrCore(spaces+'  ')
    return returnedStr + spaces+'>'

  def copy(self):
    newAxisWcs = WCSAxis(self.ctype, self.refInPixels, self.refInWorld\
      , self.worldUnit, self.axisNumber, self.extensionType)
    return newAxisWcs

#.......................................................................
class _WCSMapping:
  """
A superclass which contains the methods to convert from pixel to world coordinates and back again.
  """
  def __init__(self, pixToWorldMatrix):
    self._pixToWorldMatrix = pixToWorldMatrix

  def _pixelToWorldDeltas(self, pixelDeltaValues):
    numAxes = self._pixToWorldMatrix.shape[0]
    worldDeltaValues = []
    for row in range(numAxes):
      worldDeltaValues.append((self._pixToWorldMatrix[row,:] * pixelDeltaValues).sum())

    return nu.array(worldDeltaValues)

  def _worldToPixelDeltas(self, worldDeltaValues):
    numAxes = self._pixToWorldMatrix.shape[0]

    invMatrix = nu.linalg.inv(self._pixToWorldMatrix)

    pixelDeltaValues = []
    for row in range(numAxes):
      pixelDeltaValues.append((invMatrix[row,:] * worldDeltaValues).sum())

    return nu.array(pixelDeltaValues)

  def pixelToWorld(self, pixelValues):
    raise ex.EmptyMethod()

  def worldToPixel(self, worldValues):
    raise ex.EmptyMethod()

#.......................................................................
class WCSAxisSimple(WCSAxis, _WCSMapping):
  """
This is intended to be the shop-front for any WCS axis for which the mapping between pixel and world coordinates depends only on that axis - i.e. there is no rotation implicit in that particular coordinate transform.
  """
  def __init__(self, ctype, refInPixels, refInWorld, pixelDeltaWorld\
    , worldUnit='', axisNumber=None, extensionType=None):

    WCSAxis.__init__(self, ctype, refInPixels, refInWorld, worldUnit, axisNumber, extensionType)
    _WCSMapping.__init__(self, nu.array([[pixelDeltaWorld]]))
    self._pixelDeltaWorld = pixelDeltaWorld

  def pixelToWorld(self, pixelValue):
    worldDeltaValue = float(self._pixelToWorldDeltas(pixelValue - self.refInPixels)[0]) # converts from numpy array scalar to honest-to-god python scalar.
    return worldDeltaValue + self.refInWorld

  def worldToPixel(self, worldValue):
    pixelDeltaValue = float(self._worldToPixelDeltas(worldValue - self.refInWorld)[0]) # converts from numpy array scalar to honest-to-god python scalar.
    return pixelDeltaValue + self.refInPixels

  def pixelsToWorld(self, pixelValues):
    worldDeltaValues = (pixelValues - self.refInPixels)*self._pixelDeltaWorld
    return worldDeltaValues + self.refInWorld

  def worldsToPixel(self, worldValues):
    pixelDeltaValues = (worldValues - self.refInWorld)/self._pixelDeltaWorld
    return pixelDeltaValues + self.refInPixels

  def _getCdeltKwd(self):
    kwdRoots = self._kwdRoots[self.extensionType]
    kwdName = '%s%d' % (kwdRoots[-1], self.axisNumber)
    return {'name':kwdName,'value':self._pixelDeltaWorld}

  def compileListOfKwds(self):
    listOfKwds = WCSAxis.compileListOfKwds(self)
    cdeltKwd = self._getCdeltKwd()
    listOfKwds.append(cdeltKwd)
    return listOfKwds

  def _getStrCore(self, spaces=''):
    returnedStr = WCSAxis._getStrCore(self, spaces)

    if self.extensionType==None:
      returnedStr += spaces+'     pixel size = %f (note: can be -ve)\n' % (self._pixelDeltaWorld)

    return returnedStr

  def __str__(self, spaces=''):
    returnedStr = spaces+'<WCSAxisSimple instance.\n'
    returnedStr += self._getStrCore(spaces+'  ')
    return returnedStr + spaces+'>'

  def copy(self):
    newAxisWcs = WCSAxisSimple(self.ctype, self.refInPixels, self.refInWorld\
      , self._pixelDeltaWorld, self.worldUnit, self.axisNumber, self.extensionType)
    return newAxisWcs

  def writeToHeader(self, hdu, adjustExtType=True):
    extensionType = readExtType(hdu)
    if extensionType!=self.extensionType:
      if adjustExtType:
        self.extensionType = extensionType
      else:
        raise MismatchedExtensionType(extensionType, self.extensionType)

    listOfKwds = self.compileListOfKwds()
    for kwd in listOfKwds:
      if str(kwd['value'])=='':
        continue
      hdu.header.update(kwd['name'], kwd['value']) # Strictly speaking this is a side effect, tsk. Better to return the hdu??

##### also write comments??

#.......................................................................
class WCSAxesJoint(_WCS, _WCSMapping):
  """
This is intended to be the way to describe several WCS axes for which the the mapping between pixel and world coordinates involves all of the axes and can only be described by a matrix with non-zero off-diagonal terms.
  """
  def __init__(self, wcsAxisList, pixToWorldMatrix, extensionType=None):
    """
Specification of the arguments:
	- wcsAxisList should be a simple list of WCSAxis objects.

	- pixToWorldMatrix should be a square 2D numpy array of floats. This should have the same number of rows as the number of elements in wcsAxisList.
    """
    _WCS.__init__(self, extensionType)
    _WCSMapping.__init__(self, pixToWorldMatrix)
    self._wcsAxisList = wcsAxisList

    numAxesInCombo = len(self._wcsAxisList)
    self._refsInPixels = nu.zeros([numAxesInCombo], nu.float)
    self._refsInWorld  = nu.zeros([numAxesInCombo], nu.float)
    for i in range(numAxesInCombo):
      self._refsInPixels[i] = self._wcsAxisList[i].refInPixels
      self._refsInWorld[ i] = self._wcsAxisList[i].refInWorld

    self.setExtTypeOfAxes()

  def setExtTypeOfAxes(self):
    for wcsAxis in self._wcsAxisList:
      wcsAxis.extensionType = self.extensionType

  def pixelToWorld(self, pixelValues):
    worldDeltaValues = self._pixelToWorldDeltas(pixelValues - self._refsInPixels)
    return worldDeltaValues + self._refsInWorld

  def worldToPixel(self, worldValues):
    pixelDeltaValues = self._worldToPixelDeltas(worldValues - self._refsInWorld)
    return pixelDeltaValues + self._refsInPixels

  def _getCDKwds(self):
    cdKwdRoot = self._cdKwdRoots[self.extensionType]
    numAxesInCombo = len(self._wcsAxisList)
    listOfKwds = []
    for row in range(numAxesInCombo):
      rowAxis = self._wcsAxisList[row].axisNumber
      for col in range(numAxesInCombo):
        colAxis = self._wcsAxisList[col].axisNumber
        kwdName = '%s%d%s%d' % (cdKwdRoot, rowAxis, '_', colAxis)
        listOfKwds.append({'name':kwdName,'value':self._pixToWorldMatrix[row,col]})

    return listOfKwds

  def compileListsOfKwds(self):
    numAxesInCombo = len(self._wcsAxisList)
    listsOfKwds = []
    for i in range(numAxesInCombo):
      listOfKwds.append(self._wcsAxisList[i].compileListOfKwds())

    return listOfKwds+self._getCDKwds()

  def __str__(self, spaces=''):
    numAxesInCombo = len(self._wcsAxisList)
    returnedStr = spaces+'<WCSAxesJoint object.\n'

    for axis in self._wcsAxisList:
      returnedStr += axis.__str__(spaces+'  ')+'\n'

    returnedStr += spaces+'Elements of the transformation matrix:\n'
    if self.extensionType==None:
      returnedStr += spaces+'  row  (axis)  col  (axis)  value:\n'
      for row in range(numAxesInCombo):
        rowAxis = self._wcsAxisList[row].axisNumber
        for col in range(numAxesInCombo):
          colAxis = self._wcsAxisList[col].axisNumber
          returnedStr += spaces+'  %2d     %2d    %2d     %2d    %f\n'\
            % (row, rowAxis, col, colAxis, self._pixToWorldMatrix[row,col])

    else:
      listCDKwds = self._getCDKwds()
      for kwd in listCDKwds:
        returnedStr += spaces+'  %s = %s\n' % (kwd['name'], kwd['value'])

    return returnedStr + spaces+'>'

  def copy(self):
    newAxisCombo = WCSAxesJoint(self._wcsAxisList[:], self._pixToWorldMatrix.copy()\
      , self.extensionType)
    return newAxisCombo

#.......................................................................
def readExtType(hdu):
  # Get extensionType:
  #
  try:
    extensionType = hdu.header['XTENSION']
  except KeyError:
    if hdu.header['SIMPLE']:
      extensionType = 'IMAGE' # in the the primary HDU.

  return extensionType

#.......................................................................
def readWCSFromFITS(hdu):
  extensionType = readExtType(hdu)

  # Get the number of axes:
  #
  if extensionType=='IMAGE':
    numAxes = hdu.header['NAXIS']
  elif extensionType=='BINTABLE':
    numAxes = hdu.header['TFIELDS'] # actually the number of table columns.
  else:
    raise UnsupportedExtensionType(extensionType)

  ctypeKwdRoot = _WCS._ctypeKwdRoots[extensionType]
  cdKwdRoot    = _WCS._cdKwdRoots[   extensionType]
  kwdRoots     = _WCS._kwdRoots[     extensionType]

  # Find all CD keywords and construct a matrix of their values:
  #
  cdKwdFound  = nu.zeros([numAxes,numAxes], nu.bool)
  cdKwdValues = nu.zeros([numAxes,numAxes], nu.float)
  for i in range(numAxes):
    for j in range(numAxes):
      kwdName = '%s%d_%d' % (cdKwdRoot, i+1, j+1)
      try:
        kwdValA = hdu.header[kwdName]
      except KeyError:
        continue

      cdKwdFound[i,j] = True
      cdKwdValues[i,j] = kwdValA

      if i==j: continue

      # If we got this far, we must have found the keyword. The symmetric one should also be present.
      #
      kwdName = '%s%d_%d' % (cdKwdRoot, j+1, i+1)
      kwdValB = hdu.header[kwdName]

      cdKwdFound[j,i] = True
      cdKwdValues[j,i] = kwdValB

  # Now I want to do some checks and book-keeping to make sure that each axis takes part in no more than 1 combo, and that for each member of each combo, CD kwds exist for all members of the combo (including itself):
  #
  listOfCombos = []
  comboOfAxis = nu.zeros([numAxes], nu.int) # we define that valid combo numbers start from 1.
  for i in range(numAxes):
    if not cdKwdFound[i,:].any(): # means this axis is not part of a combo.
      continue

    if comboOfAxis[i]==0: # this means we have not previously looked at any members of the combo of which this axis is part. We should load all the members of this combo.

      # Make a list of all axis numbers in the combo:
      #
      comboAxisIs = []
      for j in range(numAxes):
        if cdKwdFound[i,j]:
          if comboOfAxis[j]>0: raise ComboSurprise(j, comboOfAxis[j])
          comboAxisIs.append(j)

      # Append this object to the list of combos; then use the new length of this list as the 'combo number' to assign all axes of the combo:
      #
      listOfCombos.append(comboAxisIs)
      numOfCurrentCombo = len(listOfCombos)
      for i in comboAxisIs:
        comboOfAxis[i] = numOfCurrentCombo

    else: # we have previously treated this combo, starting from a different axis. Check that the correct CD values are present:
      numOfPreviousCombo = comboOfAxis[i]
      for j in range(numAxes):
        if cdKwdFound[i,j] and comboOfAxis[j]!=numOfPreviousCombo:
          raise MismatchedCombos(numOfPreviousCombo, comboOfAxis[j])
        if not cdKwdFound[i,j] and comboOfAxis[j]==numOfPreviousCombo:
          raise UnwantedCombo(i, j, j, numOfPreviousCombo)

  # Extract and store the non-mapping keyword values for all axes present:
  #
  tempListOfWcsAxes = []
  for i in range(numAxes):
    aI = i+1
    ctypeKwd = '%s%d' % (ctypeKwdRoot, aI)
    try:
      ctype = hdu.header[ctypeKwd]
    except KeyError:
      tempListOfWcsAxes.append(None)
      continue # no CTYPEi/TCTYPi, so assume no WCS kwds this axis.

    # Read the other non-mapping keywords, i.e. 'CRPIX', 'CRVAL' and 'CUNIT'.
    #
    kwdName = '%s%d' % (kwdRoots[0], aI) # 'CRPIX'/
    refInPixels = hdu.header[kwdName]
    kwdName = '%s%d' % (kwdRoots[1], aI) # 'CRVAL'/
    refInWorld  = hdu.header[kwdName]
    kwdName = '%s%d' % (kwdRoots[2], aI) # 'CUNIT'/
    try:
      worldUnit = hdu.header[kwdName]
    except KeyError:
      worldUnit = ''

    if comboOfAxis[i]!=0: # this axis is part of a joint-transform combination. Just load a non-committal axis:
      tempListOfWcsAxes.append(WCSAxis(ctype, refInPixels, refInWorld\
        , worldUnit, aI, extensionType))
    else: # look for CDELT:
      kwdName = '%s%d' % (kwdRoots[3], aI) # 'CDELT'/
      pixelDeltaWorld = hdu.header[kwdName]
      tempListOfWcsAxes.append(WCSAxisSimple(ctype, refInPixels, refInWorld\
        , pixelDeltaWorld, worldUnit, aI, extensionType))

  # Now fill the list of elements. I'll do this in 2 passes, the 1st to push all the simple axes, the 2nd to push all the joint axes.
  #
  listOfElements = []
  for i in range(numAxes):
    if tempListOfWcsAxes[i]==None or comboOfAxis[i]!=0: # the first means there are no WCS kwds at all for axis i+1, the second means the axis is part of a joint-transform combination.
      continue

    listOfElements.append(tempListOfWcsAxes[i])

  # Now the 2nd pass to extract and push all the joint-transform combinations.
  #
  for comboAxisIs in listOfCombos:
    wcsAxisList = []
    numAxesThisCombo = len(comboAxisIs)
    pixToWorldMatrix = nu.zeros([numAxesThisCombo,numAxesThisCombo], nu.float)
    for ii in range(numAxesThisCombo):
      i = comboAxisIs[ii]
      wcsAxisList.append(tempListOfWcsAxes[i])

      for jj in range(numAxesThisCombo):
        j = comboAxisIs[jj]
        pixToWorldMatrix[ii,jj] = cdKwdValues[i,j]

    # Now construct the combo and add it to the list:
    #
    axisCombo = WCSAxesJoint(wcsAxisList, pixToWorldMatrix, extensionType)
    listOfElements.append(axisCombo)

  totalWCS = FitsHeaderWCS(extensionType, listOfElements)

  return totalWCS

#. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
class FitsHeaderWCS(_WCS):
  _maxAllowedAxisNum = 99

  def __init__(self, extensionType=None, listOfElements=[]):
    """
The elements in listOfElements are expected to be objects of type either WCSAxisSimple or WCSAxesJoint.
    """
    if not extensionType in self._validExtensionTypes:
      raise UnsupportedExtensionType(extensionType)

    self.extensionType = extensionType

    # For convenience, convert all the WCSAxisSimple elements into single-component WCSAxesJoint objects:
    #
    self._listOfCombos = []
    for element in listOfElements:
      if   element.__class__==WCSAxisSimple:
        axis = WCSAxis(element.ctype, element.refInPixels\
          , element.refInWorld, element.worldUnit, element.axisNumber\
          , self.extensionType)
        pixToWorldMatrix = nu.array([[element._pixelDeltaWorld]])
        self._listOfCombos.append(WCSAxesJoint([axis], pixToWorldMatrix, self.extensionType))

      elif element.__class__==WCSAxesJoint:
        element.extensionType = self.extensionType
        element.setExtTypeOfAxes()
        self._listOfCombos.append(element)

      else:
        raise ex.UnrecognizedChoiceObject(element.__class__.__name__)

    # Note that we set all extensionType values of the components to be the same as that of the totalWCS.

  def hasAxis(self, axisNum):
    for wcsCombo in self._listOfCombos:
      numAxes = len(wcsCombo._wcsAxisList)
      for j in range(numAxes):
        if wcsCombo._wcsAxisList[j].axisNumber==axisNum:
          return True

    else: # didn't find axis at all.
      return False

  def getAxis(self, axisNum):
    """Returns a WCSAxisSimple object provided that (i) that axis number exists in the FitsHeaderWCS; (ii) it is not part of a joint-transform combination with another axis."""
    for wcsCombo in self._listOfCombos:
      numAxes = len(wcsCombo._wcsAxisList)
      for j in range(numAxes):
        wcsAxisSpecs = wcsCombo._wcsAxisList[j]
        if wcsAxisSpecs.axisNumber==axisNum:
          if numAxes<=1:
            pixelDeltaWorld = float(wcsCombo._pixToWorldMatrix[0,0])
            break
          else:
            raise AxisIsInJoint(axisNum)
        # end if wcsAxisSpecs.axisNumber==axisNum

      else: # didn't find the axis in this combo.
        continue # do next combo.
      # end inner loop over axes this combo.

      # If got to here, means the axis was found, and it was non-joint: so we broke out of the inner loop. So break out of the outer one too - nothing more to do.
      break
    else: # didn't find axis at all.
      raise AxisNotFound(axisNum)
    # end outer loop over combos.

    # Convert the current WcsAxisSpecs object to a WCSAxisSimple object:
    #
    wcsAxis = WCSAxisSimple(wcsAxisSpecs.ctype, wcsAxisSpecs.refInPixels\
      , wcsAxisSpecs.refInWorld, pixelDeltaWorld, wcsAxisSpecs.worldUnit\
      , wcsAxisSpecs.axisNumber, wcsAxisSpecs.extensionType)

    return wcsAxis

  def getJointWithAxis(self, axisNum):
    """Returns a WCSAxesJoint object provided that (i) that axis number exists in the FitsHeaderWCS; (ii) it is part of a joint-transform combination with another axis."""
    for wcsCombo in self._listOfCombos:
      numAxes = len(wcsCombo._wcsAxisList)
      for j in range(numAxes):
        wcsAxisSpecs = wcsCombo._wcsAxisList[j]
        if wcsAxisSpecs.axisNumber==axisNum:
          if numAxes<=1:
            raise AxisIsNotInJoint(axisNum)
          else:
            break # success. Bust out of these loops, carrying wcsCombo.
        # end if wcsAxisSpecs.axisNumber==axisNum

      else: # didn't find the axis in this combo.
        continue # do next combo.
      # end inner loop over axes this combo.

      # If got to here, means the axis was found, and it was in a combo: so we broke out of the inner loop. So break out of the outer one too - nothing more to do.
      break
    else: # didn't find axis at all.
      raise AxisNotFound(axisNum)
    # end outer loop over combos.

    return wcsCombo

  def addElement(self, element):
    if   element.__class__==WCSAxisSimple:
      axis = WCSAxis(element.ctype, element.refInPixels\
        , element.refInWorld, element.worldUnit, element.axisNumber\
        , self.extensionType)
      pixToWorldMatrix = nu.array([[element._pixelDeltaWorld]])
      self._listOfCombos.append(WCSAxesJoint([axis], pixToWorldMatrix, self.extensionType))

    elif element.__class__==WCSAxesJoint:
      element.extensionType = self.extensionType
      element.setExtTypeOfAxes()
      self._listOfCombos.append(element)

    else:
      raise ex.UnrecognizedChoiceObject(element.__class__.__name__)

  def compileListOfKwds(self):
    listOfKwds = []
    for wcsCombo in self._listOfCombos:
      numAxes = len(wcsCombo._wcsAxisList)
      if numAxes>1:
        listOfKwds += wcsCombo.compileListOfKwds()
      else:
        wcsAxisSpecs = wcsCombo._wcsAxisList[0]
        pixelDeltaWorld = float(wcsCombo._pixToWorldMatrix[0,0])
        wcsAxis = WCSAxisSimple(wcsAxisSpecs.ctype, wcsAxisSpecs.refInPixels\
          , wcsAxisSpecs.refInWorld, pixelDeltaWorld, wcsAxisSpecs.worldUnit\
          , wcsAxisSpecs.axisNumber, wcsAxisSpecs.extensionType)

        listOfKwds += wcsAxis.compileListOfKwds()

    return listOfKwds

  def writeToHeader(self, hdu, adjustExtType=True):
    extensionType = readExtType(hdu)
    if extensionType!=self.extensionType:
      if adjustExtType:
        self.extensionType = extensionType
        for element in self._listOfCombos:
          element.extensionType = extensionType
          element.setExtTypeOfAxes()
      else:
        raise MismatchedExtensionType(extensionType, self.extensionType)

    listOfKwds = self.compileListOfKwds()
    for kwd in listOfKwds:
      if str(kwd['value'])=='':
        continue
      hdu.header.update(kwd['name'], kwd['value'])

##### also write comments??

    return hdu

  def __str__(self, spaces=''):
    returnedStr = spaces+'<FitsHeaderWCS object.\n'
    returnedStr += spaces+'  Extension type: %s\n' % (self.extensionType)

    for wcsCombo in self._listOfCombos:
      numAxes = len(wcsCombo._wcsAxisList)
      if numAxes>1:
        returnedStr += spaces+wcsCombo.__str__(self.extensionType, spaces+'  ')+'\n'

      else:
        wcsAxisSpecs = wcsCombo._wcsAxisList[0]
        pixelDeltaWorld = float(wcsCombo._pixToWorldMatrix[0,0])
        wcsAxis = WCSAxisSimple(wcsAxisSpecs.ctype, wcsAxisSpecs.refInPixels\
          , wcsAxisSpecs.refInWorld, pixelDeltaWorld, wcsAxisSpecs.worldUnit\
          , wcsAxisSpecs.axisNumber, wcsAxisSpecs.extensionType)

        returnedStr += spaces+wcsAxis.__str__(spaces+'  ')+'\n'

    return returnedStr+spaces+'>'

  def copy(self):
    listOfElements = []
    for wcsCombo in self._listOfCombos:
      numAxes = len(wcsCombo._wcsAxisList)

      if numAxes>1:
        listOfElements.append(wcsCombo.copy())

      else:
        wcsAxisSpecs = wcsCombo._wcsAxisList[0]
        pixelDeltaWorld = float(wcsAxisSpecs._pixToWorldMatrix[0,0])
        wcsAxis = WCSAxisSimple(wcsAxisSpecs.ctype, wcsAxisSpecs.refInPixels\
          , wcsAxisSpecs.refInWorld, pixelDeltaWorld, wcsAxisSpecs.worldUnit\
          , wcsAxisSpecs.axisNumber, wcsAxisSpecs.extensionType)

        listOfElements.append(wcsAxis.copy())

    newTotalWcs = FitsHeaderWCS(self.extensionType, listOfElements)
    return newTotalWcs


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == '__main__':
  pass



