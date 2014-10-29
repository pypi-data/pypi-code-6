from voluptuous import Match

from datatypes.core import SingleValueValidator

ogc_urn_schema = Match(pattern='urn:ogc:def:crs:EPSG::\d{4,5}')

class OgcUrn(SingleValueValidator):
    def define_schema(self):
        return ogc_urn_schema

    def define_error_message(self):
        return "Value must be a correctly formatted OGC URN"
