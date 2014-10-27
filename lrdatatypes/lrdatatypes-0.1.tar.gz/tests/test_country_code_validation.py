import unittest

from datatypes.exceptions import DataDoesNotMatchSchemaException
from datatypes.validators.iso_country_code_validator import valid_countries
from datatypes import country_code_validator


class TestCountryCodeValidation(unittest.TestCase):
    def test_cannot_submit_invalid_country(self):
        self.assertRaises(DataDoesNotMatchSchemaException, country_code_validator.validate, 'FOO')
        self.assertRaises(DataDoesNotMatchSchemaException, country_code_validator.validate, '')
        self.assertRaises(DataDoesNotMatchSchemaException, country_code_validator.validate, 234)
        self.assertRaises(DataDoesNotMatchSchemaException, country_code_validator.validate, None)

    def test_can_submit_invalid_country(self):
        try:
            country_code_validator.validate('GB')
        except DataDoesNotMatchSchemaException as e:
            print valid_countries
            self.fail('Should have validated ' + repr(e))
