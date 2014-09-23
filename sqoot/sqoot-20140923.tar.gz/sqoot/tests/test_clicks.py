#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# (c) 2014 Rajat Agarwal 
import logging; log = logging.getLogger(__name__)

from . import BaseEndpointTestCase



class ClicksEndpointTestCase(BaseEndpointTestCase):
    """
    General
    """
    def test_clicks(self):
        print
        print "----------------------------------------------------------------------"
        print "Request: "
        params = {'from':'2014-01-01T00:00:00Z',
                  'to':'2014-06-01T00:00:00Z',
                  'page':1
                 }
        response = self.api.clicks(params)
        print "Response: "
        print response
        #assert 'categories' in response

    def test_clicks_default(self):
        print
        print "----------------------------------------------------------------------"
        print "Request: "
        params = {}
        response = self.api.clicks(params)
        print "Response: "
        print response
        #assert 'categories' in response
