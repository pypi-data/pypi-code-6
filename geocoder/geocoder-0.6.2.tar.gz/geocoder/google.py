#!/usr/bin/python
# coding: utf8

from base import Base
import hashlib
import urllib
import hmac
import base64
import urlparse


class Google(Base):
    name = 'Google'
    url = 'https://maps.googleapis.com/maps/api/geocode/json'

    def __init__(self, location, short_name=True, client='', secret='', api_key=''):
        self.location = location
        self.short_name = short_name
        self.json = dict()
        self.params = dict()
        self.params['sensor'] = 'false'
        self.params['address'] = location

        # New Encryption for Authentication Google Maps for Business
        if bool(client and secret):
            self.params['client'] = client
            self.params['signature'] = self.get_signature(self.url, self.params, secret)

        # Using old Authentication Google Maps V3
        elif api_key:
            self.params['key'] = api_key

    def get_signature(self, url, params, secret):
        # Convert the URL string to a URL
        params = urllib.urlencode(params)
        url = urlparse.urlparse(url + '?' + params)

        # Signature Key
        urlToSign = url.path + "?" + url.query

        # Decode the private key into its binary format
        decodedKey = base64.urlsafe_b64decode(secret)

        # Create a signature using the private key and the URL-encoded
        # string using HMAC SHA1. This signature will be binary.
        signature = hmac.new(decodedKey, urlToSign, hashlib.sha1)

        # Encode the binary signature into base64 for use within a URL
        encodedSignature = base64.urlsafe_b64encode(signature.digest())
        return encodedSignature

    @property
    def lat(self):
        return self.safe_coord('location-lat')

    @property
    def lng(self):
        return self.safe_coord('location-lng')

    @property
    def status(self):
        return self.safe_format('status')

    @property
    def quality(self):
        return self.safe_format('geometry-location_type')

    @property
    def bbox(self):
        south = self.json.get('southwest-lat')
        west = self.json.get('southwest-lng')
        north = self.json.get('northeast-lat')
        east = self.json.get('northeast-lng')
        return self.safe_bbox(south, west, north, east)

    @property
    def address(self):
        return self.safe_format('results-formatted_address')

    @property
    def postal(self):
        if self.short_name:
            return self.safe_format('postal_code')
        else:
            return self.safe_format('postal_code-long_name')

    @property
    def street_number(self):
        if self.short_name:
            return self.safe_format('street_number')
        else:
            return self.safe_format('street_number-long_name')

    @property
    def route(self):
        if self.short_name:
            return self.safe_format('route')
        else:
            return self.safe_format('route-long_name')

    @property
    def neighborhood(self):
        if self.short_name:
            return self.safe_format('neighborhood')
        else:
            return self.safe_format('neighborhood-long_name')

    @property
    def sublocality(self):
        if self.short_name:
            return self.safe_format('sublocality')
        else:
            return self.safe_format('sublocality-long_name')

    @property
    def locality(self):
        if self.short_name:
            return self.safe_format('locality')
        else:
            return self.safe_format('locality-long_name')

    @property
    def county(self):
        if self.short_name:
            return self.safe_format('administrative_area_level_2')
        else:
            return self.safe_format('administrative_area_level_2-long_name')

    @property
    def state(self):
        if self.short_name:
            return self.safe_format('administrative_area_level_1')
        else:
            return self.safe_format('administrative_area_level_1-long_name')

    @property
    def country(self):
        if self.short_name:
            return self.safe_format('country')
        else:
            return self.safe_format('country-long_name')

if __name__ == '__main__':
    g = Google("Orleans, Ottawa")
    print g.url