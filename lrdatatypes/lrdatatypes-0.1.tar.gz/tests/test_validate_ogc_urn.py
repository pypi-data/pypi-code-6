import unittest

from datatypes import ogc_urn_validator
from datatypes.exceptions import DataDoesNotMatchSchemaException


class ValidatorsTestCase(unittest.TestCase):
    def test_validate_ogc_urn(self):
        try:
            ogc_urn_validator.validate('urn:ogc:def:crs:EPSG::27700')
            ogc_urn_validator.validate('urn:ogc:def:crs:EPSG::1234')
        except DataDoesNotMatchSchemaException as e:
            self.fail("Should not have thrown " + repr(e))

        self.assertRaises(DataDoesNotMatchSchemaException, ogc_urn_validator.validate, 'XXXXX')
        self.assertRaises(DataDoesNotMatchSchemaException, ogc_urn_validator.validate, 'urn:ogc:def:crs:XXX:27700')
