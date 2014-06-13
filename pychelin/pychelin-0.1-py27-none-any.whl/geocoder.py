import binascii
import hmac
import hashlib
import requests

from datetime import (
    datetime,
    timedelta,
)

from iso3166 import countries
from urllib import (
    urlencode,
    unquote,
)
from .parser import getParser

__all__ = [
    'Geocoder',
    'GeocoderError',
]

BASE_URL = "http://apir.viamichelin.com"
GEOCODER_BASE_URL = "/apir/1/geocode4f.%s?"


class GeocoderError(requests.ConnectionError):
    pass


class Geocoder(object):
    def __init__(self, authkey, key, output='xml'):
        """helper class to retrieve lat/long from an address using the
        viamichelin api.

        @param authkey: ID of your viamichelin api account
        @type authkey: string

        @param key: Password of your viamichelin api account
        @type key: string

        @param output: type of the response.
        @type output: string. Must be 'xml' or 'json'
        """
        self.base_url = BASE_URL
        self.output = output
        self.geocode_base_url = GEOCODER_BASE_URL % output
        self.authkey = authkey
        self.key = key

        # The parser class corresponding to the response format
        self.parser = getParser(output)

    def __generate_url(self, data):
        """generate the url with urlencode and add a parameter which is a b64
        signature of the generated url.
        """
        geocode_url = unquote(self.geocode_base_url + urlencode(data))
        signature_url = urlencode(
            {'signature': self.__sign_url(geocode_url)}
        )
        return self.base_url + geocode_url + '&' + signature_url

    def __sign_url(self, url):
        """Use HMAC-SHA1 to sign url
        """
        hashed = hmac.new(self.key.encode('utf-8'), url, hashlib.sha1)
        return binascii.b2a_base64(hashed.digest())[:-1]  # Remove last '='

    def parse(self, xml_string):
        """return a list of dictionary corresponding to the xml passed.
        @param xml_string: the result of reverse function.
        @type xml_string: string
        """
        return self.parser(xml_string)

    def reverse(
        self, country="", zip_code="", city="", address="", count=20,
        expires=None, charset="utf-8", ie="utf-8"
    ):
        """return an xml string of all the result from api viamichelin.
        @type country: string with ISO alpha 3 code of the country
        @type zip_code: string
        @type city: string
        @type address: string
        @param count: number max of results.
        @type count: integer
        @param expire: when the request expire. Must be GMT
        @type expire: datetime.datetime
        @type charset: string. Ex: 'utf-8'
        @type ie: string
        Raises:
            RequestsError: raise if the module requests raise an exception
        """

        if not (zip_code or city or address):
            raise Exception(
                "You must provide at least one of those parameters: "
                "city, zip_code, address"
            )
        if not country:
            raise Exception("You must provide the country")

        data = {
            'authkey': self.authkey,
            'country': countries.get(country).alpha3,
            'zip': zip_code,
            'city': city.encode('utf8'),
            'address': address.encode('utf-8'),
            'nb': str(count),
            'charset': charset,
            'ie': ie,
        }

        # Expires tomorow if not defined
        data['expires'] = (
            expires.strftime("%Y-%m-%dT%H:%M:%S")
            if expires
            else datetime.now() + timedelta(1)
        )

        # Generate the url signed
        url = self.__generate_url(data)

        # Request the api
        try:
            r = requests.get(url)
        except requests.ConnectionError as e:
            raise GeocoderError(e)

        # We return an xml formatted response that can be passed to the parse
        # function.
        return r.text
