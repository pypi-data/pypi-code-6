import fileinput

from loaders import *
from src.utils import sanitize, state_codes


class Builder:
    good_line_re = re.compile(r'{\s*"type":\s*"Feature",\s*"properties":\s*')

    def __init__(self, converter):
        self.converter = converter
        self.raw_geo_dir = 'geojson'
        if not isdir(self.raw_geo_dir):
            mkdir(self.raw_geo_dir)

    def build_neighborhood_shapes(self, outfile):
        if isfile(outfile):
            print "%s already exists, skipping building raw geofile" % outfile
            return

        print "Building neighborhood shape files"

        shapefiles_dir = download_neighborhood_shapes()

        raw_geofile = '%s/raw_shapes_neighborhood.json' % self.raw_geo_dir
        self.converter.to_geojson(outfile=raw_geofile, shapefile_prefix='neighborhood', shapefiles_dir=shapefiles_dir)

        # Format results

        raw_geo_re = re.compile(
            '^(\{.*?)"STATE":\s*"([^"]+)".*?"CITY":\s*"([^"]+)".\s*"NAME":\s*"([^"]+)".*?\}.*"geometry":\s*(\{.*?\})\s*\},*$')

        doc_template = '{"id": "%(id)s", "state": "%(state)s", "city": "%(city)s", "neighborhood": "%(neighborhood)s", "geometry": %(coordinates)s}\n'

        with open(outfile, 'a') as out:
            print "Formatting %s into output file %s" % (raw_geofile, outfile)

            for line in fileinput.input(raw_geofile):
                is_good_line = self.good_line_re.match(line)
                if is_good_line is None:
                    continue

                m = raw_geo_re.match(line)

                (neighborhood, city, state, coordinates) = (m.group(4), m.group(3), m.group(2), m.group(5))
                id = sanitize("%s_%s_%s" % (neighborhood, city, state))

                data = {
                    'id': id,
                    'neighborhood': neighborhood,
                    'city': city,
                    'state': state,
                    'coordinates': coordinates
                }

                out.write(doc_template % data)

    def build_city_shapes(self, outfile):
        if isfile(outfile):
            print "%s already exists, skipping building geofile" % outfile
            return

        print "Building city shape files"

        shapefiles_dir = download_city_shapes()

        raw_geofile = '%s/raw_shapes_city.json' % self.raw_geo_dir
        self.converter.to_geojson(outfile=raw_geofile, shapefile_prefix='city', shapefiles_dir=shapefiles_dir)

        # Format results

        raw_geo_re = re.compile(
            '^\{.*?\{.*?\s*"STATEFP":\s*"([^"]+)".*?NAME":\s*"([^"]+)".*?\}.*"geometry":\s*(\{.*?\})\s*\},*$')

        doc_template = '{"id": "%(id)s", "state": "%(state)s", "city": "%(city)s", "geometry": %(coordinates)s}\n'

        with open(outfile, 'a') as out:
            print "Formatting %s into output file %s" % (raw_geofile, outfile)

            for line in fileinput.input(raw_geofile):
                is_good_line = self.good_line_re.match(line)
                if is_good_line is None:
                    continue

                m = raw_geo_re.match(line)

                (state_code, city, coordinates) = (m.group(1), m.group(2), m.group(3))
                state = state_codes[state_code] if state_code in state_codes else state_code
                id = sanitize("%s_%s" % (city, state))

                data = {
                    'id': id,
                    'city': city,
                    'state': state,
                    'coordinates': coordinates
                }

                out.write(doc_template % data)

    def build_state_shapes(self, outfile):
        if isfile(outfile):
            print "%s already exists, skipping building raw geofile" % outfile
            return

        print "Building state shape files"

        shapefiles_dir = download_state_shapes()

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

                m = raw_geo_re.match(line)

                (postal, state, id, coordinates) = (m.group(1), m.group(2), sanitize(m.group(2)), m.group(3))

                data = {
                    'id': id,
                    'state': state,
                    'postal': postal,
                    'coordinates': coordinates
                }

                out.write(doc_template % data)

    def build_zip_shapes(self, outfile):
        if isfile(outfile):
            print "%s already exists, skipping building raw geofile" % outfile
            return

        print "Building zip shape files"

        shapefiles_dir = download_zip_shapes()

        raw_geofile = '%s/raw_shapes_state.json' % self.raw_geo_dir
        self.converter.to_geojson(outfile=raw_geofile, shapefile_prefix='zip', shapefiles_dir=shapefiles_dir)

        # Format results

        raw_geo_re = re.compile('^\{.*?"ZCTA5CE10":\s*"([^"]+)".*?\}.*"geometry":\s*(\{.*?\})\s*\},*$')

        doc_template = '{"id": "%(id)s", "zipcode": "%(zipcode)s", "geometry": %(coordinates)s}\n'

        with open(outfile, 'a') as out:
            print "Formatting %s into output file %s" % (raw_geofile, outfile)

            for line in fileinput.input(raw_geofile):
                is_good_line = self.good_line_re.match(line)
                if is_good_line is None:
                    continue

                m = raw_geo_re.match(line)

                (zipcode, coordinates) = (m.group(1), m.group(2))

                data = {
                    'id': zipcode,
                    'zipcode': zipcode,
                    'coordinates': coordinates
                }

                out.write(doc_template % data)

    @staticmethod
    def build_neighborhood_suggestions(outfile, neighborhood_geofile):
        if isfile(outfile):
            print "%s already exists, skipping building raw geofile" % outfile
            return

        if not isfile(neighborhood_geofile):
            raise ValueError("a valid GeoJSON file must be supplied to build suggestions")

        print "Building neighborhood suggestion files"

        neighborhood_re = re.compile('^.*?"state":\s*"([^"]+)",\s*"city":\s*"([^"]+)",\s*"neighborhood":\s*"([^"]+)".*')

        doc_template = '{"name" : "%(id)s","suggest" : { "input": "%(full_neighborhood)s", "output": "%(full_neighborhood)s", "payload" : {"type": "neighborhood", "id": "%(id)s"}}}\n'

        with open(outfile, 'a') as out:
            print "Formatting %s into output file %s" % (neighborhood_geofile, outfile)

            for line in fileinput.input(neighborhood_geofile):
                m = neighborhood_re.match(line)

                state = m.group(1).upper()
                city = m.group(2)
                neighborhood = m.group(3)

                id = ("%s_%s_%s" % (neighborhood, city, state)).lower().replace(' ', '_').replace('-', '_')
                full_neighborhood = ("%s, %s, %s" % (neighborhood, city, state))

                data = {
                    'id': id,
                    'full_neighborhood': full_neighborhood
                }

                out.write(doc_template % data)

    @staticmethod
    def build_city_suggestions(outfile, city_geofile):
        if isfile(outfile):
            print "%s already exists, skipping building raw geofile" % outfile

        if not isfile(city_geofile):
            raise ValueError("a valid GeoJSON file must be supplied to build suggestions")

        print "Building city suggestion files"

        city_re = re.compile('^.*?"state": "([^"]+)", "city": "([^"]+)".*')

        doc_template = '{"name" : "%(id)s","suggest" : {"input": "%(city)s, %(state)s","output": "%(city)s, %(state)s","payload": {"type": "city", "id": "%(id)s"}}}\n'

        with open(outfile, 'a') as out:
            print "Formatting %s into output file %s" % (city_geofile, outfile)

            for line in fileinput.input(city_geofile):
                m = city_re.match(line)

                state = m.group(1)
                city = m.group(2)

                data = {
                    'state': state,
                    'city': city,
                    'id': ("%s_%s" % (city, state)).lower()
                }

                out.write(doc_template % data)


    @staticmethod
    def build_zip_suggestions(outfile, zip_geofile):
        if isfile(outfile):
            print "%s already exists, skipping building raw geofile" % outfile

        if not isfile(zip_geofile):
            raise ValueError("a valid GeoJSON file must be supplied to build suggestions")

        print "Building zip suggestion files"

        city_re = re.compile('^.*?"zipcode": "([^"]+)".*')

        doc_template = '{"name" : "%(id)s","suggest" : {"input": "%(zip)s", "output": "%(zip)s", "payload": {"type": "zip", "id": "%(id)s"}}}\n'

        with open(outfile, 'a') as out:
            print "Formatting %s into output file %s" % (zip_geofile, outfile)

            for line in fileinput.input(zip_geofile):
                m = city_re.match(line)

                zip = m.group(1)

                data = {
                    'zip': zip,
                    'id': ("%s" % zip)
                }

                out.write(doc_template % data)
