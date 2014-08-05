#!/usr/bin/env python
# Program Name: OpenElectrons_LSM303D.py 
# ===========================                
# Copyright (c) 2014 OpenElectrons.com
# 
# This program is free software. You can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published by 
# the Free Software Foundation; version 3 of the License.              
# Read the license at: http://www.gnu.org/licenses/gpl.txt             
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
# 07/30/14        Michael Giles     Initial authoring.
#
## @package OpenElectrons_LSM303D
# Python library for Openelectrons_LSM303D.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from OpenElectrons_i2c import OpenElectrons_i2c

## LSM303D: this class provides functions for accelerometer and magnetomter of the LSM303 IC
#  for read and write operations.
class LSM303D(OpenElectrons_i2c):

    #LSM303D addresses
    LSM303D_ADDRESS = (0x3A)   
    
    #accelerometer register constants
    ACCEL_REG1 = 0x20 
    ACCEL_REG4 = 0x23
    ACCEL_X_L = 0x28
    ACCEL_X_H = 0x29
    ACCEL_Y_L = 0x2A
    ACCEL_Y_H = 0x2B
    ACCEL_Z_L = 0x2C
    ACCEL_Z_H = 0x2D
    
    #magnetometer register addresses
    MAG_REG5 = 0x24
    MAG_REG6 = 0x25
    MAG_REG7 = 0x26
    MAG_X_L = 0x08
    MAG_X_H = 0x09
    MAG_Y_L = 0x0A
    MAG_Y_H = 0x0B
    MAG_Z_L = 0x0C
    MAG_Z_H = 0x0D
    
    #magnetometer gain constants
    MAG_G13 = 0x20 # +/- 1.3
    MAG_G19 = 0x40 # +/- 1.9
    MAG_G25 = 0x60 # +/- 2.5
    MAG_G40 = 0x80 # +/- 4.0
    MAG_G47 = 0xA0 # +/- 4.7
    MAG_G56 = 0xC0 # +/- 5.6
    MAG_G81 = 0xE0 # +/- 8.1
    
    ## Initialize the class with the i2c address of the LSM303D and set function parameters for accleerometer and magnetometer
    #  @param self The object pointer.
    #  @param i2c_address Address of your accelerometer.
    def __init__(self, lsm303d_address = LSM303D_ADDRESS ):
        OpenElectrons_i2c.__init__(self, lsm303d_address >> 1)
        # Enable the accelerometer
        try:
            self.writeByte(self.ACCEL_REG1, 0x37)
            # Acceleromter default low resolution
            #self.writeByte(self.ACCEL_REG4, 0)
            # Set magnetometer control registers
            self.writeByte(self.MAG_REG5, 0x08)
            self.writeByte(self.MAG_REG6, 0x00)
            self.writeByte(self.MAG_REG7, 0x00)
        except:
            print "Error: Could not initialize the accelerometer and/or magnetometer"
            print "Check I2C connection and address to resolve the issue"
            return 
  
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
            print "Error: Could not read accelerometer z-axis"
            return ""     

    ## Reads the accelerometer x, y, z values
    #  @param self The object pointer.
    def readAcclAll(self):
        try:
            res = [(self.readAcclX(),
                    self.readAcclY(),
                    self.readAcclZ())]
            return res
        except:
            print "Error: Could not read accelerometer values"
            return ""
            
    ## Interprets signed 16-bit magnetometer value along x-axis
    #  @param self The object pointer.
    def readMagX(self):
        try:
            xl = self.readByte(self.MAG_X_L)
            xh = self.readByteSigned(self.MAG_X_H)
            X = xl | (xh << 8) 
            return X 
        except:
            print "Error: Could not read magnetometer x-axis"
            return ""
    
    ## Interprets signed 16-bit magnetometer along y-axis
    #  @param self The object pointer.    
    def readMagY(self):
        try:
            yl = self.readByte(self.MAG_Y_L)
            yh = self.readByteSigned(self.MAG_Y_H)
            Y =  yl | (yh << 8) 
            return Y 
        except:
            print "Error: Could not read magnetometer y-axis"
            return ""
            
    ## Interprets signed 16-bit magnetometer along z-axis
    #  @param self The object pointer.
    def readMagZ(self):
        try:
            zl = self.readByte(self.MAG_Z_L)
            zh = self.readByteSigned(self.MAG_Z_H)
            Z = zl | (zh << 8)  
            return Z 
        except:
            print "Error: Could not read magnetometer z-axis"
            return ""
        
    ## Reads the magnetometer x, y, z values
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

    from time import sleep 
    
    lsm = LSM303D()

    print '[(Accelerometer X, Y, Z), (Magnetometer X, Y, Z, orientation)]'
    while True:
        print lsm.readAcclAll() + lsm.readMagAll()
        sleep(1) 