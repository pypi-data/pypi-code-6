#!/usr/bin/python
# Program Name: L3GD20.py 
# ===========================                                          
#                                                                      
# Copyright (c) 2014 by openelectrons.com                                
# Email: info (<at>) openelectrons (<dot>) com                           
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
# Some of this code is derived from Adafruit_L3GD20.py
#
# When        Who             Comments
# 07/9/13    Nitin Patil    Initial authoring.
# 07/31/14   Michael Giles  OpenElectron_i2c 
#
# Python library for Openelectrons.com  Gyroscope L3GD20.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.


from OpenElectrons_i2c import OpenElectrons_i2c
import time

## L3GD20: this class provides functions for the gyroscope of the LSM303 IC
#  for read and write operations.
class L3GD20(OpenElectrons_i2c):

    # L3GD20 constants    
    XAXIS = 0
    YAXIS = 1
    ZAXIS = 2
    # L3GD20 defualt i2c address
    GYRO_ADDRESS = (0xD6)  
    # L3GD20 registers
    L3G20D_WHO_AM_I    =  0x0F

    L3G20D_CTRL_REG1   = 0x20
    L3G20D_CTRL_REG2   = 0x21
    L3G20D_CTRL_REG3   =  0x22
    L3G20D_CTRL_REG4   =  0x23
    L3G20D_CTRL_REG5   =  0x24
    L3G20D_REFERENCE   =  0x25
    L3G20D_OUT_TEMP    =  0x26
    L3G20D_STATUS_REG  =  0x27

    L3G20D_OUT_X_L     =  0x28
    L3G20D_OUT_X_H     =  0x29
    L3G20D_OUT_Y_L     =  0x2A
    L3G20D_OUT_Y_H     =  0x2B
    L3G20D_OUT_Z_L     =  0x2C
    L3G20D_OUT_Z_H     =  0x2D

    L3G20D_FIFO_CTRL_REG = 0x2E
    L3G20D_FIFO_SRC_REG  = 0x2F
    L3G20D_INT1_CFG      = 0x30
    L3G20D_INT1_SRC      = 0x31
    L3G20D_INT1_THS_XH   = 0x32
    L3G20D_INT1_THS_XL   = 0x33
    L3G20D_INT1_THS_YH   = 0x34
    L3G20D_INT1_THS_YL   = 0x35
    L3G20D_INT1_THS_ZH   = 0x36
    L3G20D_INT1_THS_ZL   = 0x37
    L3G20D_INT1_DURATION = 0x38
    
    # lib variables
    RAD_TO_DEG = 57.29578
    M_PI = 3.14159265358979323846
    
    gyroSampleCount =0
    gyroSample = [0,0,0]
    gyroHeading = 0
    gyroLastMesuredTime = time.time()
    gyroScaleFactor = 0.07

    ## Initialize the class with the i2c address of the L3GD20 and set function parameters for gyro
    #  @param self The object pointer.
    #  @param i2c_address Address of your gyro.
    def __init__(self, gyro_address = GYRO_ADDRESS):
        #define the gyro address
        OpenElectrons_i2c.__init__(self, gyro_address >> 1)
        # Enable the gyro
        try:
            self.writeByte(self.L3G20D_CTRL_REG1, 0x0F)
            #Continuos update, 500 dps full scale as default
            self.writeByte(self.L3G20D_CTRL_REG4, 0x70)
            gyroLastMesuredTime = time.time()
        except:
            print "Error: Could not initialize gyroscope"
            print "Check I2C connection and address to resolve the issue"
            return 
        
    ## Interprets signed 12-bit Gyro component from list
    #  @param self The object pointer.
    #  @param array The list of gyro data generated from the L3GD20
    #  @param idx The location of the desired element in the list
    def accel12(self, list, idx):
        try:
            n = list[idx] | (list[idx+1] << 8) # Low, high bytes
            if n > 32767: n -= 65536           # 2's complement signed
            return n >> 4                      # 12-bit resolution
        except:
            print "Error: Could not read 12-bit gyro value" 
            return ""   

    ## Interprets signed 16-bit Gyro component from list
    #  @param self The object pointer.
    #  @param array The list of gyro data generated from the L3GD20
    #  @param idx The location of the desired element in the list
    def int16(self, list, idx):
        try:
            n = (list[idx] << 8) | list[idx+1]   # High, low bytes
            return n if n < 32768 else n - 65536 # 2's complement signed
        except:
            print "Error: Could not read 16-bit gyro value" 
            return "" 

    ## Sets the range for gyro 
    #  @param self The object pointer.
    #  @param range The range to set the gyro.    
    def rangeSelect(self,range):
        try:
            self.writeByte(self.L3G20D_CTRL_REG5, 0x02)
            if range == 250:
                self.writeByte(self.L3G20D_CTRL_REG4, 0xc0)
                self.gyroScaleFactor = 0.00875  
                return 
            if range == 500:
                self.writeByte(self.L3G20D_CTRL_REG4, 0xd0)
                self.gyroScaleFactor = 0.0175  
                return 
            if range == 2000:
                self.writeByte(self.L3G20D_CTRL_REG4, 0xe0) 
                self.gyroScaleFactor = 0.07 
                return 
            self.writeByte(self.L3G20D_CTRL_REG4, 0xe0)
            self.gyroScaleFactor = 0.07 
            return 
        except:
            print "Error: Could not set gyro range" 
            return "" 
   
    ## Reads the gyro sum value 
    #  @param self The object pointer.
    def measureGyroSum(self):
        try:
            rate = self.read()
            self.gyroSample[0] += rate[0]
            self.gyroSample[1] += rate[1]
            self.gyroSample[2] += rate[2]
            self.gyroSampleCount += 1
            return self.gyroSample
        except:
            self.gyroSampleCount = "Error: Could not read gyro sample"
            print "Error: Could not read gyro sum value" 
            return ""
  
    ## Reads the x,y,z gyro values
    #  @param self The object pointer.
    def read(self):
        # Read the gyroscope
        try:        
            list = self.readArray(self.L3G20D_OUT_X_L  | 0x80, 6)
            res = ( self.gyroScaleFactor*self.int16(list, 0),
                    self.gyroScaleFactor*self.int16(list, 2),
                    self.gyroScaleFactor*self.int16(list, 4) )
            return res
        except:
            print "Error: Could not read gyro values" 
            return "" 

    ## Writes to a register to configure gyro
    #  @param self The object pointer.
    #  @param register The register address to write to the L3GD20.
    #  @param r_value The value to write to the register.
    def configL3GD20(self, register, r_value):
        try:
            self.writeByte(register,r_value)
        except:
            print "Error: Could not configure gyro" 
            return "" 
     
    ## Converts degrees to radian
    #  @param self The object pointer.
    #  @param d_value The degree value to convert to radian. 
    def deg2rad(self,d_value):
        r_value = d_value/57.2957795
        return  r_value
        
    ## Converts radian to degrees
    #  @param self The object pointer.
    #  @param r_value The radian value to convert to degrees. 
    def rad2deg(self,r_value):
        d_value = r_value*57.2957795
        return  d_value
    
    ## Reads the heading/angle value of the gyro
    #  @param self The object pointer.
    def measureGyro(self):
        try:
            currentTime = time.time()
            rate = self.read()
            if abs(rate[self.ZAXIS]) > 8  :
                self.gyroHeading += rate[self.ZAXIS] * ((currentTime - self.gyroLastMesuredTime) );
            self.gyroLastMesuredTime = time.time()
            return self.gyroHeading
        except:
            print "Error: Could not read gyro heading"
            return ""
        
        
# Simple example prints gyro data once per second:
if __name__ == '__main__':

    from time import sleep
    
    gyro = L3GD20()
    print gyro.deg2rad(1)
    gyro.rangeSelect(2000)
    print gyro.gyroScaleFactor
    while True:
        print gyro.measureGyroSum(), gyro.gyroSampleCount
        print gyro.measureGyro()
        sleep(.01)
