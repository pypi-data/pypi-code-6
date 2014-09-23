#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# (c) 2014 Rajat Agarwal
import logging; log = logging.getLogger(__name__)

from . import BaseEndpointTestCase



class MerchantsEndpointTestCase(BaseEndpointTestCase):
    """
    General
    """
    def test_merchants(self):
        print
        print "----------------------------------------------------------------------"
        print "Request: "
        params = {'id':'761254',
                 }
        response = self.api.merchants('761254', params)
        #response = self.api.merchants(params)
        print "Response: "
        print response

    def test_merchants_factual(self):
        print
        print "----------------------------------------------------------------------"
        print "Request: "
        params = {'id':'274cd394-fcd3-4d17-8c37-8f5fcafeee80',
                  'namespace':'factual'
                 }
        response = self.api.merchants('274cd394-fcd3-4d17-8c37-8f5fcafeee80',params)
        #response = self.api.merchants(params)
        print "Response: "
        print response

    """
    # Not yet supported
    def test_merchants_foursquare(self):
        print
        print "----------------------------------------------------------------------"
        print "Request: "
        params = {'id':'',
                  'namespace':'foursquare'
                 }
        response = self.api.merchants(params)
        response = self.api.merchants(params)
        print "Response: "
        print response

    def test_merchants_facebook(self):
        print
        print "----------------------------------------------------------------------"
        print "Request: "
        params = {'id':'',
                  'namespace':'facebook'
                 }
        response = self.api.merchants(params)
        response = self.api.merchants(params)
        print "Response: "
        print response

    def test_merchants_google(self):
        print
        print "----------------------------------------------------------------------"
        print "Request: "
        params = {'id':'',
                  'namespace':'google'
                 }
        response = self.api.merchants(params)
        response = self.api.merchants(params)
        print "Response: "
        print response

    def test_merchants_citysearch(self):
        print
        print "----------------------------------------------------------------------"
        print "Request: "
        params = {'id':'',
                  'namespace':'citySearch'
                 }
        response = self.api.merchants(params)
        response = self.api.merchants(params)
        print "Response: "
        print response

    def test_merchants_yelp(self):
        print
        print "----------------------------------------------------------------------"
        print "Request: "
        params = {'id':'',
                  'namespace':'yelp'
                 }
        response = self.api.merchants(params)
        response = self.api.merchants(params)
        print "Response: "
        print response
    """
