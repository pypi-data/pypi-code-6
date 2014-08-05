#!/usr/bin/env python
# Program Name: OpenElectrons_BMP180.py 
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
# Some of this code is derived from Adafruit_BMP085.py
#
# History:
# Date            Author            Comments
# 07/31/14        Michael Giles     Initial authoring.
#
# @package OpenElectrons_BMP180
# Python library for Openelectrons_BMP180.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import time
from OpenElectrons_i2c import OpenElectrons_i2c

## BMP180: this class provides functions for temperature, pressure, and altitude of the BMP180 IC
#  for read and write operations.

class BMP180(OpenElectrons_i2c) :
  
    # BMP180 default i2c address
    PRESSURE_ADDRESS = (0xEE)  

    # Operating Modes
    __BMP180_ULTRALOWPOWER     = 0
    __BMP180_STANDARD          = 1
    __BMP180_HIGHRES           = 2
    __BMP180_ULTRAHIGHRES      = 3

    # BMP180 Registers
    __BMP180_CAL_AC1           = 0xAA  # R   Calibration data (16 bits)
    __BMP180_CAL_AC2           = 0xAC  # R   Calibration data (16 bits)
    __BMP180_CAL_AC3           = 0xAE  # R   Calibration data (16 bits)
    __BMP180_CAL_AC4           = 0xB0  # R   Calibration data (16 bits)
    __BMP180_CAL_AC5           = 0xB2  # R   Calibration data (16 bits)
    __BMP180_CAL_AC6           = 0xB4  # R   Calibration data (16 bits)
    __BMP180_CAL_B1            = 0xB6  # R   Calibration data (16 bits)
    __BMP180_CAL_B2            = 0xB8  # R   Calibration data (16 bits)
    __BMP180_CAL_MB            = 0xBA  # R   Calibration data (16 bits)
    __BMP180_CAL_MC            = 0xBC  # R   Calibration data (16 bits)
    __BMP180_CAL_MD            = 0xBE  # R   Calibration data (16 bits)
    __BMP180_CONTROL           = 0xF4
    __BMP180_TEMPDATA          = 0xF6
    __BMP180_PRESSUREDATA      = 0xF6
    __BMP180_READTEMPCMD       = 0x2E
    __BMP180_READPRESSURECMD   = 0x34

    # Private Fields
    _cal_AC1 = 0
    _cal_AC2 = 0
    _cal_AC3 = 0
    _cal_AC4 = 0
    _cal_AC5 = 0
    _cal_AC6 = 0
    _cal_B1 = 0
    _cal_B2 = 0
    _cal_MB = 0
    _cal_MC = 0
    _cal_MD = 0

    ## Initialize the class with the i2c address of the BMP180
    #  @param self The object pointer.
    #  @param i2c_address Address of your accelerometer.
    def __init__(self, pressure_address = PRESSURE_ADDRESS):
        OpenElectrons_i2c.__init__(self, pressure_address >> 1)
        # Make sure the specified mode is in the appropriate range
        self.mode = self.__BMP180_STANDARD   
        # Read the calibration data
        self.readCalibrationData()

    ## Reads the calibration data from the BMP180 IC
    #  @param self The object pointer.
    def readCalibrationData(self):
        try:
            self._cal_AC1 = self.readIntegerSignedBE(self.__BMP180_CAL_AC1)   # INT16
            self._cal_AC2 = self.readIntegerSignedBE(self.__BMP180_CAL_AC2)   # INT16
            self._cal_AC3 = self.readIntegerSignedBE(self.__BMP180_CAL_AC3)   # INT16
            self._cal_AC4 = self.readIntegerBE(self.__BMP180_CAL_AC4)   # UINT16
            self._cal_AC5 = self.readIntegerBE(self.__BMP180_CAL_AC5)   # UINT16
            self._cal_AC6 = self.readIntegerBE(self.__BMP180_CAL_AC6)   # UINT16
            self._cal_B1 = self.readIntegerSignedBE(self.__BMP180_CAL_B1)     # INT16
            self._cal_B2 = self.readIntegerSignedBE(self.__BMP180_CAL_B2)     # INT16
            self._cal_MB = self.readIntegerSignedBE(self.__BMP180_CAL_MB)     # INT16
            self._cal_MC = self.readIntegerSignedBE(self.__BMP180_CAL_MC)     # INT16
            self._cal_MD = self.readIntegerSignedBE(self.__BMP180_CAL_MD)     # INT16
        except:
            print "Error: Could not retrieve calibration data"
            return ""
            
    ## Prints the calibration data for debugging purposes
    #  @param self The object pointer.
    def showCalibrationData(self):
        try:
            print "DBG: AC1 = %6d" % (self._cal_AC1)
            print "DBG: AC2 = %6d" % (self._cal_AC2)
            print "DBG: AC3 = %6d" % (self._cal_AC3)
            print "DBG: AC4 = %6d" % (self._cal_AC4)
            print "DBG: AC5 = %6d" % (self._cal_AC5)
            print "DBG: AC6 = %6d" % (self._cal_AC6)
            print "DBG: B1  = %6d" % (self._cal_B1)
            print "DBG: B2  = %6d" % (self._cal_B2)
            print "DBG: MB  = %6d" % (self._cal_MB)
            print "DBG: MC  = %6d" % (self._cal_MC)
            print "DBG: MD  = %6d" % (self._cal_MD)
        except:
            print "Error: Could not print calibration data"
            return ""
            
    ## Reads raw temperature value
    #  @param self The object pointer.
    def readRawTemp(self):
        try:
            self.writeByte(self.__BMP180_CONTROL, self.__BMP180_READTEMPCMD)
            time.sleep(0.005)  # Wait 5ms
            raw = self.readIntegerBE(self.__BMP180_TEMPDATA)
            return raw
        except:
            print "Error: Could not read raw temperature value"
            return ""

    ## Reads raw pressure value
    #  @param self The object pointer.    
    def readRawPressure(self):
        try:
            self.writeByte(self.__BMP180_CONTROL, self.__BMP180_READPRESSURECMD + (self.mode << 6))
            if (self.mode == self.__BMP180_ULTRALOWPOWER):
                time.sleep(0.005)
            elif (self.mode == self.__BMP180_HIGHRES):
                time.sleep(0.014)
            elif (self.mode == self.__BMP180_ULTRAHIGHRES):
                time.sleep(0.026)
            else:
                time.sleep(0.008)
            msb = self.readByte(self.__BMP180_PRESSUREDATA)
            lsb = self.readByte(self.__BMP180_PRESSUREDATA+1)
            xlsb = self.readByte(self.__BMP180_PRESSUREDATA+2)
            raw = ((msb << 16) + (lsb << 8) + xlsb) >> (8 - self.mode)
            return raw
        except:
            print "Error: Could not read raw pressure value"
            return ""            

    ## Reads the temperature value in degrees Celcius calculated from the raw temperature value
    #  @param self The object pointer.  
    def readTemperature(self):
        try:
            UT = 0
            X1 = 0
            X2 = 0
            B5 = 0
            temp = 0.0
            # Read raw temp before aligning it with the calibration values
            UT = self.readRawTemp()
            X1 = ((UT - self._cal_AC6) * self._cal_AC5) >> 15
            X2 = (self._cal_MC << 11) / (X1 + self._cal_MD)
            B5 = X1 + X2
            temp = ((B5 + 8) >> 4) / 10.0
            return temp
        except:
            print "Error: Could not read temperature value"
            return ""

    ## Reads the pressure value in pascal calculated from the raw pressure value
    #  @param self The object pointer.  
    def readPressure(self):
        try:
            UT = 0
            UP = 0
            B3 = 0
            B5 = 0
            B6 = 0
            X1 = 0
            X2 = 0
            X3 = 0
            p = 0
            B4 = 0
            B7 = 0
            UT = self.readRawTemp()
            UP = self.readRawPressure()
            # True Temperature Calculations
            X1 = ((UT - self._cal_AC6) * self._cal_AC5) >> 15
            X2 = (self._cal_MC << 11) / (X1 + self._cal_MD)
            B5 = X1 + X2
            # Pressure Calculations
            B6 = B5 - 4000
            X1 = (self._cal_B2 * (B6 * B6) >> 12) >> 11
            X2 = (self._cal_AC2 * B6) >> 11
            X3 = X1 + X2
            B3 = (((self._cal_AC1 * 4 + X3) << self.mode) + 2) / 4
    
            X1 = (self._cal_AC3 * B6) >> 13
            X2 = (self._cal_B1 * ((B6 * B6) >> 12)) >> 16
            X3 = ((X1 + X2) + 2) >> 2
            B4 = (self._cal_AC4 * (X3 + 32768)) >> 15
            B7 = (UP - B3) * (50000 >> self.mode)
            if (B7 < 0x80000000):
                p = (B7 * 2) / B4
            else:
                p = (B7 / B4) * 2
            X1 = (p >> 8) * (p >> 8)
            X1 = (X1 * 3038) >> 16
            X2 = (-7357 * p) >> 16
            p = p + ((X1 + X2 + 3791) >> 4)
            return p
        except:
            print "Error: Could not read pressure value"
            return ""

    ## Reads the altitude value in meters calculated from the pressure value
    #  @param self The object pointer.  
    #  @param seaLevelPressure The sea level pressure.
    def readAltitude(self, seaLevelPressure=101325):
        try:
            altitude = 0.0
            pressure = float(self.readPressure())
            altitude = 44330.0 * (1.0 - pow(pressure / seaLevelPressure, 0.1903))
            return altitude
            return 0
        except:
            print "Error: Could not read altitude"
            return ""            

# example displays temperature, pressure, and altitude values 
if __name__ == '__main__':

    from time import sleep

    bmp = BMP180()
   
    while True:
        temp = bmp.readTemperature()
        pressure = bmp.readPressure()
        altitude = bmp.readAltitude()
        print "Temperature: %.2f C" % temp
        print "Pressure:    %.2f hPa" % (pressure / 100.0)
        print "Altitude:    %.2f" % altitude
        sleep(1) 
