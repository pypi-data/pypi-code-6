#*********************************************************************
#*
#* $Id: yocto_carbondioxide.py 15257 2014-03-06 10:19:36Z seb $
#*
#* Implements yFindCarbonDioxide(), the high-level API for CarbonDioxide functions
#*
#* - - - - - - - - - License information: - - - - - - - - - 
#*
#*  Copyright (C) 2011 and beyond by Yoctopuce Sarl, Switzerland.
#*
#*  Yoctopuce Sarl (hereafter Licensor) grants to you a perpetual
#*  non-exclusive license to use, modify, copy and integrate this
#*  file into your software for the sole purpose of interfacing
#*  with Yoctopuce products.
#*
#*  You may reproduce and distribute copies of this file in
#*  source or object form, as long as the sole purpose of this
#*  code is to interface with Yoctopuce products. You must retain
#*  this notice in the distributed source file.
#*
#*  You should refer to Yoctopuce General Terms and Conditions
#*  for additional information regarding your rights and
#*  obligations.
#*
#*  THE SOFTWARE AND DOCUMENTATION ARE PROVIDED 'AS IS' WITHOUT
#*  WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING 
#*  WITHOUT LIMITATION, ANY WARRANTY OF MERCHANTABILITY, FITNESS
#*  FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO
#*  EVENT SHALL LICENSOR BE LIABLE FOR ANY INCIDENTAL, SPECIAL,
#*  INDIRECT OR CONSEQUENTIAL DAMAGES, LOST PROFITS OR LOST DATA,
#*  COST OF PROCUREMENT OF SUBSTITUTE GOODS, TECHNOLOGY OR 
#*  SERVICES, ANY CLAIMS BY THIRD PARTIES (INCLUDING BUT NOT 
#*  LIMITED TO ANY DEFENSE THEREOF), ANY CLAIMS FOR INDEMNITY OR
#*  CONTRIBUTION, OR OTHER SIMILAR COSTS, WHETHER ASSERTED ON THE
#*  BASIS OF CONTRACT, TORT (INCLUDING NEGLIGENCE), BREACH OF
#*  WARRANTY, OR OTHERWISE.
#*
#*********************************************************************/


__docformat__ = 'restructuredtext en'
from yoctopuce.yocto_api import *


#--- (YCarbonDioxide class start)
#noinspection PyProtectedMember
class YCarbonDioxide(YSensor):
    """
    The Yoctopuce application programming interface allows you to read an instant
    measure of the sensor, as well as the minimal and maximal values observed.
    
    """
#--- (end of YCarbonDioxide class start)
    #--- (YCarbonDioxide return codes)
    #--- (end of YCarbonDioxide return codes)
    #--- (YCarbonDioxide definitions)
    #--- (end of YCarbonDioxide definitions)

    def __init__(self, func):
        super(YCarbonDioxide, self).__init__(func)
        self._className = 'CarbonDioxide'
        #--- (YCarbonDioxide attributes)
        self._callback = None
        #--- (end of YCarbonDioxide attributes)

    #--- (YCarbonDioxide implementation)
    def _parseAttr(self, member):
        super(YCarbonDioxide, self)._parseAttr(member)

    @staticmethod
    def FindCarbonDioxide(func):
        """
        Retrieves a CO2 sensor for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>
        
        This function does not require that the CO2 sensor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YCarbonDioxide.isOnline() to test if the CO2 sensor is
        indeed online at a given time. In case of ambiguity when looking for
        a CO2 sensor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.
        
        @param func : a string that uniquely characterizes the CO2 sensor
        
        @return a YCarbonDioxide object allowing you to drive the CO2 sensor.
        """
        # obj
        obj = YFunction._FindFromCache("CarbonDioxide", func)
        if obj is None:
            obj = YCarbonDioxide(func)
            YFunction._AddToCache("CarbonDioxide", func, obj)
        return obj

    def nextCarbonDioxide(self):
        """
        Continues the enumeration of CO2 sensors started using yFirstCarbonDioxide().
        
        @return a pointer to a YCarbonDioxide object, corresponding to
                a CO2 sensor currently online, or a None pointer
                if there are no more CO2 sensors to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YCarbonDioxide.FindCarbonDioxide(hwidRef.value)

#--- (end of YCarbonDioxide implementation)

#--- (CarbonDioxide functions)

    @staticmethod
    def FirstCarbonDioxide():
        """
        Starts the enumeration of CO2 sensors currently accessible.
        Use the method YCarbonDioxide.nextCarbonDioxide() to iterate on
        next CO2 sensors.
        
        @return a pointer to a YCarbonDioxide object, corresponding to
                the first CO2 sensor currently online, or a None pointer
                if there are none.
        """
        devRef = YRefParam()
        neededsizeRef = YRefParam()
        serialRef = YRefParam()
        funcIdRef = YRefParam()
        funcNameRef = YRefParam()
        funcValRef = YRefParam()
        errmsgRef = YRefParam()
        size = YAPI.C_INTSIZE
        #noinspection PyTypeChecker,PyCallingNonCallable
        p = (ctypes.c_int * 1)()
        err = YAPI.apiGetFunctionsByClass("CarbonDioxide", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YCarbonDioxide.FindCarbonDioxide(serialRef.value + "." + funcIdRef.value)

#--- (end of CarbonDioxide functions)
