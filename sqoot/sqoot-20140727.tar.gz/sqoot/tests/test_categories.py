#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# (c) 2014 Rajat Agarwal 
import logging; log = logging.getLogger(__name__)

from . import BaseEndpointTestCase



class CategoriesEndpointTestCase(BaseEndpointTestCase):
    """
    General
    """
    def test_categories(self):
        print 
        print "----------------------------------------------------------------------"
        print "Request: "
        response = self.api.categories()
        print "Response: "
        print response
        #assert 'categories' in response
