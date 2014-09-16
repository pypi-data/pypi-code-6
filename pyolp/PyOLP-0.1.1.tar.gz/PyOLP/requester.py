#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright (C) 2013, Cameron White
#                                                                              
# PyGithub is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.                                                           
#                                                                              
# PyGithub is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS   
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#                                                                      
# You should have received a copy of the GNU Lesser General Public License
# along with PyGithub. If not, see <http://www.gnu.org/licenses/>.

from . import api_exceptions
import urllib
import json

try:
    from urllib import urlopen
except ImportError:
    from urllib.request import urlopen

try: 
    from urlparse import urlparse 
except ImportError:
    from urllib.parse import urlparse

class Requester:
    
    def __init__(self, base_url):

        o = urlparse(base_url)
        self.__base_url = o.geturl()
    
    def requestJsonAndCheck(self, url, parameters=None, requestHeaders=None):
        return self.__check(*self.requestJson(url, parameters, requestHeaders))

    def requestJson(self, url, parameters=None, requestHeaders=None):
        
        parameters = dict(parameters) if parameters else {}
        requestHeaders = dict(requestHeaders) if requestHeaders else {}
        
        if parameters:        
            url = self.__addParametersToUrl(url, parameters)
        
        connection = urlopen(self.__base_url + url)

        output = connection.read()

        try:
            responseHeaders = connection.headers.headers
        except AttributeError:
            responseHeaders = connection.headers.values()

        status = connection.getcode()

        connection.close()
        
        if isinstance(output, bytes):
            output = output.decode("utf-8")

        return status, responseHeaders, json.loads(output)

    def __check(self, status, responseHeaders, output):
        if status >= 400:
            raise api_exceptions.ApiException(status, output)
        return responseHeaders, output
    
    @staticmethod
    def __addParametersToUrl(url, parameters):
        if len(parameters) == 0:
            return url
        else:
            return url + "?" + urllib.urlencode(parameters)
