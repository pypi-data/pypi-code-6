#!/usr/bin/python
# coding: utf8

from base import Base
import re
import requests


class Canadapost(Base):
    provider = 'CanadaPost'
    api = 'Addres Complete API'
    url = 'https://ws1.postescanada-canadapost.ca/AddressComplete'
    url += '/Interactive/RetrieveFormatted/v2.00/json3ex.ws'
    _description = 'The next generation of address finders, AddressComplete uses intelligent, fast\n'
    _description += 'searching to improve data accuracy and relevancy. Simply start typing a business\n'
    _description += 'name, address or Postal Code and AddressComplete will suggest results as you go.'
    _api_reference = ['[{0}](https://www.canadapost.ca/pca/)'.format(api)]
    _api_parameter = [':param ``country``: (default=\'CAN\') biase the search on a selected country.']
    _api_parameter  = [':param ``key``: (optional) use your own API Key from CanadaPost Address Complete.']
    _example = ['>>> g = geocoder.canadapost(\'<address>\')',
                '>>> g.postal',
                '\'K1R 7K9\'']

    def __init__(self, location, country='CAN', key=''):
        self.location = location
        self._country = country
        self.key = key
        self.json = dict()
        self.parse = dict()
        self.params = dict()
        self.params['Key'] = self._retrieve_api_key()
        self.params['Id'] = self._retrieve_id()

        # Initialize
        self._connect()
        self._parse(self.content)
        self._test()
        self._json()

    def _retrieve_api_key(self):
        if self.api_key:
            return self.api_key
        else:
            url = 'http://www.canadapost.ca/cpo/mc/personal/postalcode/fpc.jsf'
            try:
                r = requests.get(url)
            except:
                self.status = 'ERROR - URL Connection'

            expression = r'key=(....-....-....-....)'
            pattern = re.compile(expression)
            match = pattern.search(r.content)
            if match:
                key = match.group(1)
                self.api_key = key
                return key
            else:
                self.status = 'ERROR - No API Key'

    def _retrieve_id(self):
        params = dict()
        params['Key'] = self.api_key
        params['SearchTerm'] = self.location
        params['Country'] = self._country

        url = 'https://ws1.postescanada-canadapost.ca/AddressComplete'
        url += '/Interactive/Find/v2.00/json3ex.ws'
        r = requests.get(url, params=params)
        json = r.json()

        items = json['Items']

        if items:
            items = items[0]
            if items['Description']:
                self.status = 'ERROR - {0}'.format(items['Description'])
            elif 'Id' in items:
                return items['Id']
        else:
            self.status = 'ERROR - No results found'

    @property
    def ok(self):
        return bool(self.postal)

    @property
    def status_description(self):
        if self.postal:
            return 'OK'
        else:
            return self.status

    @property
    def quality(self):
        return self._get_json_str('Type')

    @property
    def address(self):
        return self._get_json_str('Line1')

    @property
    def postal(self):
        return self._get_json_str('PostalCode')

    @property
    def street_number(self):
        return self._get_json_str('BuildingNumber')

    @property
    def route(self):
        return self._get_json_str('Street')

    @property
    def locality(self):
        return self._get_json_str('City')

    @property
    def state(self):
        return self._get_json_str('ProvinceName')

    @property
    def country(self):
        return self._get_json_str('CountryName')

if __name__ == '__main__':
    g = Canadapost(location="453 Booth Street, Ottawa")
    g.help()
    g.debug()