# -*- coding: utf-8 -*-
 
ROTATE_NONE = 'N'
ROTATE_90   = 'R'
ROTATE_180  = 'I'
ROTATE_270  = 'B'

BARCODE_128 = 'C'

BARCODE_TYPES = {'C' : True}
ROTATE_TYPES = {
  'N' : True,
  'R' : True,
  'I' : True,
  'B' : True,
  'O' : True
}

ALIGN_CENTER = 'C'
ALIGN_LEFT   = 'L'

class Font:
  def __init__(self, type='0', width=10, height=10, orientation='O',fontname=''):
    #assert (type >= ord('0') and type <= ord('9')) \
    #    or (type >= ord('A') and type <= ord('Z')), \
    #    InvalidFont('Invalid font type')
    self.type = type
    self.width = width
    self.height = height
    self.orientation = orientation
    self.fontname = fontname
        
  def tostring(self):
    return "^A"+str(self.type)+","+self.orientation \
        +','+str(self.width)+","+str(self.height)
    
class Location:
  def __init__(self, x=0, y=0):
    self.x = x
    self.y = y
  def tostring(self):
    return '^FO'+str(self.x)+","+str(self.y)

class Label:
  def __init__(self, data="label", font=Font(), location=Location(), \
               alignment=ALIGN_LEFT, isblock=False, block_width=900):
    assert data != '', NoDataException('Data cannot be empty')
    self.data = data
    self.font = font
    self.location = location
    self.isblock = isblock
    self.alignment = alignment
    self.block_width = block_width
        
  def tostring(self, br=''):
    output = br + self.location.tostring() \
        + self.font.tostring()
    if self.isblock == True:
        output += '^FB'+str(self.block_width)+',2,,'+self.alignment
    output += '^FD' + self.data.replace('^','') + '^FS\n'
    return output
            
class Barcode:

  CODE11  = '1'
  CODE128 = 'C'
  ITF14   = '2'
  CODE39  = '3'
  CODE49  = '4'

  def __init__(self, data='12345', type='0', location=Location(), \
               rotate='O', height=50, showtext=False, width=65):
    assert type == Barcode.CODE128 \
        or type == Barcode.ITF14 \
        or type == Barcode.CODE11 \
        or type == Barcode.CODE39 \
        or type == Barcode.CODE49, \
        AssertionError('Barcode type not implemented yet')
    assert rotate == ROTATE_NONE or rotate == ROTATE_90 \
        or rotate == ROTATE_180 or rotate == ROTATE_270 \
        or rotate == 'O'
        
    self.rotate = rotate
    self.data = data
    self.location = location
    self.type = type
    self.height = height
    self.showtext = showtext
    self.width = width
    
  def tostring(self, br=''):
      rotate = '' if self.rotate == 'O' else self.rotate
      return '^BY' + str(self.width) + br + self.location.tostring() \
          + '^B' + self.type + rotate + ',' + str(self.height) \
          + ','+('Y' if self.showtext == True else 'N') \
          + ',N,N' + '^FD' + str(self.data) + '^FS\n'
        
class Document:
  def __init__(self, breaks='', rotate='N', quantity=1, print_speed=4):
    assert rotate in ROTATE_TYPES
    self.rotate = rotate
    self.breaks = breaks
    self.labels = []
    self.quantity = quantity
    self.print_speed = print_speed
    
  def add(self, item):
    self.labels.append(item)
        
  def tostring(self):
    out = ""
    out += "^XA\n^CI28\n^PQ"+str(self.quantity)+'^LH0,0^LT0^MNW^JMA'
    if not self.print_speed is None:
        out += "^PR"+str(self.print_speed)+","+str(self.print_speed)
    if self.rotate != 'N':
        out += "^FW"+self.rotate
    for lbl in self.labels:
        out += lbl.tostring(br=self.breaks)
        
    out += self.breaks + "^XZ"
    
    return out
    
class Rect:
  def __init__(self, width=100, height=100,
    location=Location(), tickness=4):
    self.location = location
    self.tickness = tickness
    self.width = width
    self.height = height
        
  def tostring(self, br=''):
    return self.location.tostring() + \
        '^GB'+str(self.width)+','+str(self.height) + \
        ','+str(self.tickness) + \
        '^FS'

class NoDataException(Exception):
  pass
class InvalidFont(Exception):
  pass