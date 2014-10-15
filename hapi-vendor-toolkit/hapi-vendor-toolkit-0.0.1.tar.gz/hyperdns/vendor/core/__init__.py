"""Utilities for vendor development.

Note: Due to the use of namespace packages to put all drivers in
hyperdns.vendor.drivers.<vkey>, we must make hyperdns.vendor a
namespace package, meaning that it can only contain other packages
and can not itself, contain modules.  For this reason, core
it's own package and is broken out into the detailed files.
"""
from .exceptions import (
    ZoneNotFoundException,
    ResourceNotFoundException,
    RecordAlreadyExistsException,
    TransactionInProgressException,
    TransactionNotInProgressException,
    NotLoggedInException,
    OperationNotSupportedException,
    ImplementationMissingException,
    LoginFailureException,
    MissingRequiredConfigurationException,
    MalformedZoneFQDN,
    ZoneAlreadyExistsException,
    CommunicationsFailureException,
    CreateRecordException,
    DeleteRecordException,
    ZoneCreationException,
    ZoneDeletionException,
    RESTResourceeDisappearanceException,
    ResourceDeletionFailure,
    CanNotUpdateSOARecordsException,
    UnsupportedRecordTypeException
)
from .interface import HyperDNSDriverInterface
from .abstract import AbstractDriver
import time

class ProfilePoint(object):
    """Provide a named sample of a set of time values.  This will maintain
    a circular buffer of the last few samples, according to historySize.
    
    Example::
        p=ProfilePoint('myPoint')
        p.start()
        ....// something that takes 1 second
        p.end()
    
    Which will result in::
        name=myPoint
        count=1
        history=[1]
        historySize=10
        total=1
        avg=1
        delta=1
        last_delta_string=1.000
        
    """
    def __init__(self,name,historySize=10):
        self.name=name
        self.count=0
        self.historyBuffer=[]
        self.historySize=historySize
        self.start_time=None
        self.total=0
        self.delta=None
        
    def start(self):
        """Save the start time, and reset the end_time but take no other action"""
        self.start_time=time.time()
        self.end_time=None
        self.delta=None
    
    def end(self):
        """Calculate the time relative to the last recorded
        start time.
        """
        if self.start_time==None:
            raise Exception('Attempt to call end() on profile point without calling start() first')
        end_time=time.time()
        self.delta=end_time-self.start_time
        idx=self.count % self.historySize
        if idx>=len(self.historyBuffer):
            self.historyBuffer.append(self.delta)
        else:
            self.historyBuffer[idx]=self.delta
        self.count=self.count+1
        self.last_value=self.delta
        self.total=self.total+self.delta

    @property
    def last_delta_string(self):
        if self.delta==None:
            return "n/a"
        else:
            return "%.3fs" % self.delta
    
    @property
    def avg(self):
        """Return 0 or the simple average (total/count)"""
        if self.count==0:
            return 0
        return self.total/self.count
        
    @property
    def history(self):
        if self.count<self.historySize:
            return self.historyBuffer
        retval=[]
        for x in range(self.count-self.historySize,self.count):
            retval.append(self.historyBuffer[x % self.historySize])
        return retval
        

from functools import wraps
        
class login_required(object):
    """This decorator can be used to ensure that a vendor is logged in.
    If the driver's self.loggedIn property is not set, a login will be
    attempted.  If that fails, then a NotLoggedInException will be thrown.
    If the driver's self.loggedIn property is set, then no actions are
    taken and the function call is processed normally.
    
    Example:
    
    ::
    
        @login_required()
        def hasResource(self):
            pass
        
    """
    
    def __init__(self):
        pass
        
    def __call__(self,func):
        @wraps(func)
        def decorated(*args,**kwargs):
            self=args[0]
            if not self.loggedIn:
                if not self.login():
                    raise NotLoggedInException()
                self.loggedIn=True
            return func(*args,**kwargs)
        return decorated

from .base import (
    BaseDriver
)
from .http import HTTPDriver
from .registry import (
    import_driver,
    getAvailableVendorDrivers,
    getAvailableVendorNames,
    getAvailableVendorKeys,
    getAvailableVendorKeyNameTuples,
    _auto_discover_drivers
)

try:
    _auto_discover_drivers()
except:
    pass