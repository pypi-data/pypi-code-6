#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# (c) 2014 Rajat Agarwal
import logging; log = logging.getLogger(__name__)

from . import BaseEndpointTestCase



class ProvidersEndpointTestCase(BaseEndpointTestCase):
    """
    General
    """
    def test_providers(self):
        print
        print "----------------------------------------------------------------------"
        print "Request: "
        response = self.api.providers()
        print "Response: "
        print response
