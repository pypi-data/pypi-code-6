#!/usr/bin/env python
#
# Copyright (c) 2014 OpenElectrons.com
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
# Some of this code is derived from Adafruit_LMS303.py
#
# History:
# Date            Author            Comments
# 05/19/14        Michael Giles     Initial authoring.
# 05/23/14        Michael Giles     Error handling and documenting

## @package OpenElectrons_LSM303
# This is the OpenElectrons_i2c module for LSM303.

from OpenElectrons_i2c import OpenElectrons_i2c

## ACCEL: this class provides functions for accelerometer of the LSM303 IC
#  for read and write operations.
class ACCEL(OpenElectrons_i2c):

    #accelerometer addresses
    ACCEL_ADDRESS = (0x32)   
                                             
    #register constants
    ACCEL_REG1 = 0x20 
    ACCEL_REG4 = 0x23
    ACCEL_X_L = 0x28
    ACCEL_X_H = 0x29
    ACCEL_Y_L = 0x2A
    ACCEL_Y_H = 0x2B
    ACCEL_Z_L = 0x2C
    ACCEL_Z_H = 0x2D
    

    ## Initialize the class with the i2c address of the Accelerometer
    #  @param self The object pointer.
    #  @param i2c_address Address of your accelerometer.
    def __init__(self, accel_address = ACCEL_ADDRESS ):
        OpenElectrons_i2c.__init__(self, accel_address >> 1)
        # Enable the accelerometer
        try:
            self.writeByte(self.ACCEL_REG1, 0x27)
            # default low resolution
            self.writeByte(self.ACCEL_REG4, 0)
        except:
            print "Error: Could not initialize the accelerometer"
            print "Check I2C connection and address to resolve the issue"
            return 
  
    ## Interprets signed 12 bit accelerometer data from a list
    #  @param self The object pointer.
    #  @param array The list of accelerometer data generated from the LSM303
    #  @param idx The location of the desired element in the list
    def accl(self, array, idx):
        try:
            n = array[idx] | (array[idx+1] << 8) # Low, high bytes
            if n > 32767: n -= 65536           # 2's complement signed
            return n >> 4                      # 12-bit resolution
        except: 
            print "Error: Could not read accelerometer value" 
            return "" 

    ## Interprets signed 12-bit accelerometer value along x-axis 
    #  @param self The object pointer.
    def readAcclX(self):
        try:
            xl = self.readByte(self.ACCEL_X_L)
            xh = self.readByteSigned(self.ACCEL_X_H)
            X = xl | (xh << 8) 
            return X >> 4
        except:
            print "Error: Could not read accelerometer x-axis"
            return "" 
    
    ## Interprets signed 12-bit accelerometer value along y-axis 
    #  @param self The object pointer.
    def readAcclY(self):
        try:
            yl = self.readByte(self.ACCEL_Y_L)
            yh = self.readByteSigned(self.ACCEL_Y_H)
            Y = yl | (yh << 8) 
            return Y >> 4
        except:
            print "Error: Could not read accelerometer y-axis"
            return ""  

    ## Interprets signed 12-bit accelerometer value along z-axis 
    #  @param self The object pointer.
    def readAcclZ(self):
        try:
            zl = self.readByte(self.ACCEL_Z_L)
            zh = self.readByteSigned(self.ACCEL_Z_H)
            Z = zl | (zh << 8) 
            return Z >> 4
        except:
            print "Error: Could not read accelerometer y-axis"
            return ""               

    ## Reads the accelerometer
    #  @param self The object pointer.
    def readAcclAll(self):
        try:
            array = self.readArray(self.ACCEL_X_L | 0x80, 6)
            res = [(self.readAcclX(),
                    self.readAcclY(),
                    self.readAcclZ())]
            return res
        except:
            print "Error: Could not read accelerometer values"
            return ""

## MAG: this class provides functions for magnetometer of the LSM303 IC
#  for read and write operations.
class MAG(OpenElectrons_i2c):
    
    #magnetometer constants
    MAG_ADDRESS = (0x3C) 
    
    #register addresses
    MAG_REG1 = 0x01
    MAG_REG4 = 0x02
    MAG_X_H = 0x03
    MAG_X_L = 0x04
    MAG_Y_H = 0x07
    MAG_Y_L = 0x08
    MAG_Z_H = 0x05
    MAG_Z_L = 0x06
    
    #magnetometer gain constants
    MAG_G13 = 0x20 # +/- 1.3
    MAG_G19 = 0x40 # +/- 1.9
    MAG_G25 = 0x60 # +/- 2.5
    MAG_G40 = 0x80 # +/- 4.0
    MAG_G47 = 0xA0 # +/- 4.7
    MAG_G56 = 0xC0 # +/- 5.6
    MAG_G81 = 0xE0 # +/- 8.1
    
    ## Initialize the class with the i2c address of the Magnetometer
    #  @param self The object pointer.
    #  @param i2c_address Address of your magnetometer.
    def __init__(self, mag_address = MAG_ADDRESS ):
        OpenElectrons_i2c.__init__(self, mag_address >> 1)        
        # Enable the magnetometer
        try:
            self.writeByte(self.MAG_REG4, 0x00)
        except:
            print "Error: Could not initialize the magnetometer"
            print "Check I2C connection and address to resolve the issue"
            return 
        
    ## Interprets signed 16 bit magnetometer value along x-axis
    #  @param self The object pointer.
    def readMagX(self):
        try:
            xh = self.readByteSigned(self.MAG_X_H)
            xl = self.readByte(self.MAG_X_L)
            X = xl | (xh << 8)   
            return X 
        except:
            print "Error: Could not read magnetometer x-axis"
            return ""
            
    ## Interprets signed 16 bit magnetometer value along y-axis
    #  @param self The object pointer.
    def readMagY(self):
        try:
            yh = self.readByteSigned(self.MAG_Y_H)
            yl = self.readByte(self.MAG_Y_L)
            Y = yl | (yh << 8)   
            return Y 
        except:
            print "Error: Could not read magnetometer y-axis"
            return ""
            
    ## Interprets signed 16 bit magnetometer value along z-axis
    #  @param self The object pointer.
    def readMagZ(self):
        try:
            zh = self.readByteSigned(self.MAG_Z_H)
            zl = self.readByte(self.MAG_Z_L)
            Z = zl | (zh << 8)             
            return Z 
        except:
            print "Error: Could not read magnetometer z-axis"
            return ""
    
    ## Reads the magnetometer
    #  @param self The object pointer.
    def readMagAll(self):        
        try:
            res = [(self.readMagX(),
                    self.readMagY(),
                    self.readMagZ())]
            return res
        except:
            print "Error: Could not read magnetometer values"
            return ""
    
    ## Writes a desired gain value for the magnetometer
    #  @param gain Gain value to write to the magnetometer
    def setMagnetGain(gain=MAG_G13):
        try:
            self.writeByte(MAG_REG1, gain)
        except: 
            print "Error: Could not change magnetometer gain"
            return ""


# Simple example prints accel/mag data once per second:
if __name__ == '__main__':

    import time
    
    acl = ACCEL()
    mag = MAG()

    print '[(Accelerometer X, Y, Z), (Magnetometer X, Y, Z, orientation)]'
    while True:
        print acl.readAcclAll() + mag.readMagAll()
        time.sleep(1) 