import unittest
from copy import deepcopy

from datatypes.exceptions import DataDoesNotMatchSchemaException

from datatypes import proprietor_validator
from datatypes.core import unicoded

proprietor =  unicoded({
    "title" : "Mrs",
    "full_name": "Bootata Smick",
    "decoration": "tidy"
})

proprietor_with_additional_fields =  unicoded({
    "title" : "",
    "full_name": "Spielataville Heights Council",
    "decoration": "",
    "an_unknown": "thing"
})

class TestProprietorValidation(unittest.TestCase):

    def test_can_validate_valid_proprietor(self):
        try:
            proprietor_validator.validate(proprietor)
        except DataDoesNotMatchSchemaException as e:
            self.fail("Could not validate proprietor: " + repr(e))

    def test_can_validate_valid_proprietor_with_extra_keys(self):
        try:
            proprietor_validator.validate(proprietor_with_additional_fields)
        except DataDoesNotMatchSchemaException as e:
            self.fail("Could not validate proprietor: " + repr(e))

    def test_does_not_validate_proprietor_without_title(self):
        invalid_proprietor= deepcopy(proprietor)
        del invalid_proprietor["title"]
        self.assertRaisesRegexp(DataDoesNotMatchSchemaException, "title is a required field", proprietor_validator.validate, invalid_proprietor)

    def test_does_not_validate_proprietor_without_full_name(self):
        invalid_proprietor = deepcopy(proprietor)
        del invalid_proprietor["full_name"]
        self.assertRaisesRegexp(DataDoesNotMatchSchemaException, "full_name is a required field", proprietor_validator.validate, invalid_proprietor)

    def test_does_not_validate_proprietor_without_decoration(self):
        invalid_proprietor= deepcopy(proprietor)
        del invalid_proprietor["decoration"]
        self.assertRaisesRegexp(DataDoesNotMatchSchemaException, "decoration is a required field", proprietor_validator.validate, invalid_proprietor)
