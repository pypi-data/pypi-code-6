import ctypes
import ctypes.util

Foundation = ctypes.cdll.LoadLibrary(ctypes.util.find_library('Foundation'))
objc = ctypes.cdll.LoadLibrary(ctypes.util.find_library('objc'))

void_p = ctypes.c_void_p
ull = ctypes.c_uint64

objc.objc_getClass.restype = void_p
objc.sel_registerName.restype = void_p
objc.objc_msgSend.restype = void_p
objc.objc_msgSend.argtypes = [void_p, void_p]

C = objc.objc_getClass
msg = objc.objc_msgSend
n = objc.sel_registerName

# constants from Foundation

NSActivityIdleDisplaySleepDisabled             = (1 << 40)
NSActivityIdleSystemSleepDisabled              = (1 << 20)
NSActivitySuddenTerminationDisabled            = (1 << 14)
NSActivityAutomaticTerminationDisabled         = (1 << 15)
NSActivityUserInitiated                        = (0x00FFFFFF | NSActivityIdleSystemSleepDisabled)
NSActivityUserInitiatedAllowingIdleSystemSleep = (NSActivityUserInitiated & ~NSActivityIdleSystemSleepDisabled)
NSActivityBackground                           = 0x000000FF
NSActivityLatencyCritical                      = 0xFF00000000

def beginActivityWithOptions(options, reason=b""):
    """Wrapper for:
    
    [ [ NSProcessInfo processInfo] 
        beginActivityWithOptions: (int)options
                          reason: (str)reason
    ]
    """
    NSProcessInfo = C('NSProcessInfo')
    NSString = C('NSString')
    
    if not isinstance(reason, bytes):
        reason = reason.encode('utf8')
    
    reason = msg(NSString, n("stringWithUTF8String:"), reason)
    info = msg(NSProcessInfo, n('processInfo'))
    activity = msg(info,
        n('beginActivityWithOptions:reason:'),
        ull(options),
        void_p(reason)
    )
    return activity

def endActivity(activity):
    """end a process activity assertion"""
    NSProcessInfo = C('NSProcessInfo')
    info = msg(NSProcessInfo, n('processInfo'))
    msg(info, n("endActivity:"), void_p(activity))

_theactivity = None

def nope():
    """disable App Nap by setting NSActivityUserInitiatedAllowingIdleSystemSleep"""
    global _theactivity
    _theactivity = beginActivityWithOptions(
        NSActivityUserInitiatedAllowingIdleSystemSleep,
        b"Because Reasons"
    )

def nap():
    """end the caffeinated state started by `nope`"""
    global _theactivity
    if _theactivity is not None:
        endActivity(_theactivity)
        _theactivity = None


nope()