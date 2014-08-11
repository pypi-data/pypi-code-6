#!/usr/bin/python
# coding: utf8

import requests
import sys
import os
try:
    import simplejson as json
except:
    import json


class Geocoder(object):
    """
    geocoder object
    ~~~~~~~~~~~~~~~
    >>> g = geocoder.google('1600 Amphitheatre Pkwy, Mountain View, CA')
    >>> g.latlng
    (37.784173, -122.401557)
    >>> g.country
    'United States'
    """
    def __init__(self, provider, proxies='', timeout=5.0):
        self.provider = provider
        self.proxies = proxies
        self.timeout = timeout
        self.name = provider.name

        # Connecting to HTTP provider
        self._get_proxies()
        self._get_timeout()
        self._connect()
        self._add_data()

    def __repr__(self):
        return '<[{0}] Geocoder {1} [{2}]>'.format(self.status, self.name, self.address)

    def save(self, filepath, ext='geojson'):
        """
        Saves Geocoded date to a local file.

            >>> g = geocoder.google(<address>)
            >>> g.save('GoogleResult.geojson')
            ...
        """
        basename, ext = os.path.splitext(filepath)
        if ext == '.geojson':
            data = self.geojson
        elif ext == '.json':
            data = self.json
        else:
            data = self.geojson

        with open(filepath, 'wb') as f:
            dump = json.dumps(data, ensure_ascii=False, indent=4)
            f.write(dump)

    def _get_proxies(self):
        if self.proxies:
            if isinstance(self.proxies, str):
                if 'http://' not in self.proxies:
                    name = 'http://{0}'.format(self.proxies)
                self.proxies = {'http': name}
        else:
            self.proxies = {}

    def _get_timeout(self):
        if isinstance(self.timeout, int):
            self.timeout = float(self.timeout)

    def _connect(self):
        """ Requests the Geocoder's URL with the Address as the query """
        self.url = ''
        self.status = 404
        try:
            r = requests.get(
                self.provider.url,
                params=self.provider.params,
                headers=self.provider.headers,
                timeout=self.timeout,
                proxies=self.proxies
            )
            self.url = r.url
            self.status = r.status_code
        except KeyboardInterrupt:
            sys.exit()
        except:
            self.status = 'ERROR - URL Connection'

        if self.status == 200:
            try:
                self.provider.load(r.json())
                self.status = self.provider.status
            except:
                if not self.provider.json:
                    self.status = 'ERROR - JSON Corrupt'

    def _add_data(self):
        # Get Attributes from Provider
        self.quality = self.provider.quality
        self.ok = self.provider.ok
        self.quality = self.provider.quality
        self.location = self.provider.location

        # Geometry
        self.lng = self.provider.lng
        self.lat = self.provider.lat
        self.bbox = self.provider.bbox

        # Address
        self.address = self.provider.address
        self.postal = self.provider.postal
        self.street_number = self.provider.street_number
        self.route = self.provider.route
        self.neighborhood = self.provider.neighborhood
        self.sublocality = self.provider.sublocality
        self.locality = self.provider.locality
        self.county = self.provider.county
        self.state = self.provider.state
        self.country = self.provider.country

        # Alternate Names
        self.street_name = self.route
        self.street = self.route
        self.district = self.neighborhood
        self.city = self.locality
        self.admin2 = self.county
        self.division = self.county
        self.admin1 = self.state
        self.province = self.state

        # More ways to spell X.Y
        x, y = self.lng, self.lat
        self.x, self.longitude = x, x
        self.y, self.latitude = y, y
        self.latlng = (self.lat, self.lng)
        self.xy = (x, y)

        # Bounding Box - SouthWest, NorthEast - [y1, x1, y2, x2]
        self.south = self.provider.south
        self.west = self.provider.west
        self.southwest = self.provider.southwest
        self.southeast = self.provider.southeast
        self.north = self.provider.north
        self.east = self.provider.east
        self.northeast = self.provider.northeast
        self.northwest = self.provider.northwest

        # Population Field (integer)
        self.population = self.provider.population
        self.pop = self.population

        # IP Address
        self.ip = self.provider.ip
        self.isp = self.provider.isp

        # Geom for PostGIS
        self.geom = "POINT({0} {1})".format(self.lng, self.lat)

        # Build Elevation
        self.elevation = self.provider.elevation
        self.resolution = self.provider.resolution
        self.feet = self.provider.feet
        self.meters = self.provider.meters

        # Build JSON
        self.json = self._build_json()
        self.geojson = self._build_geojson()

    def _build_json(self):
        json = dict()
        json['provider'] = self.name
        json['location'] = self.location
        json['ok'] = self.ok
        json['status'] = self.status
        json['url'] = self.url

        if self.postal:
            json['postal'] = self.postal

        if self.address:
            json['address'] = self.address

        if self.ok:
            json['quality'] = self.quality
            json['lng'] = self.x
            json['lat'] = self.y

        if self.isp:
            json['isp'] = self.isp

        if self.bbox:
            json['bbox'] = self.bbox

        if self.street_number:
            json['street_number'] = self.street_number

        if self.route:
            json['route'] = self.route

        if self.neighborhood:
            json['neighborhood'] = self.neighborhood

        if self.sublocality:
            json['sublocality'] = self.sublocality

        if self.locality:
            json['locality'] = self.locality

        if self.county:
            json['county'] = self.county

        if self.state:
            json['state'] = self.state

        if self.country:
            json['country'] = self.country

        if self.population:
            json['population'] = self.population

        if self.ip:
            json['ip'] = self.ip

        if self.elevation:
            json['meters'] = self.meters
            json['resolution'] = self.resolution
            self.address = self.meters + 'm'

        return json

    def _build_geojson(self):
        geojson = dict()
        if self.bbox:
            geojson['bbox'] = [self.west, self.south, self.east, self.north]
        geojson['type'] = 'Feature'
        geojson['geometry'] = {'type':'Point', 'coordinates': [self.lng, self.lat]}
        geojson['properties'] = self.json
        geojson['crs'] = {'type': 'name', "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}
        return geojson


    def debug(self):
        print '============'
        print 'Debug Geocoder'
        print '-------------'
        print 'Provider:', self.name
        print 'Location:', self.location
        print 'Lat & Lng:', self.latlng
        print 'Bbox:', self.bbox
        print 'OK:', self.ok
        print 'Status:', self.status
        print 'Quality:', self.quality
        print 'Url:', self.url
        print 'Proxies:', self.proxies
        print ''
        print 'Address'
        print '-------'
        print 'Address: ', self.address
        print 'Postal:', self.postal
        print 'Street Number:', self.street_number
        print 'Route:', self.route
        print 'Neighborhood:', self.neighborhood
        print 'SubLocality:', self.sublocality
        print 'City:', self.city
        print 'County:', self.county
        print 'State:', self.state
        print 'Country:', self.country
        print '============'
        print 'JSON Objects'
        print '------------'
        for item in self.provider.json.items():
            print item

if __name__ == '__main__':
    from google import Google
    location = 'Olreans, Ottawa'

    provider = Google(location)
    g = Geocoder(provider)
    print g
    print g.url
    
    os
    g.neighborhood