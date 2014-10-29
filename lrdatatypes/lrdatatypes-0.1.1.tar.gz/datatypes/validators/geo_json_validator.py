import json
from voluptuous import Required, In, Optional, All, Length, extra
import geojson

from datatypes.validators import ogc_urn_validator
from datatypes.core import DictionaryValidator, SingleValueValidator
from datatypes.core import unicoded


# This isn't intended to be a full GeoJSON validator, rather a constraining
# validator to support the types / models that the land registry have.
#
# We will also check that the GeoJSON supplied parses fully in the clean_data method
from datatypes.exceptions import DataDoesNotMatchSchemaException

geo_json_schema = {
    Required('type'): All(unicode, In(['Feature'])),

    # Currently we're only allowing named CRS
    Required('crs'): {
        Required('type'): In(['name']),
        Required('properties'): {
            Required('name'): ogc_urn_validator.ogc_urn_schema
        }
    },

    # These are our currently supported geometry types
    Required('geometry'): {
        Required('type'): All(unicode, In(['Polygon', 'MultiPolygon'])),
        Required('coordinates'): [
            #[
            #    All(Length(min=2, max=2), [float])
            #]
        ]
    },

    Optional('properties'): {
        extra: object
    }
}


class GeoJson(DictionaryValidator):
    def define_schema(self):
        return geo_json_schema

    def define_error_dictionary(self):
        return {
            'geometry.type': 'A polygon or multi-polygon is required',
            'geometry.coordinates': 'Coordinates must be floating point number pairs',

            'crs': "A valid 'CRS' containing an EPSG is required",
            'crs.type': 'CRS type must be "name"',
            'crs.properties': 'CRS properties are required',
        }

    def clean_input(self, dictionary):
        try:
            unicoded(geojson.loads(json.dumps(dictionary)))
        except ValueError as exception:
            raise DataDoesNotMatchSchemaException(cause=exception, message='Valid GeoJSON is required')

        return dictionary


class GeoJsonString(SingleValueValidator):
    geo_dict_validator = GeoJson()

    def define_error_message(self):
        return 'Valid GeoJSON is required'

    def define_schema(self):
        return {}

    def validate(self, data):
        try:
            GeoJsonString.geo_dict_validator.validate(self.clean_input(data))
        except DataDoesNotMatchSchemaException as exception:
            raise DataDoesNotMatchSchemaException(message=self.error_message, field_errors=exception.field_errors)

    def clean_input(self, data):
        try:
            return unicoded(geojson.loads(data))
        except Exception as exception:
            raise DataDoesNotMatchSchemaException(cause=exception, message=self.error_message)
