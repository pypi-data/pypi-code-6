#*********************************************************************
#*
#* $Id: yocto_voc.py 15257 2014-03-06 10:19:36Z seb $
#*
#* Implements yFindVoc(), the high-level API for Voc functions
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


#--- (YVoc class start)
#noinspection PyProtectedMember
class YVoc(YSensor):
    """
    The Yoctopuce application programming interface allows you to read an instant
    measure of the sensor, as well as the minimal and maximal values observed.
    
    """
#--- (end of YVoc class start)
    #--- (YVoc return codes)
    #--- (end of YVoc return codes)
    #--- (YVoc definitions)
    #--- (end of YVoc definitions)

    def __init__(self, func):
        super(YVoc, self).__init__(func)
        self._className = 'Voc'
        #--- (YVoc attributes)
        self._callback = None
        #--- (end of YVoc attributes)

    #--- (YVoc implementation)
    def _parseAttr(self, member):
        super(YVoc, self)._parseAttr(member)

    @staticmethod
    def FindVoc(func):
        """
        Retrieves a Volatile Organic Compound sensor for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>
        
        This function does not require that the Volatile Organic Compound sensor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YVoc.isOnline() to test if the Volatile Organic Compound sensor is
        indeed online at a given time. In case of ambiguity when looking for
        a Volatile Organic Compound sensor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.
        
        @param func : a string that uniquely characterizes the Volatile Organic Compound sensor
        
        @return a YVoc object allowing you to drive the Volatile Organic Compound sensor.
        """
        # obj
        obj = YFunction._FindFromCache("Voc", func)
        if obj is None:
            obj = YVoc(func)
            YFunction._AddToCache("Voc", func, obj)
        return obj

    def nextVoc(self):
        """
        Continues the enumeration of Volatile Organic Compound sensors started using yFirstVoc().
        
        @return a pointer to a YVoc object, corresponding to
                a Volatile Organic Compound sensor currently online, or a None pointer
                if there are no more Volatile Organic Compound sensors to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YVoc.FindVoc(hwidRef.value)

#--- (end of YVoc implementation)

#--- (Voc functions)

    @staticmethod
    def FirstVoc():
        """
        Starts the enumeration of Volatile Organic Compound sensors currently accessible.
        Use the method YVoc.nextVoc() to iterate on
        next Volatile Organic Compound sensors.
        
        @return a pointer to a YVoc object, corresponding to
                the first Volatile Organic Compound sensor currently online, or a None pointer
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
        err = YAPI.apiGetFunctionsByClass("Voc", 0, p, size, neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(
                YAPI.yapiGetFunctionInfo(p[0], devRef, serialRef, funcIdRef, funcNameRef, funcValRef, errmsgRef)):
            return None

        return YVoc.FindVoc(serialRef.value + "." + funcIdRef.value)

#--- (end of Voc functions)
