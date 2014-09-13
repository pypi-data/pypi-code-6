import fileinput
import re
import json
from os.path import isdir, isfile
from os import mkdir

import loader
from utils import sanitize, state_codes


class Formatter:
    good_line_re = re.compile(r'{\s*"type":\s*"Feature",\s*"properties":\s*')

    def __init__(self, converter):
        self.converter = converter
        self.raw_geo_dir = 'geojson'
        if not isdir(self.raw_geo_dir):
            mkdir(self.raw_geo_dir)

    def format_neighborhood_shapes(self, outfile):
        if isfile(outfile):
            print "%s already exists, skipping formatting geofile" % outfile
            return

        print "Building neighborhood shape files"

        shapefiles_dir = loader.download_neighborhood_shapes()

        raw_geofile = '%s/raw_shapes_neighborhood.json' % self.raw_geo_dir
        self.converter.to_geojson(outfile=raw_geofile, shapefile_prefix='neighborhood', shapefiles_dir=shapefiles_dir)

        # Format results

        raw_geo_re = re.compile(
            '^(\{.*?)"STATE":\s*"([^"]+)".*?"CITY":\s*"([^"]+)".\s*"NAME":\s*"([^"]+)".*?\}.*"geometry":\s*(\{.*?\})\s*\},*$')
        leading_zero_re = re.compile('([+-])0')

        doc_template = '{"id": "%(id)s", "state": "%(state)s", "city": "%(city)s", "neighborhood": "%(neighborhood)s", "center_lat": %(center_lat)s, "center_lon": %(center_lon)s, "geometry": %(coordinates)s}\n'

        with open(outfile, 'a') as out:
            print "Formatting %s into output file %s" % (raw_geofile, outfile)

            for line in fileinput.input(raw_geofile):
                is_good_line = self.good_line_re.match(line)
                if is_good_line is None:
                    continue

                m = raw_geo_re.match(line)

                (neighborhood, city, state, coordinates) = (m.group(4), m.group(3), m.group(2), m.group(5))
                id = sanitize("%s_%s_%s" % (neighborhood, city, state))

                # hack because there's no center included in neighborhood shape file
                # we'll use the first coord we find as the center
                c = json.loads(coordinates)['coordinates']
                while type(c) is list and len(c) and type(c[0]) is list:
                    c = c[0]

                center_lat = c[1]
                center_lon = c[0]

                data = dict(
                    id=id,
                    neighborhood=neighborhood,
                    city=city,
                    state=state,
                    center_lat=center_lat,
                    center_lon=center_lon,
                    coordinates=coordinates
                )

                out.write(doc_template % data)

    def format_city_shapes(self, outfile):
        if isfile(outfile):
            print "%s already exists, skipping formatting geofile" % outfile
            return

        print "Building city shape files"

        shapefiles_dir = loader.download_city_shapes()

        raw_geofile = '%s/raw_shapes_city.json' % self.raw_geo_dir
        self.converter.to_geojson(outfile=raw_geofile, shapefile_prefix='city', shapefiles_dir=shapefiles_dir)

        # Format results

        raw_geo_re = re.compile(
            '^\{.*?\{.*?\s*"STATEFP":\s*"([^"]+)".*?NAME":\s*"([^"]+)".*?"INTPTLAT":\s*"([^"]+)".*?INTPTLON":\s*"([^"]+)".*?\}.*"geometry":\s*(\{.*?\})\s*\},*$')
        leading_zero_re = re.compile('([+-])0')

        doc_template = '{"id": "%(id)s", "state": "%(state)s", "city": "%(city)s", "center_lat": %(center_lat)s, "center_lon": %(center_lon)s, "geometry": %(coordinates)s}\n'

        with open(outfile, 'a') as out:
            print "Formatting %s into output file %s" % (raw_geofile, outfile)

            for line in fileinput.input(raw_geofile):
                is_good_line = self.good_line_re.match(line)
                if is_good_line is None:
                    continue

                city_info = raw_geo_re.match(line)

                state_code = city_info.group(1)
                city = city_info.group(2)
                center_lat = leading_zero_re.sub(r'\1', city_info.group(3)).replace('+', '')
                center_lon = leading_zero_re.sub(r'\1', city_info.group(4)).replace('+', '')
                coordinates = city_info.group(5)

                state = state_codes[state_code] if state_code in state_codes else state_code
                id = sanitize("%s_%s" % (city, state))

                data = dict(
                    id=id,
                    city=city,
                    state=state,
                    center_lat=center_lat,
                    center_lon=center_lon,
                    coordinates=coordinates
                )

                out.write(doc_template % data)

    def format_state_shapes(self, outfile):
        if isfile(outfile):
            print "%s already exists, skipping formatting geofile" % outfile
            return

        print "Building state shape files"

        shapefiles_dir = loader.download_state_shapes()

        raw_geofile = '%s/raw_shapes_state.json' % self.raw_geo_dir
        self.converter.to_geojson(outfile=raw_geofile, shapefile_prefix='state', shapefiles_dir=shapefiles_dir)

        # Format results

        raw_geo_re = re.compile(
            '^\{.*?: \{.*?"STUSPS": "([^"]+)", "NAME": "([^"]+)".*?\}.*"geometry":\s*(\{.*?\})\s*\},*$')

        doc_template = '{"id": "%(id)s", "state": "%(state)s", "postal": "%(postal)s", "geometry": %(coordinates)s}\n'

        with open(outfile, 'a') as out:
            print "Formatting %s into output file %s" % (raw_geofile, outfile)

            for line in fileinput.input(raw_geofile):
                is_good_line = self.good_line_re.match(line)
                if is_good_line is None:
                    continue

                state_info = raw_geo_re.match(line)

                (postal, state, coordinates) = (state_info.group(1), state_info.group(2), state_info.group(3))

                data = dict(
                    id=sanitize(state),
                    state=state,
                    postal=postal,
                    coordinates=coordinates
                )

                out.write(doc_template % data)

    def format_zip_shapes(self, outfile):
        if isfile(outfile):
            print "%s already exists, skipping formatting geofile" % outfile
            return

        print "Building zip shape files"

        shapefiles_dir = loader.download_zip_shapes()

        raw_geofile = '%s/raw_shapes_zip.json' % self.raw_geo_dir
        self.converter.to_geojson(outfile=raw_geofile, shapefile_prefix='zip', shapefiles_dir=shapefiles_dir)

        # Format results

        raw_geo_re = re.compile('^\{.*?"ZCTA5CE10":\s*"([^"]+)".*?"INTPTLAT10":\s*"([^"]+)".*?INTPTLON10":\s*"([^"]+)".*?\}.*"geometry":\s*(\{.*?\})\s*\},*$')
        leading_zero_re = re.compile('([+-])0')

        doc_template = '{"id": "%(id)s", "zipcode": "%(zipcode)s", "center_lat": %(center_lat)s, "center_lon": %(center_lon)s, "geometry": %(coordinates)s}\n'

        with open(outfile, 'a') as out:
            print "Formatting %s into output file %s" % (raw_geofile, outfile)

            for line in fileinput.input(raw_geofile):
                is_good_line = self.good_line_re.match(line)
                if is_good_line is None:
                    continue

                zip_info = raw_geo_re.match(line)

                zipcode = zip_info.group(1)
                center_lat = leading_zero_re.sub(r'\1', zip_info.group(2)).replace('+', '')
                center_lon = leading_zero_re.sub(r'\1', zip_info.group(3)).replace('+', '')
                coordinates = zip_info.group(4)

                data = dict(
                    id=zipcode,
                    zipcode=zipcode,
                    center_lat=center_lat,
                    center_lon=center_lon,
                    coordinates=coordinates
                )

                out.write(doc_template % data)

    @staticmethod
    def format_neighborhood_suggestions(outfile, neighborhood_geofile):
        if isfile(outfile):
            print "%s already exists, skipping formatting geofile" % outfile
            return

        if not isfile(neighborhood_geofile):
            raise ValueError("a valid GeoJSON file must be supplied to format suggestions")

        print "Building neighborhood suggestion files"

        neighborhood_re = re.compile('^.*?"id": "([^"]+)", "state":\s*"([^"]+)",\s*"city":\s*"([^"]+)",\s*"neighborhood":\s*"([^"]+)", "center_lat": ([^,]+), "center_lon": ([^,]+),.*')

        doc_template = '{"name" : "%(id)s","suggest" : { "input": "%(full_neighborhood)s", "output": "%(full_neighborhood)s", "payload" : {"type": "neighborhood", "id": "%(id)s", "center": {"lat": %(center_lat)s, "lon": %(center_lon)s}}}}\n'

        with open(outfile, 'a') as out:
            print "Formatting %s into output file %s" % (neighborhood_geofile, outfile)

            for line in fileinput.input(neighborhood_geofile):
                m = neighborhood_re.match(line)

                id = m.group(1)
                state = m.group(2).upper()
                city = m.group(3)
                neighborhood = m.group(4)
                center_lat = m.group(5)
                center_lon = m.group(6)

                full_neighborhood = ("%s, %s, %s" % (neighborhood, city, state))

                data = dict(
                    id=id,
                    full_neighborhood=full_neighborhood,
                    center_lat=center_lat,
                    center_lon=center_lon
                )

                out.write(doc_template % data)

    @staticmethod
    def format_city_suggestions(outfile, city_geofile):
        if isfile(outfile):
            print "%s already exists, skipping formatting geofile" % outfile
            return

        if not isfile(city_geofile):
            raise ValueError("a valid GeoJSON file must be supplied to format suggestions")

        print "Building city suggestion files"

        city_re = re.compile('^.*?"id": "([^"]+)", "state": "([^"]+)", "city": "([^"]+)", "center_lat": ([^,]+), "center_lon": ([^,]+),.*')

        doc_template = '{"name" : "%(id)s","suggest" : {"input": "%(city)s, %(state)s","output": "%(city)s, %(state)s","payload": {"type": "city", "id": "%(id)s", "center": {"lat": %(center_lat)s, "lon": %(center_lon)s}}}}\n'

        with open(outfile, 'a') as out:
            print "Formatting %s into output file %s" % (city_geofile, outfile)

            for line in fileinput.input(city_geofile):
                m = city_re.match(line)

                id = m.group(1)
                state = m.group(2)
                city = m.group(3)
                center_lat = m.group(4)
                center_lon = m.group(5)

                data = dict(
                    id=id,
                    state=state,
                    city=city,
                    center_lat=center_lat,
                    center_lon=center_lon
                )

                out.write(doc_template % data)


    @staticmethod
    def format_zip_suggestions(outfile, zip_geofile):
        if isfile(outfile):
            print "%s already exists, skipping formatting geofile" % outfile
            return

        if not isfile(zip_geofile):
            raise ValueError("a valid GeoJSON file must be supplied to format suggestions")

        print "Building zip suggestion files"

        city_re = re.compile('^.*?"id": "([^"]+)", "zipcode": "([^"]+)", "center_lat": ([^,]+), "center_lon": ([^,]+),.*')

        doc_template = '{"name" : "%(id)s","suggest" : {"input": "%(zip)s", "output": "%(zip)s", "payload": {"type": "zip", "id": "%(id)s", "center": {"lat": %(center_lat)s, "lon": %(center_lon)s}}}}\n'

        with open(outfile, 'a') as out:
            print "Formatting %s into output file %s" % (zip_geofile, outfile)

            for line in fileinput.input(zip_geofile):
                m = city_re.match(line)

                id = m.group(1)
                zipcode = m.group(2)
                center_lat = m.group(3)
                center_lon = m.group(4)

                data = dict(
                    id=id,
                    zip=zipcode,
                    center_lat=center_lat,
                    center_lon=center_lon
                )

                out.write(doc_template % data)
