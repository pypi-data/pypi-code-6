import logging
from  hyperdns.vendor.core import (
    HyperDNSDriverInterface,
    ZoneNotFoundException,
    TransactionInProgressException,
    TransactionNotInProgressException,
    NotLoggedInException,
    LoginFailureException,
    MissingRequiredConfigurationException
) 
from hyperdns.netdns import (
    splitHostFqdn
    )
import time
from .base import (
    login_required,
    BaseDriver
)
from http.client import HTTPConnection,HTTPSConnection
import json
import urllib.parse
import requests

class HTTPDriver(BaseDriver):
    """This utility class can be used for simple JSON based REST apis.
    
    It expects a 'host' and a 'port' parameter in the settings, and will
    automatically login when constructed - or throw an exception (see BaseDriver)
    
    An HTTPS connection is created by default, but that can be changed by
    passing secure=False to the ctor, which will use an HTTPConnection instead
    of an HTTPSConnection.

    """
    def __init__(self,settings,immediateLogin=True,secure=True):
        
        self.host=settings.get('host')
        if self.host==None:
            raise MissingRequiredConfigurationException("Missing host parameter in settings")
        while self.host.endswith('/'):
            self.host=self.host[:-1]
            
        self.port=int(settings.get('port'))
        if self.port==None:
            raise MissingRequiredConfigurationException("Missing port parameter in settings")
        
        if self.port==443:
            self.uriPrefix="https://%s:%s" % (self.host,self.port)
        else:
            self.uriPrefix="http://%s:%s" % (self.host,self.port)
                
        self.loggedIn=False
        
        # Build headers
        self.headers = {
            'Content-Type': 'application/json'
        }

        super(HTTPDriver,self).__init__(settings,immediateLogin)

        self.httplog=logging.getLogger('vendorhttp.%s' % self.vkey)

    @login_required()
    def logout(self):
        self.loggedIn=False


    def _execute(self, uri, method, request_data = None):
        """Execute a commands against the rest server.
        
        This internal method does not require login.  It executes the method
        an honors 307 responses to assemble multi-part responses.  It also
        decodes the response object on success.

        :param str uri: The uri of the resource to access.
        :param str method: One of 'DELETE', 'GET', 'POST', or 'PUT'
        :param str request_data: Any arguments to be sent as a part of the request
        :rtype: Tuple (status,result)
        :returns: The status and the response, where success status is read as
           a 200.  If not success, then the HTTP response is provided, otherwise
           the JSON response is decoded and returned.
        """
        # Prepare arguments
        if request_data is None:
            request_data = {}
        request_data = json.dumps(request_data)
        
        url='%s%s' % (self.uriPrefix,uri)
        self.httplog.debug("Executing '%s' on %s with data:%s'" % (method,url,request_data))
        
        response = requests.request(method, url, params=None, data=request_data, headers=self.headers)
        
        if response.status_code == 307:
            while response.status_code == 307:
                time.sleep(1)
                uri = response.getheader('Location')
                self.httplog.debug("Polling %s\n" % uri)

                response = requests.request('GET', url)
        
        self.httplog.debug("Result %d on %s %s" % (response.status_code,method,url))
                
        if response.status_code < 200 or response.status_code > 299:
            return (False,response)
        
        if response.status_code == 204: # no content
            return (True,None)
        
        return (True,response.json())


    @login_required()
    def _grab(self,uri,args={},exceptionIfNotFound=True):
        """ simple GET of a URI, requiring login, with optional json body from args.
        This method wraps :meth:`_execute` with a login requirement and transmutes
        any failures into an Exception.  It also returns only the resulting object
        in the case of success, avoiding the need to unwrap the response.
        
        :raises Exception: If the GET did not succeed
        :returns: The fetched object
        :rtype: JSON
        """
        (success,obj) = self._execute(uri, 'GET',args)
        if not success:
            if not exceptionIfNotFound and obj.status_code==404:
                return None
            raise Exception("Failed (%s:%s) executing GET on '%s' with args: %s" % 
                            (obj.status_code,obj.content,uri,args))
        return obj
        
