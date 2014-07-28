#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# (c) 2014 Rajat Agarwal 
import logging; log = logging.getLogger(__name__)

from . import BaseEndpointTestCase



class CommissionsEndpointTestCase(BaseEndpointTestCase):
    """
    General
    """
    def test_commissions(self):
        print
        print "----------------------------------------------------------------------"
        print "Request: "
        params = {'from':'2014-01-01T00:00:00Z',
                  'to':'2014-06-01T00:00:00Z',
                 }
        response = self.api.commissions(params)
        print "Response: "
        print response

    def test_commissions_default(self):
        print
        print "----------------------------------------------------------------------"
        print "Request: "
        params = {}
        response = self.api.commissions(params)
        print "Response: "
        print response
