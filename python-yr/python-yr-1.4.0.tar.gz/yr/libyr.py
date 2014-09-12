#!/usr/bin/env python3

import sys
import json
import xmltodict # <~ the only external dependency
from yr.utils import Connect, Location, LocationXYZ, Language, YrException

class Yr:

    def py2json(self, python):
        return json.dumps(python, indent=4)

    def xml2dict(self, xml):
        return xmltodict.parse(xml)

    def dict2xml(self, dictionary):
        return xmltodict.unparse(dictionary, pretty=True)

    def py2result(self, python, as_json=False): # default is return result as dictionary ;)
        if as_json:
            return self.py2json(python)
        else:
            return python

    def forecast(self, as_json=False):
        if self.location_xyz:
            times = self.dictionary['weatherdata']['product']['time']
        else:
            times = self.dictionary['weatherdata']['forecast']['tabular']['time']
        for time in times:
            yield self.py2result(time, as_json)

    def now(self, as_json=False):
        return next(self.forecast(as_json))

    def __init__(self, location_name=None, location_xyz=None, forecast_link='forecast', language_name='en'):
        self.language_name = language_name
        self.forecast_link = forecast_link       
        self.language = Language(self.language_name)
        if location_name:
            self.location_name = location_name
            self.location_xyz = None
            self.location = Location(self.location_name, self.forecast_link, self.language)
        elif location_xyz:
            self.location_name = None
            self.location_xyz = location_xyz
            self.location = LocationXYZ(location_xyz[0], location_xyz[1], location_xyz[2])
        else:
            raise YrException("location_name or location_xyz parameter must be set")
        self.connect = Connect(self.location)
        self.xml_source = self.connect.read()
        self.dictionary = self.xml2dict(self.xml_source)
        self.credit = {
            'text': self.language.dictionary['credit'],
            'url': 'http://www.yr.no/'
        }

if __name__ == '__main__':
    print(Yr(location_name='Czech_Republic/Prague/Prague').now(as_json=True))
