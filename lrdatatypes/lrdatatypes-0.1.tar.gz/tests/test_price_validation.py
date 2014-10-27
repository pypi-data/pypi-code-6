# -*- coding: utf-8 -*-

import unittest
from datatypes.exceptions import DataDoesNotMatchSchemaException
from datatypes import price_validator


class TestPriceValidation(unittest.TestCase):
    def test_can_validate_price(self):
        try:
            price_validator.validate("123.00")
            price_validator.validate("234.23")
            price_validator.validate("20000.19")
            price_validator.validate(20000.19)
        except DataDoesNotMatchSchemaException as e:
            self.fail("Could not validate price " + repr(e))

    def test_cannot_validate_invalid_price(self):
        self.assertRaises(DataDoesNotMatchSchemaException, price_validator.validate, "foo")
        self.assertRaises(DataDoesNotMatchSchemaException, price_validator.validate, 123.3333333)
        self.assertRaises(DataDoesNotMatchSchemaException, price_validator.validate, "123.333434343434")
        self.assertRaises(DataDoesNotMatchSchemaException, price_validator.validate, "£123.33")