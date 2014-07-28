#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# (c) 2014 Rajat Agarwal
import logging; log = logging.getLogger(__name__)

from . import BaseEndpointTestCase

class DealsEndpointTestCase(BaseEndpointTestCase):
    """
    General
    """
    def test_deals(self):
        print
        print "----------------------------------------------------------------------"
        print "Request: "
        params = {
                  "total": 1000,
                  "page": 1,
                  "per_page": 10,
                  "query": "bagel",
                  "online": 1,
                  "location": {"address":     "444 Castro St.",
                               "locality":    "Mountain View",
                               "region":      "CA",
                               "postal_code": "94041",
                               "country":     "United States",
                               "latitude":    37.390751,
                               "longitude":   -122.080953
                              },
                  #"radius": 11, #TODO::: Doesn't seem to work
                  #"category_slugs": [], # [] means you're restricting to a 0 set and it would imply 0 results
                  #"provider_slugs": [], # [] means you're restricting to a 0 set and it would imply 0 results
                  "updated_after": "2013-11-04T16:18:04Z",
                  "order": "expires_at"
                 }
        response = self.api.deals(params)
        print "Response: "
        print response


    def test_deals_default(self):
        print
        print "----------------------------------------------------------------------"
        print "Request: "
        params = {
                  "location": {"address":     "444 Castro St.",
                               "locality":    "Mountain View",
                               "region":      "CA",
                               "postal_code": "94041",
                               "country":     "United States",
                               "latitude":    37.390751,
                               "longitude":   -122.080953
                              },
                 }
        response = self.api.deals(params)
        print "Response: "
        print response


    def test_deal(self):
        print
        print "----------------------------------------------------------------------"
        print "Request: "
        params = {
                  "user_id":1234, # Dummy user ID - helps track when commissions api is called
                  # Any other information that we want to track for this deal
                 }
        response = self.api.deals.deal(781892, params)
        print "Response: "
        print response


    def test_clickTrack(self):
        print
        print "----------------------------------------------------------------------"
        print "Request: "
        response = self.api.deals.clickTrack(781892)
        print "Response: "
        f = open('deal.html', 'w')
        f.write(response['data'])
        f.close()
        print "Wrote response to deal.html"
        #print response

    def test_image(self):
        print
        print "----------------------------------------------------------------------"
        print "Request: "
        params = {
                  "offer_id":1234,
                  "geometry":"400x300"
                 }
        response = self.api.deals.image(781892, params)
        print "Response: "
        f = open('dealImage.gif', 'wb')
        f.write(response['data'])
        f.close()
        print "Wrote response to dealImage.gif"
        #print response
