#!/usr/bin/python
# coding: utf8

from base import Base


class Bing(Base):
    name = 'Bing'
    url = 'http://dev.virtualearth.net/REST/v1/Locations'

    def __init__(self, location, key):
        self.location = location
        self.params = dict()
        self.json = dict()
        self.params['maxResults'] = 1
        self.params['key'] = key
        self.params['q'] = location
        if not key:
            self.help_key()

    @property
    def lat(self):
        return self.safe_coord('coordinates-0')

    @property
    def lng(self):
        return self.safe_coord('coordinates-1')

    @property
    def route(self):
        return self.safe_format('address-addressLine')

    @property
    def address(self):
        return self.safe_format('address-formattedAddress')

    @property
    def status(self):
        return self.safe_format('statusDescription')

    @property
    def quality(self):
        return self.safe_format('resources-entityType')

    @property
    def postal(self):
        return self.safe_format('address-postalCode')

    @property
    def bbox(self):
        south = self.json.get('bbox-0')
        west = self.json.get('bbox-1')
        north = self.json.get('bbox-2')
        east = self.json.get('bbox-3')
        return self.safe_bbox(south, west, north, east)

    @property
    def locality(self):
        return self.safe_format('address-locality')

    @property
    def state(self):
        return self.safe_format('address-adminDistrict')

    @property
    def country(self):
        return self.safe_format('address-countryRegion')

    def help_key(self):
        print '<ERROR>'
        print 'Please provide a <key> paramater when using Bing'
        print '    >>> import geocoder'
        print '    >>> key = "XXXX"'
        print '    >>> g = geocoder.bing(<location>, key=key)'
        print ''
        print 'How to get a Key?'
        print '-----------------'
        print 'http://msdn.microsoft.com/en-us/library/ff428642.aspx'
