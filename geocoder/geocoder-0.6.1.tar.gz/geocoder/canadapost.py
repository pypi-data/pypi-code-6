#!/usr/bin/python
# coding: utf8

from base import Base
import re
import requests


class Canadapost(Base):
    name = 'Canada Post'
    url = 'https://ws1.postescanada-canadapost.ca/AddressComplete'
    url += '/Interactive/RetrieveFormatted/v2.00/json3ex.ws'
    error = 'ERROR - Unknown'

    def __init__(self, location, country, api_key):
        self.location = location
        self.country_code = country
        self.api_key = api_key
        self.json = dict()
        self.params = dict()
        self.params['Key'] = self.retrieve_api_key()
        self.params['Id'] = self.retrieve_id()

    def retrieve_api_key(self):
        if self.api_key:
            return self.api_key
        else:
            url = 'http://www.canadapost.ca/cpo/mc/personal/postalcode/fpc.jsf'
            r = requests.get(url)

            expression = r'key=(....-....-....-....)'
            pattern = re.compile(expression)
            match = pattern.search(r.content)
            if match:
                key = match.group(1)
                self.api_key = key
                return key

    def retrieve_id(self):
        params = dict()
        params['Key'] = self.api_key
        params['SearchTerm'] = self.location
        params['Country'] = self.country_code

        url = 'https://ws1.postescanada-canadapost.ca/AddressComplete'
        url += '/Interactive/Find/v2.00/json3ex.ws'
        r = requests.get(url, params=params)
        json = r.json()

        items = json['Items']

        if items:
            items = items[0]
            if items['Description']:
                self.error = 'ERROR - {0}'.format(items['Description'])
            elif 'Id' in items:
                return items['Id']
        else:
            self.error = 'ERROR - No results found'

    @property
    def ok(self):
        return bool(self.postal)

    @property
    def status(self):
        if self.postal:
            return 'OK'
        else:
            return self.error

    @property
    def quality(self):
        return self.safe_format('DataLevel')

    @property
    def address(self):
        return self.safe_format('Line1')

    @property
    def postal(self):
        return self.safe_format('PostalCode')

    @property
    def street_number(self):
        return self.safe_format('BuildingNumber')

    @property
    def route(self):
        return self.safe_format('Street')

    @property
    def locality(self):
        return self.safe_format('City')

    @property
    def state(self):
        return self.safe_format('ProvinceName')

    @property
    def country(self):
        return self.safe_format('CountryName')

if __name__ == '__main__':
    g = Canadapost(location="1552 Payette dr., Ottawa", country='CAN', api_key='GM59-UZ98-UD69-KW35')
    print g.url
    print g.params