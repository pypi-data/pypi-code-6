#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# (c) 2014 Rajat Agarwal
import logging; log = logging.getLogger(__name__)

from . import BaseEndpointTestCase

class CouponsEndpointTestCase(BaseEndpointTestCase):
    """
    General
    """
    def test_coupons(self):
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
        response = self.api.coupons(params)
        print "Response: "
        print response


    def test_coupons_default(self):
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
        response = self.api.coupons(params)
        print "Response: "
        print response


    def test_coupon(self):
        print
        print "----------------------------------------------------------------------"
        print "Request: "
        params = {
                  "user_id":1234, # Dummy user ID - helps track when commissions api is called
                  # Any other information that we want to track for this coupon
                 }
        response = self.api.coupons.coupon(9722, params)
        print "Response: "
        print response


    def test_clickTrack(self):
        print
        print "----------------------------------------------------------------------"
        print "Request: "
        response = self.api.coupons.clickTrack(9722)
        print "Response: "
        f = open('coupon.html', 'w')
        f.write(response['data'])
        f.close()
        print "Wrote response to coupon.html"
        #print response

    def test_image(self):
        print
        print "----------------------------------------------------------------------"
        print "Request: "
        params = {
                  "offer_id":9722,
                  "geometry":"400x300"
                 }
        response = self.api.coupons.image(9722, params)
        print "Response: "
        f = open('couponImage.gif', 'wb')
        f.write(response['data'])
        f.close()
        print "Wrote response to couponImage.gif"
        #print response
