import json
import unittest

from datatypes.exceptions import DataDoesNotMatchSchemaException
from geojson_fixtures import *
from datatypes import geo_json_validator, geo_json_string_validator


class TestGeoJsonValidator(unittest.TestCase):
    def test_can_validate_geo_json_dictionary(self):
        try:
            geo_json_validator.validate(sample_geojson_polygon)
            geo_json_validator.validate(sample_geojson_polygon)
            geo_json_validator.validate(sample_geojson_from_migration)
            geo_json_validator.validate(sample_lincolns_inn_fields)
        except DataDoesNotMatchSchemaException as exception:
            self.fail("Should not have thrown exception " + repr(exception))

#    def test_does_not_validate_invalid_geo_json_dictionary(self):
#        self.assertRaises(DataDoesNotMatchSchemaException, geo_json_validator.validate, sample_invalid_geojson)

    def test_cannot_validate_points(self):
        self.assertRaises(DataDoesNotMatchSchemaException, geo_json_validator.validate, sample_invalid_point)

    def test_raises_correct_error_message_for_nested_structure(self):
        try:
            geo_json_validator.validate(sample_invalid_point)
        except DataDoesNotMatchSchemaException as exception:
#            self.assertEqual(exception.field_errors['geometry.coordinates'],
#                             'Coordinates must be floating point number pairs')

            self.assertEqual(exception.field_errors['geometry.type'], 'A polygon or multi-polygon is required')
            self.assertEqual(exception.field_errors['crs'], "A valid 'CRS' containing an EPSG is required")

    def test_can_validate_geo_json_string(self):
        try:
            geo_json_string_validator.validate(json.dumps(sample_geojson_from_migration))
        except DataDoesNotMatchSchemaException as exception:
            self.fail("Should not have thrown exception " + repr(exception))

    def test_does_not_validate_invalid_geo_json_string(self):
        self.assertRaises(DataDoesNotMatchSchemaException, geo_json_string_validator.validate, sample_invalid_geojson)

    def test_string_validator_returns_correct_error_messages(self):
        try:
            geo_json_string_validator.validate(sample_invalid_point)
            self.fail("Should have thrown exception")
        except DataDoesNotMatchSchemaException as exception:
            self.assertEquals(exception.message, geo_json_string_validator.error_message)
